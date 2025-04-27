import json

text_file = "AVT-VQDB-UHD-1_1withScores.txt"
json_file = "/home/roberto/Scaricati/Tesi/Lavorosullatesi/Tesi/Dataset/AVT-VQDB-UHD-1_1.json"

with open(text_file, "r") as f:
    lines = [line.strip() for line in f if line.strip()]

with open(json_file, "r") as f:
    data = json.load(f)

distorted_videos = data.get("distorted_videos", [])
json_filenames = {
    entry.get("file_name", "").removesuffix(".mp4").removesuffix(".mkv") 
    for entry in distorted_videos if "file_name" in entry
}

for line in lines:
    line_without_ext = line.removesuffix(".mp4").removesuffix(".mkv")  
    if line_without_ext in json_filenames:
        print(f"{line} -> Found")
    else:
        print(f"{line} -> Not Found")
