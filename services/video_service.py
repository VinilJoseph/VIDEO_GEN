import os
import time
from pathlib import Path
from typing import Optional
from google import genai
from google.genai import types
from services.cloudinary_service import CloudinaryService

class VideoService:
    """
    Service for generating videos using Veo 3.1
    """
    
    def __init__(self, api_key: str):
        self.client = genai.Client(api_key=api_key)
        self.output_dir = Path("output")
        self.output_dir.mkdir(exist_ok=True)
        
        # Initialize Cloudinary service (with error handling if credentials missing)
        try:
            self.cloudinary_service = CloudinaryService()
        except ValueError as e:
            print(f"⚠️ Warning: {e}. Cloudinary upload will be disabled.")
            self.cloudinary_service = None
    
    def generate_video(
        self, 
        prompt: str, 
        aspect_ratio: str = "16:9",
        poll_interval: int = 10,
        upload_to_cloudinary: bool = True
    ) -> tuple[str, str, Optional[str]]:
        """
        Generate a video from a prompt and optionally upload to Cloudinary.
        
        Args:
            prompt: The prompt for video generation
            aspect_ratio: Video aspect ratio (default: "16:9")
            poll_interval: Seconds between polling checks (default: 10)
            upload_to_cloudinary: Whether to upload to Cloudinary (default: True)
        
        Returns:
            tuple: (file_path, filename, cloudinary_url)
        """
        # Call the generate_videos method with the Veo 3.1 model ID
        operation = self.client.models.generate_videos(
            model="veo-3.1-generate-preview",
            prompt=prompt,
            config=types.GenerateVideosConfig(
                aspect_ratio=aspect_ratio,
            )
        )
        
        # Poll the operation status until the video is ready
        while not operation.done:
            print("Waiting for video generation to complete...")
            time.sleep(poll_interval)
            operation = self.client.operations.get(operation)
        
        # Check if operation was successful
        if operation.error:
            raise Exception(f"Video generation failed: {operation.error}")
        
        # Download the generated video
        generated_video = operation.response.generated_videos[0]
        self.client.files.download(file=generated_video.video)
        
        # Generate filename with timestamp
        timestamp = time.strftime("%Y%m%d_%H%M%S")
        filename = f"veo31_video_{timestamp}.mp4"
        file_path = self.output_dir / filename
        generated_video.video.save(str(file_path))
        
        cloudinary_url = None
        
        # Upload to Cloudinary if enabled and service is available
        if upload_to_cloudinary and self.cloudinary_service:
            print(f"Uploading video to Cloudinary: {filename}...")
            try:
                # Use filename without extension as public_id
                public_id = f"veo31-videos/{filename.replace('.mp4', '')}"
                upload_result = self.cloudinary_service.upload_video(
                    str(file_path),
                    public_id=public_id
                )
                cloudinary_url = upload_result.get("secure_url")
                print(f"✅ Video uploaded to Cloudinary: {cloudinary_url}")
                
                # Delete local file after successful upload to save disk space
                try:
                    if file_path.exists():
                        file_path.unlink()
                        print(f"🗑️ Local file deleted after Cloudinary upload")
                except Exception as e:
                    print(f"⚠️ Could not delete local file: {e}")
            except Exception as e:
                print(f"⚠️ Cloudinary upload failed: {e}")
                # Continue even if Cloudinary upload fails (local file remains)
        elif upload_to_cloudinary and not self.cloudinary_service:
            print("⚠️ Cloudinary service not available. Skipping upload.")
        
        return str(file_path), filename, cloudinary_url

