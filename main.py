from tkinter import *
from tkinter.ttk import Progressbar
from pytube import YouTube, request
from pytube.cli import on_progress
from pytube.innertube import InnerTube
from time import time
import pytube.request
import os
import ffmpeg
import subprocess
import shutil
import time
import json
import webbrowser
import pathlib
import ssl
import threading

root = Tk()
video = None
resolutions = ["144p", "240p", "360p", "480p", "720p", "1080p", "1440p", "2160p"]
resVar = StringVar()
authVar = IntVar()
authRVar = StringVar(value="no")
_client_id = '861556708454-d6dlm3lh05idd8npek18k6be8ba3oc68.apps.googleusercontent.com'
_client_secret = 'SboVhoG9s0rNafixCSGGKXAT'
filename = 'defaultclients.json'
with open(filename) as f:
    _default_clients = json.load(f)
_cache_dir = pathlib.Path(__file__).parent.resolve() / '__cache__'
_token_file = os.path.join(_cache_dir, 'tokens.json')
ssl._create_default_https_context = ssl._create_stdlib_context

def submit():
    global video
    url = urlEntry.get()
    try:
        if(authRVar.get()=="yes" or os.path.exists(_token_file)):
            authenticateButton.config(state="active")
            video = YouTube(url, on_progress_callback=on_progress, use_oauth=True)
        else:
            video = YouTube(url, on_progress_callback=on_progress) 
        #print(video.streams)
        TitleLabel.config(text=f"Title: {video.title}")
        submitButton.config(state="disabled")
        videoButton.config(state="active")
        audioButton.config(state="active")
        for widget in root.winfo_children():
                if isinstance(widget, Radiobutton):
                    widget.configure(state="disabled")
    except Exception as e:
        if("regex_search" in str(e)):
            TitleLabel.config(text="Please enter a valid url.")
        elif("is unavailable" in str(e)):
            TitleLabel.config(text="Not a valid Youtube video.")
        else:
            print(e)

def videostream():
    rbsExist = False
    videoButton.config(state="disabled")
    audioButton.config(state="active")
    downloadButton.config(state="active")
    for widget in root.winfo_children():
        if(isinstance(widget, Radiobutton) and widget.cget('text') in resolutions):
            rbsExist = True
            if(widget.cget('state')=="disabled"):
                 widget.config(state="active")
    if not rbsExist:
        videoLabel = Label(root, text="Available Video Qualities:")
        videoLabel.pack()
        for res in resolutions:
            videoStream = video.streams.filter(res=res, subtype="mp4").first()
            if(videoStream!=None and videoStream.is_adaptive):
                resRadioButton = Radiobutton(root, text=res, variable=resVar, value=res)
                resRadioButton.pack()
            else:
                if(video.streams.get_by_resolution(res)!=None):
                    resRadioButton = Radiobutton(root, text=res, variable=resVar, value=res)
                    resRadioButton.pack()

def audiostream():
    audioButton.config(state="disabled")
    videoButton.config(state="active")
    downloadButton.config(state="active")
    # Disables all Radio Buttons
    for widget in root.winfo_children():
        if(isinstance(widget, Radiobutton) and widget.cget('text') in resolutions):
            widget.configure(state="disabled")

def downloadstream():
    # Function to start the download in a separate thread
    def start_download():
        try:
            dashFlag = False
            if audioButton.cget('state')=="disabled":
                processLabel.config(text="Downloading audio..")
                processLabel.update()
                out_path = video.streams.get_audio_only().download()
                idtfier = out_path.split('.')
                os.rename(out_path, f"{idtfier[0]}.mp3")
                processLabel.config(text="Your audio has been downloaded!")

            else:
                resolution = resVar.get()
                if(video.streams.filter(res=resolution, subtype="mp4").first()).is_adaptive:
                    dashFlag = True
                if dashFlag: 
                    processLabel.config(text="Downloading video..")
                    processLabel.update()
                    out_path = video.streams.filter(res=resolution, subtype="mp4").first().download()
                    idtfier = out_path.split('.')
                    os.rename(out_path, f"Video." + idtfier[-1])
                    processLabel.config(text="Downloading audio..")
                    processLabel.update()
                    out_path = video.streams.get_audio_only().download()
                    idtfier = out_path.split('.')
                    os.rename(out_path, f"Audio." + idtfier[-1])
                    processLabel.config(text="Merging audio and video files..")
                    processLabel.update()
                    subprocess.run(f"ffmpeg -hide_banner -loglevel error -i Video.mp4 -i Audio.mp4 -c copy Output.mp4", shell=True)
                    os.remove("Audio.mp4")
                    os.remove("Video.mp4")
                    processLabel.config(text="Your video has been downloaded!")
                else:
                    out_path = video.streams.filter(progressive=True, res=resolution).first().download()
                    processLabel.config(text="Your video has been downloaded!")

        except Exception as e:
            print(e)
        finally:
            # Re-enable the download button after completion
            downloadButton.config(state="active")

    # Disable the download button while downloading
    downloadButton.config(state="disabled")

    # Create a new thread for downloading
    download_thread = threading.Thread(target=start_download)
    download_thread.start()

def on_progress(stream, chunk, bytes_remaining):
    total_size = stream.filesize
    bytes_downloaded = total_size - bytes_remaining
    percentage_of_completion = bytes_downloaded / total_size * 100
    per = str(int(percentage_of_completion))
    old_perc = percentage_of_completion
    progressLabel.config(text=per + '%')
    progressLabel.update()
    progressBar.config(value=percentage_of_completion)
    progressBar.update()

def _new_fetch_bearer_token(self):
    """Fetch an OAuth token."""
    # Subtracting 30 seconds is arbitrary to avoid potential time discrepencies
    start_time = int(time.time() - 30)
    data = {
        'client_id': _client_id,
        'scope': 'https://www.googleapis.com/auth/youtube'
    }
    response = request._execute_request(
        'https://oauth2.googleapis.com/device/code',
        'POST',
        headers={
            'Content-Type': 'application/json'
        },
        data=data
    )
    response_data = json.loads(response.read())
    verification_url = response_data['verification_url']
    user_code = response_data['user_code']
    processLabel.config(text=f'Please visit: {verification_url} and input code: {user_code},\nand then press Authenticate to continue.', fg="blue", cursor="hand2")
    processLabel.bind("<Button-1>", lambda e: callback(verification_url))
    processLabel.update()
    authenticateButton.wait_variable(authVar)
    data = {
        'client_id': _client_id,
        'client_secret': _client_secret,
        'device_code': response_data['device_code'],
        'grant_type': 'urn:ietf:params:oauth:grant-type:device_code'
    }
    try:
        response = request._execute_request(
            'https://oauth2.googleapis.com/token',
            'POST',
            headers={
                'Content-Type': 'application/json'
            },
            data=data
        )
        response_data = json.loads(response.read())

        self.access_token = response_data['access_token']
        self.refresh_token = response_data['refresh_token']
        self.expires = start_time + response_data['expires_in']
        self.cache_tokens()
        processLabel.unbind("<Button-1>")
        processLabel.config(text="Authentication Successful", fg="black", cursor="arrow")
    except:
        processLabel.config(text=f"Authentication Unsuccessful, press Submit and try again.")
        submitButton.config(state="active")

def __newinit__(self, client='ANDROID_CREATOR', use_oauth=False, allow_cache=True):
    """Initialize an InnerTube object.

    :param str client:
        Client to use for the object.
        Default to web because it returns the most playback types.
    :param bool use_oauth:
        Whether or not to authenticate to YouTube.
    :param bool allow_cache:
        Allows caching of oauth tokens on the machine.
    """
    self.context = _default_clients[client]['context']
    self.header = _default_clients[client]['header']
    self.api_key = _default_clients[client]['api_key']
    self.access_token = None
    self.refresh_token = None
    self.use_oauth = use_oauth
    self.allow_cache = allow_cache

    # Stored as epoch time
    self.expires = None

    # Try to load from file if specified
    if self.use_oauth and self.allow_cache:
        # Try to load from file if possible
        if os.path.exists(_token_file):
            with open(_token_file) as f:
                data = json.load(f)
                self.access_token = data['access_token']
                self.refresh_token = data['refresh_token']
                self.expires = data['expires']
                self.refresh_bearer_token()

def callback(url):
    webbrowser.open_new(url)

def _new_cache_tokens(self):
        """Cache tokens to file if allowed."""
        if not self.allow_cache:
            return

        data = {
            'access_token': self.access_token,
            'refresh_token': self.refresh_token,
            'expires': self.expires
        }
        if not os.path.exists(_cache_dir):
            os.mkdir(_cache_dir)
        with open(_token_file, 'w') as f:
            json.dump(data, f)

def selectall(event):
    # select text
    event.widget.select_range(0, 'end')
    # move cursor to the end
    event.widget.icursor('end')

def _new_get_throttling_function_name(js: str) -> str:
    import logging
    import re
    logger = logging.getLogger(__name__)
    """Extract the name of the function that computes the throttling parameter.

    :param str js:
        The contents of the base.js asset file.
    :rtype: str
    :returns:
        The name of the function used to compute the throttling parameter.
    """
    function_patterns = [
        # https://github.com/ytdl-org/youtube-dl/issues/29326#issuecomment-865985377
        # https://github.com/yt-dlp/yt-dlp/commit/48416bc4a8f1d5ff07d5977659cb8ece7640dcd8
        # var Bpa = [iha];
        # ...
        # a.C && (b = a.get("n")) && (b = Bpa[0](b), a.set("n", b),
        # Bpa.length || iha("")) }};
        # In the above case, `iha` is the relevant function name
        r'a\.[a-zA-Z]\s*&&\s*\([a-z]\s*=\s*a\.get\("n"\)\)\s*&&\s*',
        r'\([a-z]\s*=\s*([a-zA-Z0-9$]+)(\[\d+\])?\([a-z]\)',
        r'\([a-z]\s*=\s*([a-zA-Z0-9$]+)(\[\d+\])\([a-z]\)'
    ]
    logger.debug('Finding throttling function name')
    for pattern in function_patterns:
        regex = re.compile(pattern)
        function_match = regex.search(js)
        if function_match:
            logger.debug("finished regex search, matched: %s", pattern)
            if len(function_match.groups()) == 1:
                return function_match.group(1)
            idx = function_match.group(2)
            if idx:
                idx = idx.strip("[]")
                array = re.search(
                    r'var {nfunc}\s*=\s*(\[.+?\]);'.format(
                        nfunc=re.escape(function_match.group(1))),
                    js
                )
                if array:
                    array = array.group(1).strip("[]").split(",")
                    array = [x.strip() for x in array]
                    return array[int(idx)]

    raise RegexMatchError(
        caller="_new_get_throttling_function_name", pattern="multiple"
    )

InnerTube.fetch_bearer_token = _new_fetch_bearer_token
InnerTube.__init__ = __newinit__ 
InnerTube.cache_tokens = _new_cache_tokens
pytube.cipher.get_throttling_function_name = _new_get_throttling_function_name

root.title("Youtube Downloader")

urlEntry = Entry(root, width=52)
urlEntry.pack()
urlEntry.bind('<Control-KeyRelease-a>', selectall)

if not os.path.exists(_token_file):
    TitleLabel = Label(root, text="Authenticate?")
    TitleLabel.pack()
    authRadioButton1 = Radiobutton(root, text="Yes", variable=authRVar, value="yes")
    authRadioButton1.pack()
    authRadioButton2 = Radiobutton(root, text="No", variable=authRVar, value="no")
    authRadioButton2.pack()

else:
    TitleLabel = Label(root, text="")
    TitleLabel.pack()

progressLabel = Label(root, text="")
progressLabel.pack()
progressBar = Progressbar(root, length=200, mode='determinate')
progressBar.pack()

submitButton = Button(root, text="Submit", command=submit, width=8)
submitButton.pack()
videoButton = Button(root, text="Video", command=videostream, state="disabled", width=8)
videoButton.pack()
audioButton = Button(root, text="Audio", command=audiostream, state="disabled", width=8)
audioButton.pack()
downloadButton = Button(root, text="Download", command=downloadstream, state="disabled", width=8)
downloadButton.pack()

authenticateButton = Button(root, text="Authenticate", command=lambda: authVar.set(1), state="disabled", width=10)
authenticateButton.pack()

processLabel = Label(root, text="")
processLabel.pack(side=BOTTOM)

root.mainloop()
