# 🚧 AI-Based Pothole Detection and Road Damage Monitoring

An AI-powered computer vision system for detecting potholes in road images and video using **YOLO11**. The project aims to automate road inspection and provide information that can later be used for road-condition monitoring and maintenance prioritization.

---

## 📌 Project Overview

Potholes are a common road-safety problem that can cause vehicle damage, accidents, and traffic disruptions. Traditional road inspection is mostly manual, time-consuming, and difficult to scale.

This project aims to develop an automated pothole detection system using:

- 📷 Camera / road images or video
- 🤖 YOLO11 object detection
- 👁️ OpenCV for image and video processing
- 📊 Model evaluation metrics
- 📍 GPS-based location tagging *(planned/integration stage)*
- 🚗 RC car-based road inspection platform *(planned/integration stage)*

The system will detect potholes from road images/video and draw bounding boxes around the detected regions.

---

## 🎯 Objectives

The main objectives of this project are:

1. Detect potholes automatically using deep learning.
2. Train a YOLO11 model on a pothole dataset.
3. Process road images and videos using OpenCV.
4. Evaluate the model using standard object-detection metrics.
5. Display detected potholes with confidence scores and bounding boxes.
6. Associate detected potholes with geographical locations using GPS.
7. Develop a low-cost prototype for automated road inspection.

---

## 🧠 System Architecture

```text
                 ┌─────────────────────┐
                 │   Road Camera       │
                 │ Image / Video Input │
                 └──────────┬──────────┘
                            │
                            ▼
                 ┌─────────────────────┐
                 │       OpenCV        │
                 │ Preprocessing/Input │
                 └──────────┬──────────┘
                            │
                            ▼
                 ┌─────────────────────┐
                 │      YOLO11         │
                 │   Object Detector   │
                 └──────────┬──────────┘
                            │
                  ┌─────────┴─────────┐
                  │                   │
                  ▼                   ▼
          ┌──────────────┐     ┌──────────────┐
          │  Pothole     │     │  Confidence  │
          │  Bounding Box│     │    Score     │
          └──────┬───────┘     └──────────────┘
                 │
                 ▼
        ┌────────────────────┐
        │ Severity / Analysis│
        └─────────┬──────────┘
                  │
                  ▼
        ┌────────────────────┐
        │ GPS Location Tag   │
        │    (Planned)       │
        └─────────┬──────────┘
                  │
                  ▼
        ┌────────────────────┐
        │ Road Damage Report │
        │ / Visualization    │
        └────────────────────┘
