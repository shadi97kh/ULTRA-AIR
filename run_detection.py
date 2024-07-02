import os
import shutil
import subprocess
from pathlib import Path
import logging

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def run_detection(image_path, model_path, output_path):
    """
    Run YOLOv9 detection using detect.py script and save results in specified directory.
    """
    logging.info(f"Running detection on {image_path} using model {model_path}")
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
    logging.info(f"Detection complete for model {model_path}")

def move_and_format_results(src_folder, dest_folder):
    """
    Move detection results from source folder to destination folder and format the text files.
    """
    os.makedirs(dest_folder, exist_ok=True)
    logging.info(f"Formatting results from {src_folder} to {dest_folder}")

    for result_txt in Path(src_folder).rglob('*.txt'):
        if result_txt.stem.endswith('_uncertainties'):
            continue  # Skip the separate uncertainty files

        with open(result_txt, 'r') as f:
            lines = f.readlines()
        
        new_lines = []
        for line in lines:
            parts = line.strip().split()
            class_id = parts[0]
            bbox = parts[1:]  # Extract bounding box coordinates
            new_lines.append(f"{class_id} {' '.join(bbox)}\n")

        uncertainty_path = result_txt.parent / f"{result_txt.stem}_uncertainties.txt"
        if uncertainty_path.exists():
            with open(uncertainty_path, 'r') as f_unc:
                uncertainties = f_unc.readlines()
            for idx, line in enumerate(new_lines):
                if idx < len(uncertainties):
                    line = line.strip() + f" {uncertainties[idx].strip().split()[-1]}\n"
                    new_lines[idx] = line

        image_name = result_txt.stem
        dest_txt_path = os.path.join(dest_folder, f"{image_name}.txt")
        dest_img_path = os.path.join(dest_folder, f"{image_name}.png")  # Save images as PNG

        with open(dest_txt_path, 'w') as f:
            f.writelines(new_lines)
        
        src_img_path = str(result_txt).replace('.txt', '.jpg')  # Assuming the images are saved as JPG
        if os.path.exists(src_img_path):
            shutil.copy(src_img_path, dest_img_path)
    
    logging.info(f"Formatting complete for results in {src_folder}")

def main():
    # Paths to your images, model, and output directories
    image_dir = '/content/drive/MyDrive/test5/images'
    model_path_c = '/content/drive/MyDrive/yolov9c_results/v0.0.2.20_fold_Sub016/weights/best.pt'
    model_path_e = '/content/drive/MyDrive/results_6fold/v0.0.2.40_fold_Sub016/weights/best.pt'
    output_dir_c = '/content/drive/MyDrive/detection_DIR/test5/yolov9c'
    output_dir_e = '/content/drive/MyDrive/detection_DIR/test5/yolov9e'

    # Run detection for YOLOv9c
    run_detection(image_dir, model_path_c, output_dir_c)
    # Run detection for YOLOv9e
    run_detection(image_dir, model_path_e, output_dir_e)

    # Move and format the results
    formatted_results_dir_c = os.path.join(output_dir_c, 'formatted_results')
    formatted_results_dir_e = os.path.join(output_dir_e, 'formatted_results')
    move_and_format_results(output_dir_c, formatted_results_dir_c)
    move_and_format_results(output_dir_e, formatted_results_dir_e)

    logging.info("Detection and formatting complete.")

if __name__ == "__main__":
    main()
