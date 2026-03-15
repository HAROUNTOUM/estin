import io
import os
from google.oauth2 import service_account
from googleapiclient.discovery import build
from googleapiclient.http import MediaIoBaseUpload
from django.conf import settings

class GoogleDriveService:
    def __init__(self):
        cred_path = os.path.join(settings.BASE_DIR, 'secrets', 'google_drive_creds.json')
        self.creds = service_account.Credentials.from_service_account_file(
            cred_path, scopes=['https://www.googleapis.com/auth/drive.file']
        )
        self.service = build('drive', 'v3', credentials=self.creds)

    def get_or_create_subfolder(self, folder_name, parent_id):
        query = (f"name = '{folder_name}' and '{parent_id}' in parents and "
                 f"mimeType = 'application/vnd.google-apps.folder' and trashed = false")
        response = self.service.files().list(q=query, fields='files(id)').execute()
        files = response.get('files', [])

        if files:
            return files[0].get('id')

        folder_metadata = {
            'name': folder_name,
            'mimeType': 'application/vnd.google-apps.folder',
            'parents': [parent_id]
        }
        new_folder = self.service.files().create(body=folder_metadata, fields='id').execute()
        return new_folder.get('id')

    def upload_stream(self, file_obj, file_name, metadata):
        # 1. Racine de la promotion (depuis settings.py)
        current_id = settings.GOOGLE_DRIVE_PROMOTIONS.get(metadata['level'])

        # 2. Génération dynamique du chemin : Semestre -> Année -> Module -> Type
        path = [metadata['semester'], metadata['year'], metadata['module'], metadata['type']]
        for segment in path:
            current_id = self.get_or_create_subfolder(segment, current_id)

        # 3. Upload direct depuis la RAM
        media = MediaIoBaseUpload(io.BytesIO(file_obj.read()), mimetype='application/pdf')
        file_metadata = {'name': file_name, 'parents': [current_id]}
        uploaded = self.service.files().create(body=file_metadata, media_body=media, fields='id').execute()

        return uploaded.get('id')
