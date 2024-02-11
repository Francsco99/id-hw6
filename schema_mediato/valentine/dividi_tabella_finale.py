import os
import json

def split_json(input_file, output_dir, num_files=10):
    with open(input_file, 'r') as f:
        data = json.load(f)
    
    total_records = len(data)
    records_per_file = total_records // num_files
    
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
    
    for i in range(num_files):
        start_index = i * records_per_file
        end_index = (i + 1) * records_per_file if i < num_files - 1 else total_records
        
        output_file = os.path.join(output_dir, f"part_{i+1}.json")
        with open(output_file, 'w') as f_out:
            json.dump(data[start_index:end_index], f_out, indent=4)
        
        print(f"File {output_file} creato con successo.")

# Utilizzo:
ABS_PATH = os.path.dirname(os.path.abspath(__file__))
input_file_path = ABS_PATH+"/json/final_table.json"
output_directory =ABS_PATH+ "/json/parts"
split_json(input_file_path, output_directory)
