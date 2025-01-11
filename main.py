import csv
from utils.extract_utils import extract_videos_from_playlist, get_video_details, extract_line_links

def main(playlist_url, n=3):
    """
    Main orchestrating function:
      1. Retrieve all video URLs from the playlist.
      2. Iterate over each video, extract the description and find links with surrounding text.
      3. Save the result to a JSON file with an intuitive structure.
    """
    video_urls = extract_videos_from_playlist(playlist_url, limit=n)

    results = {
        "playlist_url": playlist_url,
        "videos": []
    }

    for video_url in video_urls:
        title, description = get_video_details(video_url)
        links = extract_line_links(description)

        # Append to final structure
        results["videos"].append({
            "video_url": video_url,
            "links": links
        })

    # The CSV filename could be customized if desired
    output_file = r"./output/playlist_extracted_links.csv"
    with open(output_file, mode='w', newline='', encoding='utf-8') as csvfile:
        writer = csv.writer(csvfile)
        # Write the CSV header row
        writer.writerow(["video_url", "text", "link"])

        for video_url in video_urls:
            title, description = get_video_details(video_url)
            links = extract_line_links(description)

            for link_info in links:
                writer.writerow([
                    video_url,
                    title,
                    link_info['text'],
                    link_info['link']
                ])

    print(f"Data extracted and saved to {output_file}")

if __name__ == "__main__":
    # Example usage:
    # Replace this with your actual playlist URL
    YT_PLAYLIST_URL = "https://www.youtube.com/playlist?list=PLUQDw_ve-LUDhbDD5JuVLv0wpbIEExbHY"
    main(YT_PLAYLIST_URL, n=3)
