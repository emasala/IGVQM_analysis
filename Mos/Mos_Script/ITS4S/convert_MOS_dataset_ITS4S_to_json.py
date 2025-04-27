import sys
import re
import json

#File_Name,SESSION,SRC,HRC,MOS,SOS,NUM_SUBJ,SRC_Description,HRC_Description,,Subjects-->,1,2,3,4,5,6,10,11,12,13,14,15,16,18,19,20,21,23,24,25,26,27,29,30,31,32,33
#Broadcast_001-Bsrc11A_1256K,Broadcast,Bsrc11A,1256K,4,0.733799385705343,27,"SRC taken from ""Tears"", RSRC A = Action movie","HRC = ""H.264 coded at 1.256 Mbps, reduced resolution (824 x 464)""",, ,4,4,4,3,4,4,3,3,3,3,4,3,5,4,4,4,5,5,5,4,5,5,4,5,3,4,4


def decode_line(line):
    v_line = line.split(';')
    print(v_line)
    PVS_ID=v_line[0].strip()
    PVS_params = {}
    # first element of the line
    PVS_params['PVS_ID']=PVS_ID
    PVS_params['Session']=v_line[1]
    PVS_params['SRC'] = v_line[2]
    PVS_params['HRC'] = v_line[3]
    MOS= float(v_line[4])
    SOS = float(v_line[5])
    PVS_params['NUM_SUBJ']=int(v_line[6])
    NUM_SUBJ=int(v_line[6])
    PVS_params['SRC_Description'] = v_line[7]
    PVS_params['HRC_Description'] = v_line[8]
   
    
    OS={}
    total=0
    for i in range(27):  
        value = v_line[11 + i].strip()
        if value!="":
         total+=int(value)
        OS[i + 1] = int(value) if value else "" 
    
    
    computed_MOS = total / float(NUM_SUBJ)


    return {'PVS': {'PVS_ID': PVS_ID} | PVS_params, 'MOS': MOS,'SOS':SOS,'OS':OS,'Computed_MOS' : computed_MOS}
    
def decode_other_lines(line):
    Os_Information={}
    v_line = line.split(';')
    Os_Information['Metric']=v_line[10]
    for i in range(27):  
        value = v_line[11 + i].strip()
        Os_Information[i + 1] = value
    return Os_Information 



## __main__ ##

if len(sys.argv) <= 1:
    sys.stderr.write("ERROR: missing datafile.csv\n")
    sys.exit()

# dictionary
csv_information = {}
# void list: save each line of the file
file_line_information = []
#os_information
os_information=[]
# open the file
f = open(sys.argv[1], 'r')
# read first line of the file
header = f.readline()
# read second line of the file
line = f.readline()
linenumber=2
while linenumber<815:
    # work on the current line and save in the list file_line_information
    file_line_information.append(decode_line(line))
    line = f.readline()
    linenumber+=1
for linenumber in range(816, 823):
        line = f.readline().strip()
        if line: 
            os_information.append(decode_other_lines(line))
f.close()

csv_information['dataset_name'] = 'ITS4S'
csv_information['Sessions']=list(set([x['PVS']['Session'] for x in file_line_information]))
csv_information['SRC_Names']=list(set([x['PVS']['SRC'] for x in file_line_information]))
csv_information['HRC_Names']=list(set([x['PVS']['HRC'] for x in file_line_information]))
csv_information['SRC_Descriptions']=list(set([x['PVS']['SRC_Description'] for x in file_line_information]))
csv_information['HRC_Descriptions']=list(set([x['PVS']['HRC_Description'] for x in file_line_information]))
csv_information['scores'] = file_line_information
csv_information['OS_information']=os_information

# Save to JSON file
json_file_path = "ScoresITS4S.json"  
with open(json_file_path, 'w') as json_file:
    json.dump(csv_information, json_file, indent=4,ensure_ascii=False)

#print(f"Data has been written to {json_file_path}")
#print(json.dumps(csv_information, sort_keys=False, indent=4))
