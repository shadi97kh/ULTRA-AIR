# ULTRA-AIR: Ultrasound Landmark Tracking for Real-Time Anatomical Airway Identification and Reliability Check

This repository contains the official code and experimental results for the paper:

> Z. Khodagholi, J. Sun, N. Awad, A. Vankayalapati, G. R. Dion and L. J. Brattain,
> **"ULTRA-AIR: Ultrasound Landmark Tracking for Real-Time Anatomical Airway Identification and Reliability Check,"**
> *2024 IEEE 20th International Conference on Body Sensor Networks (BSN)*, Chicago, IL, USA, 2024, pp. 1-4.
> doi: [10.1109/BSN63547.2024.10780557](https://doi.org/10.1109/BSN63547.2024.10780557)

ULTRA-AIR is a YOLOv9-based pipeline for real-time identification of airway landmarks in neck ultrasound, with an epistemic-uncertainty reliability check based on a Gaussian Mixture Model. It is designed to support safer percutaneous tracheostomy and other airway-management procedures by flagging predictions the model is not confident about.

**Keywords:** Adaptive Optimization, Airway Management, Epistemic Uncertainty, Gaussian Mixture Model, Neck Ultrasound, Percutaneous Tracheostomy, Trustworthy AI, YOLOv9.

## Overview

The pipeline detects four anatomical landmarks in neck ultrasound images (see [data.yaml](data.yaml)):

| Class ID | Landmark          |
| -------- | ----------------- |
| 0        | Thyroid-cartilage |
| 1        | Strap-muscle      |
| 2        | Tracheal-ring     |
| 3        | Thyroid-gland     |

Models are trained and evaluated with **7-fold subject-wise cross-validation** (one subject held out per fold) and the per-prediction epistemic uncertainty is post-processed with a Gaussian Mixture Model to derive a reliability check on each detection.

## Repository Layout

- [train.py](train.py) — YOLOv9 training entry point.
- [val.py](val.py) — Validation / evaluation script.
- [detect.py](detect.py) — Inference script; also writes per-detection confidence and epistemic-uncertainty values.
- [plot_uncertainty.py](plot_uncertainty.py) — Aggregates `*_uncertainties.txt` files produced by `detect.py` and plots confidence vs. uncertainty (with optional GMM threshold line).
- [export.py](export.py) — Model export utilities (ONNX, TorchScript, etc.).
- [benchmarks.py](benchmarks.py) — Speed/accuracy benchmarks.
- [data.yaml](data.yaml) — Dataset configuration with the four airway landmark classes.
- [models/](models/) — YOLOv9 model definitions and configs.
- [utils/](utils/) — Shared utilities, including the `calculate_uncertainty` helper used by `detect.py`.
- [datasets/](datasets/) — `train` / `val` / `test` splits used by the pipeline.
- [Final_Results/](Final_Results/) — Per-fold results (`v0.0.2.20_fold_Sub011` … `Sub017`), confusion matrices, PR curves, and certainty/uncertainty scatter plots reported in the paper.
- [fold_generator.ipynb](fold_generator.ipynb) — Generates the 7 subject-wise folds.
- [yolo_pipeline.ipynb](yolo_pipeline.ipynb) — End-to-end pipeline notebook.
- [train_yolov9_object_detection_on_neck_ultrasound_7fold.ipynb](train_yolov9_object_detection_on_neck_ultrasound_7fold.ipynb) — Combined 7-fold training notebook.
- [tutorial.ipynb](tutorial.ipynb) — Walkthrough.

## Installation

```bash
git clone https://github.com/shadi97kh/UltraSound-Project.git
cd UltraSound-Project
pip install -r requirements.txt
```

A CUDA-capable GPU is recommended for training. PyTorch ≥ 1.7 is required (see [requirements.txt](requirements.txt)).

## Usage

### 1. Generate the 7 folds

Open [fold_generator.ipynb](fold_generator.ipynb) and run it to produce subject-wise splits under `datasets/`.

### 2. Train

Train a single fold (replace `<fold>` and adjust hyperparameters as needed):

```bash
python train.py \
    --data data.yaml \
    --cfg models/detect/yolov9-c.yaml \
    --weights '' \
    --img 640 \
    --epochs 100 \
    --name fold_<fold>
```

To reproduce the full 7-fold experiment from the paper, run [train_yolov9_object_detection_on_neck_ultrasound_7fold.ipynb](train_yolov9_object_detection_on_neck_ultrasound_7fold.ipynb).

### 3. Validate

```bash
python val.py --data data.yaml --weights runs/train/fold_<fold>/weights/best.pt --img 640
```

### 4. Inference with reliability check

`detect.py` writes per-detection confidence and epistemic uncertainty alongside the standard YOLO output:

```bash
python detect.py \
    --weights runs/train/fold_<fold>/weights/best.pt \
    --source path/to/ultrasound/images \
    --data data.yaml \
    --save-txt --save-conf
```

Then aggregate uncertainty across a run and plot confidence vs. uncertainty (optionally with a GMM-derived threshold):

```bash
python plot_uncertainty.py --dir runs/detect/exp --threshold 0.15
```

## Results

Per-fold and aggregate results referenced in the paper — including the precision-recall curves, confusion matrices, and confidence/uncertainty scatter plots — are stored in [Final_Results/](Final_Results/).

## Citation

If you use this code or build on this work, please cite:

```bibtex
@INPROCEEDINGS{10780557,
  author    = {Khodagholi, Z. and Sun, J. and Awad, N. and Vankayalapati, A. and Dion, G. R. and Brattain, L. J.},
  booktitle = {2024 IEEE 20th International Conference on Body Sensor Networks (BSN)},
  title     = {ULTRA-AIR: Ultrasound Landmark Tracking for Real-Time Anatomical Airway Identification and Reliability Check},
  year      = {2024},
  pages     = {1--4},
  address   = {Chicago, IL, USA},
  doi       = {10.1109/BSN63547.2024.10780557}
}
```

## License

Released under the [MIT License](LICENSE). The detection code builds on the YOLOv9 / YOLOv5 codebase, which is distributed under its own license; please consult upstream for those terms.
