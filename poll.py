import requests
import subprocess

def poll():
    url = 'https://zflgbchggtuhujsqdbuo.supabase.co/rest/v1/youtube_videos?select=*'
    headers = {
        'apikey': 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6InpmbGdiY2hnZ3R1aHVqc3FkYnVvIiwicm9sZSI6InNlcnZpY2Vfcm9sZSIsImlhdCI6MTY4NTk2Njc4NiwiZXhwIjoyMDAxNTQyNzg2fQ.pBg1MpN3OgS90fP5HYIM_AHCbIwN9Hw9_Y0WXxujbp4',
        'Authorization': 'Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6InpmbGdiY2hnZ3R1aHVqc3FkYnVvIiwicm9sZSI6InNlcnZpY2Vfcm9sZSIsImlhdCI6MTY4NTk2Njc4NiwiZXhwIjoyMDAxNTQyNzg2fQ.pBg1MpN3OgS90fP5HYIM_AHCbIwN9Hw9_Y0WXxujbp4'
    }
    response = requests.get(url, headers=headers)
    videos = response.json()

    if len(videos) == 0:
        print("No videos to download")
        return
    
    # Start bot server
    # Kill the server if it is already running which is telegram-bot-api
    subprocess.run("pkill -f telegram-bot-api", shell=True)
    subprocess.run("sh /data/telegram-youtube-video-uploader/yt/run.sh", shell=True)

    for video in videos:
        if video["format"] == "mp3":
            print(f"Downloading Audio {video['link']}")
            response = subprocess.run(f"sh /data/telegram-youtube-video-uploader/yt/audio.sh {video['link']}", shell=True, capture_output=True)
        else:
            print(f"Downloading Video {video['link']}")
            response = subprocess.run(f"sh /data/telegram-youtube-video-uploader/yt/video.sh {video['link']}", shell=True, capture_output=True)

        # Delete the row again
        delete_url = f'https://zflgbchggtuhujsqdbuo.supabase.co/rest/v1/youtube_videos?id=eq.{video["id"]}'
        response = requests.delete(delete_url, headers=headers)

        # Delete all *.mp4, *.mp3 files
        subprocess.run("rm -f /data/telegram-youtube-video-uploader/yt/*.mp4", shell=True)
        subprocess.run("rm -f /data/telegram-youtube-video-uploader/yt/*.mp3", shell=True)

if __name__ == "__main__":
    poll()
