import time
from utils import AdbProcess, wait_until_found

def train_bo_binh(adb: AdbProcess, running: bool = False):
    """ Train Bo Binh """
    print("Training Bo Binh...")
    pos = wait_until_found(adb, "./images/bo_binh_2.png", timeout=400, running=running)
    if pos:
        adb.tap(*pos)
    time.sleep(0.5)
    pos_tap = wait_until_found(adb, "./images/bo_binh_3.png", timeout=10, running=running)
    if pos_tap:
        adb.tap(*pos_tap)
    time.sleep(0.5)
    adb.tap(985, 592)  # Tap on the train button
    time.sleep(0.5)

def train_ky_binh(adb: AdbProcess, running: bool = False):
    """ Train Ky Binh """
    print("Training Ky Binh...")
    pos = wait_until_found(adb, "./images/ky_binh_2.png", timeout=400, running=running)
    if pos:
        adb.tap(*pos)
    time.sleep(0.5)
    pos_tap = wait_until_found(adb, "./images/ky_binh_3.png", timeout=10, running=running)
    if pos_tap:
        adb.tap(*pos_tap)
    time.sleep(0.5)
    adb.tap(985, 592)  # Tap on the train button
    time.sleep(0.5)

def train_xe_phong(adb: AdbProcess, running: bool = False):
    """ Train Xe Phong """
    print("Training Xe Phong...")
    pos = wait_until_found(adb, "./images/xe_2.png", timeout=400, running=running)
    if pos:
        adb.tap(*pos)
    time.sleep(0.5)
    pos_tap = wait_until_found(adb, "./images/xe_3.png", timeout=10, running=running)
    if pos_tap:
        adb.tap(*pos_tap)
    time.sleep(0.5)
    adb.tap(985, 592)  # Tap on the train button
    time.sleep(0.5)