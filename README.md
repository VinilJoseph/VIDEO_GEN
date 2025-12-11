# Veo 3.1 Video Generation API

FastAPI-based REST API for generating educational videos using Google's Veo 3.1 AI model. Features automatic prompt enhancement, video generation, and Cloudinary CDN storage.

## Overview

Generates AI-powered videos from text prompts using Google Veo 3.1. Optimized for creating educational content with automatic prompt enhancement via Gemini AI and cloud storage via Cloudinary.

## Tech Stack

- Python 3.8+
- FastAPI
- Google Veo 3.1 (video generation)
- Google Gemini 1.5 Pro (prompt enhancement)
- Cloudinary (video storage and CDN)
- Pydantic (data validation)

## Installation

1. Clone repository:

```bash
git clone <repository-url>
cd video_gen
```

2. Create virtual environment:

```bash
python -m venv venv
venv\Scripts\activate  # Windows
source venv/bin/activate  # macOS/Linux
```

3. Install dependencies:

```bash
pip install -r requirements.txt
```

4. Create `.env` file:

```env
GEMINI_API_KEY=your_google_api_key_here
CLOUDINARY_CLOUD_NAME=your_cloud_name
CLOUDINARY_API_KEY=your_api_key
CLOUDINARY_API_SECRET=your_api_secret
PORT=8000
```

**Note**: Cloudinary credentials are optional. Without them, videos are stored locally only.

## Getting API Keys

1. Google API Key: Visit [Google AI Studio](https://makersuite.google.com/app/apikey) and create an API key with access to Veo 3.1 and Gemini models.

2. Cloudinary: Sign up at [Cloudinary](https://cloudinary.com/), go to Dashboard → Settings, and copy your credentials.

## Usage

Run the API server:

```bash
python app.py
```

Or with uvicorn:

```bash
uvicorn app:app --reload --host 0.0.0.0 --port 8000
```

API available at `http://localhost:8000`

API documentation:

- Swagger UI: `http://localhost:8000/docs`
- ReDoc: `http://localhost:8000/redoc`

Test standalone video generation:

```bash
python veo31.py
```

## API Endpoints

### GET /

Returns API information and available endpoints.

### GET /health

Health check endpoint.

### POST /api/generate-video

Generate a video from a text prompt.

Request:

```json
{
  "prompt": "Friendly cartoon Mickey Mouse teaches vowels to toddlers",
  "aspect_ratio": "16:9",
  "enhance_prompt": true
}
```

Response:

```json
{
  "message": "Video generated successfully",
  "cloudinary_url": "https://res.cloudinary.com/.../video.mp4",
  "original_prompt": "...",
  "enhanced_prompt": "...",
  "filename": "veo31_video_20251209_154532.mp4"
}
```

**Note**: Video generation takes 2-5 minutes. The API polls until completion.

### GET /api/videos

List all videos stored in Cloudinary.

Query parameters:

- `folder` (optional): Cloudinary folder (default: "veo31-videos")
- `max_results` (optional): Maximum results (default: 500)

## Project Structure

```
video_gen/
├── app.py                 # Main FastAPI application
├── veo31.py              # Standalone test script
├── requirements.txt      # Dependencies
├── models/
│   └── schemas.py       # Pydantic models
└── services/
    ├── video_service.py      # Video generation
    ├── prompt_enhancer.py    # Prompt enhancement
    └── cloudinary_service.py # Cloudinary integration
```

## Deployment

### Railway

1. Connect repository to Railway
2. Set environment variables in Railway dashboard
3. Deploy

### Manual

```bash
uvicorn app:app --host 0.0.0.0 --port $PORT
```

## Troubleshooting

**API Key Not Found**

- Ensure `.env` file exists with `GEMINI_API_KEY` or `GOOGLE_API_KEY`

**Cloudinary Upload Fails**

- Add Cloudinary credentials to `.env` or disable Cloudinary uploads

**Video Generation Takes Too Long**

- Normal: 2-5 minutes. Check API quota limits and internet connection.

**Import Errors**

- Run `pip install -r requirements.txt`

**Port Already in Use**

- Change PORT in `.env` or kill the process using the port

## Example Prompts

See `prompt.md` for examples. Good prompts should:

- Be clear and descriptive
- Include visual elements (colors, characters, objects)
- Specify age-appropriate content
- Mention motion and animation details
