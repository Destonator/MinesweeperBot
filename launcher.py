# pyinstaller --onedir --windowed --icon=icon.icns launcher.py
import tkinter
import subprocess
import os
import sys

process = None
def app_root():
    if getattr(sys, 'frozen', False):
        # Launcher.app/Contents/MacOS -> go to Launcher.app root
        return os.path.abspath(os.path.join(os.path.dirname(sys.executable), "..", ".."))
    return os.path.dirname(os.path.abspath(__file__))


def get_base_path():
    if getattr(sys, 'frozen', False):
        return os.path.abspath(
            os.path.join(os.path.dirname(sys.executable), "bot", "bot")
        )
    else:
        return os.path.dirname(os.path.abspath(__file__))

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


    process = subprocess.Popen([bot_path], cwd=os.path.dirname(bot_path))

    # print("Executable:", sys.executable)
    # print("Launcher dir:", launcher_dir)
    # print("Dist dir:", dist_dir)
    # print("Bot path:", bot_path)
    # print("Exists:", os.path.exists(bot_path))

    check_process()

root = tkinter.Tk()
root.title("Minesweeper Bot")
#root.configure(bg="white")
root.minsize(300, 150)
root.lift()
root.focus_force()
root.attributes("-topmost", True)
#root.after(100, lambda: root.attributes("-topmost", False))

selected_mode = "Easy"

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

root.mainloop()