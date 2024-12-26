from flask import Flask, render_template, request, Response
from astro_bot import AstroBot
import threading
import os
import telebot

app = Flask(__name__)
bot = AstroBot()

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/', methods=['POST'])
def webhook():
    if request.headers.get('content-type') == 'application/json':
        json_string = request.get_data().decode('utf-8')
        update = telebot.types.Update.de_json(json_string)
        bot.bot.process_new_updates([update])
        return Response('ok', status=200)
    else:
        return Response(status=403)

def run_bot():
    bot.run()

if __name__ == '__main__':
    # Start the bot in a separate thread
    bot_thread = threading.Thread(target=run_bot)
    bot_thread.start()
    
    # Run the Flask app
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)
