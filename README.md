Spotify Hand Gesture Controller

This project allows you to control Spotify playback using hand gestures detected through your webcam. It uses computer vision to recognize gestures and maps them to actions such as play, pause, volume control, and track navigation.

**Features:**
Play music using an open palm gesture
Pause music using a fist gesture
Skip to next track with a right swipe
Go to previous track with a left swipe
Control volume using finger distance (pinch gesture)
Real-time hand tracking through webcam

**Tech Stack:**
Python
OpenCV
MediaPipe
NumPy
Spotipy (Spotify Web API)
python-dotenv

**Setup Instructions**
1. Clone the Repository
git clone https://github.com/your-username/spotify-gesture-controller.git
cd spotify-gesture-controller
2. Install Dependencies
pip install opencv-python mediapipe numpy spotipy python-dotenv
3. Set Up Spotify API
Go to the Spotify Developer Dashboard and create an application.
Add the following Redirect URI:
http://127.0.0.1:8888/callback
4. Create a .env File
Create a .env file in the root directory and add:

SPOTIPY_CLIENT_ID=your_client_id
SPOTIPY_CLIENT_SECRET=your_client_secret
SPOTIPY_REDIRECT_URI=http://127.0.0.1:8888/callback

5. Run the Application
python main.py

**Please Note**
Spotify Premium is required for playback control
Make sure Spotify is open and playing on your device
Use the same Spotify account for authentication
Ensure proper lighting for better gesture detection

**Gesture Controls:**

Open palm: Play
Fist: Pause
Swipe right: Next track
Swipe left: Previous track
Pinch gesture: Volume control

**How It Works**
MediaPipe is used to detect hand landmarks from the webcam feed.
Gesture recognition is implemented using the relative positions of these landmarks. 
OpenCV handles video capture and display. Spotipy is used to communicate with the Spotify API and execute playback commands.

**Future Improvements**
Display current song and artist
Improve gesture accuracy
Add custom gesture mapping
Enhance UI with better visuals
