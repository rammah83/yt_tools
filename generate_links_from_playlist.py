# generate_links_from_playlist.py
# Created/Modified files during execution:

import re
import json
from pytube import Playlist
from pytube import YouTube

print("generate_links_from_playlist.py")

def extract_videos_from_playlist(playlist_url):
    """
    Fetches a list of video URLs from the specified YouTube playlist.

    :param playlist_url: URL of the YouTube playlist
    :return: List of video URLs
    """
    playlist = Playlist(playlist_url)
    return list(playlist.video_urls)

def get_video_description(video_url):
    """
    Retrieves the description for a given YouTube video.

    :param video_url: URL of the YouTube video
    :return: String containing the description of the video
    """
    yt = YouTube(video_url)
    return yt.description

def extract_links_with_text(description):
    """
    Extracts links from the video description. This function looks for:
      1. Markdown-style links: [Text](URL)
      2. Plain URLs

    :param description: The video description text
    :return: List of dictionaries with the structure:
             [
               {
                 'text': <text_for_link_or_url>,
                 'link': <the_actual_url>
               },
               ...
             ]
    """
    links_found = []

    # Find Markdown links of the form [Text](http://...)
    markdown_pattern = r'$(?P<text>[^$]+)$$(?P<link>https?://[^$]+)\)'
    for match in re.finditer(markdown_pattern, description):
        links_found.append({
            'text': match.group('text'),
            'link': match.group('link')
        })

    # Find plain URLs in the text (not inside Markdown syntax)
    # This pattern matches HTTP/HTTPS URLs that aren't enclosed right after '['
    plain_url_pattern = r'(?<!$\()(?P<link>https?://[^\s]+)'
    for match in re.finditer(plain_url_pattern, description):
        # Use the link itself as the text
        links_found.append({
            'text': match.group('link'),
            'link': match.group('link')
        })

    return links_found