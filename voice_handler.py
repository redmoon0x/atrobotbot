from gtts import gTTS
import os
import io

class VoiceHandler:
    def __init__(self):
        # Create audio directory in project folder
        self.audio_dir = os.path.join(os.path.dirname(__file__), "temp_audio")
        os.makedirs(self.audio_dir, exist_ok=True)

    def text_to_speech(self, text: str) -> bytes:
        """Convert text to speech using Google Text-to-Speech."""
        try:
            # Create a temporary file path
            output_path = os.path.join(self.audio_dir, f"voice_{os.getpid()}.mp3")
            
            # Create gTTS instance
            tts = gTTS(text=text, lang='en', tld='co.in')
            
            # Save to file
            tts.save(output_path)
            
            # Read the generated file
            with open(output_path, 'rb') as audio_file:
                audio_content = audio_file.read()
            
            # Clean up
            if os.path.exists(output_path):
                os.remove(output_path)
                
            return audio_content

        except Exception as e:
            print(f"TTS Error: {str(e)}")
            return None
