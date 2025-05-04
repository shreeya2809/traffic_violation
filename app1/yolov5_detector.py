import torch
import os

# Load YOLOv5 model
MODEL_PATH = os.path.join(os.path.dirname(__file__), "best.pt")
model = torch.hub.load('./yolov5', 'custom', path=MODEL_PATH, source='local')

def detect_objects(image_path):
    results = model(image_path)
    results.save(save_dir="media/results")
    return results.pandas().xyxy[0].to_dict(orient="records")
