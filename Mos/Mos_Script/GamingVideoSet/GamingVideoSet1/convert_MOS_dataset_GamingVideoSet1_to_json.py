import sys
import re
import json

#Video Name,BR,PSNR,SSIM,VMAF,STRRED,SpeedQA,MosRaw Scores,Mos_After Outlier Detection
#CSGO_30fps_30sec_Part2_1280x720_1200_x264.yuv,1200,30.5914,0.96864,49.808517,110.476881,269.1072167,2.88,2.88	

def decode_line(line):
    v_line = line.split(',')
    #print(f"vline: {v_line}")
    # first element of the line
    PVS_ID = v_line[0].strip().replace('.yuv', '')
    #print(f"PVS_ID: {PVS_ID}")
    PVS_params = {}
    v_pvs = PVS_ID.split('_')
    print(f"v_pvs: {v_pvs}")

    v_pvs[0] = v_pvs[0].replace('.yuv', '')
    PVS_params['SRC'] = v_pvs[0]
    PVS_params['fps'] = int(v_pvs[1].replace('fps','')) 
    PVS_params['duration'] = int(v_pvs[2].replace('sec','')) 
    PVS_params['parts'] = v_pvs[3]
    v_res = v_pvs[4].split('x')
    PVS_params['width'] = int(v_res[0])
    PVS_params['height'] = int(v_res[1])
    PVS_params['bitrate'] = float(v_pvs[5])
    PVS_params['encoder'] = v_pvs[6].strip()
    PVS_params['yuv_fmt'] = 'yuv420p'

    MOS = float(v_line[8])
    #computed_MOS = None
    #OS = [0] * 18 	
    #for i in range(1, 18):  
    #   OS[i] = None
    # return {'PVS': {'PVS_ID': PVS_ID} | PVS_params, 'MOS': MOS, 'computed_MOS': computed_MOS, 'OS': OS,'CI' : None}

    return {'PVS': {'PVS_ID': PVS_ID} | PVS_params, 'MOS': MOS}

## __main__ ##

if len(sys.argv) <= 1:
    sys.stderr.write("ERROR: missing datafile.csv\n")
    sys.exit()

# dictionary
csv_information = {}
# void list: save each line of the file
file_line_information = []
# open the file
f = open(sys.argv[1], 'r')
# read first line of the file
header = f.readline()
# read second line of the file
line = f.readline()
while line:
    # work on the current line and save in the list file_line_information
    file_line_information.append(decode_line(line))
    line = f.readline()
f.close()

csv_information['dataset_name'] = 'GamingVideoSet1'
csv_information['SRC_names'] = list(set([x['PVS']['SRC'] for x in file_line_information]))
# csv_information['SRC_num'] = len(csv_information['SRC_names'])
csv_information['PVS_bitrates'] = sorted(list(set([x['PVS']['bitrate'] for x in file_line_information])))
csv_information['PVS_encoders'] = list(set([x['PVS']['encoder'] for x in file_line_information]))
csv_information['PVS_resolutions'] = list(set(["%sx%s" % (x['PVS']['width'], x['PVS']['height']) for x in file_line_information]))
csv_information['scores'] = file_line_information

# Save to JSON file
json_file_path = "ScoresGamingVideoSet1.json"  
with open(json_file_path, 'w') as json_file:
    json.dump(csv_information, json_file, indent=4)

print(f"Data has been written to {json_file_path}")
#print(json.dumps(csv_information, sort_keys=False, indent=4))
