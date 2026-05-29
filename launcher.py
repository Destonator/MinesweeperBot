import tkinter
import subprocess
import os
import sys

def run_bot():
    print("Running Bot")
    if getattr(sys, 'frozen', False):
        base_path = os.path.dirname(sys.executable)
    else:
        base_path = os.path.dirname(os.path.abspath(__file__))

    bot_path = os.path.join(base_path, "bot", "bot")

    subprocess.Popen(bot_path)

root = tkinter.Tk()
root.title("Launcher")

button = tkinter.Button(root, text="Run Bot", command=run_bot)
button.pack(padx=30, pady=30)

root.mainloop()