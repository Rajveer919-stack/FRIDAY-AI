import tkinter as tk
import datetime
import psutil
import platform
import subprocess
import sys
from pathlib import Path


class FridayDashboard:

    def __init__(self, root):
        self.root = root
        self.process = None

        self.root.title("FRIDAY AI | Personal Assistant")
        self.root.geometry("950x650")
        self.root.minsize(750, 550)
        self.root.configure(bg="#07111f")

        self.root.protocol("WM_DELETE_WINDOW", self.close_app)

        self.create_interface()
        self.update_clock()
        self.update_battery()
        self.check_process()

    def create_interface(self):

        header = tk.Frame(self.root, bg="#0b1b2b", height=85)
        header.pack(fill="x")
        header.pack_propagate(False)

        tk.Label(
            header,
            text="F R I D A Y",
            font=("Segoe UI", 25, "bold"),
            fg="#00e5ff",
            bg="#0b1b2b"
        ).pack(pady=(12, 0))

        tk.Label(
            header,
            text="PERSONAL AI ASSISTANT",
            font=("Segoe UI", 9),
            fg="#8da9c4",
            bg="#0b1b2b"
        ).pack()

        main = tk.Frame(self.root, bg="#07111f")
        main.pack(fill="both", expand=True, padx=25, pady=15)

        status_card = tk.Frame(
            main,
            bg="#102438",
            highlightbackground="#00bcd4",
            highlightthickness=1
        )
        status_card.pack(fill="x", pady=5)

        tk.Label(
            status_card,
            text="SYSTEM STATUS",
            font=("Segoe UI", 12, "bold"),
            fg="#00e5ff",
            bg="#102438"
        ).pack(pady=(10, 3))

        self.status_label = tk.Label(
            status_card,
            text="● DASHBOARD READY",
            font=("Segoe UI", 16, "bold"),
            fg="#00ff9c",
            bg="#102438"
        )
        self.status_label.pack(pady=(3, 10))

        info = tk.Frame(main, bg="#07111f")
        info.pack(fill="x", pady=10)

        self.clock_label = self.create_card(
            info, "TIME", "--:--:--"
        )

        self.battery_label = self.create_card(
            info, "BATTERY", "Checking..."
        )

        self.system_label = self.create_card(
            info, "SYSTEM", platform.system()
        )

        # Assistant control buttons
        controls = tk.Frame(main, bg="#07111f")
        controls.pack(fill="x", pady=10)

        self.start_button = tk.Button(
            controls,
            text="▶ START FRIDAY",
            font=("Segoe UI", 12, "bold"),
            bg="#00b894",
            fg="white",
            activebackground="#00d6a5",
            activeforeground="white",
            relief="flat",
            padx=20,
            pady=10,
            cursor="hand2",
            command=self.start_friday
        )
        self.start_button.pack(side="left", padx=(0, 12))

        self.stop_button = tk.Button(
            controls,
            text="■ STOP FRIDAY",
            font=("Segoe UI", 12, "bold"),
            bg="#d63031",
            fg="white",
            activebackground="#ff4757",
            activeforeground="white",
            relief="flat",
            padx=20,
            pady=10,
            cursor="hand2",
            command=self.stop_friday
        )
        self.stop_button.pack(side="left")

        tk.Label(
            main,
            text="ACTIVITY CONSOLE",
            font=("Segoe UI", 12, "bold"),
            fg="#00e5ff",
            bg="#07111f"
        ).pack(anchor="w", pady=(8, 5))

        self.console = tk.Text(
            main,
            height=7,
            bg="#030a12",
            fg="#8df7ff",
            insertbackground="white",
            font=("Consolas", 10),
            relief="flat",
            padx=12,
            pady=8,
            state="disabled"
        )
        self.console.pack(fill="both", expand=True)

        footer = tk.Frame(self.root, bg="#0b1b2b")
        footer.pack(fill="x", side="bottom")

        tk.Label(
            footer,
            text="FRIDAY AI | PERSONAL ASSISTANT",
            font=("Segoe UI", 9),
            fg="#8da9c4",
            bg="#0b1b2b"
        ).pack(pady=8)

        self.add_log("FRIDAY dashboard initialized.")
        self.add_log("Ready to start the voice assistant.")
        self.add_log("System: " + platform.platform())

    def create_card(self, parent, title, value):

        card = tk.Frame(
            parent,
            bg="#102438",
            highlightbackground="#164e63",
            highlightthickness=1
        )
        card.pack(side="left", fill="both", expand=True, padx=5)

        tk.Label(
            card,
            text=title,
            font=("Segoe UI", 10, "bold"),
            fg="#8da9c4",
            bg="#102438"
        ).pack(pady=(10, 3))

        label = tk.Label(
            card,
            text=value,
            font=("Segoe UI", 14, "bold"),
            fg="#00e5ff",
            bg="#102438"
        )
        label.pack(pady=(3, 10))

        return label

    def update_clock(self):

        now = datetime.datetime.now()

        self.clock_label.config(
            text=now.strftime("%I:%M:%S %p")
        )

        self.root.after(1000, self.update_clock)

    def update_battery(self):

        battery = psutil.sensors_battery()

        if battery is None:
            value = "Unavailable"
        else:
            value = f"{battery.percent:.0f}%"

            if battery.power_plugged:
                value += " ⚡"

        self.battery_label.config(text=value)
        self.root.after(10000, self.update_battery)

    def add_log(self, message):

        timestamp = datetime.datetime.now().strftime("%H:%M:%S")

        self.console.config(state="normal")
        self.console.insert("end", f"[{timestamp}] {message}\n")
        self.console.see("end")
        self.console.config(state="disabled")

    def start_friday(self):

        # Prevent launching duplicate assistant processes.
        if self.process is not None and self.process.poll() is None:
            self.add_log("FRIDAY is already running.")
            return

        main_file = Path(__file__).resolve().parent.parent / "main.py"

        if not main_file.exists():
            self.add_log("ERROR: main.py was not found.")
            self.add_log(f"Expected location: {main_file}")
            return

        try:
            self.process = subprocess.Popen(
                [sys.executable, str(main_file)],
                cwd=str(main_file.parent)
            )

            self.status_label.config(
                text="● FRIDAY RUNNING",
                fg="#00ff9c"
            )

            self.add_log("FRIDAY voice assistant launched.")

        except Exception as error:
            self.add_log(f"Could not start FRIDAY: {error}")

    def stop_friday(self):

        if self.process is not None and self.process.poll() is None:
            self.process.terminate()
            self.process = None

            self.status_label.config(
                text="● FRIDAY STOPPED",
                fg="#ff6b6b"
            )

            self.add_log("FRIDAY stop requested.")
        else:
            self.status_label.config(
                text="● DASHBOARD READY",
                fg="#00ff9c"
            )
            self.add_log("FRIDAY is not running.")

    def check_process(self):

        if self.process is not None and self.process.poll() is not None:
            self.process = None
            self.status_label.config(
                text="● FRIDAY STOPPED",
                fg="#ff6b6b"
            )

        self.root.after(1000, self.check_process)

    def close_app(self):

        if self.process is not None and self.process.poll() is None:
            self.process.terminate()

        self.root.destroy()


if __name__ == "__main__":

    root = tk.Tk()
    app = FridayDashboard(root)
    root.mainloop()