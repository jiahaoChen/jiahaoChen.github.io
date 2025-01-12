import argparse
from pytube import YouTube
import re
import subprocess
from urllib.parse import urlparse, parse_qs
import requests

def clean_youtube_url(url):
    """Clean and validate YouTube URL or video ID"""
    try:
        # Remove escape characters
        url = url.replace('\\', '')
        
        # Check if input is just a video ID
        if not any(domain in url for domain in ['youtube.com', 'youtu.be']):
            # Assume it's a video ID if it doesn't contain youtube domains
            return f"https://www.youtube.com/watch?v={url}"
            
        # Handle full URLs
        parsed_url = urlparse(url)
        if 'youtube.com' in parsed_url.netloc:
            # Extract video ID from youtube.com URL
            video_id = parse_qs(parsed_url.query)['v'][0]
            return f"https://www.youtube.com/watch?v={video_id}"
        elif 'youtu.be' in parsed_url.netloc:
            # Extract video ID from youtu.be URL
            video_id = parsed_url.path.lstrip('/')
            return f"https://www.youtube.com/watch?v={video_id}"
            
    except Exception as e:
        print(f"Error processing URL: {e}")
        return None

def sanitize_filename(title):
    """Convert video title to safe filename"""
    # Remove invalid filename characters
    title = re.sub(r'[<>:"/\\|?*]', '', title)
    # Replace spaces with spaces or underscores based on preference
    title = title.replace(' ', ' ')  # or use '_' if you prefer underscores
    # Remove any multiple spaces
    title = re.sub(r'\s+', ' ', title).strip()
    return f"{title}.md"

def get_video_title(url):
    """Get video title from YouTube with retries"""
    max_retries = 3
    for attempt in range(max_retries):
        try:
            # First try direct API call
            video_id = url.split('v=')[1].split('&')[0]
            api_url = f"https://www.youtube.com/oembed?url=https://www.youtube.com/watch?v={video_id}&format=json"
            response = requests.get(api_url, headers={
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
            })
            
            if response.status_code == 200:
                return response.json().get('title')
            
            # Fallback to pytube if API fails
            yt = YouTube(url)
            return yt.title
            
        except Exception as e:
            if attempt == max_retries - 1:  # Last attempt
                print(f"Error fetching video title: {e}")
                return None
            print(f"Attempt {attempt + 1} failed, retrying...")
            continue
    return None

def main():
    # Set up argument parser
    parser = argparse.ArgumentParser()
    parser.add_argument('youtube', help='YouTube video URL or ID')
    parser.add_argument('--pattern', default='mindmap', help='Pattern to use (default: mindmap)')
    args = parser.parse_args()

    # Clean the YouTube URL
    clean_url = clean_youtube_url(args.youtube)
    if not clean_url:
        print("Invalid YouTube URL")
        return

    # Get video title
    video_title = get_video_title(clean_url)
    if not video_title:
        print("Could not fetch video title")
        return

    # Create output filename from video title
    output_file = sanitize_filename(video_title)
    
    # Construct the fabric command with defaults
    command = [
        'fabric',
        '-y', clean_url,
        '--pattern', args.pattern,
        '--metadata',
        '-o', f'blog/{output_file}'
    ]
    print(command)
    # Execute the fabric command
    try:
        result = subprocess.run(command, check=True, capture_output=True, text=True)
        print(f"Successfully created: {output_file}")
        print(result.stdout)
    except subprocess.CalledProcessError as e:
        print(f"Error running fabric command: {e}")
        print(e.stdout)
        print(e.stderr)

if __name__ == "__main__":
    main()
