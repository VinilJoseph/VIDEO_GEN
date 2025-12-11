from pydantic import BaseModel, Field
from typing import Optional, List

class VideoGenerationRequest(BaseModel):
    prompt: str = Field(..., description="The prompt for video generation", min_length=10)
    aspect_ratio: Optional[str] = Field("16:9", description="Video aspect ratio")
    enhance_prompt: Optional[bool] = Field(True, description="Whether to enhance prompt using AI reasoning")

class VideoGenerationResponse(BaseModel):
    message: str
    cloudinary_url: Optional[str] = Field(None, description="Cloudinary CDN URL (primary URL for frontend)")
    original_prompt: str
    enhanced_prompt: Optional[str] = None
    filename: str

class CloudinaryVideo(BaseModel):
    public_id: str
    secure_url: str
    format: Optional[str] = None
    width: Optional[int] = None
    height: Optional[int] = None
    bytes: Optional[int] = None
    created_at: Optional[str] = None
    duration: Optional[float] = None
    filename: str

class VideoListResponse(BaseModel):
    total: int
    videos: List[CloudinaryVideo]
    folder: str

