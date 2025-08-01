import subprocess
import cv2

from utils import AdbProcess

selected_point = []

def click_event(event, x, y, flags, param):
    if event == cv2.EVENT_LBUTTONDOWN:
        print(f"📍 Selected point: ({x}, {y})")
        selected_point.append((x, y))
        # Vẽ dấu chấm trên ảnh
        cv2.circle(param, (x, y), 5, (0, 255, 0), -1)
        cv2.imshow("Click to select point", param)
        cv2.waitKey(500)
        cv2.destroyAllWindows()

def choose_point_on_image(img):
    if img is None:
        print(f"❌ Failed to load image")
        return None

    print("🖱️ Click on the image to select a tap point...")
    clone = img.copy()
    cv2.imshow("Click to select point", img)
    cv2.setMouseCallback("Click to select point", click_event, param=clone)
    cv2.waitKey(0)

    if selected_point:
        x, y = selected_point[0]
        return x, y
    else:
        print("⚠️ No point selected.")
        return None

if __name__ == "__main__":
    adb = AdbProcess(adb_path="./adb/adb.exe", client_ip="127.0.0.1", client_port=5555)
    command = ["./adb/adb.exe", "-s", f"127.0.0.1:5555", "exec-out", "screencap", "-p"]
    try:
        output = subprocess.check_output(command)
        with open("test.png", "wb") as f:
                f.write(output)
    except subprocess.CalledProcessError as e:
        print(f"Error capturing screenshot: {e}")

    image_path = "test.png"  # ảnh đã capture từ adb
    img = cv2.imread(image_path)
    choose_point_on_image(img)
