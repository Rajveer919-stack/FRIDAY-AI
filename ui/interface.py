import tkinter as tk
from tkinter import ttk
import datetime
import psutil
import platform


class FridayDashboard:

    def __init__(self, root):
        self.root = root

        self.root.title("FRIDAY AI | Personal Assistant")
        self.root.geometry("950x650")
        self.root.minsize(750, 550)
        self.root.configure(bg="#07111f")

        self.root.protocol("WM_DELETE_WINDOW", self.close_app)

        self.create_interface()
        self.update_clock()
        self.update_battery()

    def create_interface(self):

        # Header
        header = tk.Frame(
            self.root,
            bg="#0b1b2b",
            height=85
        )
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

        # Main container
        main = tk.Frame(
            self.root,
            bg="#07111f"
        )
        main.pack(fill="both", expand=True, padx=25, pady=20)

        # Status card
        status_card = tk.Frame(
            main,
            bg="#102438",
            highlightbackground="#00bcd4",
            highlightthickness=1
        )
        status_card.pack(fill="x", pady=10)

        tk.Label(
            status_card,
            text="SYSTEM STATUS",
            font=("Segoe UI", 12, "bold"),
            fg="#00e5ff",
            bg="#102438"
        ).pack(pady=(15, 5))

        self.status_label = tk.Label(
            status_card,
            text="● DASHBOARD READY",
            font=("Segoe UI", 17, "bold"),
            fg="#00ff9c",
            bg="#102438"
        )
        self.status_label.pack(pady=(5, 15))

        # Information cards
        info = tk.Frame(main, bg="#07111f")
        info.pack(fill="x", pady=12)

        self.clock_label = self.create_card(
            info, "TIME", "--:--:--"
        )

        self.battery_label = self.create_card(
            info, "BATTERY", "Checking..."
        )

        self.system_label = self.create_card(
            info, "SYSTEM", platform.system()
        )

        # Command history
        tk.Label(
            main,
            text="ACTIVITY CONSOLE",
            font=("Segoe UI", 12, "bold"),
            fg="#00e5ff",
            bg="#07111f"
        ).pack(anchor="w", pady=(15, 8))

        self.console = tk.Text(
            main,
            height=8,
            bg="#030a12",
            fg="#8df7ff",
            insertbackground="white",
            font=("Consolas", 10),
            relief="flat",
            padx=12,
            pady=10,
            state="disabled"
        )
        self.console.pack(fill="both", expand=True)

        self.add_log("FRIDAY dashboard initialized.")
        self.add_log("Voice assistant can be started separately.")
        self.add_log("System: " + platform.platform())

        # Footer
        footer = tk.Frame(
            self.root,
            bg="#0b1b2b"
        )
        footer.pack(fill="x", side="bottom")

        tk.Label(
            footer,
            text="FRIDAY AI  |  PERSONAL ASSISTANT",
            font=("Segoe UI", 9),
            fg="#8da9c4",
            bg="#0b1b2b"
        ).pack(pady=10)

    def create_card(self, parent, title, value):

        card = tk.Frame(
            parent,
            bg="#102438",
            highlightbackground="#164e63",
            highlightthickness=1
        )

        card.pack(
            side="left",
            fill="both",
            expand=True,
            padx=5
        )

        tk.Label(
            card,
            text=title,
            font=("Segoe UI", 10, "bold"),
            fg="#8da9c4",
            bg="#102438"
        ).pack(pady=(15, 5))

        label = tk.Label(
            card,
            text=value,
            font=("Segoe UI", 15, "bold"),
            fg="#00e5ff",
            bg="#102438"
        )

        label.pack(pady=(5, 15))

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

        self.console.insert(
            "end",
            f"[{timestamp}] {message}\n"
        )

        self.console.see("end")
        self.console.config(state="disabled")

    def close_app(self):
        self.root.destroy()


if __name__ == "__main__":

    root = tk.Tk()

    app = FridayDashboard(root)

    root.mainloop()