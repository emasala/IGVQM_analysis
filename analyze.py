import os
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import json
import sys
import re
from scipy.stats import gmean

if len(sys.argv) not in [17, 18]:  
    print("Error, format is : python3 analyze.py <dataset> <width> <height> <bitrate> <video_codec> <model_version> <output_directory> <original_video> <distorted_video> <width_old> <height_old> <fps> <duration> <mos_dir> <essim_params_string> <use_libvmaf> <use_essim>")
    sys.exit(1)

dataset = sys.argv[1]        
width = int(sys.argv[2])     
height = int(sys.argv[3])    
bitrate = sys.argv[4]   
video_codec = sys.argv[5]   
model_version = sys.argv[6] 
output_directory = sys.argv[7] 
original_video = sys.argv[8]  
distorted_video = sys.argv[9]
width_old = sys.argv[10]
height_old = sys.argv[11]
fps = sys.argv[12]
duration = sys.argv[13]
mos_dir = sys.argv[14]
use_libvmaf = sys.argv[15]
use_essim = sys.argv[16]

essim_params_string = sys.argv[17] if len(sys.argv) == 18 else ""

mos = -1
ci = -1
computed_mos = -1

temporal_pooling_count = 9

essim_param_string_list = essim_params_string.split(",")
print(essim_param_string_list)
#essim_params={}
#patterns= ['ws', 'wt', 'mk', 'md']
#for pattern in patterns:
#    match = re.search(rf'{pattern}(\d+)', essim_params_string)
#    if match:
#        essim_params[pattern] = int(match.group(1))
#ws = essim_params['ws']
#wt = essim_params['wt']
#mk = essim_params['mk']
#md = essim_params['md']

#print(f"Distorted_video: {distorted_video}")
#print(f"width_old: {width_old}, height_old: {height_old}")

temporal_pooling_values = ['mean', 'harmonic_mean', 'geometric_mean','percentile_50','percentile_5','percentile_95', 'norm_lp1', 'norm_lp2', 'norm_lp3']

vmaf_models = [
    "vmaf_v0.6.1", 
    "vmaf_v0.6.1neg", 
    "vmaf_float_v0.6.1", 
    "vmaf_float_v0.6.1neg", 
    "vmaf_float_b_v0.6.3", 
    "vmaf_b_v0.6.3", 
    "vmaf_float_4k_v0.6.1", 
    "vmaf_4k_v0.6.1", 
    "vmaf_4k_v0.6.1neg"
]

features = ["cambi",
    "float_ssim",
    "psnr_y",
    "psnr_cb",
    "psnr_cr",
    "float_ms_ssim",
    "ciede2000",
    "psnr_hvs_y",
    "psnr_hvs_cb",
    "psnr_hvs_cr",
    "psnr_hvs",
    "vmaf_float_b_v0.6.3_bagging",      
    "vmaf_float_b_v0.6.3_stddev",       
    "vmaf_float_b_v0.6.3_ci_p95_lo",    
    "vmaf_float_b_v0.6.3_ci_p95_hi",
    "vmaf_b_v0.6.3_bagging",      
    "vmaf_b_v0.6.3_stddev",       
    "vmaf_b_v0.6.3_ci_p95_lo",    
    "vmaf_b_v0.6.3_ci_p95_hi",
    "integer_vif_scale3",
    ]

essim_features = [ "eSSIM",
    "SSIM"]

mos_dataset = f"{mos_dir}/Scores{dataset}.json"
if not os.path.exists(mos_dataset):
    raise FileNotFoundError(f"Mos file '{mos_dataset}' was not found")
# read mos dataset fil
with open(mos_dataset) as f:
    data_mos = json.load(f)
#remove extension and take only the name
distorted_file_name_no_extension = distorted_video.rsplit(".", 1)[0]  
for score in data_mos["scores"]:
    # if the distorted file is found in the mos files
    if score["PVS"]["PVS_ID"] == distorted_file_name_no_extension:
        #print(score["PVS"]["PVS_ID"])  
        #set mos
        mos = score["MOS"]
        # set ci
        if "CI" in score:
         ci = score["CI"]
        else:
         ci = -1
         #set computed mos
        if "Computed_MOS" in score:
         computed_mos = score["Computed_MOS"]
        else:
         computed_mos = -1
        break          
else:
    print("No mos found")

csv_filename = f'{output_directory}/{dataset}/combined_results_{dataset}.csv'

# if csv does not exits create with temporal_pooling_count entries
if not os.path.isfile(csv_filename):
    #print("Csv does not exist")
    
    # rows to add
    new_rows = []
    for temporal_pooling_value in temporal_pooling_values:
        row = {
            "Dataset": dataset,
            "Original_file_name": original_video,
            "Distorted_file_name": distorted_video,
            "Width_original": width_old,
            "Height_original": height_old,
            "Width": width,
            "Height": height,
            "Bitrate": bitrate,
            "Video_codec": video_codec,
            "FPS": fps,
            "Duration": duration,
            "MOS": mos,
            "CI": ci,
            "Computed_Mos": computed_mos,
            #"Window_size" : ws,
            #"Window_stride" : wt,
            #"SSIM_Minkowski_pooling": mk,
            #"Mode": md,
            "temporal_pooling": temporal_pooling_value
        }
        
       #add void columns for models and features
        for model in vmaf_models:
            row[model] = ""  
        
        for feature in features:
            row[feature] = ""  
        
        if essim_param_string_list[0]!= "":
            for param_string in essim_param_string_list:
                for essim_feature in essim_features:
                    col_name = f"{essim_feature}_{param_string.strip()}"
                    row[col_name] = -1  
        
        new_rows.append(row)
    
    # create a dataframe from the rows ( one row for temporal pooling) and convert to csv
    new_df = pd.DataFrame(new_rows)
    new_df.to_csv(csv_filename, mode='w', header=True, index=False)
    #print("CSV created")
else:
    # If csv already exists , verify if distorted_video is present
    #rint("Csv already exists, check if distorted_video already exists : ")
    
    df_existing = pd.read_csv(csv_filename)
    
    if distorted_video not in df_existing['Distorted_file_name'].values:
        #print(f"{distorted_video} not found in the csv, adds rows")
        #add new rows if it another distorted video
        new_rows = []
        for temporal_pooling_value in temporal_pooling_values:
            row = {
                "Dataset": dataset,
                "Original_file_name": original_video,
                "Distorted_file_name": distorted_video,
                "Width_original": width_old,
                "Height_original": height_old,
                "Width": width,
                "Height": height,
                "Bitrate": bitrate,
                "Video_codec": video_codec,
                "FPS": fps,
                "Duration": duration,
                "MOS": mos,
                "CI": ci,
                "Computed_Mos": computed_mos,
                #"Window_size" : ws,
                #"Window_stride" : wt,
                #"SSIM_Minkowski_pooling": mk,
                #"Mode": md,
                "temporal_pooling": temporal_pooling_value
            }
            
            # Add void columns for models and features
            for model in vmaf_models:
                row[model] = ""  
            
            for feature in features:
                    row[feature] = ""  
            if essim_param_string_list[0]!= "":
                for param_string in essim_param_string_list:
                    for essim_feature in essim_features:
                        col_name = f"{essim_feature}_{param_string.strip()}"
                        if col_name not in df_existing.columns:
                            df_existing[col_name] = -1  
                            row[col_name] = -1 

            new_rows.append(row)
        
        # Add new rows to already existing dataframe
        new_df = pd.DataFrame(new_rows)
        df_existing = pd.concat([df_existing, new_df], ignore_index=True)
        
        #fill void with -1
        for col in df_existing.columns:
            df_existing[col] = df_existing[col].fillna(-1)

        # update csv with new dataframe
        df_existing.to_csv(csv_filename, mode='w', header=True, index=False)
        #print("temporal_pooling_count rows added to csv.")
    else:
        print(f"{distorted_video} is already present in the csv")
        df_existing = pd.read_csv(csv_filename)
        if essim_param_string_list[0]!= "":
            for param_string in essim_param_string_list:
                for essim_feature in essim_features:
                    col_name = f"{essim_feature}_{param_string.strip()}"
                    if col_name not in df_existing.columns:
                        #print(f"Column {col_name} does not exist. Adding to the DataFrame.")
                        df_existing[col_name] = -1 

            df_existing = df_existing.fillna(-1)   
            df_existing.to_csv(csv_filename, mode='w', header=True, index=False)
        #print("Missing columns added to the csv.")

        
        
        
#todo : remove lines here
if dataset in ["KUGVD", "GamingVideoSet1", "GamingVideoSet2"]:
    # Create the JSON path name
    if width_old != '1920' or height_old != '1080':
        json_filename = f'{output_directory}/{dataset}/vmaf_results/result__{dataset}__{original_video}__{distorted_video}__{width_old}x{height_old}__{bitrate}__{video_codec}__{fps}__{duration}__{model_version}__resized_{width}x{height}.json'
        #essim_filename = f'{output_directory}/{dataset}/essim_results/result__{dataset}__{original_video}__{distorted_video}__{width_old}x{height_old}__{bitrate}__{video_codec}__{fps}__{duration}__{model_version}__{essim_params_string}__resized_{width}x{height}.csv'
    else:
        json_filename = f'{output_directory}/{dataset}/vmaf_results/result__{dataset}__{original_video}__{distorted_video}__{width_old}x{height_old}__{bitrate}__{video_codec}__{fps}__{duration}__{model_version}.json'
        #essim_filename = f'{output_directory}/{dataset}/essim_results/result__{dataset}__{original_video}__{distorted_video}__{width_old}x{height_old}__{bitrate}__{video_codec}__{fps}__{duration}__{model_version}__{essim_params_string}.csv'
elif dataset in ["AVT-VQDB-UHD-1_1", "AVT-VQDB-UHD-1_2", "AVT-VQDB-UHD-1_3","AVT-VQDB-UHD-1_4"]:
    if original_video == "bigbuck_bunny_8bit.yuv":
        if width_old != '4000' or height_old != '2250':
            json_filename = f'{output_directory}/{dataset}/vmaf_results/result__{dataset}__{original_video}__{distorted_video}__{width_old}x{height_old}__{bitrate}__{video_codec}__{fps}__{duration}__{model_version}__resized_{width}x{height}.json'
            #essim_filename = f'{output_directory}/{dataset}/essim_results/result__{dataset}__{original_video}__{distorted_video}__{width_old}x{height_old}__{bitrate}__{video_codec}__{fps}__{duration}__{model_version}__{essim_params_string}__resized_{width}x{height}.csv'
        else:
            json_filename = f'{output_directory}/{dataset}/vmaf_results/result__{dataset}__{original_video}__{distorted_video}__{width_old}x{height_old}__{bitrate}__{video_codec}__{fps}__{duration}__{model_version}.json'
            #essim_filename = f'{output_directory}/{dataset}/essim_results/result__{dataset}__{original_video}__{distorted_video}__{width_old}x{height_old}__{bitrate}__{video_codec}__{fps}__{duration}__{model_version}__{essim_params_string}.csv'
    else:
        if width_old != '3840' or height_old != '2160':
            json_filename = f'{output_directory}/{dataset}/vmaf_results/result__{dataset}__{original_video}__{distorted_video}__{width_old}x{height_old}__{bitrate}__{video_codec}__{fps}__{duration}__{model_version}__resized_{width}x{height}.json'
            #essim_filename = f'{output_directory}/{dataset}/essim_results/result__{dataset}__{original_video}__{distorted_video}__{width_old}x{height_old}__{bitrate}__{video_codec}__{fps}__{duration}__{model_version}__{essim_params_string}__resized_{width}x{height}.csv'
        else:
            json_filename = f'{output_directory}/{dataset}/vmaf_results/result__{dataset}__{original_video}__{distorted_video}__{width_old}x{height_old}__{bitrate}__{video_codec}__{fps}__{duration}__{model_version}.json'
            #essim_filename = f'{output_directory}/{dataset}/essim_results/result__{dataset}__{original_video}__{distorted_video}__{width_old}x{height_old}__{bitrate}__{video_codec}__{fps}__{duration}__{model_version}__{essim_params_string}.csv'
else:
    if dataset in [ "ITS4S" , "AGH_NTIA_Dolby"]:
        if width_old != '1280' or height_old != '720':
            json_filename = f'{output_directory}/{dataset}/vmaf_results/result__{dataset}__{original_video}__{distorted_video}__{width_old}x{height_old}__{bitrate}__{video_codec}__{fps}__{duration}__{model_version}__resized_{width}x{height}.json'
            #essim_filename = f'{output_directory}/{dataset}/essim_results/result__{dataset}__{original_video}__{distorted_video}__{width_old}x{height_old}__{bitrate}__{video_codec}__{fps}__{duration}__{model_version}__{essim_params_string}__resized_{width}x{height}.csv'
        else:
            json_filename = f'{output_directory}/{dataset}/vmaf_results/result__{dataset}__{original_video}__{distorted_video}__{width_old}x{height_old}__{bitrate}__{video_codec}__{fps}__{duration}__{model_version}.json'
            #essim_filename = f'{output_directory}/{dataset}/essim_results/result__{dataset}__{original_video}__{distorted_video}__{width_old}x{height_old}__{bitrate}__{video_codec}__{fps}__{duration}__{model_version}__{essim_params_string}.csv'


# Print json filename
#print(f"Json file path: {json_filename}")

try:
    with open(json_filename) as f:
        data = json.load(f)
except FileNotFoundError:
    print(f"Error: Json file  '{json_filename}' not found.")
    #sys.exit(1)

essim_file_names = []
if essim_param_string_list!=['']:
    for string_i in essim_param_string_list:
        if dataset in ["KUGVD", "GamingVideoSet1", "GamingVideoSet2"]:
            if width_old != '1920' or height_old != '1080':
                essim_filename = f'{output_directory}/{dataset}/essim_results/result__{dataset}__{original_video}__{distorted_video}__{width_old}x{height_old}__{bitrate}__{video_codec}__{fps}__{duration}__{model_version}__{string_i}__resized_{width}x{height}.csv'
            else:
                essim_filename = f'{output_directory}/{dataset}/essim_results/result__{dataset}__{original_video}__{distorted_video}__{width_old}x{height_old}__{bitrate}__{video_codec}__{fps}__{duration}__{model_version}__{string_i}.csv'
        elif dataset in ["AVT-VQDB-UHD-1_1", "AVT-VQDB-UHD-1_2", "AVT-VQDB-UHD-1_3", "AVT-VQDB-UHD-1_4"]:
            if original_video == "bigbuck_bunny_8bit.yuv":
                if width_old != '4000' or height_old != '2250':
                    essim_filename = f'{output_directory}/{dataset}/essim_results/result__{dataset}__{original_video}__{distorted_video}__{width_old}x{height_old}__{bitrate}__{video_codec}__{fps}__{duration}__{model_version}__{string_i}__resized_{width}x{height}.csv'
                else:
                    essim_filename = f'{output_directory}/{dataset}/essim_results/result__{dataset}__{original_video}__{distorted_video}__{width_old}x{height_old}__{bitrate}__{video_codec}__{fps}__{duration}__{model_version}__{string_i}.csv'
            else:
                if width_old != '3840' or height_old != '2160':
                    essim_filename = f'{output_directory}/{dataset}/essim_results/result__{dataset}__{original_video}__{distorted_video}__{width_old}x{height_old}__{bitrate}__{video_codec}__{fps}__{duration}__{model_version}__{string_i}__resized_{width}x{height}.csv'
                else:
                    essim_filename = f'{output_directory}/{dataset}/essim_results/result__{dataset}__{original_video}__{distorted_video}__{width_old}x{height_old}__{bitrate}__{video_codec}__{fps}__{duration}__{model_version}__{string_i}.csv'
        else:
            if dataset in ["ITS4S", "AGH_NTIA_Dolby"]:
                if width_old != '1280' or height_old != '720':
                    essim_filename = f'{output_directory}/{dataset}/essim_results/result__{dataset}__{original_video}__{distorted_video}__{width_old}x{height_old}__{bitrate}__{video_codec}__{fps}__{duration}__{model_version}__{string_i}__resized_{width}x{height}.csv'
                else:
                    essim_filename = f'{output_directory}/{dataset}/essim_results/result__{dataset}__{original_video}__{distorted_video}__{width_old}x{height_old}__{bitrate}__{video_codec}__{fps}__{duration}__{model_version}__{string_i}.csv'

    essim_file_names.append(essim_filename)

#for filename in essim_file_names:
#    print(filename)
#print(essim_filename)
#print(use_essim)
#print(use_libvmaf)

if (use_libvmaf == "True"):
    # Take data from the frames
    frames_list = data["frames"]
    frames_rows = []

    for frame in frames_list:
        frame_num = frame["frameNum"]
        metrics = frame["metrics"]
        row = {"Frame": frame_num}
        row.update(metrics)
        frames_rows.append(row)

    # example of row in frames_rows : frame_number cambi ciede ecc
    # Create a DataFrame for current file's metrics
    dframes = pd.DataFrame(frames_rows)
    
    

if (use_essim == "True" and use_libvmaf == "True"):

    essim_dframes_list = []
    for essim_file_name, param_string in zip(essim_file_names, essim_param_string_list):
        essim_dframes = pd.read_csv(essim_file_name)
        essim_dframes.columns = essim_dframes.columns.str.strip()
        essim_dframes.rename(columns={
        'eSSIM': f'eSSIM_{param_string}',
        'SSIM': f'SSIM_{param_string}'
    }, inplace=True)
        essim_dframes_list.append(essim_dframes)

    merged_df = dframes.copy()

    for essim_df in essim_dframes_list:
        merged_df = pd.merge(merged_df, essim_df, on='Frame', how='left')
   

if use_essim == "True" and use_libvmaf == "False":

    essim_dframes_list = []
    
    for essim_file_name, param_string in zip(essim_file_names, essim_param_string_list):
        essim_dframes = pd.read_csv(essim_file_name)
        essim_dframes.columns = essim_dframes.columns.str.strip()
        essim_dframes.rename(columns={
            'eSSIM': f'eSSIM_{param_string}',
            'SSIM': f'SSIM_{param_string}'
        }, inplace=True)
        essim_dframes_list.append(essim_dframes)

    merged_essim_df = essim_dframes_list[0]

    for essim_df in essim_dframes_list[1:]:
        merged_essim_df = pd.merge(merged_essim_df, essim_df, on='Frame', how='left')
        
    print(merged_essim_df)



def calculate_metrics(dataframe_name,column_name):
    dataframe_name.columns = dataframe_name.columns.str.strip()
    if column_name in dataframe_name.columns:
        column_data = dataframe_name[column_name]
        if np.any(np.isnan(column_data)):
            #return -1 for the column if there are null values
            print(f"NaN values found in {column_name}, returning -1 for all metrics.")
            return (-1, -1, -1, -1, -1, -1, -1,-1,-1)
        
        mean_value = np.mean(dataframe_name[column_name])
        harmonic_mean_value = 1.0 / np.mean(1.0 / (dataframe_name[column_name] + 1.0)) - 1.0
        geometric_mean_value = gmean(dataframe_name[column_name])
        percentile_50 = np.percentile(dataframe_name[column_name], 50)
        percentile_5 = np.percentile(dataframe_name[column_name], 5)
        percentile_95 =np.percentile(dataframe_name[column_name], 95)
        
        #print(f"1st Percentile: {percentile_1}")
        #print(f"5th Percentile: {percentile_5}")
        #print(f"95th Percentile: {percentile_95}")

        
        # Print values
        #print(f"{column_name} Mean: {mean_value}")
        #print(f"Harmonic mean {column_name}: {harmonic_mean_value}")
        #print(f"Geometric mean {column_name}: {geometric_mean_value}")
        #print(f"{column_name} Percentiles:")
        
        
        # Norms
        norm_lp_1 = np.power(np.mean(np.power(np.array(dataframe_name[column_name]), 1)), 1.0 / 1)  
        #print(f"Norm L_1 of {column_name} values is: {norm_lp_1}")

        norm_lp_2 = np.power(np.mean(np.power(np.array(dataframe_name[column_name]), 2)), 1.0 / 2)  
        #print(f"Norm L_2 of {column_name} values is: {norm_lp_2}")

        norm_lp_3 = np.power(np.mean(np.power(np.array(dataframe_name[column_name]), 3)), 1.0 / 3)  
        #print(f"Norm L_3 of {column_name} values is: {norm_lp_3}")

        return mean_value, harmonic_mean_value, geometric_mean_value,percentile_50,percentile_5,percentile_95, norm_lp_1, norm_lp_2, norm_lp_3
    else:
        print(f"Metric '{column_name}' not found in the DataFrame.")
        return (-1,-1,-1,-1,-1,-1,-1,-1,-1)

if model_version == "vmaf_v0.6.1.json":
    metrics_to_evaluate = [
        "vmaf",
        "cambi",
        "float_ssim",
        "psnr_y",
        "psnr_cb",
        "psnr_cr",
        "float_ms_ssim",
        "ciede2000",
        "psnr_hvs_y",
        "psnr_hvs_cb",
        "psnr_hvs_cr",
        "psnr_hvs",
        "integer_vif_scale3",
        #"eSSIM",
        #"SSIM" ,
    ]
    if essim_param_string_list[0]!="":
        for string in essim_param_string_list:
            metrics_to_evaluate.append(f"eSSIM_{string}")
            metrics_to_evaluate.append(f"SSIM_{string}")

elif model_version in ["vmaf_b_v0.6.3.json", "vmaf_float_b_v0.6.3.json"]:
    metrics_to_evaluate = [
        "vmaf",
        "vmaf_bagging",
        "vmaf_stddev",
        "vmaf_ci_p95_lo",
        "vmaf_ci_p95_hi",
    ]
else:
    metrics_to_evaluate = ["vmaf"]


metrics_results = {}
for metric in metrics_to_evaluate:
    if use_essim == "True" and use_libvmaf == "True":
        results = calculate_metrics(merged_df,metric)
    elif use_essim =="True" and use_libvmaf =="False":
        results= calculate_metrics(merged_essim_df,metric) #@toredo
    else:
        results= calculate_metrics(dframes,metric)
    if results:
        metrics_results[metric] = results

# example of metrics_results :
# metrics_results[ciede2000] = {mean,harmonic_mean,..} 
df_existing = pd.read_csv(csv_filename)


def fill_dataframe(df, model_version, metric, values, start_row, temporal_pooling_count):
    # Fill the column with values for temporal_pooling_count rows starting from start_row
    values = np.array(values, dtype=np.float64)
    df[metric] = df[metric].astype(np.float64)
    mean, harmonic_mean, geometric_mean, percentile_50,percentile_5, percentile_95, norm_lp_1, norm_lp_2, norm_lp_3 = values
    df.loc[start_row:start_row + temporal_pooling_count - 1, metric] = [
        mean,
        harmonic_mean,
        geometric_mean,
        percentile_50,
        percentile_5,
        percentile_95,
        norm_lp_1,
        norm_lp_2,
        norm_lp_3,
    ]

def process_metrics(df_existing, metrics_results, model_version, temporal_pooling_count, distorted_video):
    model_base = model_version.replace(".json", "")
    
    # Find the first occurrence of 'distorted_video' in the 'Distorted_file_name' column
    first_occurrence_row = df_existing[df_existing["Distorted_file_name"] == distorted_video].index[0]
    
 
    # Loop through each metric in metrics_results
    for metric, values in metrics_results.items():
        if metric == "vmaf":
            column = model_base
        elif metric.startswith("vmaf_"):
            column = f"{model_base}_{metric.split('_', 1)[1]}"
        else:
            column = metric
        
        fill_dataframe(df_existing, model_version, column, values, first_occurrence_row, temporal_pooling_count)

if model_version in ["vmaf_v0.6.1.json", "vmaf_b_v0.6.3.json", "vmaf_float_b_v0.6.3.json"]:
    process_metrics(df_existing, metrics_results, model_version, temporal_pooling_count, distorted_video)
elif "vmaf" in metrics_results:
    mean, harmonic_mean, geometric_mean,percentile_50,percentile_5, percentile_95, norm_lp_1, norm_lp_2, norm_lp_3 = metrics_results["vmaf"]
    # Find the first occurrence row where 'Distorted_file_name' matches distorted_video
    first_occurrence_row = df_existing[df_existing["Distorted_file_name"] == distorted_video].index[0]
    
    # Fill the columns starting from the first occurrence row
    fill_dataframe(df_existing, model_version, model_version.replace(".json", ""), 
                   [mean, harmonic_mean, geometric_mean,percentile_50,percentile_5, percentile_95, norm_lp_1, norm_lp_2, norm_lp_3], 
                   first_occurrence_row, temporal_pooling_count)

# Update the csv with the new dataframe
df_existing.to_csv(csv_filename, mode='w', header=True, index=False)

print(f"Column for {model_version} added")
