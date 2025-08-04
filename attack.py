import time
from utils import AdbProcess, wait_until_found

def attack(adb: AdbProcess, running: bool = False):
    """ Perform attack actions """
    print("Starting attack...")
    home_pos = wait_until_found(adb, "./images/home.png", timeout=10, running=running)
    if home_pos:
        adb.tap(*home_pos)
    time.sleep(0.5)
    # Example of finding and tapping an image
    search_pos = wait_until_found(adb, "./images/search_1.png", timeout=10, running=running)
    if search_pos:
        adb.tap(*search_pos)
    search_2_pos = wait_until_found(adb, "./images/search_2.png", timeout=10, running=running)
    if search_2_pos:
        adb.tap(*search_2_pos)
    attack_1_pos = wait_until_found(adb, "./images/attack_1.png", timeout=10, running=running)
    if attack_1_pos:
        adb.tap(*attack_1_pos)
    attack_2_pos = wait_until_found(adb, "./images/attack_2.1.png", timeout=10, running=running)
    if attack_2_pos:
        adb.tap(*attack_2_pos)
    attack_3_pos = wait_until_found(adb, "./images/attack_3.png", timeout=10, running=running)
    if attack_3_pos:
        adb.tap(*attack_3_pos)
    # Additional attack logic can be added here
    print("Attack completed.")