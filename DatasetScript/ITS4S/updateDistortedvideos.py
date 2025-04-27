import json
import os

# Funzione per ottenere la parte della stringa tra l'ultimo underscore e .mp4
def extract_bitrate(file_name):
    base_name = os.path.basename(file_name)
    # Trova l'ultimo underscore e il suffisso '.mp4'
    start = base_name.rfind('_') + 1
    end = base_name.find('.mp4')
    # Restituisce la sottostringa
    return base_name[start:end]

# Funzione per aggiornare il valore del bitrate nei file JSON
def update_bitrate_in_json(file_path):
    with open(file_path, 'r') as f:
        data = json.load(f)
    
    for entry in data:
        file_name = entry.get('file_name', '')
        if file_name:
            # Estrai il bitrate dal nome del file
            bitrate = extract_bitrate(file_name)
            # Sostituisci il valore del bitrate
            entry['bitrate'] = bitrate
    
    # Salva il file JSON modificato
    with open(file_path, 'w') as f:
        json.dump(data, f, indent=4)

# Lista di file JSON da aggiornare
json_files = ['/home/roberto/Scaricati/Tesi/Lavorosullatesi/Tesi/DatasetScript/ITS4S/DistortedVideos.json']  # Aggiungi i percorsi dei tuoi file JSON

# Processa ogni file JSON
for json_file in json_files:
    update_bitrate_in_json(json_file)

print("Aggiornamento completato per tutti i file JSON.")
