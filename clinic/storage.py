import os
from django.core.files.storage import FileSystemStorage
from django.conf import settings


class MediaStorage(FileSystemStorage):
    """
    Custom storage backend for media files.
    Works locally and handles production gracefully.
    """
    
    def __init__(self):
        # Ensure media directory exists
        media_root = settings.MEDIA_ROOT
        if not os.path.exists(media_root):
            os.makedirs(media_root, exist_ok=True)
        super().__init__(location=str(media_root))
