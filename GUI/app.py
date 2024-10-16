import os
import random
import subprocess
from flask import Flask, render_template, send_from_directory, request, redirect, url_for, session

app = Flask(__name__)

# Replace this with the path to your folder
FOLDER_PATH = "E:/New folder/gu way/giz a brek/sling thy hook/safe pal"
THUMBNAIL_PATH = "E:/New folder/gu way/giz a brek/sling thy hook/safe pal/gui-thumbnails"  # New folder for thumbnails

# Hardcoded credentials (in a real-world app, use a secure method)
USERNAME = "admin"
PASSWORD = "t3stp4ss"

# Set a secret key for session management
app.secret_key = 'rövkött'

def generate_thumbnail(video_file):
    # Get the filename without extension
    filename = os.path.splitext(video_file)[0]
    thumbnail_file = os.path.join(THUMBNAIL_PATH, f"{filename}.jpg")  # Save as JPG
    
    # Define the full path to the ffmpeg executable
    ffmpeg_path = r"C:\ffmpeg\bin\ffmpeg.exe"  # Update this to your FFmpeg executable path

    # Command to generate the thumbnail using ffmpeg
    command = [
        ffmpeg_path,
        '-i', os.path.join(FOLDER_PATH, video_file),
        '-ss', '00:00:01.000',  # Timestamp for thumbnail
        '-vframes', '1',  # Number of frames to capture
        thumbnail_file
    ]

    # Execute the command
    subprocess.run(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE)

@app.route('/', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        
        if username == USERNAME and password == PASSWORD:
            session['logged_in'] = True
            return redirect(url_for('index'))
    
    return render_template('login.html')

@app.route('/index')
@app.route('/index', methods=['GET'])
def index():
    if not session.get('logged_in'):
        return redirect(url_for('login'))
    
    files = os.listdir(FOLDER_PATH)
    video_files = [file for file in files if file.endswith(('.mp4', '.avi', '.mov', '.mkv'))]
    
    # Generate thumbnails for new videos
    for video in video_files:
        thumbnail_file = os.path.splitext(video)[0] + '.jpg'
        if not os.path.exists(os.path.join(THUMBNAIL_PATH, thumbnail_file)):
            generate_thumbnail(video)

    # Handle search query
    search_query = request.args.get('search')
    if search_query:
        video_files = [file for file in video_files if search_query.lower() in file.lower()]

    random.shuffle(video_files)  # Shuffle video files
    return render_template('index.html', files=video_files)

@app.route('/video/<filename>')
def video_player(filename):
    return render_template('video_player.html', filename=filename)

@app.route('/files/<filename>')
def files(filename):
    return send_from_directory(FOLDER_PATH, filename)

@app.route('/thumbnails/<filename>')
def thumbnails(filename):
    return send_from_directory(THUMBNAIL_PATH, filename)

@app.route('/logout')
def logout():
    session.pop('logged_in', None)
    return redirect(url_for('login'))

if __name__ == "__main__":
    # Create thumbnails directory if it doesn't exist
    if not os.path.exists(THUMBNAIL_PATH):
        os.makedirs(THUMBNAIL_PATH)
    app.run(debug=True)
