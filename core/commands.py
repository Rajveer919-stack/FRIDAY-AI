import datetime
import os
import platform
import subprocess
import urllib.parse
import webbrowser
from pathlib import Path

import psutil


def speak_error(speaker, message):
    speaker.speak(message)


def execute_command(command, speaker):
    command = command.lower().strip()

    if not command:
        return True

    # TIME
    if command in ("time", "what time is it", "tell me the time"):
        current_time = datetime.datetime.now().strftime("%I:%M %p")
        speaker.speak(f"Boss The current time is {current_time}.")
        return True

    # DATE
    elif command in ("date", "today", "what is today's date", "tell me the date"):
        today = datetime.datetime.now().strftime("%d %B %Y")
        speaker.speak(f"Boss Today's date is {today}.")
        return True

    # DAY
    elif "what day" in command or command == "day":
        day = datetime.datetime.now().strftime("%A")
        speaker.speak(f"Today is {day}.")
        return True

    # BATTERY
    elif "battery" in command:
        battery = psutil.sensors_battery()

        if battery is None:
            speaker.speak("boss Battery information is not available.")
        else:
            status = "and charging" if battery.power_plugged else ""
            speaker.speak(f"Boss Battery is {battery.percent} percent {status}.")

        return True

    # CPU USAGE
    elif "cpu usage" in command or "processor usage" in command:
        usage = psutil.cpu_percent(interval=1)
        speaker.speak(f"Boss Current CPU usage is {usage} percent.")
        return True

    # RAM / MEMORY
    elif "ram usage" in command or "memory usage" in command:
        memory = psutil.virtual_memory()
        used_gb = round(memory.used / (1024 ** 3), 1)
        total_gb = round(memory.total / (1024 ** 3), 1)

        speaker.speak(
            f"Boss You are using {used_gb} gigabytes of RAM "
            f"out of {total_gb} gigabytes."
        )
        return True

    # DISK SPACE
    elif "disk space" in command or "storage information" in command:
        try:
            disk = psutil.disk_usage("C:\\")
            free_gb = round(disk.free / (1024 ** 3), 1)
            total_gb = round(disk.total / (1024 ** 3), 1)

            speaker.speak(
                f"Boss Drive C has {free_gb} gigabytes free "
                f"Boss out of {total_gb} gigabytes."
            )
        except Exception:
            speaker.speak("Boss I could not read disk information.")

        return True

    # COMPUTER INFORMATION
    elif "computer information" in command or "laptop information" in command:
        memory_gb = round(psutil.virtual_memory().total / (1024 ** 3), 1)

        speaker.speak(
            f"Boss You are using {platform.system()} {platform.release()}, "
            f"Boss with approximately {memory_gb} gigabytes of RAM."
        )
        return True

    # OPEN WEBSITES
    elif command in ("open google", "open google website"):
        speaker.speak("Boss Opening Google.")
        webbrowser.open("https://www.google.com")
        return True

    elif command in ("open youtube", "open youtube website"):
        speaker.speak("Boss Opening YouTube.")
        webbrowser.open("https://www.youtube.com")
        return True

    elif "open whatsapp" in command:
        speaker.speak("Boss Opening WhatsApp.")
        webbrowser.open("https://web.whatsapp.com")
        return True

    elif "open gmail" in command:
        speaker.speak("Boss Opening Gmail.")
        webbrowser.open("https://mail.google.com")
        return True

    elif "open chatgpt" in command:
        speaker.speak("Boss Opening ChatGPT.")
        webbrowser.open("https://chatgpt.com")
        return True

    elif "open github" in command:
        speaker.speak("Boss Opening GitHub.")
        webbrowser.open("https://github.com")
        return True
    # VOICE CALCULATOR
    elif command.startswith("calculate "):
        expression = command.replace("calculate ", "", 1).strip().lower()

        try:
            import ast
            import operator

            expression = expression.replace("multiplied by", "*")
            expression = expression.replace("times", "*")
            expression = expression.replace("divided by", "/")
            expression = expression.replace("plus", "+")
            expression = expression.replace("minus", "-")
            expression = expression.replace("multiply by", "*")
            expression = expression.replace("multiply", "*")

            allowed_operators = {
                ast.Add: operator.add,
                ast.Sub: operator.sub,
                ast.Mult: operator.mul,
                ast.Div: operator.truediv,
                ast.Pow: operator.pow,
            }

            def safe_calculate(node):
                if isinstance(node, ast.Expression):
                    return safe_calculate(node.body)

                if isinstance(node, ast.Constant) and type(node.value) in (int, float):
                    return node.value

                if isinstance(node, ast.BinOp) and type(node.op) in allowed_operators:
                    left = safe_calculate(node.left)
                    right = safe_calculate(node.right)

                    if isinstance(node.op, ast.Pow) and abs(right) > 10:
                        raise ValueError("Exponent too large")

                    result = allowed_operators[type(node.op)](left, right)

                    if abs(result) > 1e100:
                        raise ValueError("Result too large")

                    return result

                if isinstance(node, ast.UnaryOp) and isinstance(node.op, (ast.UAdd, ast.USub)):
                    value = safe_calculate(node.operand)
                    return value if isinstance(node.op, ast.UAdd) else -value

                raise ValueError("Invalid expression")

            tree = ast.parse(expression, mode="eval")
            result = safe_calculate(tree)

            speaker.speak(f"Boss The answer is {result}.")

        except ZeroDivisionError:
            speaker.speak("Boss You cannot divide by zero.")

        except Exception:
            speaker.speak("Boss Sorry, I could not calculate that expression.")

        return True

    # GOOGLE SEARCH
    elif command.startswith("search for "):
        query = command.replace("search for ", "", 1).strip()

        if query:
            speaker.speak(f"Boss Searching Google for {query}.")
            url = "https://www.google.com/search?q=" + urllib.parse.quote(query)
            webbrowser.open(url)

        return True

    # YOUTUBE SEARCH
    elif command.startswith("search youtube for "):
        query = command.replace("search youtube for ", "", 1).strip()

        if query:
            speaker.speak(f"Boss Searching YouTube for {query}.")
            url = (
                "https://www.youtube.com/results?search_query="
                + urllib.parse.quote(query)
            )
            webbrowser.open(url)

        return True
    # CLOSE COMMON APPLICATIONS
    elif command in ("close notepad", "close calculator", "close paint"):
        app_names = {
            "close notepad": "notepad.exe",
            "close calculator": "CalculatorApp.exe",
            "close paint": "mspaint.exe",
        }

        process_name = app_names[command]

        try:
            result = subprocess.run(
                ["taskkill", "/IM", process_name, "/T"],
                capture_output=True,
                text=True,
                timeout=5
            )

            if result.returncode == 0:
                speaker.speak("Application closed boss.")
            else:
                speaker.speak(
                    "Boss I could not close the application. "
                    "Boss It may already be closed."
                )

        except Exception:
            speaker.speak("Sorry boss, I could not close the application.")

        return True

    # OPEN WINDOWS APPS
    # OPEN COMMON WINDOWS APPLICATIONS
    elif command in ("open camera", "start camera"):
        speaker.speak("Opening Camera boss.")
        try:
            os.startfile("microsoft.windows.camera:")
        except Exception:
            speaker.speak("I could not open the Camera app.")
        return True

    elif command in ("open bluetooth", "show bluetooth"):
        speaker.speak("Opening Bluetooth settings boss.")
        os.startfile("ms-settings:bluetooth")
        return True

    elif command in ("open network settings", "open internet settings"):
        speaker.speak("Opening network settings boss.")
        os.startfile("ms-settings:network")
        return True

    elif command in ("open display settings", "show display settings"):
        speaker.speak("Opening display settings boss.")
        os.startfile("ms-settings:display")
        return True
    elif "open notepad" in command:
        speaker.speak("Opening Notepad boss.")
        subprocess.Popen(["notepad.exe"])
        return True

    elif "open calculator" in command:
        speaker.speak("Opening Calculator boss.")
        subprocess.Popen(["calc.exe"])
        return True

    elif "open file explorer" in command or command == "open files":
        speaker.speak("Opening File Explorer boss.")
        subprocess.Popen(["explorer.exe"])
        return True

    elif "open command prompt" in command or command == "open cmd":
        speaker.speak("Opening Command Prompt boss.")
        subprocess.Popen(["cmd.exe"])
        return True

    elif "open powershell" in command:
        speaker.speak("Opening PowerShell boss.")
        subprocess.Popen(["powershell.exe"])
        return True

    elif "open task manager" in command:
        speaker.speak("Opening Task Manager boss.")
        subprocess.Popen(["taskmgr.exe"])
        return True

    elif "open paint" in command:
        speaker.speak("Opening Paint boss.")
        subprocess.Popen(["mspaint.exe"])
        return True

    elif "open wordpad" in command:
        speaker.speak("Opening WordPad if available boss.")
        try:
            subprocess.Popen(["write.exe"])
        except Exception:
            speaker.speak(
                "Boss WordPad may not be installed on this Windows version."
            )
        return True

    elif "open vs code" in command or "open visual studio code" in command:
        speaker.speak("Opening Visual Studio Code boss.")
        try:
            subprocess.Popen(["code"])
        except Exception:
            speaker.speak("Boss VS Code command was not found. It may not be in PATH.")
        return True
    # WIFI SETTINGS
    elif command in (
        "open wifi",
        "open wi-fi",
        "wifi settings",
        "wifi kholo",
        "open wifi settings"
    ):
        speaker.speak("Opening Wi-Fi settings Boss.")
        os.startfile("ms-settings:network-wifi")
        return True

    # AIRPLANE MODE SETTINGS
    elif command in (
        "open airplane mode",
        "airplane mode settings",
        "airplane mode kholo"
    ):
        speaker.speak("Boss Opening Airplane Mode settings.")
        os.startfile("ms-settings:network-airplanemode")
        return True

    # WINDOWS SETTINGS
    elif "open settings" in command:
        speaker.speak("Opening Windows Settings boss.")
        os.startfile("ms-settings:")
        return True

    elif "open bluetooth settings" in command:
        speaker.speak("Opening Bluetooth settings boss.")
        os.startfile("ms-settings:bluetooth")
        return True

    elif "open wifi settings" in command or "open wi-fi settings" in command:
        speaker.speak("Opening Wi-Fi settings Boss.")
        os.startfile("ms-settings:network-wifi")
        return True

    elif "open display settings" in command:
        speaker.speak("Opening display settings Boss.")
        os.startfile("ms-settings:display")
        return True

    elif "open sound settings" in command:
        speaker.speak("Opening sound settings boss.")
        os.startfile("ms-settings:sound")
        return True

    elif "open personalization settings" in command:
        speaker.speak("Opening personalization settings boss.")
        os.startfile("ms-settings:personalization")
        return True

    elif "open bluetooth" in command:
        speaker.speak("Opening Bluetooth settings boss.")
        os.startfile("ms-settings:bluetooth")
        return True
    # WINDOW CONTROLS
    elif command in (
        "minimize window",
        "minimize this window",
        "window minimize karo"
    ):
        speaker.speak("Minimizing the active window Boss.")
        subprocess.Popen(
            [
                "powershell.exe",
                "-NoProfile",
                "-Command",
                "(New-Object -ComObject WScript.Shell).SendKeys('% n')"
            ],
            creationflags=subprocess.CREATE_NO_WINDOW
        )
        return True

    elif command in (
        "maximize window",
        "maximize this window",
        "window maximize karo"
    ):
        speaker.speak("Maximizing the active window Boss.")
        subprocess.Popen(
            [
                "powershell.exe",
                "-NoProfile",
                "-Command",
                "(New-Object -ComObject WScript.Shell).SendKeys('% x')"
            ],
            creationflags=subprocess.CREATE_NO_WINDOW
        )
        return True

    elif command in (
        "close window",
        "close this window",
        "window band karo"
    ):
        speaker.speak("Closing the active window Boss.")
        subprocess.Popen(
            [
                "powershell.exe",
                "-NoProfile",
                "-Command",
                "(New-Object -ComObject WScript.Shell).SendKeys('%{F4}')"
            ],
            creationflags=subprocess.CREATE_NO_WINDOW
        )
        return True
    # TAKE SCREENSHOT
    elif command in (
        "take screenshot",
        "take a screenshot",
        "screenshot lo",
        "screen capture"
    ):
        try:
            import pyautogui

            screenshot_folder = Path.home() / "Pictures" / "FridayScreenshots"
            screenshot_folder.mkdir(parents=True, exist_ok=True)

            timestamp = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
            screenshot_path = screenshot_folder / f"Screenshot_{timestamp}.png"

            pyautogui.screenshot().save(str(screenshot_path))

            speaker.speak("Screenshot taken and saved in your Pictures folder Boss.")

        except Exception:
            speaker.speak("Sorry, I could not take the screenshot Boss.")

        return True
        # BRIGHTNESS SETTINGS
    elif command in (
        "increase brightness",
        "brightness up",
        "brightness badhao"
    ):
        speaker.speak("Opening brightness settings Boss.")
        os.startfile("ms-settings:display")
        return True

    elif command in (
        "decrease brightness",
        "brightness down",
        "brightness kam karo"
    ):
        speaker.speak("Opening brightness settings Boss.")
        os.startfile("ms-settings:display")
        return True

    # VOLUME
    elif "volume up" in command or "increase volume" in command:
        speaker.speak("Increasing volume boss.")
        subprocess.Popen(
            [
                "powershell.exe",
                "-NoProfile",
                "-Command",
                "(New-Object -ComObject WScript.Shell).SendKeys([char]175)"
            ],
            creationflags=subprocess.CREATE_NO_WINDOW
        )
        return True

    elif "volume down" in command or "decrease volume" in command:
        speaker.speak("Decreasing volume boss.")
        subprocess.Popen(
            [
                "powershell.exe",
                "-NoProfile",
                "-Command",
                "(New-Object -ComObject WScript.Shell).SendKeys([char]174)"
            ],
            creationflags=subprocess.CREATE_NO_WINDOW
        )
        return True

    elif command in ("mute", "mute volume", "toggle mute"):
        speaker.speak("Toggling mute Boss.")
        subprocess.Popen(
            [
                "powershell.exe",
                "-NoProfile",
                "-Command",
                "(New-Object -ComObject WScript.Shell).SendKeys([char]173)"
            ],
            creationflags=subprocess.CREATE_NO_WINDOW
        )
        return True
    # SEARCH FOR FILES
    elif command.startswith("find file "):
        filename = command.replace("find file ", "", 1).strip()
        speaker.speak(f"Boss Searching for {filename}.")

        search_locations = [
    Path.home() / "Desktop",
    Path.home() / "Documents",
    Path.home() / "Downloads",
    Path.home() / "OneDrive" / "Desktop",
    Path.home() / "OneDrive" / "Documents",
]

        matches = []

        for location in search_locations:
            if location.exists():
                try:
                    for item in location.rglob("*"):
                        if filename.lower() in item.name.lower():
                            matches.append(item)

                            if len(matches) >= 10:
                                break
                except (PermissionError, OSError):
                    continue

        if matches:
            speaker.speak(f"Boss I found {len(matches)} matching files or folders.")
            os.startfile(str(matches[0]))
        else:
            speaker.speak("Boss Sorry, I could not find that file.")

        return True

    # OPEN COMMON FOLDERS
    elif "open downloads" in command:
        speaker.speak("Opening Downloads Boss.")
        os.startfile(str(Path.home() / "Downloads"))
        return True

    elif "open documents" in command:
        speaker.speak("Opening Documents Boss.")
        os.startfile(str(Path.home() / "Documents"))
        return True

    elif "open desktop" in command:
        speaker.speak("Opening Desktop Boss.")
        os.startfile(str(Path.home() / "Desktop"))
        return True

    elif "open pictures" in command:
        speaker.speak("Opening Pictures Boss.")
        os.startfile(str(Path.home() / "Pictures"))
        return True
    # MUSIC FOLDER
    elif command in ("open music", "open music folder"):
        music_folder = Path.home() / "Music"
        speaker.speak("Opening Music folder Boss.")
        music_folder.mkdir(parents=True, exist_ok=True)
        os.startfile(str(music_folder))
        return True

    # VIDEOS FOLDER
    elif command in ("open videos", "open videos folder"):
        videos_folder = Path.home() / "Videos"
        speaker.speak("Opening Videos folder Boss.")
        videos_folder.mkdir(parents=True, exist_ok=True)
        os.startfile(str(videos_folder))
        return True

    # CURRENT DATE AND TIME
    elif "open clock" in command:
        speaker.speak("Opening the Windows clock Boss.")
        os.startfile("ms-clock:")
        return True

    # NOTES
    elif command.startswith("create note "):
        note = command.replace("create note ", "", 1).strip()

        if note:
            notes_file = Path.home() / "Documents" / "FridayNotes.txt"

            try:
                notes_file.parent.mkdir(parents=True, exist_ok=True)

                with open(notes_file, "a", encoding="utf-8") as file:
                    timestamp = datetime.datetime.now().strftime(
                        "%d-%m-%Y %I:%M %p"
                    )
                    file.write(f"\n[{timestamp}] {note}\n")

                speaker.speak("Boss Your note has been saved in Documents.")
            except Exception:
                speaker.speak("Boss I could not save the note.")

        return True
    # OPEN SAVED NOTES
    elif command in (
        "open notes",
        "show my notes",
        "open friday notes",
        "read my notes"
    ):
        notes_file = Path.home() / "Documents" / "FridayNotes.txt"

        if notes_file.exists():
            speaker.speak("Boss Opening your saved notes.")
            os.startfile(str(notes_file))
        else:
            speaker.speak("Boss You do not have any saved notes yet.")

        return True

    # GREETING
  # FRIENDLY CONVERSATION
    elif command in ("hello", "hi", "hello friday", "hi friday"):
        speaker.speak("Hey! Boss Main Friday hoon. Batao, kya help chahiye?")
        return True

    elif command in ("how are you", "how are you friday"):
        speaker.speak("Main bilkul badhiya hoon Boss! Boss Tum kaise ho?")
        return True

    elif command in ("i am fine", "i am good", "main theek hoon"):
        speaker.speak("Boss Ye sunkar achha laga! Batao, aaj kya karna hai?")
        return True

    elif command in ("who are you", "what is your name"):
        speaker.speak("Boss Main Friday hoon, tumhara personal laptop assistant.")
        return True

    elif command in ("thank you", "thanks", "thank you friday"):
        speaker.speak("Boss Arey, koi baat nahi! Main tumhari help ke liye hoon.")
        return True

    elif command in ("tell me a joke", "say a joke", "joke sunao"):
        speaker.speak(
            "Boss Ek computer doctor ke paas gaya. "
            "Doctor ne poochha, kya problem hai? "
            "Computer bola, mujhe virus ho gaya hai!"
        )
        return True

    elif command in ("i am sad", "i feel sad", "main udaas hoon"):
        speaker.speak(
            "Boss Kya hua? Agar tum batana chaho, toh main sun raha hoon."
        )
        return True

    elif command in ("good morning", "good evening", "good night"):
        if command == "good morning":
            speaker.speak("Good morning Boss! Aaj ka din achha rahe.")
        elif command == "good evening":
            speaker.speak("Good evening Boss! Batao, kya haal hai?")
        else:
            speaker.speak("Good night Boss! Achhe se aaram karna.")
        return True
    # LOCK COMPUTER
    elif command in ("lock computer", "lock laptop", "lock my computer"):
        speaker.speak("Locking your computer Boss.")
        subprocess.Popen(
            ["rundll32.exe", "user32.dll,LockWorkStation"]
        )
        return True
    # SLEEP COMPUTER
    elif command in ("sleep computer", "sleep laptop", "put computer to sleep"):
        speaker.speak("Boss Putting your computer to sleep.")
        subprocess.Popen(
            [
                "powershell.exe",
                "-NoProfile",
                "-Command",
                "Add-Type -AssemblyName System.Windows.Forms; "
                "[System.Windows.Forms.Application]::SetSuspendState('Suspend', $false, $false)"
            ],
            creationflags=subprocess.CREATE_NO_WINDOW
        )
        return False
    # RESTART COMPUTER
    elif command in (
        "restart computer",
        "restart laptop",
        "restart my laptop"
    ):
        speaker.speak(
            "Boss Are you sure you want to restart? "
            "Say confirm restart to continue."
        )
        return True

    elif command == "confirm restart":
        speaker.speak("Boss Restarting your computer in 30 seconds.")
        subprocess.Popen(["shutdown.exe", "/r", "/t", "30"])
        return True

    elif command in ("cancel restart", "abort restart"):
        speaker.speak("Boss Restart cancelled.")
        subprocess.Popen(
            ["shutdown.exe", "/a"],
            creationflags=subprocess.CREATE_NO_WINDOW
        )
        return True
    # SHUTDOWN COMPUTER
    elif command in ("shutdown computer", "shutdown laptop", "turn off computer"):
        speaker.speak(
            "Boss Are you sure you want to shut down your computer? "
            "Please say confirm shutdown to continue."
        )
        return True

    elif command == "confirm shutdown":
        speaker.speak("Boss Shutting down your computer in 10 seconds.")
        subprocess.Popen(
            ["shutdown.exe", "/s", "/t", "10"]
        )
        return True

    elif command in ("cancel shutdown", "do not shutdown"):
        speaker.speak("Boss Shutdown cancelled.")
        subprocess.Popen(
            ["shutdown.exe", "/a"],
            creationflags=subprocess.CREATE_NO_WINDOW
        )
        return True

    # EXIT
    elif command in ("exit friday", "stop friday", "shutdown friday"):
        speaker.speak("Boss Goodbye. Friday is shutting down.")
        return False

   # UNKNOWN COMMAND - GEMINI AI FALLBACK
    else:
        try:
            from gemini_ai import ask_gemini

            speaker.speak("Let me think.")
            answer = ask_gemini(command)

            if answer:
                speaker.speak(answer)
            else:
                speaker.speak(
                    "Sorry Boss, Gemini is not available right now. "
                    "Please try again later."
                )

        except Exception as error:
            print("Gemini fallback error:", error)
            speaker.speak(
                "Sorry Boss, I could not answer that right now."
            )

        return True