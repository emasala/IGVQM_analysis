import json

input_file = '/home/roberto/Scaricati/Tesi/Lavorosullatesi/Tesi/Mos/ScoresAVT-VQDB-UHD-1_2.json'
output_file = './AVT-VQDB-UHD-1_2withScores.txt'

with open(input_file, 'r') as f:
    data = json.load(f)

with open(output_file, 'w') as f:
    for entry in data.get('scores', []):
        if 'PVS' in entry and 'PVS_ID' in entry['PVS']:
            f.write(entry['PVS']['PVS_ID'] + '\n')

print(f"PVS_ID values have been extracted to {output_file}")