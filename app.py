from flask import Flask, render_template, request, Response
from astro_bot import AstroBot
import threading
import os
import telebot
import logging

# Set up logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

app = Flask(__name__)
bot = AstroBot()

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/', methods=['POST'])
def webhook():
    try:
        logger.debug("Received webhook request")
        logger.debug(f"Headers: {request.headers}")
        
        if request.headers.get('content-type') == 'application/json':
            json_string = request.get_data().decode('utf-8')
            logger.debug(f"Received JSON: {json_string}")
            
            update = telebot.types.Update.de_json(json_string)
            bot.bot.process_new_updates([update])
            logger.debug("Successfully processed update")
            return Response('ok', status=200)
        else:
            logger.warning("Invalid content type")
            return Response(status=403)
    except Exception as e:
        logger.error(f"Error in webhook: {str(e)}")
        return Response(status=500)

# Remove the run_bot function and thread since we're using webhook mode
if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)
