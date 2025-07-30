import time
from utils import AdbProcess

# Danh sách ảnh cần click theo thứ tự
ACTION_IMAGES = [
    "./images/dotham_1.png",
    "./images/dotham_2.png",
    "./images/dotham_3.png",
    "./images/send.png",
    "./images/goback.png"
]

def perform_action(adb: AdbProcess, image_path: str):
    adb.screencap("screen.png")
    time.sleep(1)

    pos = adb.find_object_position("screen.png", image_path, threshold=0.8)

    if pos:
        adb.tap(*pos)
        time.sleep(3)


def perform_action_sequence(adb: AdbProcess):
    adb.tap(743, 235)
    time.sleep(0.5)

    for idx, image_path in enumerate(ACTION_IMAGES, start=1):
        adb.screencap("screen.png")
        time.sleep(0.5)

        pos = adb.find_object_position("screen.png", image_path, threshold=0.8)

        if pos:
            adb.tap(*pos)
            time.sleep(4)
        else:
            print(f"[{idx}] ❌ Not found: {image_path}")
            break

if __name__ == "__main__":
    adb = AdbProcess(adb_path="./adb/adb.exe", client_ip="127.0.0.1", client_port=5555)
    while True:
        adb.screencap("screen.png")
        t1 = adb.find_object_position("screen.png", "./images/dotham_t1.png", threshold=0.8)
        t2 = adb.find_object_position("screen.png", "./images/dotham_t2.png", threshold=0.8)
        helper_pos = adb.find_object_position("screen.png", "./images/help.png", threshold=0.8)
        if helper_pos:
            adb.tap(*helper_pos)
            time.sleep(3)            
        elif t1:
            perform_action_sequence(adb)
        elif t2:
            perform_action_sequence(adb)
        time.sleep(2)
else:
    print("This script should be run directly.")
