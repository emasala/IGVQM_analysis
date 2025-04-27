import sys
import re
import json

#src,video_name,MOS,CI
#american_football_harmonic,american_football_harmonic_200kbps_360p_59.94fps_h264.mp4,1.0,0.0

def decode_line(line):
    PVS_params = {}
    v_line = line.split(',')
    PVS_params['SRC'] = v_line[0]
    PVS_ID = v_line[1].strip().replace('.mp4', '').replace('.mkv', '')
    v_pvs = PVS_ID.split('_')
    #american_football_harmonic_200kbps_360p_59.94fps_h264.mp4
    print(v_pvs)
    if len(v_pvs) == 12:
     PVS_params['SRC'] = f"{v_pvs[0]}_{v_pvs[1]}_{v_pvs[2]}_{v_pvs[3]}_{v_pvs[4]}_{v_pvs[5]}{v_pvs[6]}{v_pvs[7]}"
     PVS_params['bitrate'] = float(v_pvs[8].replace('kbps', ''))
     if v_pvs[9]=="360p":
      PVS_params['width'] = 640
      PVS_params['height'] = 360
     elif v_pvs[9]=="480p":
      PVS_params['width'] = 854
      PVS_params['height'] = 480
     elif v_pvs[9]=="720p":
      PVS_params['width'] = 1280
      PVS_params['height'] = 720
     elif v_pvs[9]=="1080p":
      PVS_params['width'] = 1920
      PVS_params['height'] = 1080
     elif v_pvs[9]=="1440p":
      PVS_params['width'] = 2560
      PVS_params['height'] = 1440
     elif v_pvs[9]=="2160p":
      PVS_params['width'] = 3840
      PVS_params['height'] = 2160
   
     PVS_params['fps'] = float(v_pvs[10].replace('fps', ''))
     PVS_params['encoder'] = v_pvs[11].strip()
     PVS_params['yuv_fmt'] = 'yuv422p10le'
     PVS_params['duration'] = int(v_pvs[7].replace('s',''))

     MOS = float(v_line[2])
     CI = float(v_line[3])
     #computed_MOS = None
     #OS = [0] * 18 	
     #for i in range(1, 18):  
      #  OS[i] = None
    elif len(v_pvs) == 10:
     PVS_params['SRC'] = f"{v_pvs[0]}_{v_pvs[1]}_{v_pvs[2]}_{v_pvs[3]}_{v_pvs[4]}_{v_pvs[5]}"
     PVS_params['bitrate'] = float(v_pvs[6].replace('kbps', ''))
     if v_pvs[7]=="360p":
      PVS_params['width'] = 640
      PVS_params['height'] = 360
     elif v_pvs[7]=="480p":
      PVS_params['width'] = 854
      PVS_params['height'] = 480
     elif v_pvs[7]=="720p":
      PVS_params['width'] = 1280
      PVS_params['height'] = 720
     elif v_pvs[7]=="1080p":
      PVS_params['width'] = 1920
      PVS_params['height'] = 1080
     elif v_pvs[7]=="1440p":
      PVS_params['width'] = 2560
      PVS_params['height'] = 1440
     elif v_pvs[7]=="2160p":
      PVS_params['width'] = 3840
      PVS_params['height'] = 2160
   
     PVS_params['fps'] = float(v_pvs[8].replace('fps', ''))
     PVS_params['encoder'] = v_pvs[9].strip()
     PVS_params['yuv_fmt'] = 'yuv422p10le'
     PVS_params['duration'] = int(v_pvs[5].replace('s',''))

     MOS = float(v_line[2])
     CI = float(v_line[3])
     #computed_MOS = None
     #OS = [0] * 18 	
     #for i in range(1, 18):  
     #   OS[i] = None
    elif len(v_pvs) == 9:
     PVS_params['SRC'] = f"{v_pvs[0]}_{v_pvs[1]}_{v_pvs[2]}_{v_pvs[3]}_{v_pvs[4]}"
     PVS_params['bitrate'] = float(v_pvs[5].replace('kbps', ''))
     if v_pvs[6]=="360p":
      PVS_params['width'] = 640
      PVS_params['height'] = 360
     elif v_pvs[6]=="480p":
      PVS_params['width'] = 854
      PVS_params['height'] = 480
     elif v_pvs[6]=="720p":
      PVS_params['width'] = 1280
      PVS_params['height'] = 720
     elif v_pvs[6]=="1080p":
      PVS_params['width'] = 1920
      PVS_params['height'] = 1080
     elif v_pvs[6]=="1440p":
      PVS_params['width'] = 2560
      PVS_params['height'] = 1440
     elif v_pvs[6]=="2160p":
      PVS_params['width'] = 3840
      PVS_params['height'] = 2160
   
     PVS_params['fps'] = float(v_pvs[7].replace('fps', ''))
     PVS_params['encoder'] = v_pvs[8].strip()
     PVS_params['yuv_fmt'] = 'yuv422p10le'
     PVS_params['duration'] = int(v_pvs[2].replace('s',''))

     MOS = float(v_line[2])
     CI = float(v_line[3])
     #computed_MOS = None
     #OS = [0] * 18 	
     #for i in range(1, 18):  
      #  OS[i] = None
    elif len(v_pvs) == 8:
     PVS_params['SRC'] = f"{v_pvs[0]}_{v_pvs[1]}_{v_pvs[2]}_{v_pvs[3]}"
     PVS_params['bitrate'] = float(v_pvs[4].replace('kbps', ''))
     if v_pvs[5]=="360p":
      PVS_params['width'] = 640
      PVS_params['height'] = 360
     elif v_pvs[5]=="480p":
      PVS_params['width'] = 854
      PVS_params['height'] = 480
     elif v_pvs[5]=="720p":
      PVS_params['width'] = 1280
      PVS_params['height'] = 720
     elif v_pvs[5]=="1080p":
      PVS_params['width'] = 1920
      PVS_params['height'] = 1080
     elif v_pvs[5]=="1440p":
      PVS_params['width'] = 2560
      PVS_params['height'] = 1440
     elif v_pvs[5]=="2160p":
      PVS_params['width'] = 3840
      PVS_params['height'] = 2160
   
     PVS_params['fps'] = float(v_pvs[6].replace('fps', ''))
     PVS_params['encoder'] = v_pvs[7].strip()
     PVS_params['yuv_fmt'] = 'yuv422p10le'
     PVS_params['duration'] = int(v_pvs[1].replace('s',''))

     MOS = float(v_line[2])
     CI = float(v_line[3])
     #computed_MOS = None
     #OS = [0] * 18 	
     #for i in range(1, 18):  
     #   OS[i] = None
    elif len(v_pvs) == 7:
     PVS_params['SRC'] = f"{v_pvs[0]}_{v_pvs[1]}_{v_pvs[2]}"
     PVS_params['bitrate'] = float(v_pvs[3].replace('kbps', ''))
     if v_pvs[4]=="360p":
      PVS_params['width'] = 640
      PVS_params['height'] = 360
     elif v_pvs[4]=="480p":
      PVS_params['width'] = 854
      PVS_params['height'] = 480
     elif v_pvs[4]=="720p":
      PVS_params['width'] = 1280
      PVS_params['height'] = 720
     elif v_pvs[4]=="1080p":
      PVS_params['width'] = 1920
      PVS_params['height'] = 1080
     elif v_pvs[4]=="1440p":
      PVS_params['width'] = 2560
      PVS_params['height'] = 1440
     elif v_pvs[4]=="2160p":
      PVS_params['width'] = 3840
      PVS_params['height'] = 2160
   
     PVS_params['fps'] = float(v_pvs[5].replace('fps', ''))
     PVS_params['encoder'] = v_pvs[6].strip()
     PVS_params['yuv_fmt'] = 'yuv422p10le'
     MOS = float(v_line[2])
     CI = float(v_line[3])
     #computed_MOS = None
     #OS = [0] * 18 	
     #for i in range(1, 18):  
     #   OS[i] = None
    elif len(v_pvs) == 6: 
     PVS_params['SRC'] = f"{v_pvs[0]}_{v_pvs[1]}"
     PVS_params['bitrate'] = float(v_pvs[2].replace('kbps', ''))
     if v_pvs[3]=="360p":
      PVS_params['width'] = 640
      PVS_params['height'] = 360
     elif v_pvs[3]=="480p":
      PVS_params['width'] = 854
      PVS_params['height'] = 480
     elif v_pvs[3]=="720p":
      PVS_params['width'] = 1280
      PVS_params['height'] = 720
     elif v_pvs[3]=="1080p":
      PVS_params['width'] = 1920
      PVS_params['height'] = 1080
     elif v_pvs[3]=="1440p":
      PVS_params['width'] = 2560
      PVS_params['height'] = 1440
     elif v_pvs[3]=="2160p":
      PVS_params['width'] = 3840
      PVS_params['height'] = 2160
   
     PVS_params['fps'] = float(v_pvs[4].replace('fps', ''))
     PVS_params['encoder'] = v_pvs[5].strip()
     PVS_params['yuv_fmt'] = 'yuv422p10le'
     MOS = float(v_line[2])
     CI = float(v_line[3])
     #computed_MOS = None
     #OS = [0] * 18 	
     #for i in range(1, 18):  
      #  OS[i] = None
    #return {'PVS': {'PVS_ID': PVS_ID} | PVS_params, 'MOS': MOS, 'computed_MOS': computed_MOS, 'OS': OS,'CI' : CI}

    return {'PVS': {'PVS_ID': PVS_ID} | PVS_params, 'MOS': MOS,'CI' : CI}


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

csv_information['dataset_name'] = 'AVT-VQDB-UHD-1_4'
csv_information['SRC_names'] = list(set([x['PVS']['SRC'] for x in file_line_information]))
# csv_information['SRC_num'] = len(csv_information['SRC_names'])
csv_information['PVS_bitrates'] = sorted(list(set([x['PVS']['bitrate'] for x in file_line_information])))
csv_information['PVS_encoders'] = list(set([x['PVS']['encoder'] for x in file_line_information]))
csv_information['PVS_resolutions'] = list(set(["%sx%s" % (x['PVS']['width'], x['PVS']['height']) for x in file_line_information]))
csv_information['scores'] = file_line_information

# Save to JSON file
json_file_path = "ScoresAVT-VQDB-UHD-1_4.json"  
with open(json_file_path, 'w') as json_file:
    json.dump(csv_information, json_file, indent=4)

#print(f"Data has been written to {json_file_path}")
#print(json.dumps(csv_information, sort_keys=False, indent=4))
