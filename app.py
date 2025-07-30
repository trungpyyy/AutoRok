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
        self.root.title("Android Automation Tool")
        self.root.iconphoto(False, tk.PhotoImage(file="./public/icon.png"))
        self.root.geometry("400x600")

        label = tk.Label(root, text="Welcome to the Android Automation Tool!")
        label.pack(pady=10)

        self.button_frame = tk.Frame(root)
        self.button_frame.pack(pady=10)

        self.start_button = tk.Button(self.button_frame, text="Start Automation", command=self.start_automation_ui)
        self.stop_button = tk.Button(self.button_frame, text="Stop Automation", command=self.stop_automation_ui)

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
        def wait_until_found(adb, template_path, timeout=10, interval=2, threshold=0.8):
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

            time.sleep(2)
            for idx, image_path in enumerate(ACTION_IMAGES, start=1):
                pos = wait_until_found(adb, image_path, timeout=10)
                if pos:
                    adb.tap(*pos)
                else:
                    print(f"[{idx}] ❌ Not found: {image_path}")
                    break

        while self.running:
            adb.screencap("screen.png")
            t1 = adb.find_object_position("screen.png", "./images/dotham_t1.png", threshold=0.8)
            t2 = adb.find_object_position("screen.png", "./images/dotham_t2.png", threshold=0.8)
            helper_pos = adb.find_object_position("screen.png", "./images/help.png", threshold=0.8)
            if helper_pos:
                adb.tap(*helper_pos)
                time.sleep(3)
            if t1:
                perform_action_sequence(adb)
            if t2:
                perform_action_sequence(adb)
            time.sleep(2)

if __name__ == "__main__":
    root = tk.Tk()
    app = AutomationApp(root)
    root.mainloop()