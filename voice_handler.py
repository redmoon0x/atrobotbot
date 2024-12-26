import pyttsx3
import os
import io

class VoiceHandler:
    def __init__(self):
        # Initialize the TTS engine
        self.engine = pyttsx3.init()
        # Adjust voice settings for child-like voice
        self.engine.setProperty('rate', 175)     # Slightly faster
        self.engine.setProperty('pitch', 200)    # Higher pitch
        self.engine.setProperty('volume', 0.9)
        
        # Try to set a female/child voice if available
        voices = self.engine.getProperty('voices')
        for voice in voices:
            if "female" in voice.name.lower():
                self.engine.setProperty('voice', voice.id)
                break
        
        # Create audio directory in project folder
        self.audio_dir = os.path.join(os.path.dirname(__file__), "temp_audio")
        os.makedirs(self.audio_dir, exist_ok=True)

    def text_to_speech(self, text: str) -> bytes:
        """Convert text to speech using pyttsx3."""
        try:
            # Create output file path
            output_path = os.path.join(self.audio_dir, f"voice_{os.getpid()}.mp3")
            
            # Generate speech
            self.engine.save_to_file(text, output_path)
            self.engine.runAndWait()
            
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
