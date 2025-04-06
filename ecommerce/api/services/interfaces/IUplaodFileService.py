from typing import List

class IUplaodFileService:
    def upload_file_as_base64(self, image, subfolder: str) -> str:
        pass

    def upload_file_to_gallery(self, images, subfolder: str) -> List[str]:
        pass

    def upload_pdf_file(self, image, subfolder: str) -> str:
        pass

    def delete_image_file(self, file_name_with_path: str, folder_name: str) -> bool:
        pass

    
