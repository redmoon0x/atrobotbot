from flask import Flask
from astro_bot import AstroBot
import threading
import os

app = Flask(__name__)
bot = AstroBot()

@app.route('/')
def home():
    return 'Bot is running!'

def run_bot():
    bot.run()

if __name__ == '__main__':
    # Start the bot in a separate thread
    bot_thread = threading.Thread(target=run_bot)
    bot_thread.start()
    
    # Run the Flask app
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)
