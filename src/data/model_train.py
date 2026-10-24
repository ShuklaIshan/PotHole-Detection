from pathlib import Path
import yaml
from ultralytics import YOLO

dataset = Path("/kaggle/input/YOUR-DATASET-SLUG")


data_config = {
    "path": str(dataset),
    "train": "images/train",
    "val": "images/val",
    "test": "images/test",
    "nc": 1,
    "names": {0: "pothole"},
}

yaml_path = Path("/kaggle/working/all_country_pothole.yaml")
yaml_path.write_text(yaml.safe_dump(data_config, sort_keys=False))

model = YOLO("yolo11n.pt")

results = model.train(
    data=str(yaml_path),
    epochs=50,
    imgsz=640,
    batch=16,
    patience=10,
    device=0,
    project="/kaggle/working/runs",
    name="all_country_pothole",
    pretrained=True,
)