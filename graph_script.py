import matplotlib.pyplot as plt
import pandas as pd
import os
import numpy as np
import sys
from matplotlib.lines import Line2D

if len(sys.argv) < 3:
    print("You need to call like graph_script <output_dir> <dataset_name>")
    sys.exit(1)
# define axis_limits
axis_limits = {
    "MOS": (1, 5),
    "vmaf_v0.6.1": (0, 100),
    "vmaf_v0.6.1neg" : (0, 100),
    "vmaf_float_v0.6.1": (0, 100),
    "vmaf_float_v0.6.1neg": (0,100),
    "vmaf_float_b_v0.6.3": (0,100),
    "vmaf_b_v0.6.3": (0,100),
    "vmaf_float_4k_v0.6.1": (0,100),
    "vmaf_4k_v0.6.1": (0,100),
    "vmaf_4k_v0.6.1neg": (0,100),
    "float_ssim": (0.6, 1),
    "float_ms_ssim": (0.6, 1),
    "psnr_y": (20, 50),
    "psnr_cb": (20, 50),
    "psnr_cr": (20, 50),
    "psnr_hvs_y": (20, 50),
    "psnr_hvs_cb" : (20, 50),
    "psnr_hvs_cr": (20, 50),
    "psnr_hvs": (20, 50),
    "ciede2000": (20, 50), #to do
    "cambi": (0, 10),  #to do
    "integer_vif_scale3" : (0.5,1),
    "vmaf_float_b_v0.6.3_bagging" :(0, 100),      
    "vmaf_float_b_v0.6.3_stddev" : (0, 100),       
    "vmaf_float_b_v0.6.3_ci_p95_lo":(0, 100),    
    "vmaf_float_b_v0.6.3_ci_p95_hi":(0, 100),
    "vmaf_b_v0.6.3_bagging":(0, 100),      
    "vmaf_b_v0.6.3_stddev":(0, 100),       
    "vmaf_b_v0.6.3_ci_p95_lo":(0, 100),    
    "vmaf_b_v0.6.3_ci_p95_hi":(0, 100),
    "eSSIM":(0, 1),
    "SSIM":(0, 1),
}
temporal_pooling_marker_map = {
    'mean': 'o',  
    'harmonic_mean': 'x',  
    'geometric_mean': 'h',  
    'percentile_50': '^',  
    'percentile_5': 'v',  
    'percentile_95': 'p',  
    'norm_lp1': '*',  
    'norm_lp2': 'D',  
    'norm_lp3': 's',  
    }

output_dir = sys.argv[1]
dataset = sys.argv[2]
print(output_dir)
print(dataset)

csv_file = f'{output_dir}/{dataset}/combined_results_{dataset}.csv'
print(csv_file)

if not os.path.exists(csv_file):
    print(f"File CSV for dataset {dataset} not found")
else:
    data = pd.read_csv(csv_file)
    # define x columns, vmaf models, features, temporal pooling values and other for b models
    x_column = "MOS"
    vmaf_models = [
        "vmaf_v0.6.1", "vmaf_v0.6.1neg", "vmaf_float_v0.6.1", "vmaf_float_v0.6.1neg",
        "vmaf_float_b_v0.6.3", "vmaf_b_v0.6.3", "vmaf_float_4k_v0.6.1",
        "vmaf_4k_v0.6.1", "vmaf_4k_v0.6.1neg",
    ]
    features = ["cambi", "float_ssim", "psnr_y",
        "psnr_cb", "psnr_cr", "float_ms_ssim", "ciede2000", "psnr_hvs_y",
        "psnr_hvs_cb", "psnr_hvs_cr", "psnr_hvs","vmaf_float_b_v0.6.3_bagging",
        "vmaf_b_v0.6.3_bagging", "integer_vif_scale3"#"eSSIM","SSIM"
        ]
    
    if "integer_vif_scale3" in data.columns:
        start_index = data.columns.get_loc("integer_vif_scale3") + 1
        # Selezionare colonne che iniziano con "eSSIM_" o "SSIM_" dopo "integer_vif_scale3"
        eSSIM_features = [col for col in data.columns[start_index:] if col.startswith(("eSSIM_", "SSIM_"))]
        for feature in eSSIM_features:
            axis_limits[feature] = (0.4, 1)

    print("eSSIM Features:", eSSIM_features)
    
    #temporal_pooling_values = ["mean", "harmonic_mean", "geometric_mean", "total_variation,"percentile_5","percentile_95","norm_lp1", "norm_lp2", "norm_lp3"]
    temporal_pooling_graph = ["mean", "harmonic_mean", "geometric_mean","percentile_50","percentile_5","percentile_95","norm_lp1", "norm_lp2", "norm_lp3"]

    lo_column_float_b = "vmaf_float_b_v0.6.3_ci_p95_lo"
    hi_column_float_b = "vmaf_float_b_v0.6.3_ci_p95_hi"
    lo_column_b = "vmaf_b_v0.6.3_ci_p95_lo"
    hi_column_b = "vmaf_b_v0.6.3_ci_p95_hi"
    stddev_column_float_b_v0_6_3 = "vmaf_float_b_v0.6.3_stddev"
    stddev_column_b_v0_6_3 = "vmaf_b_v0.6.3_stddev"

    if x_column not in data.columns:
        raise ValueError(f"Columns {x_column} not found in the csv for {dataset}.")
    # create the output path for every dataset
    output_path = f"{output_dir}/{dataset}/graph_results/"
    os.makedirs(output_path, exist_ok=True)
    # Graph 
    # - for all the PVS, a scatter plot with the VMAF model's mean as the central value and error bars based on the hi and lo values as the lower and upper limits: HILO.
    # - for all the PVS, a scatter plot with the VMAF model's mean with standard deviation as the central value and error bars based on the hi and lo values as the lower and upper limits: HILO.
    # - for all the pvs  a scatter plot with the VMAF model's mean as the central value and error bars based on the 5th and 95th percentiles as lower and upper limits : "Percentile5_95_vsVmafMean"
    # - for every features all the pvs : for every pvs  different points for the different temporal pooling  : "PVS dir"
    # - for every features all the pvs : for every pvs  different points for the different temporal pooling : "PVS dir"
    
    
    
    # where to save analysis    

    hi_lo_output_path = os.path.join(output_path,"HI_LO")
    pvs_path=os.path.join(output_path,"PVS")
    percentile_path = os.path.join(output_path,"Percentile5_95_vsVmafMeanPercentile_50")
    meanvsmeanpath = os.path.join(output_path,"MeanModel1vsMeanModel2")
    
    os.makedirs(hi_lo_output_path, exist_ok=True)
    os.makedirs(pvs_path, exist_ok=True)
    os.makedirs(percentile_path, exist_ok=True)
    
    # extract all the different pvs
    pvs=data['Distorted_file_name'].unique()
    colors_temporal_pooling = [
    "black","blue", "green", "red", "purple", "orange", "brown", "pink","cyan"
    ]
    # Create dictionaries that map each element (e.g., codec, FPS, duration, bitrate, temporal pooling) to a specific color
    # based on its position in the respective list. Each color is selected from the previously generated color palettes.
    temporal_pooling_color_map={temporal_pooling : colors_temporal_pooling[i] for i ,temporal_pooling in enumerate(temporal_pooling_graph)}
    colors_vmaf = [
    "black","blue", "green", "red", "purple", "orange", "brown", "pink","cyan"
    ]
    vmaf_color_map = {vmaf_model: colors_vmaf[i] for i, vmaf_model in enumerate(vmaf_models)}
    
    features_graph = ["psnr_y",
        "psnr_hvs_y",
    ]
    for feature in features_graph+eSSIM_features:
     plt.figure(figsize=(10, 6))
     # Initialize lists for labels and colors, and a set to avoid duplicate labels
     labels = []
     colors = []
     added_labels = set()
     for pvs_value in pvs:
         output_dir = f"{pvs_path}/all_features/"
         if not os.path.exists(output_dir):
            os.makedirs(output_dir)
        # Filter the data for the current pvs_value
         filtered_data = data[data['Distorted_file_name'] == pvs_value]
         if filtered_data.empty:
            print(f"No data found for the pvs sequence: {pvs_value} in dataset {dataset}")
            continue
         # Extract the MOS value
         x_value = filtered_data['MOS'].values[0]
         temporal_pooling_value="mean"
         # Filter the data for the mean temporal_pooling value
         temporal_filtered_data = filtered_data[filtered_data['temporal_pooling'] == temporal_pooling_value]
         if temporal_filtered_data.empty:
            print(f"No data found for temporal pooling {temporal_pooling_value} in {pvs_value}")
            continue
        # Extract the feature value for the temporal filtered data
         feature_value = temporal_filtered_data[feature].values
         if feature_value == -1:
            continue
         # Create a scatter plot with the x_value and feature_value, using the corresponding color
         plt.scatter(x_value, feature_value, color="black", marker='o', alpha=0.7)
         if temporal_pooling_value not in added_labels:
               labels.append(f"{temporal_pooling_value}")
               added_labels.add(temporal_pooling_value)
               
     plt.title(f"Dataset {dataset} : {feature} vs {x_column}")
     plt.xlabel(x_column)
     plt.ylabel(feature)
     # Set axis limits
     if "MOS" in axis_limits:
         plt.xlim(axis_limits["MOS"])  
     if feature in axis_limits:
         plt.ylim(axis_limits[feature])  
     plt.grid(True)
     plt.xticks(rotation=45)
     # display the legend
     plt.legend(title="Temporal Pooling", labels=labels, loc='center left', bbox_to_anchor=(1, 0.5))
     
     output_dir = os.path.join(pvs_path, "all_features", "mean")
     os.makedirs(output_dir, exist_ok=True)
     output_file = os.path.join(output_dir, f"mean_{feature}vsMOS.png")     
     plt.savefig(output_file, bbox_inches='tight')
     print(f"Graph saved: {output_file}")
     plt.close()
     
    for vmaf_model in vmaf_models:
        plt.figure(figsize=(10, 6))
        labels = []
        colors = []
        added_labels = set()
        for pvs_value in pvs:
            output_dir = f"{pvs_path}/all_vmaf_models/"
            if not os.path.exists(output_dir):
                os.makedirs(output_dir)
            filtered_data = data[data['Distorted_file_name'] == pvs_value]
            if filtered_data.empty:
                print(f"No data found for the pvs sequence: {pvs_value} in dataset {dataset}")
                continue
            x_value = filtered_data['MOS'].values[0]
            temporal_pooling_value="mean"
            temporal_filtered_data = filtered_data[filtered_data['temporal_pooling'] == temporal_pooling_value]
            if temporal_filtered_data.empty:
                print(f"No data found for temporal pooling {temporal_pooling_value} in {pvs_value}")
                continue
            model_value = temporal_filtered_data[vmaf_model].values
            if model_value == -1:
                continue
            plt.scatter(x_value, model_value, color="black", marker='o', alpha=0.7)
            if temporal_pooling_value not in added_labels:
               labels.append(f"{temporal_pooling_value}")
               added_labels.add(temporal_pooling_value)

        plt.title(f"Dataset {dataset} : {vmaf_model} vs {x_column}")
        plt.xlabel(x_column)
        plt.ylabel(vmaf_model)
        if "MOS" in axis_limits:
         plt.xlim(axis_limits["MOS"])  
        if vmaf_model in axis_limits:
         plt.ylim(axis_limits[vmaf_model]) 
        plt.grid(True)
        plt.xticks(rotation=45)
        plt.legend(title="Temporal Pooling", labels=labels, loc='center left', bbox_to_anchor=(1, 0.5))

        output_dir = os.path.join(pvs_path, "all_vmaf_models", "mean")
        os.makedirs(output_dir, exist_ok=True)
        output_file = os.path.join(output_dir, f"mean_{vmaf_model}vsMOS.png")    
        plt.savefig(output_file, bbox_inches='tight')
        print(f"Graph saved: {output_file}")
        plt.close()
     
     
     # float b model
    
    #float b model
    plt.figure(figsize=(10, 6))
    labels = []
    colors = []
    added_labels = set()
    for pvs_value in pvs : 
        output_dir = f"{hi_lo_output_path}/float_b_model/"
        if not os.path.exists(output_dir):
            os.makedirs(output_dir) 
        filtered_data = data[data['Distorted_file_name'] == pvs_value]
        if filtered_data.empty:
            print(f"No data found for the pvs sequence: {pvs_value} in dataset {dataset}")
            continue
        x_value = filtered_data['MOS'].values[0]
        for temporal_pooling_value in ["mean"]:
            temporal_filtered_data = filtered_data[filtered_data['temporal_pooling'] == temporal_pooling_value]
            if temporal_filtered_data.empty:
                print(f"No data found for temporal pooling {temporal_pooling_value} in {pvs_value}")
                continue
            y_value = temporal_filtered_data["vmaf_float_b_v0.6.3"].values 
            if  y_value == -1:
                continue
            lo_value = temporal_filtered_data["vmaf_float_b_v0.6.3_ci_p95_lo"].values 
            hi_value = temporal_filtered_data["vmaf_float_b_v0.6.3_ci_p95_hi"].values 
            if hi_value < lo_value or hi_value < y_value or lo_value > y_value:       
                print("Invalid values")
                continue
            
            plt.errorbar(x_value, y_value, yerr=[y_value-lo_value,hi_value-y_value],color="black", marker='o')
            if temporal_pooling_value not in added_labels:
                labels.append(f"{temporal_pooling_value}")
                added_labels.add(temporal_pooling_value)
        plt.title(f" Dataset {dataset} : vmaf_float_b_v0.6.3 vs {x_column}")
        plt.xlabel("MOS")
        plt.ylabel("vmaf_float_b_v0.6.3")
        if "MOS" in axis_limits:
            plt.xlim(axis_limits["MOS"])
        if "vmaf_float_b_v0.6.3" in axis_limits:
            plt.ylim(axis_limits["vmaf_float_b_v0.6.3"])
            
        plt.grid(True)
        plt.xticks(rotation=45)
        plt.legend(title="Temporal Pooling", labels=labels, loc='center left', bbox_to_anchor=(1, 0.5))       
    output_dir = os.path.join(hi_lo_output_path, "float_b_model", "mean")
    os.makedirs(output_dir, exist_ok=True)
    output_file = os.path.join(output_dir, f"mean_hilo_vmaf_float_b_v0.6.3.png")     
    print(f"Graph saved: {output_file}")  
    plt.savefig(output_file, bbox_inches='tight') 
    plt.close()
    
     # float b model stdev
    plt.figure(figsize=(10, 6))
    labels = []
    colors = []
    added_labels = set()
    for pvs_value in pvs : 
        output_dir = f"{hi_lo_output_path}/float_b_model/"
        if not os.path.exists(output_dir):
            os.makedirs(output_dir) 
        filtered_data = data[data['Distorted_file_name'] == pvs_value]  
        if filtered_data.empty:
            print(f"No data found for the pvs sequence: {pvs_value} in dataset {dataset}")
            continue
        x_value = filtered_data['MOS'].values[0]   
        for temporal_pooling_value in ["mean"]:
            temporal_filtered_data = filtered_data[filtered_data['temporal_pooling'] == temporal_pooling_value]
            if temporal_filtered_data.empty:
                print(f"No data found for temporal pooling {temporal_pooling_value} in {pvs_value}")
                continue 
            y_value = temporal_filtered_data["vmaf_float_b_v0.6.3"].values    
            if  y_value == -1:
                continue
            stddev_float_b_value = temporal_filtered_data["vmaf_float_b_v0.6.3_stddev"].values
            lo_value_float_stddev= y_value - stddev_float_b_value
            hi_value_float_stdev = y_value + stddev_float_b_value

            if hi_value_float_stdev < lo_value_float_stddev:
                print(f"Invalid confidence interval: hi_value_float_stdev < lo_value_float_stddev (hi={hi_value_float_stdev}, lo={lo_value_float_stddev})")
                continue
        
            if hi_value_float_stdev < y_value or lo_value_float_stddev > y_value:
                print(f"Invalid confidence interval: interval does not contain the central value (y_value={y_value})")
                continue
            
            plt.errorbar(x_value, y_value, yerr=[y_value-lo_value_float_stddev,hi_value_float_stdev-y_value],color="black", marker='o')
            if temporal_pooling_value not in added_labels:
                labels.append(f"{temporal_pooling_value}")
                added_labels.add(temporal_pooling_value)
        plt.title(f"Dataset {dataset} : vmaf_float_b_v0.6.3 with stddev vs {x_column}")  
        plt.xlabel("MOS")
        plt.ylabel("vmaf_float_b_v0.6.3")
        if "MOS" in axis_limits:
            plt.xlim(axis_limits["MOS"])
        if "vmaf_float_b_v0.6.3" in axis_limits:
            plt.ylim(axis_limits["vmaf_float_b_v0.6.3"])
       
        plt.grid(True)
        plt.xticks(rotation=45)
        plt.legend(title="Temporal Pooling", labels=labels, loc='center left', bbox_to_anchor=(1, 0.5))
    output_dir = os.path.join(hi_lo_output_path, "float_b_model", "mean")
    os.makedirs(output_dir, exist_ok=True)
    output_file = os.path.join(output_dir, f"mean_hilostddev_vmaf_float_b_v0.6.3_stddev.png")       
    print(f"Graph saved: {output_file}")
    plt.savefig(output_file, bbox_inches='tight')
    plt.close()

     # b model

    plt.figure(figsize=(10, 6))
    labels = []
    colors = []
    added_labels = set()
    for pvs_value in pvs : 
        output_dir = f"{hi_lo_output_path}/b_model/"
        if not os.path.exists(output_dir):
            os.makedirs(output_dir) 
        filtered_data = data[data['Distorted_file_name'] == pvs_value]
        if filtered_data.empty:
            print(f"No data found for the pvs sequence: {pvs_value} in dataset {dataset}")
            continue
        x_value = filtered_data['MOS'].values[0]
        for temporal_pooling_value in ["mean"]:
            temporal_filtered_data = filtered_data[filtered_data['temporal_pooling'] == temporal_pooling_value]
            if temporal_filtered_data.empty:
                print(f"No data found for temporal pooling {temporal_pooling_value} in {pvs_value}")
                continue
            y_value = temporal_filtered_data["vmaf_b_v0.6.3"].values  
            if  y_value == -1:
                continue
            lo_value = temporal_filtered_data["vmaf_b_v0.6.3_ci_p95_lo"].values 
            hi_value = temporal_filtered_data["vmaf_b_v0.6.3_ci_p95_hi"].values 
            if hi_value < lo_value or hi_value < y_value or lo_value > y_value:       
                print("Invalid values")
                continue
            plt.errorbar(x_value, y_value, yerr=[y_value-lo_value,hi_value-y_value],color="black", marker='o')
            if temporal_pooling_value not in added_labels:
                labels.append(f"{temporal_pooling_value}")
                added_labels.add(temporal_pooling_value)
        plt.title(f"Dataset {dataset}:vmaf_b_v0.6.3 vs {x_column}")
        plt.xlabel("MOS")
        plt.ylabel("vmaf_b_v0.6.3")
        if "MOS" in axis_limits:
            plt.xlim(axis_limits["MOS"])
        if "vmaf_b_v0.6.3" in axis_limits:
            plt.ylim(axis_limits["vmaf_b_v0.6.3"])
            
        plt.grid(True)
        plt.xticks(rotation=45)
        plt.legend(title="Temporal Pooling", labels=labels, loc='center left', bbox_to_anchor=(1, 0.5))   
    output_dir = os.path.join(hi_lo_output_path, "b_model", "mean")
    os.makedirs(output_dir, exist_ok=True)
    output_file = os.path.join(output_dir, f"mean_hilo_vmaf_b_v0.6.3.png")     
    print(f"Graph saved: {output_file}")  
    plt.savefig(output_file, bbox_inches='tight') 
    plt.close()
    
    # b model stdev
    plt.figure(figsize=(10, 6))
    labels = []
    colors = []
    added_labels = set()
    for pvs_value in pvs : 
        output_dir = f"{hi_lo_output_path}/b_model/"
        if not os.path.exists(output_dir):
            os.makedirs(output_dir) 
        filtered_data = data[data['Distorted_file_name'] == pvs_value]  
        if filtered_data.empty:
            print(f"No data found for the pvs sequence: {pvs_value} in dataset {dataset}")
            continue
        x_value = filtered_data['MOS'].values[0]   
        for temporal_pooling_value in ["mean"]:
            temporal_filtered_data = filtered_data[filtered_data['temporal_pooling'] == temporal_pooling_value]
            if temporal_filtered_data.empty:
                print(f"No data found for temporal pooling {temporal_pooling_value} in {pvs_value}")
                continue 
            y_value= temporal_filtered_data["vmaf_b_v0.6.3"].values    
            if  y_value == -1:
                continue
            stddev_b_value = temporal_filtered_data["vmaf_b_v0.6.3_stddev"].values
            lo_value_b_stddev= y_value - stddev_b_value
            hi_value_b_stdev = y_value + stddev_b_value
            
            if  hi_value_b_stdev  < lo_value_b_stddev:
                print(f"Invalid confidence interval: hi_value_b_stdev < lo_value_b_stddev (hi={hi_value_b_stdev}, lo={lo_value_b_stddev})")
                continue
        
            if hi_value_b_stdev < y_value or lo_value_b_stddev > y_value:
                print(f"Invalid confidence interval: interval does not contain the central value (y_value={y_value})")
                continue
            
            plt.errorbar(x_value, y_value, yerr=[y_value-lo_value_b_stddev,hi_value_b_stdev-y_value],color="black", marker='o')
            if temporal_pooling_value not in added_labels:
                labels.append(f"{temporal_pooling_value}")
                added_labels.add(temporal_pooling_value)
        plt.title(f"Dataset {dataset} : vmaf_b_v0.6.3 with stddev  vs {x_column}")
        plt.xlabel("MOS")
        plt.ylabel("vmaf_b_v0.6.3")
        if "MOS" in axis_limits:
            plt.xlim(axis_limits["MOS"])
        if "vmaf_b_v0.6.3" in axis_limits:
            plt.ylim(axis_limits["vmaf_b_v0.6.3"])
       
        plt.grid(True)
        plt.xticks(rotation=45)
        plt.legend(title="Temporal Pooling", labels=labels, loc='center left', bbox_to_anchor=(1, 0.5))  
    output_dir = os.path.join(hi_lo_output_path, "b_model", "mean")
    os.makedirs(output_dir, exist_ok=True)
    output_file = os.path.join(output_dir, f"mean_hilostddev_vmaf_b_v0.6.3_stddev.png")     
    print(f"Graph saved: {output_file}")
    plt.savefig(output_file, bbox_inches='tight')
    plt.close()
    
    
     
    
    for feature in features+eSSIM_features:
     plt.figure(figsize=(10, 6))
     # Initialize lists for labels and colors, and a set to avoid duplicate labels
     labels = []
     colors = []
     added_labels = set()
     for pvs_value in pvs:
         output_dir = f"{pvs_path}/all_features/"
         if not os.path.exists(output_dir):
            os.makedirs(output_dir)
        # Filter the data for the current pvs_value
         filtered_data = data[data['Distorted_file_name'] == pvs_value]
         if filtered_data.empty:
            print(f"No data found for the pvs sequence: {pvs_value} in dataset {dataset}")
            continue
         # Extract the MOS value
         x_value = filtered_data['MOS'].values[0]
         for temporal_pooling_value in temporal_pooling_graph:
             # Filter the data for the current temporal_pooling value
            temporal_filtered_data = filtered_data[filtered_data['temporal_pooling'] == temporal_pooling_value]
            if temporal_filtered_data.empty:
                print(f"No data found for temporal pooling {temporal_pooling_value} in {pvs_value}")
                continue
            # Extract the feature value for the temporal filtered data
            feature_value = temporal_filtered_data[feature].values
            if feature_value == -1:
                continue
            # Get the color associated with the temporal_pooling value
            color = temporal_pooling_color_map[temporal_pooling_value]
            marker = temporal_pooling_marker_map.get(temporal_pooling_value, 'o')  # o is the Default marker
            # Create a scatter plot with the x_value and feature_value, using the corresponding color
            plt.scatter(x_value, feature_value, color=color, marker=marker, alpha=0.7)
            if temporal_pooling_value not in added_labels:
               labels.append(f"{temporal_pooling_value}")
               added_labels.add(temporal_pooling_value)
     
     
     plt.title(f"{x_column} vs {feature}")
     plt.xlabel(x_column)
     plt.ylabel(feature)
     # Set axis limits
     if "MOS" in axis_limits:
         plt.xlim(axis_limits["MOS"])  
     if feature in axis_limits:
         plt.ylim(axis_limits[feature])  
     plt.grid(True)
     plt.xticks(rotation=45)
     # display the legend
     plt.legend(title="Temporal Pooling", labels=labels, loc='center left', bbox_to_anchor=(1, 0.5))
     output_dir = os.path.join(pvs_path, "all_features", "all_pooling")
     os.makedirs(output_dir, exist_ok=True)
     output_file = os.path.join(output_dir, f"scatter_{feature}vsMOS.png")    
     
     plt.savefig(output_file, bbox_inches='tight')
     print(f"Graph saved: {output_file}")
     plt.close()
   
    for vmaf_model in vmaf_models:
        plt.figure(figsize=(10, 6))
        labels = []
        colors = []
        added_labels = set()
        for pvs_value in pvs:
            output_dir = f"{pvs_path}/all_vmaf_models/"
            if not os.path.exists(output_dir):
                os.makedirs(output_dir)
            filtered_data = data[data['Distorted_file_name'] == pvs_value]
            if filtered_data.empty:
                print(f"No data found for the pvs sequence: {pvs_value} in dataset {dataset}")
                continue
            x_value = filtered_data['MOS'].values[0]
            for temporal_pooling_value in ["harmonic_mean","geometric_mean","mean",]:
                temporal_filtered_data = filtered_data[filtered_data['temporal_pooling'] == temporal_pooling_value]
                if temporal_filtered_data.empty:
                    print(f"No data found for temporal pooling {temporal_pooling_value} in {pvs_value}")
                    continue
                model_value = temporal_filtered_data[vmaf_model].values
                if model_value == -1:
                    continue
                color = temporal_pooling_color_map[temporal_pooling_value]
                marker = temporal_pooling_marker_map.get(temporal_pooling_value, 'o')  # o is the Default marker
                plt.scatter(x_value, model_value, color=color, marker=marker, alpha=0.7)
                if temporal_pooling_value not in added_labels:
                    labels.append(f"{temporal_pooling_value}")
                    added_labels.add(temporal_pooling_value)

        plt.title(f"Dataset {dataset} : {vmaf_model} vs {x_column} ")
        plt.xlabel(x_column)
        plt.ylabel(vmaf_model)
        if "MOS" in axis_limits:
         plt.xlim(axis_limits["MOS"])  
        if vmaf_model in axis_limits:
         plt.ylim(axis_limits[vmaf_model]) 
        plt.grid(True)
        plt.xticks(rotation=45)
        plt.legend(title="Temporal Pooling", labels=labels, loc='center left', bbox_to_anchor=(1, 0.5))
        output_dir = os.path.join(pvs_path, "all_vmaf_models", "mhmgm")
        os.makedirs(output_dir, exist_ok=True)
        output_file = os.path.join(output_dir, f"scatter_{vmaf_model}vsMOS.png")    
        plt.savefig(output_file, bbox_inches='tight')
        print(f"Graph saved: {output_file}")
        plt.close()
        
    for vmaf_model in vmaf_models:
        plt.figure(figsize=(10, 6))
        labels = []
        colors = []
        added_labels = set()
        for pvs_value in pvs:
            output_dir = f"{pvs_path}/all_vmaf_models/"
            if not os.path.exists(output_dir):
                os.makedirs(output_dir)
            filtered_data = data[data['Distorted_file_name'] == pvs_value]
            if filtered_data.empty:
                print(f"No data found for the pvs sequence: {pvs_value} in dataset {dataset}")
                continue
            x_value = filtered_data['MOS'].values[0]
            for temporal_pooling_value in ["percentile_50","norm_lp1","norm_lp2","norm_lp3","mean"]:
                temporal_filtered_data = filtered_data[filtered_data['temporal_pooling'] == temporal_pooling_value]
                if temporal_filtered_data.empty:
                    print(f"No data found for temporal pooling {temporal_pooling_value} in {pvs_value}")
                    continue
                model_value = temporal_filtered_data[vmaf_model].values
                if model_value == -1:
                    continue
                color = temporal_pooling_color_map[temporal_pooling_value]
                marker = temporal_pooling_marker_map.get(temporal_pooling_value, 'o')  # o is the Default marker
                plt.scatter(x_value, model_value, color=color, marker=marker, alpha=0.7)
                if temporal_pooling_value not in added_labels:
                    labels.append(f"{temporal_pooling_value}")
                    added_labels.add(temporal_pooling_value)

        plt.title(f"Dataset {dataset} : {vmaf_model} vs {x_column} ")
        plt.xlabel(x_column)
        plt.ylabel(vmaf_model)
        if "MOS" in axis_limits:
         plt.xlim(axis_limits["MOS"])  
        if vmaf_model in axis_limits:
         plt.ylim(axis_limits[vmaf_model]) 
        plt.grid(True)
        plt.xticks(rotation=45)
        plt.legend(title="Temporal Pooling", labels=labels, loc='center left', bbox_to_anchor=(1, 0.5))
        output_dir = os.path.join(pvs_path, "all_vmaf_models", "mp50norms")
        os.makedirs(output_dir, exist_ok=True)
        output_file = os.path.join(output_dir, f"scatter_{vmaf_model}vsMOS.png")    
        plt.savefig(output_file, bbox_inches='tight')
        print(f"Graph saved: {output_file}")
        plt.close()
        
    

    
    # Percentile

    for vmaf_model in vmaf_models:
        plt.figure(figsize=(10, 6))
        labels = []
        added_labels = set()
    
        for pvs_value in pvs:
            output_dir = f"{percentile_path}/error_bar/"
            if not os.path.exists(output_dir):
                os.makedirs(output_dir) 
            
            filtered_data = data[data['Distorted_file_name'] == pvs_value]
            if filtered_data.empty:
                print(f"No data found for the pvs sequence: {pvs_value} in dataset {dataset}")
                continue
        
            x_value = filtered_data['MOS'].values[0]
        
            for temporal_pooling_value in ["mean", "percentile_50"]:
                temporal_filtered_data = filtered_data[filtered_data['temporal_pooling'] == temporal_pooling_value]
                temporal_pooling_lo = "percentile_5"
                percentile_5_data = filtered_data[filtered_data['temporal_pooling'] == temporal_pooling_lo]
                temporal_pooling_hi = "percentile_95"
                percentile_95_data = filtered_data[filtered_data['temporal_pooling'] == temporal_pooling_hi]
            
                if temporal_filtered_data.empty:
                    print(f"No data found for temporal pooling {temporal_pooling_value} in {pvs_value}")
                    continue
            
                y_value = temporal_filtered_data[vmaf_model].values
                if y_value == -1:
                    continue
            
                lo_value_percentile_5 = percentile_5_data[vmaf_model].values
                hi_value_percentile_95 = percentile_95_data[vmaf_model].values
                # Check if the values are valid (not NaN, not empty, and positive values)
                
                if len(lo_value_percentile_5) == 0 or len(hi_value_percentile_95) == 0:
                    print(f"Invalid percentile data for {temporal_pooling_value} in {pvs_value}")
                    continue

                # Ensure the error bars are non-negative and logical
                if lo_value_percentile_5 >= y_value or hi_value_percentile_95 <= y_value:
                    print(f"Invalid error bar values for {temporal_pooling_value} in {pvs_value}")
                    continue
            
                marker = temporal_pooling_marker_map.get(temporal_pooling_value, 'o')  
                if temporal_pooling_value == "mean":
                    color='blue'
                else:
                    color='red'
                plt.errorbar(
                x_value, 
                y_value, 
                yerr=[y_value - lo_value_percentile_5, hi_value_percentile_95 - y_value], 
                marker=marker,
                color=color, 
                )
                if temporal_pooling_value not in added_labels:
                    labels.append(temporal_pooling_value)  
                    added_labels.add(temporal_pooling_value)

        plt.title(f" {vmaf_model}  vs {x_column} vs with percentiles")
        plt.xlabel("MOS")
        plt.ylabel(vmaf_model)
        if "MOS" in axis_limits:
            plt.xlim(axis_limits["MOS"])
        if vmaf_model in axis_limits:
            plt.ylim(axis_limits[vmaf_model])
    
        plt.grid(True)
        plt.xticks(rotation=45)
        plt.legend(title="Temporal Pooling", labels=labels, loc='center left', bbox_to_anchor=(1, 0.5))  

    
        output_file = f"{percentile_path}/error_bar/combined_mean_median_{vmaf_model}.png"
        print(f"Graph saved: {output_file}")
        plt.savefig(output_file, bbox_inches='tight')
        plt.close()
    
    
    
    temporal_pooling_value="mean"
    labels=[]
    added_labels = set()  

    for vmaf_model_x in vmaf_models: 
        
       for vmaf_model_y in vmaf_models:  
           if vmaf_model_x == vmaf_model_y:  
               continue
           plt.figure(figsize=(10, 6))

           
           for pvs_value in pvs:
               output_dir = f"{meanvsmeanpath}/model_vs_model"
               if not os.path.exists(output_dir):
                   os.makedirs(output_dir) 
               filtered_data = data[data['Distorted_file_name'] == pvs_value]
               if filtered_data.empty:
                   print(f"No data found for the pvs sequence: {pvs_value}")
                   continue
               x_value = filtered_data['MOS'].values[0]

               mean_filtered_data = filtered_data[filtered_data['temporal_pooling'] == temporal_pooling_value]
               
               if mean_filtered_data.empty:
                   print(f"No data found for temporal pooling {temporal_pooling_value} in {pvs_value}")
                   continue 
               
               model_value_x=mean_filtered_data[vmaf_model_x].values[0]
               model_value_y=mean_filtered_data[vmaf_model_y].values[0]
               
               
               if model_value_y == -1 or model_value_x ==-1:
                   continue
                
               color_x = vmaf_color_map[vmaf_model_x]
               color_y = vmaf_color_map[vmaf_model_y]

               marker = 'o'  
               #plt.scatter(model_value_x, model_value_y, color=color, marker=marker, alpha=0.7)
               plt.scatter(x_value, [model_value_x], color=color_x,marker=marker)
               if vmaf_model_x not in added_labels:
                    labels.append(f"{vmaf_model_x}")
                    added_labels.add(vmaf_model_x)
               plt.scatter(x_value, [model_value_y], color=color_y,marker=marker)
               if vmaf_model_y not in added_labels:
                    labels.append(f"{vmaf_model_y}")
                    added_labels.add(vmaf_model_y)
               
               plt.title(f"Dataset {dataset} : {vmaf_model_x} vs {vmaf_model_y} for {temporal_pooling_value}")
               plt.xlabel("MOS")
               plt.ylabel(f"{vmaf_model_x} vs {vmaf_model_y}")
               if "MOS" in axis_limits:
                 plt.xlim(axis_limits["MOS"])  
               plt.ylim(0,100)
               plt.grid(True)
               plt.xticks(rotation=45)
               legend_elements = [
                Line2D([0], [0], marker=marker, color='w', markerfacecolor=color_x, markersize=10, label=vmaf_model_x),
                Line2D([0], [0], marker=marker, color='w', markerfacecolor=color_y, markersize=10, label=vmaf_model_y)
                ]
               plt.legend(handles=legend_elements, title="VMAF_MODELS", loc='center left', bbox_to_anchor=(1, 0.5))
              # plt.legend(title="VMAF_MODELS", labels=labels, loc='center left', bbox_to_anchor=(1, 0.5)) 
           
           output_file = f"{meanvsmeanpath}/model_vs_model/{vmaf_model_x}_vs_{vmaf_model_y}_{temporal_pooling_value}.png"
           #print(f"Graph saved: {output_file}")
           plt.savefig(output_file, bbox_inches='tight')
           plt.close()
           
        