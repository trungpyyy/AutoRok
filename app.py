"""
Learn tkinter, Python, and ADB by building a simple Android automation tool.
This tool automates tasks on an Android device using ADB commands and image recognition.
"""
import tkinter as tk
import threading
import time
from utils import AdbProcess
from test import choose_point_on_image  # Add this import

class AutomationApp:
    def __init__(self, root):
        self.root = root
        self.running = False
        self.thread = None
        self.tap_point = None
        self.task_spy = False
        self.check_count = 0
        self.task_cave_probe = False
        self.root.title("Android Automation Tool")
        self.root.iconphoto(False, tk.PhotoImage(file="./public/icon.png"))
        self.root.geometry("400x600")

        label = tk.Label(root, text="Welcome to the Android Automation Tool!")
        label.pack(pady=10)

        self.button_frame = tk.Frame(root)
        self.button_frame.pack(pady=10)

        self.start_button = tk.Button(self.button_frame, text="Start Automation", command=self.start_automation_ui)
        self.stop_button = tk.Button(self.button_frame, text="Stop Automation", command=self.stop_automation_ui)

        text_spy = tk.StringVar(value="Enable Spy Task")
        self.spy_checkbox = tk.Checkbutton(root, textvariable=text_spy, command=lambda: setattr(self, 'task_spy', not self.task_spy))
        self.spy_checkbox.pack(pady=5)
        text_cave_probe = tk.StringVar(value="Enable Cave Probe Task")
        self.cave_probe_checkbox = tk.Checkbutton(root, textvariable=text_cave_probe, command=lambda: setattr(self, 'task_cave_probe', not self.task_cave_probe))
        self.cave_probe_checkbox.pack(pady=5)
        self.show_start()

    def show_start(self):
        self.start_button.pack(pady=10)
        self.stop_button.pack_forget()

    def show_stop(self):
        self.stop_button.pack(pady=10)
        self.start_button.pack_forget()

    def start_automation_ui(self):
        self.start_automation()
        self.show_stop()

    def stop_automation_ui(self):
        self.stop_automation()
        self.show_start()

    def start_automation(self):
        if not self.running:
            if self.tap_point is None:
                adb = AdbProcess(adb_path="./adb/adb.exe", client_ip="127.0.0.1", client_port=5555)
                adb.screencap("screen.png")
                self.tap_point = choose_point_on_image("screen.png")
            self.running = True
            self.thread = threading.Thread(target=self.automation_loop, daemon=True)
            self.thread.start()
            print("Automation started!")

    def stop_automation(self):
        self.running = False
        print("Automation stopped!")

    def automation_loop(self):
        adb = AdbProcess(adb_path="./adb/adb.exe", client_ip="127.0.0.1", client_port=5555)
        ACTION_IMAGES = [
            "./images/dotham_1.png",
            "./images/dotham_2.png",
            "./images/dotham_3.png",
            "./images/send.png",
            "./images/goback.png"
        ]
        ACTION_IMAGES_CAVE_PROBE = [
            "./images/cave_probe_4.png",
            "./images/send.png",
            "./images/goback.png"
        ]
        def wait_until_found(adb, template_path, timeout=10, interval=0.5, threshold=0.8):
            start_time = time.time()
            while time.time() - start_time < timeout and self.running:
                adb.screencap("screen.png")
                time.sleep(0.3)
                pos = adb.find_object_position("screen.png", template_path, threshold=threshold)
                if pos:
                    return pos
                time.sleep(interval)
            return None

        def perform_action_sequence(adb):
            # Use the selected tap point
            if self.tap_point is None:
                print("❌ No tap point selected, skipping action sequence.")
                return
            adb.tap(*self.tap_point)

            time.sleep(0.5)
            for idx, image_path in enumerate(ACTION_IMAGES, start=1):
                pos = wait_until_found(adb, image_path, timeout=10)
                if pos:
                    adb.tap(*pos)
                else:
                    print(f"[{idx}] ❌ Not found: {image_path}")
                    break
        def perform_action_cave_probe(adb):
            # Use the selected tap point
            if self.tap_point is None:
                print("❌ No tap point selected, skipping action sequence.")
                return
            adb.tap(*self.tap_point)
            cave_probe_pos =wait_until_found(adb, "./images/dotham_1.png", timeout=5)
            if cave_probe_pos:
                adb.tap(*cave_probe_pos)
            time.sleep(0.8)
            adb.tap(750, 212) # CAVE_PROBE 2
            if self.check_count == 0:
                self.check_count = 1
                time.sleep(0.8)
                adb.tap(993, 335) # CAVE_PROBE 3
            elif self.check_count == 1:
                self.check_count = 2
                time.sleep(0.8)
                adb.tap(991, 477) # CAVE_PROBE 3
            else:
                self.check_count = 0
                time.sleep(0.8)
                adb.tap(995, 472) # CAVE_PROBE 3

            time.sleep(0.8)
            for idx, image_path in enumerate(ACTION_IMAGES_CAVE_PROBE, start=1):
                pos = wait_until_found(adb, image_path, timeout=10)
                if pos:
                    adb.tap(*pos)
                else:
                    print(f"[{idx}] ❌ Not found: {image_path}")
                    break
        while self.running:
            adb.screencap("screen.png")
            goback_pos = adb.find_object_position("screen.png", "./images/goback.png", threshold=0.8)
            if goback_pos:
                adb.tap(*goback_pos)
                time.sleep(3)
                continue
            close_pos = adb.find_object_position("screen.png", "./images/close.png", threshold=0.8)
            if close_pos:
                adb.tap(*close_pos)
                time.sleep(3)
                continue
            t1 = adb.find_object_position("screen.png", "./images/dotham_t1.png", threshold=0.8)
            t2 = adb.find_object_position("screen.png", "./images/dotham_t2.png", threshold=0.8)
            helper_pos = adb.find_object_position("screen.png", "./images/help.png", threshold=0.8)
            if helper_pos:
                adb.tap(*helper_pos)
                time.sleep(3)
            if t1 and self.task_spy:
                perform_action_sequence(adb)
            if t2 and self.task_spy:
                perform_action_sequence(adb)
            if t1 and self.task_cave_probe:
                perform_action_cave_probe(adb)
            if t2 and self.task_cave_probe:
                perform_action_cave_probe(adb)
            time.sleep(2)
        print("Automation done running...")
if __name__ == "__main__":
    root = tk.Tk()
    app = AutomationApp(root)
    root.mainloop()