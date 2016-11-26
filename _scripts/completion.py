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
    title_data = ""
    artist = None
    title = None

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
            if len(self.title_data) > 0:
                if self.title_data.find(":") > 0:
                    self.artist = self.title_data.split(":")[0]
                    self.title = self.title_data.split(":")[1].replace(
                        " - Music on Google Play", "")
                else:
                    raise Exception(
                        "could not find deliminator in title':' in ",
                        self.title_data)

    def handle_data(self, data):
        if self.grab_data:
            self.title_data += data


def get_title(id):
    youtube = build(YOUTUBE_API_SERVICE_NAME, YOUTUBE_API_VERSION,
                    developerKey=DEVELOPER_KEY)

    # Call the videos.list method to retrieve location details for each video.
    video_response = youtube.videos().list(
        id=id,
        part='snippet'
    ).execute().get("items", [])[0]
    return video_response["snippet"]["title"]


def substitute_file(input_file, replacer_function, on_lines=True):
    fh = open(input_file, "r")
    _text = fh.read(-1)
    fh.close()
    # split on the spaces
    if on_lines:
        _words = _text.split("\n")
        for i in range(len(_words)):
            _words[i] = replacer_function(_words[i])
        output_contents = '\n'.join(_words)
    else:
        output_contents = replacer_function(_text)
    output_file = join(TEMP_DIR, basename(input_file + "-copy"))
    fh = open(output_file, "w+")
    fh.write(output_contents)
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
            return "<a href=\"" + word + "\">" \
                   "<img src=\"http://img.youtube.com/vi/" + token + \
                   "/0.jpg\" alt=\"" + desc + "\"></a>"
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
            return "<a href=\""+word+"\"><img src=\""+album_art+"\" alt=\"" + parser['title'] + \
                   " - " + parser["artist"] + "\"></a>"
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
                # rename(join(CURRENT_DIRECTORY, filename), target_filename)
            parser = GooglePlayParser()
            contents = open(target_filename, "r").read(-1)
            try:
                parser.feed(contents)
            except Exception as e:
                print("got exception: ", e, " on ", target_filename)
            album_art = parser.found_url
            return "<a href=\"" + word + "\"><img src=\"" + album_art + "\" alt=\"" + \
                   parser.title + " - " + parser.artist + "\"></a>"
        return word

    if not isdir(TEMP_DIR):
        mkdir(TEMP_DIR)
    return substitute_file(input_file, replacer)


def tablelize(input_file):
    """
    combine images into a table

    :param input_file: the contents of the file
    :return:
    """

    def replacer(contents):
        _lines = contents.split('\n')
        image_count = 0
        for replacer_i in range(len(_lines)):
            if _lines[replacer_i].find("<a ") == 0:
                image_count = image_count+1
            else:
                if image_count > 0:
                    for j in range(1, image_count + 1):
                        _lines[replacer_i - j] = "<td>" + _lines[replacer_i - j] + "</td>"
                        if image_count == j:
                            _lines[replacer_i - j] = "<table><tr>" + _lines[replacer_i - j]
                        elif j == 1:
                            _lines[replacer_i - j] = _lines[replacer_i - j] + "</tr></table>"
                image_count = 0
        out_contents = "\n".join(_lines)
        return out_contents

    if not isdir(TEMP_DIR):
        mkdir(TEMP_DIR)
    return substitute_file(input_file, replacer, on_lines=False)


if __name__ == "__main__":
    input_file = expanduser(argv[1])
    output_file = input_file
    # output_file = youtube(input_file=output_file)
    output_file = bandcamp(output_file)
    output_file = google_play(output_file)
    output_file = tablelize(output_file)