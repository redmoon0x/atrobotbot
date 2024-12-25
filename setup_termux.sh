#!/data/data/com.termux/files/usr/bin/bash

# Update package list
pkg update -y

# Install required packages
pkg install -y python git

# Create bot directory
mkdir -p ~/astrobot

# Install Python dependencies
pip install -r requirements.txt

# Setup environment
echo "Creating .env file..."
if [ ! -f .env ]; then
    echo "GEMINI_API_KEY=your_gemini_api_key" > .env
    echo "TELEGRAM_TOKEN=your_telegram_token" >> .env
fi

echo "Setup complete! Edit .env with your API keys and run: python astro_bot.py"
