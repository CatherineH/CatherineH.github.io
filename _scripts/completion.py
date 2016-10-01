"""
The following script contains several helpers to complete images and links.
"""
from HTMLParser import HTMLParser
from os import environ, mkdir, listdir
from os.path import expanduser, isdir, basename, join, exists, dirname, \
    realpath
from sys import argv
from time import sleep

from bandcamp_dl import Bandcamp

from apiclient.discovery import build
from wget import download

DEVELOPER_KEY = environ['GOOGLE_API_KEY']
YOUTUBE_API_SERVICE_NAME = "youtube"
YOUTUBE_API_VERSION = "v3"
TEMP_DIR = expanduser("~/tmp")
CURRENT_DIRECTORY = dirname(realpath(__file__))


class GooglePlayParser(HTMLParser):
    grab_data = False
    def handle_starttag(self, tag, attrs):
        # grab the link to the album art
        if tag == "img":
            grab_src = False
            for attr in attrs:
                if attr[0] == "alt":
                    if attr[1].find("Cover art") >= 0:
                        grab_src = True
            if grab_src:
                for attr in attrs:
                    if attr[0] == "src":
                        self.found_url = attr[1]
        # grab the page title to get the title and album artist
        if tag == "title":
            self.grab_data = True
        else:
            self.grab_data = False

    def handle_data(self, data):
        if self.grab_data:
            self.artist = data.split(":")[0]
            self.title = data.split(":")[1].replace(" - Music on Google Play", "")

def get_title(id):
    youtube = build(YOUTUBE_API_SERVICE_NAME, YOUTUBE_API_VERSION,
                    developerKey=DEVELOPER_KEY)

    # Call the videos.list method to retrieve location details for each video.
    video_response = youtube.videos().list(
    id=id,
    part='snippet'
    ).execute().get("items", [])[0]
    return video_response["snippet"]["title"]


def substitute_file(input_file, replacer_function):
    fh = open(input_file, "r")
    _text = fh.read(-1)
    fh.close()
    # split on the spaces
    _words = _text.split("\n")
    for i in range(len(_words)):
        _words[i] = replacer_function(_words[i])
    output_file = join(TEMP_DIR, basename(input_file + "-copy"))
    fh = open(output_file, "w+")
    fh.write('\n'.join(_words))
    fh.close()
    return output_file


def youtube(input_file):
    """
    Replace the youtube urls with screenshots and links

    :param input_file: the file to analyze
    :return:
    """
    def replacer(word):
        https_part = "https://www.youtube.com/watch?v="
        if word.find(https_part) == 0:
            token = word.replace(https_part, '')
            desc = get_title(token)
            return "[![" + desc + "](http://img.youtube.com/vi/" + token + \
                        "/0.jpg)](" + word + ")"
        return word
    return substitute_file(input_file, replacer)


def bandcamp(input_file):
    """
    Replace bandcamp urls with album covers and links back to the album.

    :param str input_file: the file to analyze
    :return: the filename of the output file
    :rtype: str
    """
    def replacer(word):
        if word.find("bandcamp.com/album") >= 0:
            parser = Bandcamp().parse(word)
            album_art = parser["art"].replace("_16.jpg", "_14.jpg")
            return "[!["+parser['title']+" - "+parser["artist"]+"]("+\
                        album_art+")]("+word+")"
        return word
    return substitute_file(input_file, replacer)


def google_play(input_file):
    """
    Replace google play urls with album covers and links back to the album

    :param input_file: the file to analyze
    :return: the filename of the output file
    :rtype: str
    """
    def replacer(word):
        if word.find("play.google.com") >= 0:
            target_filename = join(TEMP_DIR, basename(word))
            if not exists(target_filename):
                filename = download(word, target_filename)
                sleep(1)
                #rename(join(CURRENT_DIRECTORY, filename), target_filename)
            parser = GooglePlayParser()
            contents = open(target_filename, "r").read(-1)
            parser.feed(contents)
            album_art = parser.found_url
            return "[![" + parser.title + " - " + parser.artist + "](" + \
                   album_art + ")](" + word + ")"
        return word
    if not isdir(TEMP_DIR):
        mkdir(TEMP_DIR)
    return substitute_file(input_file, replacer)

if __name__ == "__main__":
    input_file = expanduser(argv[1])
    output_file = input_file
    #output_file = youtube(input_file=output_file)
    output_file = bandcamp(output_file)
    output_file = google_play(output_file)