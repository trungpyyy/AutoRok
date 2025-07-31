import subprocess
import cv2
import time
class AdbProcess:
    def __init__(self, adb_path="./adb/adb.exe", client_ip="127.0.0.1", client_port=5555):
        self.adb_path = adb_path
        self.client_ip = client_ip
        self.client_port = client_port
        if self.client_ip and self.client_port:
            self.connect_client()

    def connect_client(self):
        address = f"{self.client_ip}:{self.client_port}"
        command = [self.adb_path, "connect", address]
        try:
            subprocess.check_output(command)
            print(f"Connected to client at {address}.")
        except subprocess.CalledProcessError as e:
            print(f"Error connecting to client at {address}: {e}")

    def tap(self, x, y):
        command = [self.adb_path, "-s", f"{self.client_ip}:{self.client_port}", "shell", "input", "tap", str(x), str(y)]
        try:
            subprocess.check_output(command)
        except subprocess.CalledProcessError as e:
            print(f"Error tapping at ({x}, {y}): {e}")

    
    def swipe(self, x1, y1, x2, y2, duration=500):
        command = [self.adb_path, "shell", "input", "swipe", str(x1), str(y1), str(x2), str(y2), str(duration)]
        try:
            subprocess.check_output(command)
            print(f"Swiped from ({x1}, {y1}) to ({x2}, {y2}) in {duration}ms.")
        except subprocess.CalledProcessError as e:
            print(f"Error swiping from ({x1}, {y1}) to ({x2}, {y2}): {e}")

    def find_object_position(self, screenshot_path, template_path, threshold=0.8):
        screen = cv2.imread(screenshot_path)
        template = cv2.imread(template_path)

        result = cv2.matchTemplate(screen, template, cv2.TM_CCOEFF_NORMED)
        _, max_val, _, max_loc = cv2.minMaxLoc(result)

        if max_val >= threshold:
            h, w = template.shape[:2]
            return (max_loc[0] + w // 2, max_loc[1] + h // 2)
        else:
            return None

    def screencap(self, save_path="screen.png"):
        command = [self.adb_path, "-s", f"{self.client_ip}:{self.client_port}", "exec-out", "screencap", "-p"]
        try:
            output = subprocess.check_output(command)
            with open(save_path, "wb") as f:
                f.write(output)
        except subprocess.CalledProcessError as e:
            print(f"Error capturing screenshot: {e}")

def wait_until_found(adb, template_path, timeout=10, interval=0.5, threshold=0.8, running=False):
    """ Wait until the template image is found on the screen.
    Args:
        adb: AdbProcess instance to interact with the device.
        template_path: Path to the template image to find.
        timeout: Maximum time to wait for the image to be found.
        interval: Time interval between checks.
        threshold: Confidence threshold for image matching.
        running: Flag to control the loop execution.
    Returns:
        Tuple of (x, y) coordinates if found, otherwise None.
    """
    start_time = time.time()
    while time.time() - start_time < timeout and running:
        adb.screencap("screen.png")
        time.sleep(0.3)
        pos = adb.find_object_position("screen.png", template_path, threshold=threshold)
        if pos:
            return pos
        time.sleep(interval)
    return None