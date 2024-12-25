import edge_tts
import asyncio
import tempfile
import os

class VoiceHandler:
    def __init__(self):
        self.voice = "en-US-AriaNeural"
        self.pitch = "+20Hz"
        self.rate = "+15%"
        # Use Termux's temp directory
        self.temp_dir = "/data/data/com.termux/files/usr/tmp"
        os.makedirs(self.temp_dir, exist_ok=True)

    async def text_to_speech_async(self, text: str) -> bytes:
        """Convert text to speech using Edge TTS."""
        try:
            communicate = edge_tts.Communicate(
                text, 
                self.voice, 
                pitch=self.pitch, 
                rate=self.rate
            )
            
            # Use Termux-specific temp path
            temp_path = os.path.join(self.temp_dir, f"voice_{os.getpid()}.mp3")
            
            # Save audio to file
            await communicate.save(temp_path)
            
            # Read and return content
            with open(temp_path, 'rb') as audio_file:
                audio_content = audio_file.read()
            
            # Cleanup
            os.unlink(temp_path)
            return audio_content

        except Exception as e:
            print(f"TTS Error in Termux: {str(e)}")
            return None

    def text_to_speech(self, text: str) -> bytes:
        """Synchronous wrapper for text_to_speech_async."""
        return asyncio.run(self.text_to_speech_async(text))
