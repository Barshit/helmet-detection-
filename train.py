from ultralytics import YOLO
import torch
import multiprocessing

def run_train():
    print("CUDA available:", torch.cuda.is_available())
    print("Device:", torch.cuda.get_device_name(0) if torch.cuda.is_available() else "CPU")

    model = YOLO("yolov8n.pt")
    model.train(
        data="data.yaml",
        epochs=30,
        imgsz=640,
        batch=8,
        device=0,
        workers=4  # you can lower this if you still get issues
    )

if __name__ == "__main__":
    # on Windows, safe to call freeze_support() for spawn method
    multiprocessing.freeze_support()
    run_train()
