import json
import os

# Funzione per elaborare i dati
def process_video_data(videos):
    processed_videos = []

    for video in videos:
        file_name = video["file_name"]
        
        # Estrai la parte desiderata del nome del file
        main_part = file_name.split('_', 2)[-1].replace('.y4m', '')  # Prendi dopo il secondo "_"
        
        # Dividi sulla base di "at"
        codec_and_bitrate = main_part.split('at')
        
        if len(codec_and_bitrate) == 2:
            video_codec = codec_and_bitrate[0]
            bitrate = codec_and_bitrate[1]
        else:
            video_codec = "Unknown"
            bitrate = "Unknown"
        
        # Aggiorna il dizionario con i nuovi valori
        processed_video = {
            "id": video["id"],
            "file_name": file_name,
            "width": video["width"],
            "height": video["height"],
            "bitrate": bitrate,
            "video_codec": video_codec,
            "bitdepth": video["bitdepth"],
            "pixel_format": video["pixel_format"],
            "fps": video["fps"],
            "duration": video["duration"]
        }
        processed_videos.append(processed_video)

    return processed_videos

# Leggi il file JSON di input
input_file = "AGH_NTIA_Dolby.json"
output_file = "AGH_NTIA_Dolbyfixed.json"

if os.path.exists(input_file):
    with open(input_file, "r") as f:
        try:
            data = json.load(f)
        except json.JSONDecodeError as e:
            print(f"Errore nel parsing del file JSON: {e}")
            exit(1)
        
        # Estrai la lista dei video distorti
        if "distorted_videos" in data and isinstance(data["distorted_videos"], list):
            distorted_videos = data["distorted_videos"]
        else:
            print("Struttura JSON non valida: 'distortedvideos' mancante o non è una lista.")
            exit(1)
    
    # Processa i dati
    processed_data = process_video_data(distorted_videos)
    
    # Aggiorna il JSON originale con i dati elaborati
    data["distorted_videos"] = processed_data
    
    # Salva i risultati in un file JSON
    with open(output_file, "w") as f:
        json.dump(data, f, indent=4)
    
    print(f"I dati elaborati sono stati salvati in {output_file}")
else:
    print(f"File di input {input_file} non trovato!")
