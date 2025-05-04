import torch
import os
import sys

# Add YOLOv5 path to system
YOLOV5_PATH = os.path.join(os.path.dirname(__file__), 'yolov5')
sys.path.append(YOLOV5_PATH)

from models.experimental import attempt_load
from utils.torch_utils import select_device

# Load model
MODEL_PATH = os.path.join(os.path.dirname(__file__), 'best.pt')
device = select_device('')
model = attempt_load(MODEL_PATH, map_location=device)
model.eval()

# Example dummy function
def detect_objects(image_path):
    return [{"name": "helmet", "confidence": 0.92}]
