import os
import telebot
import requests
import asyncio
import io
import speech_recognition as sr
from pydub import AudioSegment
from personality import AstroboyPersonality
from news_fetcher import NewsFetcher
from dotenv import load_dotenv
from voice_handler import VoiceHandler

# Load environment variables
load_dotenv()

class AstroBot:
    def __init__(self):
        self.bot = telebot.TeleBot(os.getenv("TELEGRAM_TOKEN"))
        self.personality = AstroboyPersonality()
        self.news_fetcher = NewsFetcher()
        self.recognizer = sr.Recognizer()
        self.voice_handler = VoiceHandler()
        self.setup_handlers()
        
        # Add webhook mode if URL is provided
        self.webhook_url = os.getenv("WEBHOOK_URL")
        if self.webhook_url:
            self.bot.remove_webhook()
            self.bot.set_webhook(url=self.webhook_url)
        
    def setup_handlers(self):
        @self.bot.message_handler(commands=['start'])
        def start_command(message):
            self.bot.reply_to(message, "Hi! I'm Astro! 👋 What's up?")

        @self.bot.message_handler(commands=['news'])
        def news_command(message):
            try:
                category = message.text.split()[1] if len(message.text.split()) > 1 else None
                news = self.news_fetcher.get_random_news(category)
                response = self.personality.react_to_news(news)
                if 'link' in news:
                    response += f"\n\nRead more: {news['link']}"
                self.bot.reply_to(message, response)
            except Exception:
                self.bot.reply_to(message, "Try: /news [top|tech|science|india|business]")

        @self.bot.message_handler(func=lambda message: True)
        def handle_message(message):
            try:
                # Get and send text response only
                response = self.personality.get_response(message.text)
                self.bot.reply_to(message, response)
            except Exception as e:
                print(f"Message handling error: {str(e)}")
                self.bot.reply_to(message, "Oops! Something went wrong! 😅")

        @self.bot.message_handler(content_types=['photo'])
        def handle_photo(message):
            try:
                # Get file info
                file_info = self.bot.get_file(message.photo[-1].file_id)
                file_url = f"https://api.telegram.org/file/bot{os.getenv('TELEGRAM_TOKEN')}/{file_info.file_path}"
                
                # Download file content
                downloaded_file = requests.get(file_url).content
                
                # Process with personality
                loop = asyncio.new_event_loop()
                asyncio.set_event_loop(loop)
                response = loop.run_until_complete(
                    self.personality.process_media(downloaded_file, "image/jpeg")
                )
                loop.close()
                
                self.bot.reply_to(message, response)
            except Exception as e:
                print(f"Photo error: {str(e)}")  # For debugging
                self.bot.reply_to(message, "Ooh! I can't see the picture clearly! Can you send it again? 🤔")

        @self.bot.message_handler(content_types=['voice', 'audio'])
        def handle_audio(message):
            try:
                # Get file info and content
                file_info = self.bot.get_file(message.voice.file_id if hasattr(message, 'voice') else message.audio.file_id)
                file_url = f"https://api.telegram.org/file/bot{os.getenv('TELEGRAM_TOKEN')}/{file_info.file_path}"
                audio_content = requests.get(file_url).content
                
                # Get clean response without emojis for voice
                loop = asyncio.new_event_loop()
                asyncio.set_event_loop(loop)
                voice_response = loop.run_until_complete(
                    self.personality.process_media(audio_content, "audio/mpeg", True)
                )
                loop.close()
                
                # Generate and send only voice response
                audio_content = self.voice_handler.text_to_speech(voice_response)
                if audio_content:
                    self.bot.send_voice(
                        message.chat.id,
                        audio_content,
                        reply_to_message_id=message.message_id
                    )
                
            except Exception as e:
                print(f"Audio error: {str(e)}")
                self.bot.reply_to(message, "I had trouble with that audio message. Could you try again? 🎤")

    def run(self):
        if not self.webhook_url:
            self.bot.infinity_polling()
        # If webhook_url is set, the bot will handle updates through the webhook

def main():
    bot = AstroBot()
    bot.run()

if __name__ == "__main__":
    main()
