import os
import subprocess
import sys

if len(sys.argv) < 6:
    print("You need to call like analyze_results_script <result_dir> <mos_dir> <dataset_name> <use_libvmaf> <use_essim> ")
    sys.exit(1)

result_dir = sys.argv[1]
mos_dir=sys.argv[2]
dataset = sys.argv[3]
use_libvmaf=sys.argv[4]
use_essim=sys.argv[5]

print(result_dir)
print(mos_dir)
print(dataset)
print(use_libvmaf)
print(use_essim)


vmaf_dir = os.path.join(result_dir,dataset, "vmaf_results")
essim_dir = os.path.join(result_dir,dataset,"essim_results")

for filename in os.listdir(vmaf_dir):
    vmaf_path = os.path.join(vmaf_dir, filename)
    
    if os.path.isfile(vmaf_path):
        use_libvmaf = True  
        
        file_name = os.path.basename(vmaf_path)
        file_name_no_ext = os.path.splitext(file_name)[0]
        
        parts = file_name_no_ext.split('__')
    
        #print(f"NFilename: {file_name}")
        #for i, part in enumerate(parts):
        #    print(f"Indice {i}: {part}")
            
        if len(parts) >= 10:
            dataset = parts[1]  
            original_video = parts[2]  
            distorted_video=parts[3]
            width_old, height_old = parts[4].split('x')  
            bitrate = parts[5]  
            video_codec = parts[6] 
            fps = parts[7]  
            duration=parts[8]
            model_version = parts[9]  
            print(model_version)
            
            if "resized" in file_name:
                if len(parts) >= 11:
                    dimensions = os.path.splitext(file_name)[0].split('_')[-1]  
                    width_new, height_new = map(int, dimensions.split('x'))  
                else:
                    width_new, height_new = width_old, height_old  
            else:
                width_new, height_new = width_old, height_old
            
        else:
            print(f"File {file_name} format is wrong")
        command_vmaf = f"python3 analyze.py {dataset} {width_new} {height_new} {bitrate} {video_codec} {model_version} {result_dir} {original_video} {distorted_video} {width_old} {height_old} {fps} {duration} {mos_dir} {use_libvmaf} {use_essim}"
        print(command_vmaf)
        subprocess.run(command_vmaf, shell=True, check=True)

        
for filename in os.listdir(essim_dir):
    essim_path = os.path.join(essim_dir, filename)
    
    if os.path.isfile(essim_path):
        use_essim = True  
        file_name = os.path.basename(essim_path)
        file_name_no_ext = os.path.splitext(file_name)[0]

        
        parts = file_name_no_ext.split('__')
        
        print(f"Nome del file: {file_name}")
        
        if len(parts) >= 11:
            dataset = parts[1] 
            original_video = parts[2]  
            distorted_video=parts[3]
            width_old, height_old = parts[4].split('x') 
            bitrate = parts[5]  
            video_codec = parts[6]  
            fps = parts[7]  
            duration=parts[8]
            model_version = parts[9]  
            essim_params_string=parts[10]
            
            if "resized" in file_name:
                if len(parts) >= 12:
                    dimensions = os.path.splitext(file_name)[0].split('_')[-1]  
                    width_new, height_new = map(int, dimensions.split('x'))  
                else:
                    print(f"File {file_name}: format is wrong ")
                    width_new, height_new = width_old, height_old 
            else:
                width_new, height_new = width_old, height_old
        else:
            print(f"File {file_name} format is wrong")
        command_essim = f"python3 analyze.py {dataset} {width_new} {height_new} {bitrate} {video_codec} {model_version} {result_dir} {original_video} {distorted_video} {width_old} {height_old} {fps} {duration} {mos_dir} {use_libvmaf} {use_essim} {essim_params_string}"
        print(command_essim)
        subprocess.run(command_essim, shell=True, check=True)
        
