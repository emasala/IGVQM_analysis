import json

input_file = './ScoresKUGVD.json'
output_file = './AllKUGDVwithScores.txt'

with open(input_file, 'r') as f:
    data = json.load(f)

with open(output_file, 'w') as f:
    for entry in data.get('scores', []):
        if 'PVS' in entry and 'PVS_ID' in entry['PVS']:
            f.write(entry['PVS']['PVS_ID'] + '\n')

print(f"PVS_ID values have been extracted to {output_file}")