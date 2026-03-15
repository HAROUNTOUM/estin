import os
import django

# Set up Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'estin_student.settings')
django.setup()

from froms.drive_service import GoogleDriveService # <--- CHANGE THIS
from django.conf import settings

def test_connection():
    print("🚀 Starting Google Drive Connection Test...")
    drive = GoogleDriveService()

    # Use the first ID in your settings
    first_promo = list(settings.GOOGLE_DRIVE_PROMOTIONS.keys())[0]
    parent_id = settings.GOOGLE_DRIVE_PROMOTIONS[first_promo]

    try:
        print(f"Checking access to {first_promo} (ID: {parent_id})...")
        new_id = drive.get_or_create_subfolder("TEST_CONNECTION_FOLDER", parent_id)
        print(f"✅ SUCCESS! Created/Found folder. ID: {new_id}")
        print("Now check your Google Drive. You should see 'TEST_CONNECTION_FOLDER'.")
    except Exception as e:
        print(f"❌ FAILED: {str(e)}")
        print("\nCommon fixes:")
        print("1. Did you share the folder with the service account email?")
        print("2. Is the Folder ID in settings.py correct?")
        print("3. Is the JSON file path correct?")

if __name__ == "__main__":
    test_connection()
