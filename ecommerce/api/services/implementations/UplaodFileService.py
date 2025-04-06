import os
import uuid
import logging
import base64
from django.conf import settings
from typing import List

logger = logging.getLogger(__name__)

class UploadFileService:
    def __init__(self):
        """Initialize the service with a base upload directory."""
        self.base_upload_dir = os.path.join(settings.BASE_DIR, 'upload')

    def _ensure_upload_folder_exists(self, subfolder: str) -> str:
        """Ensure the upload folder exists; create it if necessary."""
        upload_folder = os.path.join(self.base_upload_dir, subfolder)
        if not os.path.exists(upload_folder):
            os.makedirs(upload_folder)
            logger.info(f"Created upload folder: {upload_folder}")
        return upload_folder

    def _validate_file_extension(self, file_name: str, allowed_extensions: List[str]) -> bool:
        """Validate the file extension against a list of allowed extensions."""
        ext = file_name.split('.')[-1].lower()
        return ext in allowed_extensions

    def upload_file_as_base64(self, base64_string: str, file_name: str, subfolder: str) -> str:
        """Upload a base64-encoded file to the specified subfolder."""
        upload_folder = self._ensure_upload_folder_exists(subfolder)

        # Validate file extension
        if not self._validate_file_extension(file_name, ['jpg', 'png', 'jpeg']):
            return "NotImage"

        # Generate unique file name
        ext = file_name.split('.')[-1].lower()
        unique_file_name = f"{uuid.uuid4()}.{ext}"
        file_path = os.path.join(upload_folder, unique_file_name)

        # Decode and save the base64 file
        try:
            with open(file_path, 'wb') as f:
                f.write(base64.b64decode(base64_string))
            #logger.info(f"Base64 file uploaded successfully: {unique_file_name}")
            return unique_file_name
        except Exception as e:
            logger.error(f"Error uploading base64 file: {e}")
            return "UploadFailed"