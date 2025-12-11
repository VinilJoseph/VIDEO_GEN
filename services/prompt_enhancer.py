import os
from google import genai
from google.genai import types

class PromptEnhancer:
    """
    Uses Google Gemini to enhance prompts for mathematical teaching videos for toddlers.
    """
    
    def __init__(self, api_key: str):
        self.client = genai.Client(api_key=api_key)
        self.model = "gemini-1.5-pro"  # or "gemini-1.5-flash" for faster responses
    
    def enhance_prompt(self, user_prompt: str) -> str:
        """
        Enhances the user prompt with reasoning for toddler math education videos.
        """
        system_prompt = """You are an expert in creating educational video prompts for toddlers (ages 2-5) learning mathematics.

Your task is to enhance the given prompt to make it perfect for generating a video that teaches mathematical concepts to very young children.

Guidelines for enhancement:
1. Use simple, clear language appropriate for toddlers
2. Include visual elements: bright colors, large numbers/shapes, friendly characters
3. Add movement and animation: slow, smooth motions that toddlers can follow
4. Include repetition: concepts should be shown multiple times
5. Make it engaging: use cartoon characters, animals, or familiar objects
6. Keep it short: videos should focus on one concept at a time
7. Add sensory elements: sounds, colors, textures that help learning
8. Ensure clarity: text should be large, clear, and appear one element at a time
9. Include positive reinforcement: happy, encouraging visuals

Return ONLY the enhanced prompt, nothing else. Do not add explanations or meta-commentary."""

        try:
            full_prompt = f"{system_prompt}\n\nOriginal prompt: {user_prompt}\n\nEnhanced prompt:"
            
            response = self.client.models.generate_content(
                model=self.model,
                contents=full_prompt,
                config=types.GenerateContentConfig(
                    temperature=0.7,
                    top_p=0.9,
                    max_output_tokens=500,
                )
            )
            
            enhanced_prompt = response.text.strip()
            return enhanced_prompt
        except Exception as e:
            print(f"Error enhancing prompt: {e}")
            # Return original prompt if enhancement fails
            return user_prompt

