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
        "database": "ITS4S",
        "reference_videos": [{"id": i + 1, "file_name": video} for i, video in enumerate(reference_videos)],
        "distorted_videos": []
    }
    """
    for video in distorted_videos:
        parts = video.split('_')
        try:
            resolution = parts[-3].split('x')  
            width = int(resolution[0])
            height = int(resolution[1])
            bitrate = int(parts[-2])  
            
            video_codec = parts[-1].split('.')[0]  
            
            fps = int(parts[1].replace('fps', ''))  
            duration = int(parts[2].replace('sec', ''))  

            result["distorted_videos"].append({
                "id": len(result["distorted_videos"]) + 1,
                "file_name": video,
                "width": width,
                "height": height,
                "bitrate": bitrate,
                "video_codec": video_codec,
                "bitdepth": 8,
                "pixel_format": "420",
                "fps": fps,
                "duration": duration
            })
        except (IndexError, ValueError) as e:
            print(f"Error in line '{video}': {e}")
    """
    with open(output_file, 'w') as json_file:
        json.dump(result, json_file, indent=2)

file_path = '/home/roberto/Scaricati/Tesi/Lavorosullatesi/Tesi/DatasetScript/ITS4S/ITS4Sdescription.txt'
output_file = 'ITS4Sjson.json'
parse_video_files(file_path, output_file)

print(f"Json saved as {output_file}")