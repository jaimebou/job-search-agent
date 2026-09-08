#!/usr/bin/env python3
"""
upload_to_drive.py — Uploads a file to Google Drive and returns a shareable link.

Uses OAuth 2.0 with scope drive.file (only accesses files this app creates).

Usage:
    python3 upload_to_drive.py file.pdf
    python3 upload_to_drive.py file.pdf --folder "CV & Cover Letters"
    python3 upload_to_drive.py file.pdf --name "CV_012026.pdf"
    python3 upload_to_drive.py --reauth
"""

import argparse
import sys
from pathlib import Path

CREDENTIALS_FILE = Path.home() / ".cursor" / "gdrive-credentials.json"
TOKEN_FILE = Path.home() / ".cursor" / "gdrive-token-upload.json"
SCOPES = [
    "https://www.googleapis.com/auth/drive.file",
    "https://www.googleapis.com/auth/drive.readonly",
]


def get_service():
    try:
        from google.oauth2.credentials import Credentials
        from google.auth.transport.requests import Request
        from google_auth_oauthlib.flow import InstalledAppFlow
        from googleapiclient.discovery import build
    except ImportError:
        print("ERROR: Google API libraries not installed.", file=sys.stderr)
        print("Run: pip install google-api-python-client google-auth-httplib2 google-auth-oauthlib", file=sys.stderr)
        sys.exit(1)

    creds = None

    if TOKEN_FILE.exists():
        creds = Credentials.from_authorized_user_file(str(TOKEN_FILE), SCOPES)

    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            if not CREDENTIALS_FILE.exists():
                print(f"ERROR: Credentials file not found at {CREDENTIALS_FILE}", file=sys.stderr)
                print("See RUNBOOK-gdrive.md for setup instructions.", file=sys.stderr)
                sys.exit(1)
            flow = InstalledAppFlow.from_client_secrets_file(str(CREDENTIALS_FILE), SCOPES)
            creds = flow.run_local_server(port=0)

        TOKEN_FILE.write_text(creds.to_json())

    return build("drive", "v3", credentials=creds)


def list_folders(parent_id: str = "root", indent: int = 0):
    """List folders in Drive, optionally under a parent."""
    service = get_service()
    query = f"'{parent_id}' in parents and mimeType='application/vnd.google-apps.folder' and trashed=false"
    results = service.files().list(
        q=query,
        fields="files(id, name)",
        orderBy="name",
        pageSize=50,
    ).execute()
    folders = results.get("files", [])
    for f in folders:
        print(f"{'  ' * indent}{f['name']}  [{f['id']}]")
    return folders


def find_folder_by_path(path_parts: list[str]) -> str | None:
    """Navigate a folder path like ['CVs', '2025'] and return the final folder ID."""
    service = get_service()
    parent_id = "root"
    for part in path_parts:
        query = f"'{parent_id}' in parents and mimeType='application/vnd.google-apps.folder' and name='{part}' and trashed=false"
        results = service.files().list(q=query, fields="files(id, name)").execute()
        folders = results.get("files", [])
        if not folders:
            return None
        parent_id = folders[0]["id"]
    return parent_id


def create_subfolder(parent_id: str, name: str) -> str:
    """Create a subfolder under parent_id and return its ID."""
    service = get_service()
    # Check if it already exists
    query = f"'{parent_id}' in parents and mimeType='application/vnd.google-apps.folder' and name='{name}' and trashed=false"
    existing = service.files().list(q=query, fields="files(id,name)").execute().get("files", [])
    if existing:
        print(f"Folder '{name}' already exists.")
        return existing[0]["id"]
    meta = {"name": name, "mimeType": "application/vnd.google-apps.folder", "parents": [parent_id]}
    folder = service.files().create(body=meta, fields="id,name").execute()
    print(f"Created folder: {name}  [{folder['id']}]")
    return folder["id"]



def find_or_create_folder(service, folder_name: str) -> str:
    """Returns the folder ID, creating it if it doesn't exist."""
    query = f"mimeType='application/vnd.google-apps.folder' and name='{folder_name}' and trashed=false"
    results = service.files().list(q=query, fields="files(id, name)").execute()
    folders = results.get("files", [])

    if folders:
        return folders[0]["id"]

    folder_meta = {
        "name": folder_name,
        "mimeType": "application/vnd.google-apps.folder",
    }
    folder = service.files().create(body=folder_meta, fields="id").execute()
    print(f"Created Drive folder: {folder_name}")
    return folder["id"]


def upload_file(file_path: Path, drive_name: str, folder_id: str | None) -> dict:
    from googleapiclient.http import MediaFileUpload
    import mimetypes

    service = get_service()

    mime_type, _ = mimetypes.guess_type(str(file_path))
    mime_type = mime_type or "application/octet-stream"

    metadata: dict = {"name": drive_name}
    if folder_id:
        metadata["parents"] = [folder_id]

    media = MediaFileUpload(str(file_path), mimetype=mime_type, resumable=True)
    uploaded = service.files().create(
        body=metadata,
        media_body=media,
        fields="id, name, webViewLink",
    ).execute()

    # Make it accessible to anyone with the link
    service.permissions().create(
        fileId=uploaded["id"],
        body={"type": "anyone", "role": "reader"},
    ).execute()

    return uploaded


def reauth():
    """Delete the upload token and force a new auth flow."""
    if TOKEN_FILE.exists():
        TOKEN_FILE.unlink()
        print(f"Deleted existing token: {TOKEN_FILE}")
    print("Starting re-authentication...")
    get_service()
    print(f"New token saved to: {TOKEN_FILE}")


def main():
    parser = argparse.ArgumentParser(description="Upload a file to Google Drive.")
    parser.add_argument("file", nargs="?", type=Path, help="File to upload")
    parser.add_argument("--folder", type=str, default=None, help="Drive folder name (created if it doesn't exist)")
    parser.add_argument("--folder-path", type=str, default=None, help="Slash-separated folder path, e.g. 'CVs/2025'")
    parser.add_argument("--name", type=str, default=None, help="Name for the file in Drive (default: original filename)")
    parser.add_argument("--list", action="store_true", help="List root folders in Drive")
    parser.add_argument("--reauth", action="store_true", help="Force re-authentication")
    args = parser.parse_args()

    if args.reauth:
        reauth()
        return

    if args.list:
        print("Root folders in your Google Drive:\n")
        list_folders("root")
        return

    if not args.file:
        parser.print_help()
        sys.exit(1)

    if not args.file.exists():
        print(f"ERROR: File not found: {args.file}", file=sys.stderr)
        sys.exit(1)

    drive_name = args.name or args.file.name
    service = get_service()

    folder_id = None
    if args.folder_path:
        parts = [p.strip() for p in args.folder_path.split("/") if p.strip()]
        folder_id = find_folder_by_path(parts)
        if not folder_id:
            print(f"ERROR: Folder path not found in Drive: {args.folder_path}", file=sys.stderr)
            sys.exit(1)
    elif args.folder:
        folder_id = find_or_create_folder(service, args.folder)

    print(f"Uploading: {args.file.name}...")
    result = upload_file(args.file, drive_name, folder_id)

    print(f"\nSubido:  {result['name']}")
    print(f"Link:    {result['webViewLink']}")


if __name__ == "__main__":
    main()
