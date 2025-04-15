import cv2
import time
from collections import defaultdict
from ultralytics import YOLO
from signal_controller import get_priority_lane, draw_signal

# Load YOLOv8 model
model = YOLO('yolov8n.pt')

# Start camera
cap = cv2.VideoCapture(0)

# Configurable yellow light duration
YELLOW_DURATION = 3

# Signal control state
active_lane = None
next_lane = None
green_duration = 0
phase_start_time = time.time()
current_phase = "green"

while True:
    ret, frame = cap.read()
    if not ret:
        break

    results = model(frame)[0]

    # Lane-wise vehicle count
    vehicle_counts = {
        "North": defaultdict(int),
        "South": defaultdict(int),
        "East": defaultdict(int),
        "West": defaultdict(int)
    }

    for box in results.boxes:
        cls_id = int(box.cls[0])
        class_name = model.names[cls_id]
        x_center = (box.xyxy[0][0] + box.xyxy[0][2]) / 2

        if x_center < frame.shape[1] / 4:
            lane = "North"
        elif x_center < frame.shape[1] / 2:
            lane = "South"
        elif x_center < 3 * frame.shape[1] / 4:
            lane = "East"
        else:
            lane = "West"

        vehicle_counts[lane][class_name] += 1

    # Time tracking
    current_time = time.time()
    elapsed = current_time - phase_start_time

    if current_phase == "green":
        if elapsed >= green_duration:
            # Get next priority lane
            new_lane, new_duration, _ = get_priority_lane(vehicle_counts)

            if new_lane != active_lane:
                # Only switch if lane changes
                current_phase = "yellow"
                next_lane = new_lane
                phase_start_time = current_time
            else:
                # Stay on the same lane, refresh green
                green_duration = new_duration
                phase_start_time = current_time

    elif current_phase == "yellow":
        if elapsed >= YELLOW_DURATION:
            # Finalize the switch
            active_lane = next_lane
            active_lane, green_duration, _ = get_priority_lane(vehicle_counts)  # Get fresh duration
            current_phase = "green"
            phase_start_time = current_time

    # Initialization on first loop
    if active_lane is None:
        active_lane, green_duration, _ = get_priority_lane(vehicle_counts)
        current_phase = "green"
        phase_start_time = current_time   
     # Draw traffic signal light
    if current_phase == "green":
        remaining_time = max(0, int(green_duration - (time.time() - phase_start_time)))
        draw_signal(frame, active_lane, remaining_time)
    else:
        draw_signal(frame, active_lane, 0)
        cv2.putText(frame, "YELLOW: Switching to " + next_lane,
                    (10, frame.shape[0] - 20),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 255), 2)

    # Display output
    cv2.imshow("Smart Traffic AI", frame)

    # Quit key
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()