# 🧙‍♂️ Invisibility Cloak (OpenCV + Python)

A fun **Harry Potter–style Invisibility Cloak** 🪄 built using **Python & OpenCV**.  
The program detects a colored cloak (default: **red**) in front of your webcam and replaces it with the background, making the cloak — and you — appear invisible!  

---

## ✨ Features

* Real-time **video capture** using your webcam  
* **Color detection & masking** to detect cloak area  
* **Background replacement** to create invisibility effect  
* Option to **re-capture background** anytime (`b` key)  
* Simple & lightweight — runs on most systems  

---

## 🎮 Controls

* `b` → Capture/Re-capture background  
* `ESC` → Quit the program  

---

## 🧵 How it Works

1. Capture the **background frame** (without the cloak).  
2. Detect cloak color (HSV range for **red**).  
3. Create a mask for cloak area.  
4. Replace cloak region with background pixels.  
5. Merge the result → You appear invisible 👻.  

---


