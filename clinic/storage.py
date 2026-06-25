import os
import cloudinary
import cloudinary.uploader
import cloudinary.utils
from django.core.files.storage import FileSystemStorage
from django.conf import settings


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
                # Reset file pointer if it's been read
                if hasattr(content, 'seek'):
                    content.seek(0)
                
                # Read file content
                if hasattr(content, 'read'):
                    file_content = content.read()
                else:
                    file_content = content
                
                # Get file name without extension for public_id
                name_without_ext = os.path.splitext(os.path.basename(name))[0]
                
                # Upload to Cloudinary
                result = cloudinary.uploader.upload(
                    file_content,
                    folder="drpranay-portfolio",
                    resource_type="auto",
                    public_id=name_without_ext,
                )
                
                # Store the full Cloudinary public ID with folder
                return f"drpranay-portfolio/{result.get('public_id', name_without_ext)}"
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
                # Generate Cloudinary URL from public_id
                if name.startswith("drpranay-portfolio/"):
                    # Already has folder prefix
                    url = cloudinary.utils.cloudinary_url(name)[0]
                else:
                    # Add folder prefix if missing
                    full_name = f"drpranay-portfolio/{name}" if not name.startswith("/") else name.lstrip("/")
                    url = cloudinary.utils.cloudinary_url(full_name)[0]
                
                return url if url else super().url(name)
            except Exception as e:
                print(f"Cloudinary URL error: {e}")
                # Fall back to local URL
                return super().url(name)
        else:
            # Return local URL
            return super().url(name)

