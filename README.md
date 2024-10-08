# Description
A pytube-based Youtube Downloader with a GUI.
<p align="center"> <img src="https://github.com/dhairyapatel1506/youtube-downloader/assets/101339040/d8866e33-cc5f-48b8-b628-f77ce2f113cf"> </p>

# Features
- Can download different video qualities.
- Feature to download only audio.
- Can download Shorts.
- Can bypass age-restricted videos.

# Requirements
- Python
	- pytube
	- ffmpeg
- <a href="https://www.gyan.dev/ffmpeg/builds/packages/ffmpeg-7.0-essentials_build.zip">ffmpeg.exe</a>

# Download
If you do not want to set it up yourself, you can download the application directly from <a href="https://github.com/dhairyapatel1506/youtube-downloader/releases">Releases</a>.

# Setup
- **Step 1: Clone the repository.**
  - ```git clone https://github.com/dhairyapatel1506/youtube-downloader.git```
- **Step 2: Install the python dependencies.**
  - ```pip install -r requirements.txt```
## Windows
- **Step 3: Download and setup the ffmpeg executable file.**
  1. You can download the ffmpeg zip file directly from **Requirements** or you can find it on their official <a href="https://ffmpeg.org/download.html">website</a>.
  2. Once downloaded, extract it and look for _ffmpeg.exe_.
  3. Now all that's left to do is to move it to the same folder as your python (_main.py_) file.
## Linux
- **Step 3: Install ffmpeg.**
  - ```sudo apt install ffmpeg```

# Usage
Run: ```python main.py```
## Authentication
This step is optional. If you choose _No_, OAuth will not be used and you can download videos without any additional steps. Use this option only if you wish to bypass age-restricted videos or have trouble downloading certain videos. 

Once successfully authenticated, you will never be asked to do so again till your token expires or the _tokens.json_ file is deleted.
<p align="center"> <img src="https://github.com/dhairyapatel1506/youtube-downloader/assets/101339040/018f365f-7546-4c80-8034-5ec19ddc401a"> </p>

If you do wish to use OAuth, follow these steps:
- **Step 1:**
  - Paste your Youtube link.
  - Select _Yes_ to authenticate.
  - Press _Submit_.

- **Step 2:**
  <p align="center"> <img src="https://github.com/dhairyapatel1506/youtube-downloader/assets/101339040/c6c86d89-353a-45b7-99a5-20278fb1fb74"> </p>
  
  - You should see some text like this at the bottom of the app's interface. Click on it and you'll be redirected to a page on your browser.
  - Enter your code and click _Continue_.
  - After successfully completing all the steps on the page, you can close your browser and return to the application.
  - Finally, click on the Authenticate button.

You've successfully completed your OAuth process.

# ToDo
  <p>☐ Implement multi-threaded downloading to increase download speeds.</p>
  <p>☐ Display time taken to download.</p>
  <p>☐ Add support for downloading in different FPS (Frames Per Second).</p>
  <p>☐ Add capability to preview a video before downloading it.</p>
  <p><s>☑ Add capability to download multiple videos in a single session.</s></p>
  <p>☐ Add capability to download entire playlists.</p>
