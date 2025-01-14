from pprint import pprint

from tqdm import tqdm

from utils.yt_scraper import (
    extract_all_lines_links,
    save_data_to_csv,
    videos_urls_from_playlist,
)


def main(playlist_url, save_to_csv: bool = False, n: None | int = None):
    """
    Main orchestrating function:
        1. Retrieve all video URLs from the playlist.
        2. Iterate over each video, extract the description and find links with surrounding text.
        3. Save the result to a JSON file with an intuitive structure.
    """
    video_urls = videos_urls_from_playlist(playlist_url, limit=n)

    if save_to_csv:
        save_data_to_csv(video_urls)
    else:
        results = {"playlist_url": playlist_url, "videos": []}
        for video_url in tqdm(video_urls, desc="Processing videos"):
            results["videos"].append(extract_all_lines_links(video_url))
        pprint(results)


if __name__ == "__main__":
    # Example usage:
    # Replace this with your actual playlist URL
    YT_PLAYLIST_URL = (
        "https://www.youtube.com/playlist?list=PLUQDw_ve-LUDhbDD5JuVLv0wpbIEExbHY"
    )
    main(YT_PLAYLIST_URL, save_to_csv=True)
