# WebSocket Voice Chat

A simple Python-based voice chat system utilizing WebSockets, allowing users to talk to each other in real time over the internet.  
This project provides both a relay server (using WebSockets) and a Python client that streams audio between participants.

## Features

- Real-time voice communication between multiple clients
- WebSocket-based transport (works over the internet, including with Render)
- Cross-platform Python client

## Requirements

- Python 3.7+
- See `requirements.txt` for Python dependencies

## Installation

1. **Clone the repository:**
   ```bash
   git clone https://github.com/YOUR_USERNAME/YOUR_REPOSITORY.git
   cd YOUR_REPOSITORY
   ```

2. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

## Usage

### 1. Start the WebSocket Voice Relay Server

If you want to run the server locally:
```bash
python audio_ws_server.py
```
- **Or** deploy `audio_ws_server.py` as a web service on [Render](https://render.com/) or another cloud platform that supports WebSockets.

### 2. Run the Voice Chat Client

Update the `WS_URL` variable in `audio_ws_client.py` to point to your deployed server, e.g.:
```python
WS_URL = "wss://your-server.onrender.com/ws"
```
Then run:
```bash
python audio_ws_client.py
```
- Use this on two or more machines to talk to each other!

## Notes

- For the client, your computer must have a microphone and speakers.
- The server only relays data; it does not store or process audio.

## License

MIT License
