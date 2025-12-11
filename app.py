import os
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv

from models.schemas import VideoGenerationRequest, VideoGenerationResponse, VideoListResponse, CloudinaryVideo
from services.video_service import VideoService
from services.prompt_enhancer import PromptEnhancer
from services.cloudinary_service import CloudinaryService

# Load environment variables
load_dotenv()

# Get API key
api_key = os.getenv("GEMINI_API_KEY") or os.getenv("GOOGLE_API_KEY")
if not api_key:
    raise ValueError(
        "API key not found! Please set GEMINI_API_KEY or GOOGLE_API_KEY in your .env file"
    )

# Initialize services
video_service = VideoService(api_key=api_key)
prompt_enhancer = PromptEnhancer(api_key=api_key)

# Initialize Cloudinary service (with error handling if credentials missing)
try:
    cloudinary_service = CloudinaryService()
except ValueError as e:
    print(f"⚠️ Warning: {e}. Cloudinary listing will be disabled.")
    cloudinary_service = None

# Create FastAPI app
app = FastAPI(
    title="Veo 3.1 Video Generation API",
    description="API for generating educational videos for toddlers using Google Veo 3.1",
    version="1.0.0"
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Configure this properly for production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
async def root():
    return {
        "message": "Veo 3.1 Video Generation API",
        "endpoints": {
            "generate": "/api/generate-video",
            "list_videos": "/api/videos",
            "health": "/health"
        }
    }

@app.get("/health")
async def health_check():
    return {"status": "healthy"}

@app.post("/api/generate-video", response_model=VideoGenerationResponse)
async def generate_video(request: VideoGenerationRequest):
    """
    Generate a video from a prompt with optional AI enhancement.
    """
    try:
        original_prompt = request.prompt
        enhanced_prompt = None
        
        # Enhance prompt if requested
        if request.enhance_prompt:
            print(f"Enhancing prompt: {original_prompt[:50]}...")
            enhanced_prompt = prompt_enhancer.enhance_prompt(original_prompt)
            print(f"Enhanced prompt: {enhanced_prompt[:50]}...")
            prompt_to_use = enhanced_prompt
        else:
            prompt_to_use = original_prompt
        
        # Generate video and upload to Cloudinary
        print(f"Generating video with prompt: {prompt_to_use[:50]}...")
        file_path, filename, cloudinary_url = video_service.generate_video(
            prompt=prompt_to_use,
            aspect_ratio=request.aspect_ratio,
            upload_to_cloudinary=True
        )
        
        # Return response with Cloudinary URL
        return VideoGenerationResponse(
            message="Video generated successfully",
            cloudinary_url=cloudinary_url,  # Primary CDN URL for frontend
            original_prompt=original_prompt,
            enhanced_prompt=enhanced_prompt,
            filename=filename,
        )
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Video generation failed: {str(e)}")

@app.get("/api/videos", response_model=VideoListResponse)
async def get_all_videos(folder: str = "veo31-videos", max_results: int = 500):
    """
    Get all videos uploaded to Cloudinary.
    
    Args:
        folder: Cloudinary folder to search (default: "veo31-videos")
        max_results: Maximum number of videos to return (default: 500)
    
    Returns:
        VideoListResponse: List of all videos with metadata
    """
    if not cloudinary_service:
        raise HTTPException(
            status_code=503,
            detail="Cloudinary service not available. Please check your Cloudinary credentials."
        )
    
    try:
        videos_data = cloudinary_service.list_all_videos(folder=folder, max_results=max_results)
        
        # Convert to Pydantic models
        videos = [CloudinaryVideo(**video) for video in videos_data]
        
        return VideoListResponse(
            total=len(videos),
            videos=videos,
            folder=folder
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to retrieve videos: {str(e)}")

# if __name__ == "__main__":
#     import uvicorn
#     uvicorn.run(app, host="0.0.0.0", port=8000)

if __name__ == "__main__":
    import uvicorn
    port = int(os.getenv("PORT", 8000))
    uvicorn.run(app, host="0.0.0.0", port=port)