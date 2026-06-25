import os
import cloudinary
import cloudinary.uploader
from django.core.files.storage import FileSystemStorage
from django.conf import settings
from io import BytesIO


class CloudinaryMediaStorage(FileSystemStorage):
    """
    Custom storage backend that uploads files to Cloudinary if credentials are available,
    otherwise stores locally for development.
    """
    
    def __init__(self):
        self.cloud_name = os.environ.get("CLOUDINARY_CLOUD_NAME")
        self.api_key = os.environ.get("CLOUDINARY_API_KEY")
        self.api_secret = os.environ.get("CLOUDINARY_API_SECRET")
        
        # Configure cloudinary if credentials exist
        if self.cloud_name and self.api_key and self.api_secret:
            cloudinary.config(
                cloud_name=self.cloud_name,
                api_key=self.api_key,
                api_secret=self.api_secret,
                secure=True,
            )
            self.use_cloudinary = True
        else:
            self.use_cloudinary = False
            # Ensure media directory exists for local storage
            media_root = settings.MEDIA_ROOT
            if not os.path.exists(media_root):
                os.makedirs(media_root, exist_ok=True)
        
        super().__init__(location=str(settings.MEDIA_ROOT))
    
    def _save(self, name, content):
        """Save file to Cloudinary if available, otherwise save locally"""
        if self.use_cloudinary:
            try:
                # Read file content
                if hasattr(content, 'read'):
                    file_content = content.read()
                else:
                    file_content = content
                
                # Upload to Cloudinary
                result = cloudinary.uploader.upload(
                    file_content,
                    folder="drpranay-portfolio",
                    resource_type="auto",
                    public_id=os.path.splitext(name)[0],
                )
                
                # Store the Cloudinary URL
                return result.get('public_id', name)
            except Exception as e:
                print(f"Cloudinary upload error: {e}")
                # Fall back to local storage
                return super()._save(name, content)
        else:
            # Use local filesystem
            return super()._save(name, content)
    
    def url(self, name):
        """Return the URL for accessing the file"""
        if self.use_cloudinary:
            try:
                # Return Cloudinary CDN URL
                return cloudinary.utils.cloudinary_url(name)[0]
            except Exception:
                # Fall back to local URL
                return super().url(name)
        else:
            # Return local URL
            return super().url(name)

