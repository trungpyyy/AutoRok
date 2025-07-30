
import time
from utils import AdbProcess



if __name__ == "__main__":
    adb = AdbProcess(adb_path="./adb/adb.exe", client_ip="127.0.0.1", client_port=5555)
    adb.screencap("test.png")
else:
    print("This script is intended to be run directly, not imported as a module.")