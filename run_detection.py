import os
import shutil
import subprocess
from pathlib import Path
import logging

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def run_detection(image_path, model_path, output_path, imgsz):
    """
    Run YOLOv9 detection using detect.py script and save results in specified directory.
    """
    logging.info(f"Running detection on {image_path} using model {model_path}")
    # Command to run the detect.py script
    command = [
        'python', 'detect.py',
        '--weights', model_path,
        '--source', image_path,
        '--imgsz', str(imgsz),
        '--save-txt',  # Save results to text files
        '--project', output_path,
        '--name', 'detections',
        '--exist-ok'
    ]
    subprocess.run(command, check=True)
    logging.info(f"Detection complete for model {model_path}")

def main():
    # Paths to your images, model, and output directories
    image_dir = '/content/drive/MyDrive/processed_dataset1/images'
    model_path_c = '/content/drive/MyDrive/yolov9c_results/v0.0.2.20_fold_Sub017/weights/best.pt'
    model_path_e = '/content/drive/MyDrive/results_6fold/v0.0.2.40_fold_Sub017/weights/best.pt'
    output_dir_c = '/content/drive/MyDrive/detection_DIR/processed_images/yolov9c'
    output_dir_e = '/content/drive/MyDrive/detection_DIR/processed_images/yolov9e'
    imgsz = 320

    # Run detection for YOLOv9c
    run_detection(image_dir, model_path_c, output_dir_c, imgsz)
    # Run detection for YOLOv9e
    run_detection(image_dir, model_path_e, output_dir_e, imgsz)

    logging.info("Detection and formatting complete.")

if __name__ == "__main__":
    main()
