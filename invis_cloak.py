import cv2
import numpy as np
import time

# --- Function for nothing (needed for trackbars) ---
def nothing(x):
    pass

# --- Setup camera ---
cap = cv2.VideoCapture(0)
if not cap.isOpened():
    print("❌ Camera not accessible. Try index 1 or 2.")
    exit()

time.sleep(2)

# --- Create trackbars for HSV tuning ---
cv2.namedWindow("HSV Tuner")
cv2.createTrackbar("L-H", "HSV Tuner", 0, 180, nothing)
cv2.createTrackbar("L-S", "HSV Tuner", 100, 255, nothing)
cv2.createTrackbar("L-V", "HSV Tuner", 50, 255, nothing)
cv2.createTrackbar("U-H", "HSV Tuner", 10, 180, nothing)
cv2.createTrackbar("U-S", "HSV Tuner", 255, 255, nothing)
cv2.createTrackbar("U-V", "HSV Tuner", 255, 255, nothing)

# Background placeholder
background = None

print("Press 'b' to capture background | Press ESC to quit")

while True:
    ret, frame = cap.read()
    if not ret:
        break

    frame = cv2.flip(frame, 1)
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

    # --- Read values from trackbars ---
    l_h = cv2.getTrackbarPos("L-H", "HSV Tuner")
    l_s = cv2.getTrackbarPos("L-S", "HSV Tuner")
    l_v = cv2.getTrackbarPos("L-V", "HSV Tuner")
    u_h = cv2.getTrackbarPos("U-H", "HSV Tuner")
    u_s = cv2.getTrackbarPos("U-S", "HSV Tuner")
    u_v = cv2.getTrackbarPos("U-V", "HSV Tuner")

    lower_red1 = np.array([l_h, l_s, l_v])
    upper_red1 = np.array([u_h, u_s, u_v])
    lower_red2 = np.array([170, 100, 50])  # backup range
    upper_red2 = np.array([180, 255, 255])

    mask1 = cv2.inRange(hsv, lower_red1, upper_red1)
    mask2 = cv2.inRange(hsv, lower_red2, upper_red2)
    mask = mask1 + mask2

    # --- Refine mask ---
    mask = cv2.morphologyEx(mask, cv2.MORPH_OPEN, np.ones((3, 3), np.uint8), iterations=2)
    mask = cv2.morphologyEx(mask, cv2.MORPH_DILATE, np.ones((3, 3), np.uint8), iterations=1)
    mask_inv = cv2.bitwise_not(mask)

    if background is not None:
        cloak_area = cv2.bitwise_and(background, background, mask=mask)
        non_cloak_area = cv2.bitwise_and(frame, frame, mask=mask_inv)

        # --- Smooth blending ---
        cloak_area = cv2.GaussianBlur(cloak_area, (5, 5), 0)

        final = cv2.add(cloak_area, non_cloak_area)
    else:
        final = frame.copy()
        cv2.putText(final, "Press 'b' to capture background", (20, 40),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 0, 255), 2)

    # --- FPS Counter ---
    fps_text = f"FPS: {cap.get(cv2.CAP_PROP_FPS):.1f}"
    cv2.putText(final, fps_text, (20, 460), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 0), 2)

    # --- Display ---
    cv2.imshow("🪄 Invisibility Cloak", final)
    cv2.imshow("🎭 Cloak Mask", mask)

    # Keyboard controls
    key = cv2.waitKey(1) & 0xFF
    if key == 27:  # ESC
        break
    elif key == ord('b'):  # recapture background
        print("♻️ Capturing background...")
        for _ in range(60):
            ret, background = cap.read()
            if ret:
                background = cv2.flip(background, 1)
        print("✅ Background updated")

cap.release()
cv2.destroyAllWindows()