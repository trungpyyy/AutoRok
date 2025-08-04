"""
Learn tkinter, Python, and ADB by building a simple Android automation tool.
This tool automates tasks on an Android device using ADB commands and image recognition.
"""
import tkinter as tk
import threading
import time
from utils import AdbProcess, wait_until_found
from test import choose_point_on_image  # Add this import
import train
from attack import attack
class AutomationApp:
    def __init__(self, root):
        self.root = root
        self.running = False
        self.thread = None
        self.tap_point = None
        self.task_attack = False
        self.task_spy_var = tk.BooleanVar(value=True)
        self.task_spy = self.task_spy_var.get()
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
        self.spy_checkbox = tk.Checkbutton(
            root,
            textvariable=text_spy,
            variable=self.task_spy_var,                 # Gắn biến boolean
            command=lambda: setattr(self, 'task_spy', self.task_spy_var.get())
        )
        self.spy_checkbox.pack(pady=5)
        text_cave_probe = tk.StringVar(value="Enable Cave Probe Task")
        self.cave_probe_checkbox = tk.Checkbutton(
            root,
            textvariable=text_cave_probe,
            command=lambda: setattr(self, 'task_cave_probe', not self.task_cave_probe))
        self.cave_probe_checkbox.pack(pady=5)
        
        text_attack= tk.StringVar(value="Enable Attack Task")
        self.attack_checkbox = tk.Checkbutton(
            root,
            textvariable=text_attack,              # Gắn biến boolean
            command=lambda: setattr(self, 'task_attack', not self.task_attack)
        )
        self.attack_checkbox.pack(pady=5)
        
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
                self.tap_point = choose_point_on_image(adb.screencap())
                
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
      

        def perform_action_sequence(adb):
            # Use the selected tap point
            if self.tap_point is None:
                print("❌ No tap point selected, skipping action sequence.")
                return
            adb.tap(*self.tap_point)
            for idx, image_path in enumerate(ACTION_IMAGES, start=1):
                pos = wait_until_found(adb, image_path, timeout=10, running=self.running)
                if pos:
                    adb.tap(*pos)
                else:
                    print(f"[{idx}] ❌ Not found: {image_path}")
                    break
            time.sleep(0.85)

        def perform_action_cave_probe(adb):
            # Use the selected tap point
            if self.tap_point is None:
                print("❌ No tap point selected, skipping action sequence.")
                return
            adb.tap(*self.tap_point)
            cave_probe_pos =wait_until_found(adb, "./images/dotham_1.png", timeout=5, running=self.running)
            if cave_probe_pos:
                adb.tap(*cave_probe_pos)
            time.sleep(0.85)
            adb.tap(750, 212) # CAVE_PROBE 2
            time.sleep(0.85)
            adb.tap(993, 605) # CAVE_PROBE 3

            for idx, image_path in enumerate(ACTION_IMAGES_CAVE_PROBE, start=1):
                pos = wait_until_found(adb, image_path, timeout=10, running=self.running)
                if pos:
                    adb.tap(*pos)
                else:
                    print(f"[{idx}] ❌ Not found: {image_path}")
                    break
        while self.running:
            img = adb.screencap()
            goback_pos = adb.find_object_position(img, "./images/goback.png")
            if goback_pos:
                adb.tap(*goback_pos)
                time.sleep(0.5)
                continue
            back_pos = adb.find_object_position(img, "./images/back.png")
            if back_pos:
                adb.tap(*back_pos)
                time.sleep(0.5)
                continue
            close_pos = adb.find_object_position(img, "./images/close.png")
            if close_pos:
                adb.tap(*close_pos)
                time.sleep(0.5)
                continue
            close_1_pos = adb.find_object_position(img, "./images/close_1.png")
            if close_1_pos:
                adb.tap(*close_1_pos)
                time.sleep(0.5)
                continue
            ky_binh_pos = adb.find_object_position(img, "./images/train_ky_binh_1.png")
            if ky_binh_pos:
                print("🚀 Starting Ky Binh training...")
                adb.tap(*ky_binh_pos)
                train.train_ky_binh(adb, running=self.running)
            xe_phong_pos = adb.find_object_position(img, "./images/train_xe_1.png")
            if xe_phong_pos:
                print("🚀 Starting Xe Phong training...")
                adb.tap(*xe_phong_pos)
                train.train_xe_phong(adb, running=self.running)
            bo_binh_pos = adb.find_object_position(img, "./images/train_bo_binh_1.png")
            if bo_binh_pos:
                print("🚀 Starting Bo Binh training...")
                adb.tap(*bo_binh_pos)
                train.train_bo_binh(adb, running=self.running)
            cung_phap_pos = adb.find_object_position(img, "./images/train_cung_1.png")
            if cung_phap_pos:
                print("🚀 Starting Cung Phap training...")
                adb.tap(*cung_phap_pos)
                train.train_cung(adb, running=self.running)
            disconnected_pos = adb.find_object_position(img, "./images/disconnected.png")
            if disconnected_pos:
                print("❌ Device disconnected, stopping automation.")
                adb.tap(638, 471)
            helper_pos = adb.find_object_position(img, "./images/help.png")
            if helper_pos:
                adb.tap(*helper_pos)
                time.sleep(0.5)
            t1 = adb.find_object_position(img, "./images/dotham_t1.png")
            t2 = adb.find_object_position(img, "./images/dotham_t2.png")
            t3 = adb.find_object_position(img, "./images/dotham_t3.png")
            t4 = adb.find_object_position(img, "./images/dotham_t4.png")
            if (t1 or t2 or t3 or t4) and self.task_spy:
                perform_action_sequence(adb)
            if (t1 or t2 or t3 or t4) and self.task_cave_probe:
                perform_action_cave_probe(adb)
            if self.task_attack:
                check_attack_pos = adb.find_object_position(img, "./images/attack_none_2.png")
                if check_attack_pos:
                    attack(adb, running=self.running)
            time.sleep(2)
        print("Automation done running...")
if __name__ == "__main__":
    root = tk.Tk()
    app = AutomationApp(root)
    root.mainloop()