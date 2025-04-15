# 🚦 Smart Traffic Signal Controller using AI & Sensor Simulation

An AI-powered, real-time traffic signal system that dynamically prioritizes traffic flow using object detection and intelligent lane decision-making. This project is designed to simulate and optimize modern urban traffic using computer vision and adaptive signaling logic.

---

## 🔍 Overview

This system captures live traffic footage using a webcam, detects vehicles via *YOLOv8*, and intelligently manages signal transitions based on:
- Vehicle *count* and *type*
- Presence of *emergency vehicles*
- Lane *priority scores*

---

## ⚙ Features

- ✅ Real-time *vehicle detection* with YOLOv8
- 🚨 Emergency vehicle *priority handling*
- 📊 Adaptive *lane scoring* based on traffic density and vehicle type
- 🟡 Intelligent *yellow light logic* to avoid redundant switching
- ⏱ Clean *countdown timer* display
- 🔁 Smooth *green → yellow → green* phase transitions
- 🧠 Dynamic *decision-making* loop

---

## 🧰 Tech Stack

| Tool/Library | Purpose                  |
|--------------|--------------------------|
| Python 3     | Core development         |
| OpenCV       | Video stream & UI overlay |
| YOLOv8       | Real-time object detection |
| Tkinter      | (Optional) GUI dashboard |
| NumPy & time | Lane logic & timers      |

---

## 📽 How It Works

1. *Capture Frame:* Webcam provides real-time traffic input.
2. *Detection:* YOLOv8 identifies vehicle types and positions.
3. *Lane Mapping:* Vehicles are mapped to North, South, East, or West based on location.
4. *Lane Scoring:* Each lane gets a score based on:
   - Emergency vehicles: +1000
   - Bus: +3 per unit
   - Truck: +2 per unit
   - Others: +1 per unit
5. *Signal Control:*
   - The lane with the highest score gets the *green light*.
   - A *yellow light* signals transition only if the lane is about to switch.

---

## 🚦 Signal Logic Snapshot

```text
Green Phase: Active lane turns green for 5-20s (based on traffic).
Yellow Phase: Only triggers if the next lane is different.
Cycle continues in real-time without repeated switching.
