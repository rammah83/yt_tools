# generate_links_from_playlist.py
# Created/Modified files during execution:

import re
import json
from pytube import Playlist
from pytube import YouTube

print("generate_links_from_playlist.py")

def extract_videos_from_playlist(playlist_url, limit:int|None=3):
    """
    Fetches a list of video URLs from the specified YouTube playlist.

    :param playlist_url: URL of the YouTube playlist
    :param limit: Maximum number of videos to extract
    :return: List of video URLs
    """
    if limit is not None:
        playlist = Playlist(playlist_url)
        return list(playlist.video_urls)[:limit]
    playlist = Playlist(playlist_url)
    return list(playlist.video_urls)

def get_video_details(video_url):
    """
    Retrieve the title and description for a given YouTube video.

    :param video_url: URL of the YouTube video
    :return: (title, description) tuple
    """
    yt = YouTube(video_url)
    return yt.title, yt.description

def extract_line_links(description):
    """
    Extract links from each line of the video description, along with the text
    accompanying that link on the same line.

    Example line:
        'site for google: http://www.google.com'

    This would be captured as:
        {
          'text': 'site for google:',
          'link': 'http://www.google.com'
        }

    If multiple links appear on the same line, they are each extracted. For
    example:
        'Please visit http://example1.com or http://example2.com'

    yields:
        [
          {
            'text': 'Please visit',
            'link': 'http://example1.com'
          },
          {
            'text': 'or',
            'link': 'http://example2.com'
          }
        ]

    :param description: The video description text
    :return: A list of dictionaries of the form:
             [
               {
                 'text': <text_on_line_around_link>,
                 'link': <the_actual_url>
               },
               ...
             ]
    """
    links_data = []
    # Split description into lines
    lines = description.split('\n')

    # Regex to find any http/https URL
    url_pattern = re.compile(r'(https?://[^\s]+)')

    for line in lines:
        # Find all occurrences of URLs in the line
        matches = list(url_pattern.finditer(line))
        if not matches:
            continue

        # If there are multiple links on a single line,
        # we separately capture text/link pairs around each match
        start_index = 0
        for match in matches:
            url = match.group(1)

            # Text before the link
            text_before = line[start_index:match.start()].strip()
            links_data.append({
                'text': text_before,
                'link': url
            })
            start_index = match.end()

        # Optionally, capturing leftover text after the last link, if needed
        # leftover_text = line[start_index:].strip()
        # if leftover_text:
        #     # Possibly store it if it's meaningful for your use case
        #     ...

    return links_data