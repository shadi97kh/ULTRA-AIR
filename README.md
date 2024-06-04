# YOLOv9 Object Detection on Neck Ultrasound - 7 Fold Training

This repository contains the code and results for training the YOLOv9 object detection model on neck ultrasound images using a 7-fold cross-validation approach. The project is a combination of the `fold generator` and `pipeline` folders, integrating their functionalities to achieve robust training and evaluation.

## Files and Folders

- `Graphs/`
  - `PR curve 7 fold.png`: Precision-Recall curve for the 7 folds.
  - `PR curve class 2.png`: Precision-Recall curve for class 2.
  - `PR curve class 4.png`: Precision-Recall curve for class 4.
  - `PR curve class 1.png`: Precision-Recall curve for class 1.
  - `PR curve class 0.png`: Precision-Recall curve for class 0.
  - `PR for 7fold and 4classes.png`: Combined Precision-Recall curve for 7 folds and 4 classes.
  - `PR for each class across 7 folds.png`: Precision-Recall curve for each class across 7 folds.
  - `val_box_loss.png`: Validation box loss curve.
- `README.md`: This readme file.
- `results for 7 fold/`: Folder containing the results for each of the 7 folds.
- `train_yolov9_object_detection_on_neck_ultrasound_7fold.ipynb`: Jupyter notebook used for training the YOLOv9 model.

## Project Overview

This project aims to develop an object detection model to identify various structures in neck ultrasound images. By using YOLOv9, a state-of-the-art object detection algorithm, the model achieves high accuracy and efficiency.

### Key Components

- **Fold Generator**: This component generates the 7-fold cross-validation splits to ensure robust model evaluation.
- **Pipeline**: This component handles the data preprocessing, model training, and evaluation pipeline.

### Precision-Recall Curves

The precision-recall curves for each class and each fold are saved in the `Graphs` folder. These graphs provide insight into the performance of the model across different classes and folds.

### Metrics

For each fold, the precision, recall, and F1-score for each class are calculated and stored. The average precision, recall, and F1-score across all folds and classes are also provided.

## Instructions

To run the training and evaluation scripts, follow these steps:

1. **Clone this repository:**
    ```bash
    git clone https://github.com/shadi97kh/UltraSound-Project.git
    cd UltraSound-Project
    ```

2. **Ensure you have the required dependencies installed.** You can use the `requirements.txt` file to install them:
    ```bash
    pip install -r requirements.txt
    ```

3. **Open the Jupyter notebook** `train_yolov9_object_detection_on_neck_ultrasound_7fold.ipynb` and run all cells to start the training process.

### Running the Training Pipeline

The provided Jupyter notebook contains all the necessary code to preprocess the data, generate the 7-fold splits, train the YOLOv9 model, and evaluate its performance. The key steps include:

1. **Data Loading and Preprocessing**: Load the neck ultrasound images and corresponding annotations.
2. **Fold Generation**: Generate 7-fold cross-validation splits using the fold generator.
3. **Model Training**: Train the YOLOv9 model on each fold.
4. **Evaluation**: Calculate precision, recall, and F1-score for each class and fold, and plot the precision-recall curves.

## Syncing Changes with GitHub

To sync changes with GitHub, use the following commands:

1. **Commit your changes:**
    ```bash
    git add .
    git commit -m "Your commit message"
    ```

2. **Pull the latest changes:**
    ```bash
    git pull --rebase
    ```

3. **Push your changes:**
    ```bash
    git push origin main
    ```

