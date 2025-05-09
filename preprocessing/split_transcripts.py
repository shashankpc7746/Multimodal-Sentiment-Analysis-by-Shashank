import os

input_dir = 'data/mini_dataset/raw_transcripts'  # Folder with .annotprocessed files
output_dir = 'data/mini_dataset/segmented_transcripts'  # Where to save split files

os.makedirs(output_dir, exist_ok=True)

for filename in sorted(os.listdir(input_dir)):
    if filename.endswith('.annotprocessed'):
        base_name = filename.replace('.annotprocessed', '')
        input_path = os.path.join(input_dir, filename)
        
        with open(input_path, 'r', encoding='utf-8') as f:
            lines = f.readlines()
        
        for i, line in enumerate(lines, 1):
            # Remove "N_DELIM_" prefix if present
            if '_DELIM_' in line:
                _, line = line.split('_DELIM_', 1)
            output_filename = f"{base_name}_{i}.txt"
            output_path = os.path.join(output_dir, output_filename.strip())
            
            with open(output_path, 'w', encoding='utf-8') as out_f:
                out_f.write(line.strip())
