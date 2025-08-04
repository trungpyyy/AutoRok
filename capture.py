
import time
from utils import AdbProcess
import cv2


if __name__ == "__main__":
    adb = AdbProcess(adb_path="./adb/adb.exe", client_ip="127.0.0.1", client_port=5555)
    img = adb.screencap()
    cv2.imwrite("image.png", img)
else:
    print("This script is intended to be run directly, not imported as a module.")