import os
import cloudinary
import cloudinary.uploader
from cloudinary.utils import cloudinary_url
from cloudinary import Search
from dotenv import load_dotenv

load_dotenv()

class CloudinaryService:
    """
    Service for uploading videos to Cloudinary
    """
    
    def __init__(self):
        # Get Cloudinary credentials from environment variables
        cloud_name = os.getenv("CLOUDINARY_CLOUD_NAME")
        api_key = os.getenv("CLOUDINARY_API_KEY")
        api_secret = os.getenv("CLOUDINARY_API_SECRET")
        
        # Validate configuration
        if not all([cloud_name, api_key, api_secret]):
            raise ValueError(
                "Cloudinary credentials not found! Please set CLOUDINARY_CLOUD_NAME, "
                "CLOUDINARY_API_KEY, and CLOUDINARY_API_SECRET in your .env file"
            )
        
        # Configure Cloudinary
        cloudinary.config(
            cloud_name=cloud_name,
            api_key=api_key,
            api_secret=api_secret,
            secure=True
        )
    
    def upload_video(self, file_path: str, public_id: str = None) -> dict:
        """
        Upload a video file to Cloudinary.
        
        Args:
            file_path: Path to the video file
            public_id: Optional custom public ID for the video
        
        Returns:
            dict: Upload result with secure_url and other metadata
        """
        try:
            upload_result = cloudinary.uploader.upload(
                file_path,
                resource_type="video",
                public_id=public_id,
                folder="veo31-videos",  # Organize videos in a folder
                overwrite=True,
                invalidate=True  # Invalidate CDN cache
            )
            return upload_result
        except Exception as e:
            raise Exception(f"Cloudinary upload failed: {str(e)}")
    
    def get_video_url(self, public_id: str, transformations: dict = None) -> str:
        """
        Get optimized Cloudinary URL for a video.
        
        Args:
            public_id: The public ID of the video
            transformations: Optional transformation parameters
        
        Returns:
            str: Optimized video URL
        """
        try:
            url, _ = cloudinary.utils.cloudinary_url(
                public_id,
                resource_type="video",
                secure=True,
                **(transformations if transformations else {})
            )
            return url
        except Exception as e:
            raise Exception(f"Failed to generate Cloudinary URL: {str(e)}")
    
    def list_all_videos(self, folder: str = "veo31-videos", max_results: int = 500) -> list:
        """
        List all videos from Cloudinary folder.
        
        Args:
            folder: Folder path to search in (default: "veo31-videos")
            max_results: Maximum number of results to return (default: 500)
        
        Returns:
            list: List of video resources with metadata
        """
        try:
            # Use Cloudinary Search API to find all videos in the folder
            search_result = Search()\
                .expression(f"resource_type:video AND folder:{folder}")\
                .max_results(max_results)\
                .execute()
            
            videos = []
            for resource in search_result.get('resources', []):
                public_id = resource.get("public_id", "")
                # Extract filename from public_id (remove folder path)
                filename = public_id.split("/")[-1] if "/" in public_id else public_id
                
                videos.append({
                    "public_id": public_id,
                    "secure_url": resource.get("secure_url"),
                    "format": resource.get("format"),
                    "width": resource.get("width"),
                    "height": resource.get("height"),
                    "bytes": resource.get("bytes"),
                    "created_at": resource.get("created_at"),
                    "duration": resource.get("duration"),  # Video duration in seconds
                    "filename": filename
                })
            
            return videos
        except Exception as e:
            raise Exception(f"Failed to list videos from Cloudinary: {str(e)}")

