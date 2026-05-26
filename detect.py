import cv2
import os
from ultralytics import YOLO
import csv
from datetime import datetime

MODEL_PATH = r"runs\detect\train\weights\best.pt"
VIOLATION_DIR = "violations"
LOG_CSV = "violations.csv"

os.makedirs(VIOLATION_DIR, exist_ok=True)

model = YOLO(MODEL_PATH)

CLASS_NAMES = ["With Helmet", "Without Helmet"]


if not os.path.exists(LOG_CSV):
    with open(LOG_CSV, "w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(["timestamp", "class", "confidence", "filename"])

cap = cv2.VideoCapture(0)  

violation_count = 0

print("Starting video... Press 'q' to exit.")

while True:
    ret, frame = cap.read()
    if not ret:
        break

    results = model(frame)[0]
    annotated = frame.copy()

    for box in results.boxes:
        cls = int(box.cls[0])
        conf = float(box.conf[0])

        x1, y1, x2, y2 = map(int, box.xyxy[0])

        label = f"{CLASS_NAMES[cls]} {conf:.2f}"

        if CLASS_NAMES[cls] == "With Helmet":
            color = (0, 255, 0)  
        else:
            color = (0, 0, 255)  

           
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"violation_{timestamp}_{violation_count}.jpg"
            cv2.imwrite(os.path.join(VIOLATION_DIR, filename), annotated)

            
            with open(LOG_CSV, "a", newline="") as f:
                writer = csv.writer(f)
                writer.writerow([timestamp, "No Helmet", f"{conf:.2f}", filename])

            violation_count += 1

            
            try:
                import winsound
                winsound.Beep(1000, 150)
            except:
                pass

        
        cv2.rectangle(annotated, (x1, y1), (x2, y2), color, 2)
        cv2.putText(annotated, label, (x1, y1 - 10),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.6, color, 2)

    
    cv2.putText(annotated, f"Violations: {violation_count}", (10, 30),
                cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 3)

    cv2.imshow("Helmet Detection CCTV", annotated)

    if cv2.waitKey(1) & 0xFF == ord("q"):
        break

cap.release()
cv2.destroyAllWindows()
