import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk, ImageSequence   
import random
import os


#     H A C K E R   J O K E   M A C H I N E   (v1.0)


#created class for gifs  
class AnimatedGIF(tk.Label):
    def __init__(self, parent, gif_path):
        gif = Image.open(gif_path)
        self.frames = []
        for frame in ImageSequence.Iterator(gif):
            img = ImageTk.PhotoImage(frame.copy().convert("RGBA"))
            duration = frame.info.get("duration", 80)
            self.frames.append((img, duration))

        super().__init__(parent, image=self.frames[0][0], borderwidth=0)
        self.idx = 0
        self.animate()

    def animate(self):
        frame, delay = self.frames[self.idx]
        self.config(image=frame)
        self.idx = (self.idx + 1) % len(self.frames)
        self.after(delay, self.animate)


class JokeMatrix:

    def __init__(self, root):
        self.root = root
        self.root.title("Joke Terminal v1.0")
        self.root.geometry("500x500")
        self.root.config(bg="black")

        # store jokes
        self.jokes = []
        self.current_setup = ""
        self.current_punchline = ""

        # dynamic button state
        self.first_time = True

        # load jokes from txt file
        self.load_jokes()

        # open splash screen
        self.splash_screen()


    # LOAD JOKES FROM TEXT FILE
    def load_jokes(self):
        """Reads jokes from randomJokes.txt and stores them."""
        file_path = os.path.join(os.path.dirname(__file__), "randomJokes.txt")

        with open(file_path, "r", encoding="utf-8") as file:
            for line in file:
                if "?" in line:
                    setup, punchline = line.strip().split("?")
                    self.jokes.append((setup + "?", punchline))


    # CLEAR THE WINDOW
    def wipe(self):
        """Removes all widgets from the screen."""
        for w in self.root.winfo_children():
            w.destroy()


    # PAGE 1: SPLASH SCREEN
    def splash_screen(self):
        self.wipe()

        # reset for next session
        self.first_time = True

        # animated background gif
        gif_path = os.path.join(os.path.dirname(__file__), "backgrounds", "hacker_bg.gif")
        self.bg = AnimatedGIF(self.root, gif_path)
        self.bg.place(x=0, y=0, relwidth=1, relheight=1)

        # center-bottom launch button
        btn_img_path = os.path.join(os.path.dirname(__file__), "buttons", "initiate_btn.png")
        self.initiate_btn_img = tk.PhotoImage(file=btn_img_path).subsample(2,2)

        initiate_btn = tk.Button(
            self.root,
            image=self.initiate_btn_img,
            borderwidth=0,
            bg="black",
            activebackground="black",
            command=self.terminal_screen
        )
        initiate_btn.place(relx=0.5, rely=0.88, anchor="center")

  
    # PAGE 2: TERMINAL SCREEN UI
    def terminal_screen(self):
        self.wipe()

        # animated background gif for second page
        gif_path = os.path.join(os.path.dirname(__file__), "backgrounds", "terminal_bg.gif")
        self.bg2 = AnimatedGIF(self.root, gif_path)
        self.bg2.place(x=0, y=0, relwidth=1, relheight=1)

        # reset joke button state
        self.first_time = True

        # system menu button (☰)
        sys_btn = tk.Button(
            self.root,
            text="☰",
            font=("Consolas", 12, "bold"),
            fg="black",
            bg="#00E5FF",
            command=self.system_menu
        )
        sys_btn.place(x=460, y=10)

        # Boot-up terminal lines (cyan hacker style)
        boot_lines = (
            "<< INITIALIZING ALEXA HUMOR CORE >>\n"
            "<< LOADING JOKE RETRIEVAL MATRIX >>\n"
            "<< VERIFYING LAUGHTER SUBSYSTEM >>\n"
            "<< STATUS: ONLINE >>"
        )

        self.terminal_display = tk.Label(
            self.root,
            text=boot_lines,
            font=("Consolas", 13),
            fg="#00E5FF",        
            bg="black",
            justify="left",
            wraplength=600
        )
        self.terminal_display.place(relx=0.14, rely=0.40)


        # LOAD button images
        joke1_first_img_path = os.path.join(os.path.dirname(__file__), "buttons", "joke_first.png")
        joke2_btn_img_path   = os.path.join(os.path.dirname(__file__), "buttons", "joke_second.png")
        punch_btn_img_path   = os.path.join(os.path.dirname(__file__), "buttons", "punch_btn.png")

        self.joke_first_img = tk.PhotoImage(file=joke1_first_img_path).subsample(4,4)
        self.joke_second_img = tk.PhotoImage(file=joke2_btn_img_path).subsample(3,3)
        self.punch_btn_img = tk.PhotoImage(file=punch_btn_img_path).subsample(3,3)


        # --- FIRST JOKE BUTTON (appears only once) ---
        self.joke_btn_first = tk.Button(
            self.root,
            image=self.joke_first_img,
            borderwidth=0,
            bg="black",
            activebackground="black",
            command=self.handle_first_joke
        )
        self.joke_btn_first.place(x=101, y=354)

        # --- SECOND JOKE BUTTON (hidden initially) ---
        self.joke_btn_second = tk.Button(
            self.root,
            image=self.joke_second_img,
            borderwidth=0,
            bg="black",
            activebackground="black",
            command=self.handle_joke_button
        )
        self.joke_btn_second.place_forget()     

        # --- PUNCHLINE BUTTON ---
        self.punch_btn = tk.Button(
            self.root,
            image=self.punch_btn_img,
            borderwidth=0,
            bg="black",
            activebackground="black",
            command=self.display_punchline
        )
        self.punch_btn.place(x=265, y=355)


    # JOKE HANDLING FUNCTIONS
    def handle_first_joke(self):
        """Runs only once → fetch joke, then swap to NEXT JOKE button."""
        self.display_setup()

        # Hide first joke button    
        self.joke_btn_first.place_forget()

        # Show second joke button
        self.joke_btn_second.place(x=90, y=350)

        self.first_time = False



    def handle_joke_button(self):
        """Handles NEXT JOKE button only."""
        self.display_setup()


    def display_setup(self):
        """Pick a random joke and show its setup text."""
        self.current_setup, self.current_punchline = random.choice(self.jokes)
        self.terminal_display.config(
            text=f"<< JOKE RETRIEVED >>\n\n{self.current_setup}",
            fg="#00E5FF",
            wraplength=360,
            justify="left"      
        )


    def display_punchline(self):
        """Display punchline of the current joke."""
        self.terminal_display.config(
            text=f"{self.current_setup}\n\n> {self.current_punchline}",
            fg="#00E5FF",
            wraplength=360,
            justify='left'
        )

    # SYSTEM MENU POPUP
    def system_menu(self):
        menu = tk.Toplevel(self.root)
        menu.title("System Menu")
        menu.geometry("260x160")
        menu.config(bg="black")

        tk.Label(
            menu,
            text="SYSTEM OPTIONS",
            font=("Consolas", 12, "bold"),
            fg="#00E5FF",
            bg="black"
        ).pack(pady=10)

        tk.Button(
            menu,
            text="Restart",
            font=("Consolas", 11, "bold"),
            fg="black",
            bg="#00E5FF",
            width=14, 
            command=lambda: [menu.destroy(), self.splash_screen()]
        ).pack(pady=8)

        tk.Button(
            menu,
            text="Quit",
            font=("Consolas", 11, "bold"),
            fg="black",
            bg="#00E5FF",
            width=14,
            command=self.root.quit
        ).pack(pady=5)


# RUN APPLICATION
root = tk.Tk()
JokeMatrix(root)
root.mainloop()
