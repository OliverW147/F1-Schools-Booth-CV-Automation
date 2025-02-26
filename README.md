# F1 in Schools Booth Automation  

This project was created for a Year 11 F1 in Schools competition booth. It uses hand gesture recognition to trigger keyboard inputs via Discord.  

## Overview  

The system consists of two scripts:  

- **server.py**: Detects hand gestures using a webcam and sends the detected finger count to a Discord channel.  
- **client.py**: Listens for messages in the Discord channel and simulates keyboard inputs based on the received number.  

## How It Works  

1. **server.py** uses OpenCV and MediaPipe to track hand gestures and determine the number of fingers raised.  
2. The detected number is sent to a Discord channel via a webhook.  
3. **client.py** reads the messages from Discord and simulates keyboard inputs accordingly.  

## Setup  

1. Install Python and the required libraries (`discord.py`, `keyboard`, `opencv-python`, `mediapipe`, `requests`).  
2. Replace the Discord webhook URL and bot token with your own.  
3. Run `server.py` to start hand detection.  
4. Run `client.py` to start the Discord bot.  
