# pyinstaller --onedir --windowed --icon=icon.icns launcher.py

# Code for the UI and launch the bot
#Created By Deston Cauthers
import tkinter
import subprocess
import os
import sys
import json

process = None
##########
#Functions
##########
def check_process():
    global process

    if process is not None:
        ret = process.poll()  # None = still running

        if ret is not None:
            # Process finished → restore UI
            text.config(text="Bot stopped")
            button.pack(padx=30, pady=30)
            process = None
            return

    # keep checking every 500ms
    root.after(500, check_process)

def run_bot():
    global process
    print("Running Bot")
    
    button.pack_forget()

    text.config(text="Bot running, press ESC to exit")
    text.pack(padx=30, pady=30)
    
    if getattr(sys, "frozen", False):
        contents_dir = os.path.abspath(
        os.path.join(os.path.dirname(sys.executable), "..")
        )

        bot_path = os.path.join(
            contents_dir,
            "Resources",
            "bot",
            "bot"
        )
    else:
        bot_path = "dist/bot/bot"

    mode_map = {
        "Easy": "easy",
        "Medium": "medium",
        "Hard": "hard"
    }

    mode_arg = mode_map[selected_mode]

    process = subprocess.Popen([bot_path, mode_arg])
    #process = subprocess.Popen([bot_path], cwd=os.path.dirname(bot_path))

    # print("Executable:", sys.executable)
    # print("Launcher dir:", launcher_dir)
    # print("Dist dir:", dist_dir)
    # print("Bot path:", bot_path)
    # print("Exists:", os.path.exists(bot_path))

    check_process()

def set_mode(mode):
    global selected_mode
    selected_mode = mode
    print("Selected:", selected_mode)

     # Reset all buttons
    mode1_btn.config(bg="lightgray", fg="black")
    mode2_btn.config(bg="lightgray", fg="black")
    mode3_btn.config(bg="lightgray", fg="black")

    # Highlight selected button
    if mode == "Easy":
        mode1_btn.config(bg="#4CAF50", fg="white")
    elif mode == "Medium":
        mode2_btn.config(bg="#4CAF50", fg="white")
    elif mode == "Hard":
        mode3_btn.config(bg="#4CAF50", fg="white")

    update_config_display()

def update_config_display():
    mode_key = selected_mode.lower()

    cfg = CONFIG[mode_key]

    text = (
        f"LEFT: {cfg['LEFT']}   "
        f"TOP: {cfg['TOP']}   "
        f"WIDTH: {cfg['WIDTH']}   "
        f"HEIGHT: {cfg['HEIGHT']}   "
    )

    config_label.config(text=text)

#########
#Run Once
#########
root = tkinter.Tk()
root.title("Minesweeper Bot")
#root.configure(bg="white")
root.minsize(400, 250)
root.lift()
root.focus_force()
root.attributes("-topmost", True)
#root.after(100, lambda: root.attributes("-topmost", False))

selected_mode = "Easy"

#Select Mode Buttons
button_frame = tkinter.Frame(root)
button_frame.pack(pady=20)

mode1_btn = tkinter.Label(
    button_frame,
    text="Easy",
    bg="#4CAF50",   # default selected
    fg="white",
    padx=15,
    pady=8,
    cursor="hand2"
)
mode1_btn.pack(side="left", padx=5)
mode1_btn.bind("<Button-1>", lambda e: set_mode("Easy"))

mode2_btn = tkinter.Label(
    button_frame,
    text="Medium",
    bg="lightgray",
    fg="black",
    padx=15,
    pady=8,
    cursor="hand2"
)
mode2_btn.pack(side="left", padx=5)
mode2_btn.bind("<Button-1>", lambda e: set_mode("Medium"))

mode3_btn = tkinter.Label(
    button_frame,
    text="Hard",
    bg="lightgray",
    fg="black",
    padx=15,
    pady=8,
    cursor="hand2"
)
mode3_btn.pack(side="left", padx=5)
mode3_btn.bind("<Button-1>", lambda e: set_mode("Hard"))

#Configuration Paremeters
if getattr(sys, 'frozen', False):
    BASE_DIR = os.path.dirname(sys.executable)
else:
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))

if getattr(sys, "frozen", False):
    contents_dir = os.path.abspath(
        os.path.join(os.path.dirname(sys.executable), "..")
    )
    config_path = os.path.join(
        contents_dir,
        "Resources",
        "bot",
        "_internal",
        "config.json"
    )
else:
    config_path = os.path.join(BASE_DIR, "bot/config.json")

print(config_path)
with open(config_path, "r") as f:
    CONFIG = json.load(f)

config_label = tkinter.Label(
    root,
    text="",
    justify="left",
    font=("Courier", 12)
)
config_label.pack(pady=10)
update_config_display()

#Run Button
button = tkinter.Label(
    root,
    text="Run Bot",
    bg="#4CAF50",
    fg="white",
    padx=20,
    pady=10,
    cursor="hand2"
)

button.pack(padx=40, pady=20)
button.bind("<Button-1>", lambda e: run_bot())

text = tkinter.Label(root, text="")

#Label in bottom right of screen
created_label = tkinter.Label(
    root,
    text="Created by Deston Cauthers",
    fg="gray"
)
created_label.place(
    relx=1.0,
    rely=1.0,
    anchor="se",
    x=-10,
    y=-10
)

root.mainloop()