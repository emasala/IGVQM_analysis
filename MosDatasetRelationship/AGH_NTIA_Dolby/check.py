import json

with open('/home/roberto/Scaricati/Tesi/Lavorosullatesi/Tesi/Dataset/AGH_NTIA_Dolby.json', 'r') as json_file:
    data = json.load(json_file)

with open('/home/roberto/Scaricati/Tesi/Lavorosullatesi/Tesi/MosDatasetRelationship/AGH_NTIA_Dolby/AllScoresAGH_NTIA_Dolby.txt', 'r') as txt_file:
    mos_files = {line.strip() for line in txt_file.readlines()}  # Usa un set per efficienza

matching_files = [
    video["file_name"] for video in data["distorted_videos"]
    if video["file_name"] in mos_files
]

with open('matching_files.txt', 'w') as output_file:
    for file_name in matching_files:
        output_file.write(file_name + '\n')

