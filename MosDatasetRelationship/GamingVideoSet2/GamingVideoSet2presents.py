
import json

input_file = '/home/roberto/Scaricati/Tesi/Lavorosullatesi/Tesi/Mos/ScoresGamingVideoSet2.json'
output_file = './AllGamingVideoSet2withScores.txt'

with open(input_file, 'r') as f:
    data = json.load(f)

with open(output_file, 'w') as f:
    for entry in data.get('scores', []):
        if 'PVS' in entry and 'PVS_ID' in entry['PVS']:
            f.write(entry['PVS']['PVS_ID'] + '.mp4\n')

print(f"PVS_ID values have been extracted to {output_file}")