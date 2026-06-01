# pyinstaller --onedir --windowed --icon=icon.icns launcher.py

# Code for the UI and launch the bot
#Created By Deston Cauthers
import tkinter
import subprocess
import os
import sys
import json
import mss
from PIL import Image, ImageTk
#NEXT STEPS:
#Add a debug option to show what color and number the bot would recognize
process = None
##########
#Functions
##########
def check_process():#check if bot is still running
    global process

    if process is not None:
        ret = process.poll()  # None = still running

        if ret is not None:
            # Process finished → restore UI
            text.config(text="")
            text.pack_forget()
            preview_container.pack(pady=10)
            button.pack(padx=30, pady=30)

            process = None
            return

    # keep checking every 500ms
    root.after(500, check_process)

def run_bot():#Runs the bot script and edits UI
    global process
    print("Running Bot")
    
    #removes run button
    button.pack_forget()
    #removes preview image
    preview_container.pack_forget()

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

    update_parameter_labels()

def save_config():
    with open(config_path, "w") as f:
        json.dump(CONFIG, f, indent=4)

def change_value(param, delta):
    mode_key = selected_mode.lower()
    CONFIG[mode_key][param] += delta
    save_config()
    update_parameter_labels()

def create_parameter_column(param, column):
    # Parameter name
    tkinter.Label(
        parameter_frame,
        text=param,
        font=("Arial", 15, "bold")
    ).grid(row=0, column=column*3+1, padx=0)

    # Minus button
    tkinter.Button(
        parameter_frame,
        text="-",
        command=lambda: change_value(param, -1)
    ).grid(row=1, column=column*3)

    # Value label
    value_label = tkinter.Label(
        parameter_frame,
        text="0",
        width=5
    )
    value_label.grid(row=1, column=column*3 + 1)

    # Plus button
    tkinter.Button(
        parameter_frame,
        text="+",
        command=lambda: change_value(param, 1)
    ).grid(row=1, column=column*3 + 2)

    parameter_labels[param] = value_label

def update_parameter_labels():
    cfg = CONFIG[selected_mode.lower()]

    for param, label in parameter_labels.items():
        label.config(text=str(cfg[param]))
    
    update_preview()

def capture_preview():
    cfg = CONFIG[selected_mode.lower()]
    with mss.mss() as sct:
        monitor = {
            "left": cfg["LEFT"],
            "top": cfg["TOP"],
            "width": cfg["WIDTH"],
            "height": cfg["HEIGHT"]
        }

        screenshot = sct.grab(monitor)

        img = Image.frombytes(
            "RGB",
            screenshot.size,
            screenshot.rgb
        )

        return img

def update_preview():
    img = capture_preview()

    img.thumbnail((600, 400))

    tk_img = ImageTk.PhotoImage(img)

    preview_label.config(image=tk_img)
    preview_label.image = tk_img
    update_color_display()

def rgb_to_hex(rgb):
    return "#%02x%02x%02x" % tuple(rgb)

def update_color_display():
    # clear old widgets
    for widget in color_frame.winfo_children():
        widget.destroy()

    colors = CONFIG["colors"]

    row = 0

    for color_name, variants in colors.items():

        tkinter.Label(
            color_frame,
            text=color_name.capitalize(),
            width=8,
            anchor="w"
        ).grid(row=row, column=0, sticky="w", padx=(0, 10))

        for col, rgb in enumerate(variants):

            square = tkinter.Label(
                color_frame,
                bg=rgb_to_hex(rgb),
                width=3,
                height=1,
                relief="solid",
                borderwidth=1
            )

            square.grid(
                row=row,
                column=col + 1,
                padx=2,
                pady=2
            )
            square.bind(
                "<Button-1>",
                lambda e, rgb=rgb: print(rgb)
            )
        row += 1

def update_preview_visibility():
    if show_preview_var.get():
        preview_label.pack(side="left", padx=10)
    else:
        preview_label.pack_forget()

    if show_colors_var.get():
        color_frame.pack(side="left", anchor="n")
    else:
        color_frame.pack_forget()

    # Hide whole container if nothing inside it
    if show_preview_var.get() or show_colors_var.get():
        if not preview_container.winfo_ismapped():
            preview_container.pack(pady=10)
    else:
        preview_container.pack_forget()
#####################
#Define UI Elements
#####################
root = tkinter.Tk()
root.title("Minesweeper Bot")
#root.configure(bg="white")
root.minsize(400, 350)
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
    font=("Arial", 20, "bold"), 
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
    font=("Arial", 20, "bold"), 
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
    font=("Arial", 20, "bold"), 
    fg="black",
    padx=15,
    pady=8,
    cursor="hand2"
)
mode3_btn.pack(side="left", padx=5)
mode3_btn.bind("<Button-1>", lambda e: set_mode("Hard"))

#Configuration Paremeters
bounds_label = tkinter.Label(
    root,
    text="Screenshot Bounds:",
    font=("Arial", 20, "bold"), 
    fg="grey"
)
bounds_label.pack()

parameter_frame = tkinter.Frame(root)
parameter_frame.pack(pady=10)
parameter_labels = {}

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

params = ["LEFT", "TOP", "WIDTH", "HEIGHT"]

for i, param in enumerate(params):
    create_parameter_column(param, i)

#Show Preview CheckBox
show_preview_var = tkinter.BooleanVar(value=True)

show_preview_checkbox = tkinter.Checkbutton(
    root,
    text="Show Preview",
    variable=show_preview_var,
    command=update_preview_visibility
)

show_preview_checkbox.pack()

#Show Colors CheckBox
show_colors_var = tkinter.BooleanVar(value=False)

show_colors_checkbox = tkinter.Checkbutton(
    root,
    text="Show Colors",
    variable=show_colors_var,
    command=update_preview_visibility
)

show_colors_checkbox.pack()

#image Preview
preview_container = tkinter.Frame(root)
preview_container.pack(pady=10)

preview_label = tkinter.Label(preview_container)
preview_label.pack(side="left", padx=10)

color_frame = tkinter.Frame(preview_container)
#color_frame.pack(side="left", anchor="n")


# preview_label = tkinter.Label(root)
# preview_label.pack(pady=10)

#Run Button
button = tkinter.Label(
    root,
    text="Run Bot",
    bg="#4CAF50",
    font=("Arial", 20, "bold"), 
    fg="white",
    padx=20,
    pady=10,
    cursor="hand2"
)

button.place(relx=0.5, rely=1.0, anchor="s", y=-35)
button.bind("<Button-1>", lambda e: run_bot())

#Bot Running text
text = tkinter.Label(
    root, 
    text="", 
    font=("Arial", 20, "bold"), 
    fg="red"
)

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
#########
#Run Once
#########
update_parameter_labels()
update_preview()
update_color_display()

root.mainloop()