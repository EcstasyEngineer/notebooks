import os
import re
import gzip
import json
# name of channel to be scanned
channel_prefix = "https://www.youtube.com/"

# channels = [
#     "@StronnyCuttles",
#     "@ShibiCottonbum",
#     "@IceySnowpaws",
#     "@MercyModiste",
#     "@AzuraDulait",
#     "@ImmyBisou"
# ]

channels = [
    "@StronnyCuttles",
    "@ShibiCottonbum",
]

def get_channel_videos(channel):
    try:   os.mkdir(channel)
    except:   pass
    try:   os.mkdir(f"{channel}/downloaded")
    except:   pass
    try:   os.mkdir(f"{channel}/processed")
    except:   pass
    try:   os.mkdir(f"{channel}/transcripts")
    except:   pass
    try:  os.mkdir(f"{channel}/chats")
    except:  pass

    # scan channel for videos
    # live videos
    os.system(f"yt-dlp --get-id --skip-download {channel_prefix+channel} > {channel}/videos.txt")
    videos = []
    with open(f"{channel}/videos.txt", "r") as f:
        for line in f:
            if line.startswith("Error"):
                continue
            videos.append(line.strip())

    # look for filenames in {channel}/downloaded for already downloaded videos
    # the file name contains the video id in the following format:
    # 【Supermarket Simulator】Definitely not drunk on the job 🐐🍼【VAllure】 [i3rrDSjokF4].webm
    # where [i3rrDSjokF4] is the video id
    downloaded = []
    for file in os.listdir(f"{channel}/downloaded"):
        if file.endswith(".webm"):
            m = re.search(r"\[(.*?)\]", file)
            if m:
                downloaded.append(m.group(1))
                
    # do the same for transcripts
    transcripts = []
    for file in os.listdir(f"{channel}/transcripts"):
        if file.endswith(".srt"):
            m = re.search(r"\[([^\[\]]+)\](?!.*\[)", file)
            if m:
                transcripts.append(m.group(1))


    # compare list of videos to videos already downloaded
    to_download = list(set(videos) - set(downloaded) - set(transcripts))
    return to_download

def download_video(channel, video):
    print(f"Downloading {video}")
    #output = os.system(f"yt-dlp -f bestaudio -P {channel}/downloaded {channel_prefix}watch?v={video}")
    output = os.system(f"yt-dlp --write-subs --sub-lang live_chat -f bestaudio -P {channel}/downloaded {channel_prefix}watch?v={video}")
    if output!=0:
        print(f"Error downloading {video}")
        
        
def process_downloaded_files(channel):
    #collect file names in {channel}/downloaded
    downloaded_files = os.listdir(f"{channel}/downloaded")
    for file in downloaded_files:
        if file.endswith(".webm") or file.endswith(".m4a"):
            #result = os.system(f"whisper \"{channel}/downloaded/{file}\" --device cuda --output_dir --language English --model large-v3 \"{channel}/transcripts/\"")
            result = os.system(f"whisper \"{channel}/downloaded/{file}\" --device cuda --language English --output_dir \"{channel}/transcripts/\"")
            if result==0:
                #move file to {channel}/processed
                try:
                    os.rename(f"{channel}/downloaded/{file}", f"{channel}/processed/{file}")
                except:
                    print(f"Error moving {file} to {channel}/processed")
                    
        if file.endswith("live_chat.json"):
            with open(os.path.join(channel, "downloaded", file), 'r', encoding='utf-8') as input_file, open(os.path.join(channel, "chats", f"{input_file[:-15]}.txt"), 'w', encoding='utf-8') as output_file:
            #try:
                for line in input_file:
                    line = line.strip()
                    try:
                        json_data = json.loads(line)
                    except json.JSONDecodeError:
                        print(f"Invalid JSON: {line}")
                        continue

                    # Extract timestamp
                    replay_action = json_data.get('replayChatItemAction')
                    if not replay_action:
                        print(f"No replayChatItemAction: {line}")
                        continue

                    video_offset_time_msec = replay_action.get('videoOffsetTimeMsec')
                    if not video_offset_time_msec:
                        print(f"No videoOffsetTimeMsec: {line}")
                        continue

                    try:
                        timestamp_ms = int(video_offset_time_msec)
                    except ValueError:
                        print(f"Invalid videoOffsetTimeMsec value: {line}")
                        continue

                    # Validate timestamp
                    if timestamp_ms < 0 or timestamp_ms > 43200000:
                        print(f"Invalid timestamp: {line}")
                        continue

                    # Process each action
                    actions = replay_action.get('actions', [])
                    for action in actions:
                        add_chat_item_action = action.get('addChatItemAction')
                        if not add_chat_item_action:
                            continue

                        item = add_chat_item_action.get('item', {})
                        live_chat_renderer = item.get('liveChatTextMessageRenderer')
                        if not live_chat_renderer:
                            continue

                        # Extract user
                        author_name = live_chat_renderer.get('authorName', {})
                        user = author_name.get('simpleText', '')
                        if not user:
                            user = live_chat_renderer['authorExternalChannelId']
                        # if not user:
                        #     print(f"Invalid user: {line}")
                        #     continue

                        # Extract message
                        message = ''
                        message_runs = live_chat_renderer.get('message', {}).get('runs', [])
                        for run in message_runs:
                            text = run.get('text')
                            if text:
                                message += text
                            else:
                                emoji = run.get('emoji', {})
                                emoji_id = emoji.get('shortcuts', '')[0]
                                message += emoji_id

                        if not message:
                            print(f"Invalid message: {line}")
                            continue
                        
                        message = message.replace("\n", " ").replace("\t", " ")
                        # Process the extracted data (e.g., print or write to a file)
                        output_file.write(f"{user}\t{timestamp_ms}\t{message}\n")

                # except Exception as e:
                #     print(f"Unknown error: {e}")
                    
            # remove chat file
            os.remove(os.path.join(channel, "downloaded", input_file))
            
def clean_up(channel):
    #remove .tsv, .txt, .vtt files, (keeping .srt and .json), and compress json files to .json.gz in {channel}/transcripts
    transcript_files = os.listdir(f"{channel}/transcripts")
    for file in transcript_files:
        if file.endswith(".tsv") or file.endswith(".txt") or file.endswith(".vtt"):
            try:
                os.remove(f"{channel}/transcripts/{file}")
            except:
                print(f"Error removing {file}")
        if file.endswith(".json"):
            with open(f"{channel}/transcripts/{file}", "rb") as f:
                with gzip.open(f"{channel}/transcripts/{file}.gz", "wb") as f_out:
                    f_out.writelines(f)
            #remove original json file
            try:
                os.remove(f"{channel}/transcripts/{file}")
            except:
                print(f"Error removing {file}")
            
            
def main():
    for channel in channels:
        print(f"Processing {channel}")
        to_download = get_channel_videos(channel)
        for video in to_download:
            download_video(channel, video)
        process_downloaded_files(channel)
        clean_up(channel)
        
if __name__ == "__main__":
    main()