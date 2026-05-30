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
root.title("Launcher")

button = tkinter.Button(root, text="Run Bot", command=run_bot)
button.pack(padx=30, pady=30)

text = tkinter.Label(root, text="")

root.mainloop()