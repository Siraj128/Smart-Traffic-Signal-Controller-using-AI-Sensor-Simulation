import cv2

def draw_signal(frame, lane, duration):
    # Define base colors
    color_map = {
        'North': (0, 0, 255),  # Red
        'South': (0, 0, 255),
        'East': (0, 0, 255),
        'West': (0, 0, 255)
    }

    if duration > 0:
        color_map[lane] = (0, 255, 0)  # Green if active
    else:
        color_map[lane] = (0, 255, 255)  # Yellow if transitioning

    x, y = 10, 10
    for ln in ['North', 'South', 'East', 'West']:
        color = color_map[ln]
        cv2.rectangle(frame, (x, y), (x + 120, y + 40), color, -1)
        cv2.putText(frame, f"{ln}", (x + 5, y + 25),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 255), 2)
        y += 50

    label_color = (0, 255, 0) if duration > 0 else (0, 255, 255)
    cv2.putText(frame, f"LIGHT: {lane} - {duration}s",
                (10, y + 30), cv2.FONT_HERSHEY_SIMPLEX,
                0.7, label_color, 2)


def get_priority_lane(vehicle_counts):
    emergency_keywords = ['ambulance', 'fire truck', 'police']

    max_lane = None
    max_score = -1

    for lane, vehicles in vehicle_counts.items():
        score = 0
        for vehicle_type, count in vehicles.items():
            if any(keyword in vehicle_type.lower() for keyword in emergency_keywords):
                score += 1000
            elif "bus" in vehicle_type.lower():
                score += count * 3
            elif "truck" in vehicle_type.lower():
                score += count * 2
            else:
                score += count * 1

        if score > max_score:
            max_score = score
            max_lane = lane

    if max_score >= 1000:
        green_duration = 20
    elif max_score >= 10:
        green_duration = 15
    elif max_score >= 5:
        green_duration = 10
    else:
        green_duration = 5

    return max_lane, green_duration, max_score  # 👈 Also return score