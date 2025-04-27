import os
import sys
import json
from jsonschema import validate, ValidationError
import re

def create_vmaf_command(image_name, input_reference_dir, input_distorted_dir, output_dir, hash_dir, mos_dir, original_video, distorted_video, model_version, model_version_list_to_analyze,dataset, width, height, bitrate, video_codec, pixel_format, bit_depth, fps, duration, use_libvmaf,use_essim,essim_params_string_list,features_list):
    
    original_video = f'"{original_video}"'
    distorted_video = f'"{distorted_video}"'
    # The features are in a list, and I create a single string where they are joined by a comma (',')
    features = ','.join(features_list)  
    if essim_params_string != "no_essim":
        essim_params_string_list = ','.join(essim_params_strings)
    else:
        essim_params_string_list = "no_essim"
        
    model_version_list = ','.join(model_version_list_to_analyze)
    #commands creation with features if model is vmaf_v0.6.1.json
    if model_version == "vmaf_v0.6.1.json":
        command = f"podman run --rm -it \
        -v {input_reference_dir}:/reference \
        -v {input_distorted_dir}:/distorted \
        -v {output_dir}:/results \
        -v {hash_dir}:/hash \
        -v {mos_dir}:/mos \
        {image_name} \
        /bin/bash -c './run_experiments.sh /reference /distorted /results /hash /mos {model_version} {model_version_list} {dataset} {width} {height} {bitrate} {video_codec} {pixel_format} {bit_depth} {fps} {duration} {original_video} {distorted_video} {output_dir} {hash_dir} {mos_dir} {essim_params_string_list} {use_libvmaf} {use_essim}  {features}'"
    else:
        command = f"podman run --rm -it\
        -v {input_reference_dir}:/reference \
        -v {input_distorted_dir}:/distorted \
        -v {output_dir}:/results \
        -v {hash_dir}:/hash \
        -v {mos_dir}:/mos \
        {image_name} \
        /bin/bash -c './run_experiments.sh /reference /distorted /results /hash /mos {model_version} {model_version_list}  {dataset} {width} {height} {bitrate} {video_codec} {pixel_format} {bit_depth} {fps} {duration} {original_video} {distorted_video} {output_dir} {hash_dir} {mos_dir} {essim_params_string_list} {use_libvmaf} {use_essim}  {""}'"
    return command

if __name__ == '__main__':
    if len(sys.argv) != 2:
        print("The script needs two arguments. You need to call it like: python3 create_commands.py Json/config.json")
        sys.exit(1)
    
    config_file = sys.argv[1]

# 9 possible models
vmaf_models = [
    "vmaf_v0.6.1.json", 
    "vmaf_v0.6.1neg.json", 
    "vmaf_float_v0.6.1.json", 
    "vmaf_float_v0.6.1neg.json", 
    "vmaf_float_b_v0.6.3.json", 
    "vmaf_b_v0.6.3.json", 
    "vmaf_float_4k_v0.6.1.json", 
    "vmaf_4k_v0.6.1.json", 
    "vmaf_4k_v0.6.1neg.json",
]

schema_file_path = 'Json/configschema.json'

try:
    with open(config_file, 'r') as f:
        config = json.load(f)
except FileNotFoundError:
    print(f"Error: Config file '{config_file}' not found.")
    sys.exit(1)

try:
    # Read the json schema file
    with open(schema_file_path) as schema_file:
        schema = json.load(schema_file)
except FileNotFoundError:
    print(f"Error: Schema file '{schema_file_path}' not found.")
    sys.exit(1)

    
# Get data from the config file
image_name = config['IMAGE_NAME']
input_reference_dir = config['INPUT_REF_DIR']
input_distorted_dir = config['INPUT_DIST_DIR']
output_dir = config['OUTPUT_DIR']
hash_dir = config['HASH_DIR']
mos_dir = config['MOS_DIR']
dataset_dir = config['DATASET_DIR']
original_video = config['ORIGINAL_VIDEO']
model_version_list = config['MODEL_VERSION']
dataset = config['DATASET']
features_list = config['FEATURES']
use_libvmaf = config['USE_LIBVMAF']
use_essim = config ['USE_ESSIM']


essim_params_list =config["ESSIM_PARAMETERS"]
essim_params_strings = []
if not essim_params_list:
    essim_params_string="no_essim"
else:
    for param_string in essim_params_list:
        ws = param_string["Window_size"]
        wt = param_string["Window_stride"]
        mink = param_string["SSIM_Minkowski_pooling"]
        mode = param_string["Mode"]
        essim_params_string = f"ws{ws}_wt{wt}_mk{mink}_md{mode}"
        essim_params_strings.append(essim_params_string)


    
# Create the directories if they do not exist
os.makedirs(hash_dir, exist_ok=True)
os.makedirs(mos_dir, exist_ok=True)
os.makedirs(output_dir, exist_ok=True)
os.makedirs(dataset_dir, exist_ok=True)

# Read the dataset file name 
dataset_name = f"{dataset}.json"  
# Find the dataset in the correct path
dataset_file = os.path.join(dataset_dir, dataset_name)

# Verify if dataset file exists
if not os.path.isfile(dataset_file):
    print(f"Error: Dataset file '{dataset_file}' does not exixst")
    sys.exit(1)


# Validate the schema 
try:
    validate(instance=config, schema=schema)
    print("JSON is valid")
except ValidationError as e:
    print("JSON is not valid", e.message)
    sys.exit(1) 
    
# Load the video metadata
with open(dataset_file, 'r') as f:
    video_metadata = json.load(f)

# Gets the name of the original file without the extension 
# Take basename (without the path), split into "name" and "extension", then take only the name.
original_without_extension = os.path.splitext(os.path.basename(original_video))[0]
if dataset == "ITS4S":
    original_without_extension = original_without_extension.replace("_SRC", "")
    #print(original_without_extension)
elif dataset == "AGH_NTIA_Dolby":
    original_without_extension = original_without_extension.replace("_original", "") 
# Removes whitespaces from the string.
original_without_extension = original_without_extension.strip()
#print(f"Original video name (without extension): {original_without_extension}")

# Create the regex pattern to match the exact original_without_extension
# escaping any special characters
# ^ : from the start of original_without_extension to the end of the string or a "-"
# compiled in a pattern object
pattern_original = re.compile(f"^{re.escape(original_without_extension)}(_|$)")


# Loop on the files in input_distorted_dir
for distorted_file in os.listdir(input_distorted_dir):
    distorted_full_name = distorted_file  
    #take only the name without the extension and remove whitespaces
    distorted_without_extension = os.path.splitext(distorted_full_name)[0]
    distorted_without_extension= distorted_without_extension.strip()
    if pattern_original.match(distorted_without_extension):
    # If the original file name is contained in the distorted file name, generate the command
        # Find the distorted video with file_name equal to distorted_full_name 
        # Extract metadata associated with the distorted file
        metadata = None
        for video in video_metadata["distorted_videos"]:
            if video["file_name"] == distorted_full_name:
                metadata = video
                #print(f"Metadata found for {distorted_full_name}: {metadata}")  
                break

        # If the video exists, extract its metadata
        if metadata:
            width = metadata["width"]
            height = metadata["height"]
            bitrate = metadata["bitrate"]
            video_codec = metadata["video_codec"]
            pixel_format = metadata["pixel_format"]
            bit_depth = metadata["bitdepth"]
            fps = metadata["fps"]
            duration = metadata["duration"]
        
            #print(f"Metadata for {distorted_full_name}:")
            #print(f"Width: {width}, Height: {height}, Bitrate: {bitrate}, Video Codec: {video_codec}, Pixel Format: {pixel_format}, Bit Depth: {bit_depth}, FPS: {fps}, Duration: {duration}")  
            # where the commands are saved
            output_dataset_dir = os.path.join(output_dir, dataset)
            os.makedirs(output_dataset_dir, exist_ok=True)
            # output file name
            commands_file_name = f"commands_{dataset}.txt"
            if model_version_list[0] == 'VMAF_ALL':   
                for model_version in vmaf_models:
                    command = create_vmaf_command(image_name, input_reference_dir, input_distorted_dir, output_dir, hash_dir, mos_dir, original_video, distorted_full_name, model_version,vmaf_models, dataset, width, height, bitrate, video_codec, pixel_format, bit_depth, fps, duration, use_libvmaf, use_essim,essim_params_strings,features_list)
                    #print(f"Generated command: {command}")  
                    with open(os.path.join(output_dataset_dir, commands_file_name), 'a') as f:
                        f.write(command + '\n')
                        #print(f"Command written to {os.path.join(output_dataset_dir, commands_file_name)}")
            else: 
                for model_version in model_version_list:
                    command = create_vmaf_command(image_name, input_reference_dir, input_distorted_dir, output_dir, hash_dir, mos_dir, original_video, distorted_full_name, model_version,model_version_list, dataset, width, height, bitrate, video_codec, pixel_format, bit_depth, fps, duration, use_libvmaf, use_essim, essim_params_strings, features_list)
                    #print(f"Generated command: {command}")  
                    with open(os.path.join(output_dataset_dir, commands_file_name), 'a') as f:
                        f.write(command + '\n')
                        #print(f"Command written to {os.path.join(output_dataset_dir, commands_file_name)}")
        else:
            print(f"{distorted_full_name} was not found in the metadata.")

