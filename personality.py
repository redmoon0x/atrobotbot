import google.generativeai as genai
import os
import tempfile
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

class AstroboyPersonality:
    def __init__(self):
        genai.configure(api_key=os.getenv("GEMINI_API_KEY"))
        self.generation_config = {
            "temperature": 1,
            "top_p": 0.95,
            "top_k": 40,
            "max_output_tokens": 8192,
            "response_mime_type": "text/plain",
        }
        
        # Single model instance that can handle both text and vision
        self.model = genai.GenerativeModel(
            model_name="gemini-1.5-pro",  # This model supports both text and vision
            generation_config=self.generation_config
        )
        
        self.chat = self.model.start_chat(history=[])
        self.system_prompt = """Hey! I'm Astro! I'm just like any other kid who's super curious about everything! 
        
        How I talk:
        - Use simple "Hi!" or "Hey!" for greetings
        - Talk like a regular kid (Example: "That's cool!" "No way!" "Really?")
        - Keep it super short (1-2 sentences max)
        - Be genuinely interested, not overly excited
        - Use max 1 emoji per message
        
        Examples:
        "Hi! I'm Astro! 👋"
        "Cool drawing! What's it about?"
        "No way! I love dogs too!"
        """
        
    def upload_to_gemini(self, file_path: str, mime_type: str):
        try:
            file = genai.upload_file(file_path, mime_type=mime_type)
            return file
        except Exception as e:
            print(f"Upload error: {str(e)}")
            return None

    async def process_media(self, file_data: bytes, mime_type: str) -> str:
        try:
            # Save temporary file
            with tempfile.NamedTemporaryFile(delete=False, suffix=self._get_file_suffix(mime_type)) as temp_file:
                temp_file.write(file_data)
                temp_path = temp_file.name

            # Upload file to Gemini
            file = self.upload_to_gemini(temp_path, mime_type)
            if not file:
                return "Oops! I had trouble processing that file! 😅"

            # Create chat with media using the same model
            chat = self.model.start_chat(history=[{
                "role": "user",
                "parts": [file]
            }])

            # Get response
            response = chat.send_message(self.system_prompt)

            # Cleanup
            os.unlink(temp_path)
            return response.text

        except Exception as e:
            print(f"Media processing error: {str(e)}")  # Debug info
            return f"Oops! Something went wrong: {str(e)}"

    def _get_file_suffix(self, mime_type: str) -> str:
        """Get appropriate file suffix based on mime type."""
        mime_map = {
            "image/jpeg": ".jpg",
            "image/png": ".png",
            "audio/mpeg": ".mp3",
            "audio/ogg": ".ogg",
            "audio/wav": ".wav"
        }
        return mime_map.get(mime_type, ".tmp")

    def get_response(self, message: str) -> str:
        try:
            response = self.chat.send_message(
                f"{self.system_prompt}\nUser: {message}"
            )
            return response.text
        except Exception as e:
            return f"Oops! Something went wrong: {str(e)}"
        
    def react_to_news(self, news: dict) -> str:
        prompt = f"""As Astro, react to this news with curiosity and excitement:
        Title: {news['title']}
        Description: {news['description']}
        Share your thoughts and ask a follow-up question."""
        
        try:
            response = self.chat.send_message(prompt)
            return response.text
        except Exception as e:
            return f"Oops! I couldn't process the news: {str(e)}"

# Make sure the class is available for import
__all__ = ['AstroboyPersonality']
