import json

def parse_video_files(file_path, output_file):
    with open(file_path, 'r') as f:
        lines = f.readlines()

    reference_videos = []
    distorted_videos = []
    current_list = None

    for line in lines:
        line = line.strip()
        if line == "ReferenceVideos":
            current_list = reference_videos
            continue
        elif line == "DistortedVideos":
            current_list = distorted_videos
            continue
        if line and current_list is not None:
            current_list.append(line)

    result = {
        "database": "AGH_NTIA_Dolby",
        "reference_videos": [{"id": i + 1, "file_name": video} for i, video in enumerate(reference_videos)],
        "distorted_videos": []
    }


    with open(output_file, 'w') as json_file:
        json.dump(result, json_file, indent=2)

file_path = '/home/roberto/Scaricati/Tesi/Lavorosullatesi/Tesi/DatasetScript/AGH_NTIA_Dolby/AGH_NTIA_Dolbydescription.txt'
output_file = 'AGH_NTIA_Dolbyjson.json'
parse_video_files(file_path, output_file)

print(f"Json saved as {output_file}")
