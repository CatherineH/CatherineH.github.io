"""
The following script contains several helpers to complete images and links.
"""
from os import environ
from os.path import expanduser
from sys import argv
import urllib
import simplejson

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
    print('\n'.join(_words))
    output_file = input_file+"-copy"
    fh = open(output_file, "w+")
    fh.writelines('\n'.join(_words))
    fh.close()


def bandcamp(input_file):
    pass


if __name__ == "__main__":
    input_file = expanduser(argv[1])
    youtube(input_file=input_file)
