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
        "database": "AVT-VQDB-UHD-1_4",
        "reference_videos": [{"id": i + 1, "file_name": video} for i, video in enumerate(reference_videos)],
        "distorted_videos": []
    }

    for video in distorted_videos:
        parts = video.split('_')
        print(parts)
          
        for i in range(-1, -len(parts)-1, -1):
           print(f"Indice {i}: {parts[i]}")
        
        
        try:
            if len(parts) == 9:
                resolution = parts[-3].replace('p', '')
                if resolution == '360':
                    width, height = 640, 360
                elif resolution == '480':  
                    width, height = 854, 480
                elif resolution == '720':
                    width, height = 1280, 720
                elif resolution == '1080':
                    width, height = 1920, 1080
                elif resolution == '1440':
                    width, height = 2560, 1440
                elif resolution == '2160':
                    width, height = 3840, 2160
                else:
                    raise ValueError("Resolution not found")
                
                bitrate = int(parts[-4].replace('kbps', ''))
                video_codec = parts[-1].split('.')[0]
                fps = float(parts[-2].replace('fps', ''))
                duration = float(parts[-7].replace('s', ''))

            elif len(parts) == 12:
                resolution = parts[-3].replace('p', '')
                if resolution == '360':
                    width, height = 640, 360
                elif resolution == '480':  
                    width, height = 854, 480
                elif resolution == '720':
                    width, height = 1280, 720
                elif resolution == '1080':
                    width, height = 1920, 1080
                elif resolution == '1440':
                    width, height = 2560, 1440
                elif resolution == '2160':
                    width, height = 3840, 2160
                else:
                    raise ValueError("Resolution not found")

                bitrate = int(parts[-4].replace('kbps', ''))
                video_codec = parts[-1].split('.')[0]
                fps = float(parts[-2].replace('fps', ''))
                duration = float(parts[-5].replace('s', ''))

            elif len(parts) == 8:
                resolution = parts[-3].replace('p', '')
                if resolution == '360':
                    width, height = 640, 360
                elif resolution == '480':  
                    width, height = 854, 480
                elif resolution == '720':
                    width, height = 1280, 720
                elif resolution == '1080':
                    width, height = 1920, 1080
                elif resolution == '1440':
                    width, height = 2560, 1440
                elif resolution == '2160':
                    width, height = 3840, 2160
                else:
                    raise ValueError("Resolution not found")

                bitrate = int(parts[-4].replace('kbps', ''))
                video_codec = parts[-1].split('.')[0]
                fps = float(parts[-2].replace('fps', ''))
                duration = float(parts[-7].replace('s', ''))

            elif len(parts) == 7:
                resolution = parts[-3].replace('p', '')
                if resolution == '360':
                    width, height = 640, 360
                elif resolution == '480':  
                    width, height = 854, 480
                elif resolution == '720':
                    width, height = 1280, 720
                elif resolution == '1080':
                    width, height = 1920, 1080
                elif resolution == '1440':
                    width, height = 2560, 1440
                elif resolution == '2160':
                    width, height = 3840, 2160
                else:
                    raise ValueError("Resolution not found")

                bitrate = int(parts[-4].replace('kbps', ''))
                video_codec = parts[-1].split('.')[0]
                fps = float(parts[-2].replace('fps', ''))
                duration = float(8)


            result["distorted_videos"].append({
                "id": len(result["distorted_videos"]) + 1,
                "file_name": video,
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

file_path = '/home/roberto/Scaricati/Tesi/Lavorosullatesi/Tesi/DatasetScript/AVT/AVT-VQDB-UHD-1_4/AVT-VQDB-UHD-1_4description.txt'
output_file = 'AVT-VQDB-UHD-1_4.json'
parse_video_files(file_path, output_file)

print(f"Json saved as {output_file}")
