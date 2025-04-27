import json

input_file = '/home/roberto/Scaricati/Tesi/Lavorosullatesi/Tesi/Mos/ScoresITS4S.json'
output_file = './AllITS4SwithScores.txt'

with open(input_file, 'r') as f:
    data = json.load(f)

with open(output_file, 'w') as f:
    for entry in data.get('scores', []):
        if 'PVS' in entry and 'PVS_ID' in entry['PVS']:
            pvs_id = entry['PVS']['PVS_ID'].strip()
            if pvs_id and "_SRC" not in pvs_id:
                f.write(f"{pvs_id}.mp4\n")

print(f"PVS_ID values have been extracted to {output_file}")
