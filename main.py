import os.path

from moviepy.editor import *
from pytube import YouTube, Playlist

if not (os.path.exists('./Downloads/converted')):
    os.makedirs("./Downloads/converted")


def on_progress(stream, chunk, bytes_remaining):
    """Callback function"""
    total_size = stream.filesize
    bytes_downloaded = total_size - bytes_remaining
    pct_completed = bytes_downloaded / total_size * 100
    print(f"Status: {round(pct_completed, 2)} %")


def download_single_file(url):
    print("Download single file " + url)
    yt = YouTube(url, on_progress_callback=on_progress)

    title = yt.title.replace('"', '').replace('【', '').replace('】', '').replace('/', '-')
    print("Title: " + title)

    streams = yt.streams.get_lowest_resolution()  # lowest resolution is enough for mp3 file
    print(streams)

    streams.download("./Downloads", skip_existing=True)
    try:
        video = VideoFileClip(filename="./Downloads/" + title + ".mp4")
        video.audio.write_audiofile("./Downloads/converted/" + title + ".mp3")
        video.close()

        os.remove("./Downloads/" + title + ".mp4")
    except IOError as e:
        print("Error: %s", e)


def download(files: list[str]):
    print("Download files.....")
    for file in files:
        download_single_file(file)


def playlist_process(playlist: str):
    print("Processing playlist...." + playlist)
    p = Playlist(playlist)
    for url in p.video_urls:
        print("path: " + url)
        download_single_file(url)


def convert_files_to_mp3():
    files_in_dir = os.listdir("./Downloads")
    filtered = list(filter(lambda f: f.endswith(".mp4"), files_in_dir))
    convert_list(filtered)


def convert_list(list_to_convert: list[str]):
    for file in list_to_convert:
        try:
            video = VideoFileClip(filename="./Downloads/" + file)
            video.audio.write_audiofile("./Downloads/converted/" + file.replace(".mp4", ".mp3"))
            video.close()

            os.remove("./Downloads/" + file)
        except IOError as e:
            print("Error: %s", e)


manual_files = ['']  # provide list of links to youtube clips
# https://www.youtube.com/watch?v=nRVf6fAnsS4&list=RD0vxx04quIzs
# playlist_process('') # provide YT list url
# download(manual_files)
# convert_files_to_mp3()
