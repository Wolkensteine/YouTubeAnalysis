# YouTube Comments parser
# Imports
from dateutil import parser

from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

# Google API Key
api_key = 'AIzaSyCnZH1gCbjNv2gWtI_uqL1bsxGvrzPJM48'

# Channel names to analyze
channel_names = ['Staiy', 'Miimii', 'ApoRed', 'Apache207', 'HurraKinderlieder', 'Jules1', 'Jindaouis', 'MikeVallasVlogs', 'bani349', 'MontanaBlack', 'tomatolix', 'LuneOfficiel', 'KMNGANG', 'ArchitecturalDigestGermany', 'NeedToKnoww', 'MAITHINKX', '3pTV', 'TomSupreme', 'Lewinray', 'vieleRezepte', 'Simplicissimus', 'BulienJam', 'TheRealLifeGuys']
channel_ids = []  # leave empty, this will be automatically filled by the ids of the channels named above

# Videos to analyze
video_ids = []

# Define how many comments should be retrieved from each video
# 0 will be ignored and all will be retrieved
comments_to_parse_per_video = 25

# Videos to analyze per channel
# 0 will make it so only the predefined videos will be scanned      i: video_ids = []
# -1 will let the program scan all videos of a channel              i: not recommended
videos_to_parse_per_channel = 10

# Tracking variables
videos_parsed = 0                   # From how many videos comments were analyzed
comments_parsed = 0                 # How many comments were parsed via the API

# Name Dataset
dataset_name = "Top20ChannelsFromNindo-10VideosEach-25CommentsEach-CreatedOn_16-4-24_AdditionalChannelsIncluded-MiiMii_Staiy_ApoRed"


# Functions
def video_comments(video_id, video_upload_date, youtube):
    # retrieve youtube video results
    try:
        video_response = youtube.commentThreads().list(
            part='snippet,replies',
            videoId=video_id
        ).execute()
    except HttpError as error:
        print(error)
        return

    counter = 0
    break_next = 0

    # iterate video response
    while video_response:
        # extracting required info
        # from each result object
        for item in video_response['items']:

            global comments_parsed
            comments_parsed += 1

            # Extracting comments
            comment = item['snippet']['topLevelComment']['snippet']['textDisplay']

            print_to_dataset(str(comment).replace("\n", ""))

            counter += 1

            if 0 < comments_to_parse_per_video <= counter:
                break_next = 1
                break

        # Again repeat
        if 'nextPageToken' in video_response and break_next == 0:
            video_response = youtube.commentThreads().list(
                part='snippet,replies',
                videoId=video_id,
                pageToken=video_response['nextPageToken']
            ).execute()
        else:
            break


def get_video_upload_date(video_id):
    video_snippet = youtube.videos().list(
        part='snippet',
        id=video_id
    ).execute()
    return video_snippet['items'][0]['snippet']['publishedAt']


def print_to_dataset(text):
    with open("GeneratedDatasets/" + dataset_name + ".txt", "a") as file:
        file.write(text + "\n")


# Main
if __name__ == "__main__":
    print()
    print("Starting ...")
    print()

    # Create YouTube build
    youtube_build = youtube = build('youtube', 'v3',
                                    developerKey=api_key)

    if videos_to_parse_per_channel != 0:
        for name in channel_names:
            request = youtube_build.channels().list(
                part="snippet,statistics",
                forHandle=name
            )
            response = request.execute()

            channel_ids.append(response['items'][0]['id'])
            print(response['items'][0]['id'], " (", response['items'][0]['snippet']['title'], ") » Video count: ", response['items'][0]['statistics']['videoCount'], "; Subscribers: ", response['items'][0]['statistics']['subscriberCount'], "; Total views: ", response['items'][0]['statistics']['viewCount'])

        if videos_to_parse_per_channel == -1:
            for cid in channel_ids:
                request = youtube.search().list(
                    part="snippet",
                    channelId=cid,
                    order="date"
                )
                response = request.execute()

                for i in range(len(response['items'])):
                    video_ids.append(response['items'][i]['id']['videoId'])
        else:
            for cid in channel_ids:
                request = youtube.search().list(
                    part="snippet",
                    channelId=cid,
                    maxResults=videos_to_parse_per_channel,
                    order="date",
                    type="video"
                )
                response = request.execute()

                for i in range(len(response['items'])):
                    video_ids.append(response['items'][i]['id']['videoId'])

    for video_id in video_ids:
        print()
        print("Analyzing comments of video with id: ", video_id)
        print()
        video_comments(video_id, get_video_upload_date(video_id), youtube_build)
        videos_parsed += 1

    print("Finishing ...")
    print()
    print(" ========== Results ============ ")
    print()

    print("Videos analyzed: ", videos_parsed, "\nComments parsed: ", comments_parsed)
    print()
