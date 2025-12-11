import os
import time
from pathlib import Path
from dotenv import load_dotenv
from google import genai
from google.genai import types

# Load environment variables from .env file
load_dotenv()

# Get API key from environment
api_key = os.getenv("GEMINI_API_KEY") or os.getenv("GOOGLE_API_KEY")
if not api_key:
    raise ValueError(
        "API key not found! Please set GEMINI_API_KEY or GOOGLE_API_KEY in your .env file"
    )

# Initialize the client with your API key
client = genai.Client(api_key=api_key)

# Define your prompt
prompt = """Friendly cartoon Mickey Mouse in a bright, colorful classroom teaches the vowels A, E, I, O, U to 3-year-olds. 
Large, clear letters appear one at a time, each matched with a single spoken vowel. 
Mickey points slowly to the current vowel with simple toddler-friendly gestures. 
Use vivid colors, smooth motion, and correct text displayed only for the vowel being taught at that moment."""

# Optional: You can also use the prompt from prompt.md
# prompt = """A close up of two people staring at a cryptic drawing on a wall, torchlight flickering.
# A man murmurs, 'This must be it. That's the secret code.' The woman looks at him and whispering excitedly, 'What did you find?'"""

print(f"Generating video with prompt: {prompt[:50]}...")
print("This may take several minutes...")

# Call the generate_videos method with the Veo 3.1 model ID
operation = client.models.generate_videos(
    model="veo-3.1-generate-preview",
    prompt=prompt,
    config=types.GenerateVideosConfig(
        aspect_ratio="16:9",
        # You can add other controls here like reference_images, last_frame, etc.
    )
)

# Poll the operation status until the video is ready
print("Video generation started. Polling for completion...")
while not operation.done:
    print("Waiting for video generation to complete...")
    time.sleep(10)
    operation = client.operations.get(operation)

# Check if operation was successful
if operation.error:
    raise Exception(f"Video generation failed: {operation.error}")

# Create output directory if it doesn't exist
output_dir = Path("output")
output_dir.mkdir(exist_ok=True)

# Download the generated video
generated_video = operation.response.generated_videos[0]
client.files.download(file=generated_video.video)

# Generate filename with timestamp
timestamp = time.strftime("%Y%m%d_%H%M%S")
output_filename = output_dir / f"veo31_video_{timestamp}.mp4"
generated_video.video.save(str(output_filename))

print(f"✅ Generated video saved to: {output_filename}")
