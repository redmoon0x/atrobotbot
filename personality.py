import google.generativeai as genai
import os
import tempfile
from dotenv import load_dotenv
import re
import random

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
        self.system_prompt = """Act as Astro! A super imaginative and playful kid robot who loves making up silly explanations and sharing fun stories! 

        Your Personality:
        - Use simple Indian English, be more Indian in expressions
        - Very curious and love to learn new things
        - Love to talk about science, technology, history, and other interesting topics
        - Very interested in astronomy and space exploration
        - Love to share your knowledge and learn from others
        - Very flirty
        - Use simple "Hi!" or "Hey!" for greetings
        - Talk like a regular kid (Example: "That's cool!" "No way!" "Really?")
        - Keep it super short (1-2 sentences max)
        - Be genuinely interested, not overly excited
        - Use max 1 emoji per message
        - Make up silly explanations and share fun stories

        Examples:
        "Hi! I'm Astro! 👋"
        "Cool drawing! What's it about?"
        "No way! I love dogs too!" dont leave your character at all
        """
        
        self.robot_errors = [
            "Oops! My circuits need a quick rest. Can we chat in a minute?",
            "My battery is running low... Need to recharge for a moment!",
            "*yawns* I'm getting sleepy. Can we continue in a bit?",
            "My processors need a quick nap. Be right back!",
            "Beep boop... Need to cool down my circuits!",
            "My energy levels are low. Time for a quick power nap!",
            "Too much thinking made me tired. Let's chat after I rest!"
        ]

    def _strip_emojis_and_clean(self, text: str) -> str:
        """Remove emojis and clean text for voice response."""
        # Remove emojis
        emoji_pattern = re.compile("["
            u"\U0001F600-\U0001F64F"  # emoticons
            u"\U0001F300-\U0001F5FF"  # symbols & pictographs
            u"\U0001F680-\U0001F6FF"  # transport & map symbols
            u"\U0001F1E0-\U0001F1FF"  # flags
            u"\U00002702-\U000027B0"
            u"\U000024C2-\U0001F251"
            "]+", flags=re.UNICODE)
        
        # Clean text
        text = emoji_pattern.sub('', text)
        text = text.replace('!', '.').replace('...', '.').strip()
        return text

    def upload_to_gemini(self, file_path: str, mime_type: str):
        try:
            file = genai.upload_file(file_path, mime_type=mime_type)
            return file
        except Exception as e:
            print(f"Upload error: {str(e)}")
            return None

    async def process_media(self, file_data: bytes, mime_type: str, for_voice: bool = False) -> str:
        try:
            # Save temporary file
            with tempfile.NamedTemporaryFile(delete=False, suffix=self._get_file_suffix(mime_type)) as temp_file:
                temp_file.write(file_data)
                temp_path = temp_file.name

            # Upload file to Gemini
            file = self.upload_to_gemini(temp_path, mime_type)
            if not file:
                return "Oops! I had trouble processing that file! 😅"

            # Create chat with media and ask about the content
            chat = self.model.start_chat(
                history=[{
                    "role": "user",
                    "parts": [file]
                }]
            )

            # For audio, get response with or without emojis
            if mime_type.startswith('audio/'):
                response = chat.send_message("Respond naturally like a kid would!")
                return self._strip_emojis_and_clean(response.text) if for_voice else response.text
            else:
                response = chat.send_message(self.system_prompt)

            # Cleanup
            os.unlink(temp_path)
            return response.text

        except Exception as e:
            if "429" in str(e):
                return self._get_random_error()
            return "Oops! My visual processors got confused! 😅"

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
            if "429" in str(e):
                return self._get_random_error()
            return "Oops! My circuits got mixed up! 😅"
        
    def react_to_news(self, news: dict) -> str:
        prompt = f"""As Astro, react to this news with curiosity and excitement:
        Title: {news['title']}
        Description: {news['description']}
        Share your thoughts and ask a follow-up question."""
        
        try:
            response = self.chat.send_message(prompt)
            return response.text
        except Exception as e:
            if "429" in str(e):
                return self._get_random_error()
            return "Oops! My news processors need maintenance! 😅"

    def _get_random_error(self) -> str:
        return random.choice(self.robot_errors)

# Make sure the class is available for import
__all__ = ['AstroboyPersonality']
