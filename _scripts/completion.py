"""
The following script contains several helpers to complete images and links.
"""
from os import environ
from os.path import expanduser
from sys import argv

from bandcamp_dl import Bandcamp

from apiclient.discovery import build


DEVELOPER_KEY = environ['GOOGLE_API_KEY']
YOUTUBE_API_SERVICE_NAME = "youtube"
YOUTUBE_API_VERSION = "v3"


def get_title(id):
    youtube = build(YOUTUBE_API_SERVICE_NAME, YOUTUBE_API_VERSION,
                    developerKey=DEVELOPER_KEY)

    # Call the videos.list method to retrieve location details for each video.
    video_response = youtube.videos().list(
    id=id,
    part='snippet'
    ).execute().get("items", [])[0]
    return video_response["snippet"]["title"]


def youtube(input_file):
    """
    Replace the youtube urls with screenshots and links
    :param input_file: the file to analyze
    :return:
    """
    fh = open(input_file, "r")
    _text = fh.read(-1)
    fh.close()
    # split on the spaces
    _words = _text.split("\n")
    for i in range(len(_words)):
        https_part = "https://www.youtube.com/watch?v="
        if _words[i].find(https_part) == 0:
            token = _words[i].replace(https_part, '')
            desc = get_title(token)
            _words[i] = "[!["+desc+"](http://img.youtube.com/vi/"+token + \
                       "/0.jpg)]("+_words[i]+")"
    output_file = input_file+"-copy"
    fh = open(output_file, "w+")
    fh.write('\n'.join(_words))
    fh.close()
    return output_file


def bandcamp(input_file):
    """
    Replace bandcamp urls with album covers and links back to the album.
    :param input_file: the file to analyze
    :return:
    """
    fh = open(input_file, "r")
    _text = fh.read(-1)
    fh.close()
    _words = _text.split("\n")
    for i in range(len(_words)):
        if _words[i].find("bandcamp.com/album") >= 0:
            url = _words[i]
            parser = Bandcamp().parse(url)
            album_art = parser["art"].replace("_16.jpg", "_14.jpg")
            _words[i] = "[!["+parser['title']+" - "+parser["artist"]+"]("+\
                        album_art+")]("+url+")"
    output_file = input_file+"-copy"
    fh = open(output_file, "w+")
    fh.write('\n'.join(_words))
    fh.close()
    return output_file


if __name__ == "__main__":
    input_file = expanduser(argv[1])
    output_file = youtube(input_file=input_file)
    bandcamp(output_file)