import os
import shutil
import subprocess
from pathlib import Path
import json

def run_detection(image_path, model_path, output_path):
    """
    Run YOLOv9 detection using detect.py script and save results in specified directory.
    """
    # Command to run the detect.py script
    command = [
        'python', 'detect.py',
        '--weights', model_path,
        '--source', image_path,
        '--save-txt',  # Save results to text files
        '--project', output_path,
        '--name', 'detections',
        '--exist-ok'
    ]
    subprocess.run(command, check=True)

def move_and_format_results(src_folder, dest_folder):
    """
    Move detection results from source folder to destination folder and format the text files.
    """
    os.makedirs(dest_folder, exist_ok=True)
    
    for result_txt in Path(src_folder).rglob('*.txt'):
        with open(result_txt, 'r') as f:
            lines = f.readlines()
        
        new_lines = []
        for line in lines:
            parts = line.strip().split()
            class_id = parts[0]
            bbox = parts[1:]  # Extract bounding box coordinates
            new_lines.append(f"{class_id} {' '.join(bbox)}\n")
        
        image_name = result_txt.stem
        dest_txt_path = os.path.join(dest_folder, f"{image_name}.txt")
        dest_img_path = os.path.join(dest_folder, f"{image_name}.jpg")

        with open(dest_txt_path, 'w') as f:
            f.writelines(new_lines)
        
        src_img_path = str(result_txt).replace('.txt', '.png')
        if os.path.exists(src_img_path):
            shutil.copy(src_img_path, dest_img_path)

def main():
    # Paths to your images, model, and output directories
    image_dir = '/content/drive/MyDrive/OneDrive_1_6-23-2024/11_053_1TCC1.mov'
    model_path_c = '/content/drive/MyDrive/yolov9c_results/v0.0.2.20_fold_Sub016/weights/best.pt'
    model_path_e = '/content/drive/MyDrive/results_6fold/v0.0.2.40_fold_Sub016/weights/best.pt'
    output_dir_c = '/content/drive/MyDrive/detection_DIR/yolov9c'
    output_dir_e = '/content/drive/MyDrive/detection_DIR/yolov9e'

    # Run detection for YOLOv9c
    run_detection(image_dir, model_path_c, output_dir_c)
    # Run detection for YOLOv9e
    run_detection(image_dir, model_path_e, output_dir_e)

    # Move and format the results
    formatted_results_dir_c = os.path.join(output_dir_c, 'formatted_results')
    formatted_results_dir_e = os.path.join(output_dir_e, 'formatted_results')
    move_and_format_results(output_dir_c, formatted_results_dir_c)
    move_and_format_results(output_dir_e, formatted_results_dir_e)

    print("Detection and formatting complete.")

if __name__ == "__main__":
    main()
