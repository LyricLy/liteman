import argparse
import os
import pathlib

import youtube_dl
from ltman.main import process_link


ytdl_opts = {
    "format": "bestaudio/best",
    "outmpl": "%(title)s-%(id)s.%(ext)s",
    "restrictfilenames": True
}

def download_link(link):
    with youtube_dl.YoutubeDL(ytdl_opts) as dl:
        info_dict = dl.extract_info(link, download=True)
        entry = info_dict["entries"][0]
        dl = f"{entry['title']}-{entry['id']}.{entry['ext']}"
        return youtube_dl.utils.sanitize_filename(dl, restricted=True)

def file_to_mp3(file_name):
    output = file_name.rsplit(".", 1)[:-1] + ".mp3"
    os.system(f"ffmpeg -y -i {file_name} -vn -c:a libmp3lame {output}")
    os.remove(file_name)
    return output

def normalize_audio(file_name):
    os.system(f"ffmpeg-normalize {file_name} -of output -c:a libmp3lame -ext mp3")
    os.remove(file_name)


parser = argparse.ArgumentParser(description="Download, convert, and normalize online videos.")
parser.add_argument("links", type=str, nargs="+", help="Links to process.")
args = parser.parse_args()

if __name__ == "__main__":
    for link in args.links:
        normalize_audio(file_to_mp3(download_link(link)))
