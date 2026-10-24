# 🚧 AI-Based Pothole Detection and Road Damage Monitoring

An AI-powered computer vision system that detects potholes in road images and videos using **YOLO11** and **OpenCV**. The project aims to support automated road inspection by identifying potholes, visualizing their locations within images, and evaluating detection performance.

> **Current status:** Pothole detection and model evaluation are implemented. GPS-based location tagging, severity estimation, and RC car integration are planned extensions.

---

## 📌 Overview

Potholes pose risks to road safety, vehicle condition, and traffic efficiency. Traditional road inspections often require substantial manual effort and can be difficult to scale.

This project explores how deep learning and computer vision can automate part of the road inspection process.

The system processes road images or video frames, detects potholes using YOLO11, and displays detections with bounding boxes and confidence scores.

The longer-term goal is to develop a road damage monitoring system that can support road maintenance planning.

## ✨ Features

* **Pothole detection:** Detect potholes using a trained YOLO11 object detection model.
* **Image and video processing:** Support road imagery and video-based inspection workflows.
* **Detection visualization:** Display bounding boxes and confidence scores.
* **Dataset preparation:** Prepare pothole datasets for model training and evaluation.
* **Model evaluation:** Measure performance using precision, recall, mAP@50, and mAP@50–95.
* **Modular development:** Maintain separate scripts for dataset inspection, preparation, visualization, and model training.

## 🧠 System Architecture

```text
       Road Camera / Image / Video
                    |
                    v
          Image / Frame Input
                    |
                    v
             OpenCV Processing
                    |
                    v
           YOLO11 Object Detector
                    |
                    v
          Pothole Detection Results
                    |
           +--------+--------+
           |                 |
           v                 v
      Bounding Boxes    Confidence Scores
           |                 |
           +--------+--------+
                    |
                    v
          Detection Visualization
                    |
                    v
       Road Damage Monitoring Report
                    |
                    v
       Future: GPS / Severity Analysis
```

GPS tagging and severity analysis are planned extensions and are not included in the current reported model evaluation.

## 🛠️ Technology Stack

| Technology     | Purpose                                   |
| -------------- | ----------------------------------------- |
| Python         | Core programming language                 |
| YOLO11         | Pothole object detection                  |
| Ultralytics    | Model training, inference, and evaluation |
| OpenCV         | Image and video processing                |
| PyTorch        | Deep learning framework                   |
| Git and GitHub | Version control and collaboration         |

## 📂 Project Structure

```text
PotHole-Detection/
├── src/
│   └── data/
│       ├── audit_samples.py
│       ├── dataset_inspect.py
│       ├── inspect_classes.py
│       ├── model_train.py
│       ├── prepare_all_country_potholes.py
│       └── visualize_samples.py
├── data/                 # Local datasets; not tracked by Git
├── models/               # Local trained weights; not tracked by Git
├── runs/                 # Training and evaluation outputs
├── requirements.txt
├── .gitignore
└── README.md
```

The exact contents of the source directory may evolve as development con
