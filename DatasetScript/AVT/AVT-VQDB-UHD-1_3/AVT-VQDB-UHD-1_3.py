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
        "database": "AVT-VQDB-UHD-1_3",
        "reference_videos": [{"id": i + 1, "file_name": video} for i, video in enumerate(reference_videos)],
        "distorted_videos": []
    }


    for video in distorted_videos:
        parts = video.split('_')
        
        try:
            duration=float(parts[0].replace('s',''))
            parts = parts[1:]
            resolution = parts[-3].replace('p', '')
            if resolution == '360':
                width, height = 640, 360
            elif resolution == '720':
                width, height = 1280, 720
            elif resolution == '1080':
                width, height = 1920, 1080
            elif resolution == '2160':
                width, height = 3840, 2160
            else:
                raise ValueError("Resolution not found")

            bitrate = int(parts[-4].replace('kbps', ''))
            video_codec = parts[-1].split('.')[0]

           
            fps = float(parts[-2].replace('fps', ''))
            file_name = "_".join(parts) 
            result["distorted_videos"].append({
                "id": len(result["distorted_videos"]) + 1,
                "file_name": file_name,
                "width": width,
                "height": height,
                "bitrate": bitrate,
                "video_codec": video_codec,
                "bitdepth": 10,
                "pixel_format": "422",
                "fps": fps,  
                "duration": duration
            })
        except (IndexError, ValueError) as e:
            print(f"Error in line '{video}': {e}")

    with open(output_file, 'w') as json_file:
        json.dump(result, json_file, indent=2)

file_path = '/home/roberto/Scaricati/Tesi/Lavorosullatesi/Tesi/DatasetScript/AVT/AVT-VQDB-UHD-1_3/AVT-VQDB-UHD-1_3description.txt'
output_file = 'AVT-VQDB-UHD-1_3json.json'
parse_video_files(file_path, output_file)

print(f"Json saved as {output_file}")
