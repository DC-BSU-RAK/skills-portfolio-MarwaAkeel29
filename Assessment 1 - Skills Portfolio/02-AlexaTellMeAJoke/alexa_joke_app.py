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
        self.root.geometry("550x500")
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
        gif_path = os.path.join(os.path.dirname(__file__), "hacker_bg.gif")
        self.bg = AnimatedGIF(self.root, gif_path)
        self.bg.place(x=0, y=0, relwidth=1, relheight=1)

        # center-bottom launch button
        btn_img_path = os.path.join(os.path.dirname(__file__), "enter_btn.png")
        self.enter_btn_img = tk.PhotoImage(file=btn_img_path)

        launch_btn = tk.Button(
            self.root,
            image=self.enter_btn_img,
            borderwidth=0,
            bg="black",
            activebackground="black",
            command=self.terminal_screen
        )
        launch_btn.place(relx=0.5, rely=0.88, anchor="center")

  
    # PAGE 2: TERMINAL SCREEN UI
    def terminal_screen(self):
        self.wipe()

        # animated background gif for second page
        gif_path = os.path.join(os.path.dirname(__file__), "terminal_bg.gif")
        self.bg2 = AnimatedGIF(self.root, gif_path)
        self.bg2.place(x=0, y=0, relwidth=1, relheight=1)

        # reset joke button state
        self.first_time = True

        # Top hacker header
        tk.Label(
            self.root,
            text=">>> HACKER JOKE TERMINAL ONLINE",
            font=("Consolas", 16, "bold"),
            fg="#00FF00",
            bg="black"
        ).pack(pady=10)

        # system menu button (☰)
        sys_btn = tk.Button(
            self.root,
            text="☰",
            font=("Consolas", 14, "bold"),
            fg="black",
            bg="#00FF00",
            command=self.system_menu
        )
        sys_btn.place(x=10, y=10)

        # central terminal label
        self.terminal_display = tk.Label(
            self.root,
            text="Press 'Alexa tell me a Joke' to begin...",
            font=("Consolas", 14),
            fg="#00FF00",
            bg="black",
            wraplength=600,
            justify="left"
        )
        self.terminal_display.pack(pady=60)

        # button section (bottom)
        btn_frame = tk.Frame(self.root, bg="black")
        btn_frame.pack(side="bottom", pady=30)

        # LOAD button images
        joke_btn_img_path = os.path.join(os.path.dirname(__file__), "joke_btn.png")
        punch_btn_img_path = os.path.join(os.path.dirname(__file__), "punch_btn.png")

        self.joke_btn_img = tk.PhotoImage(file=joke_btn_img_path)
        self.punch_btn_img = tk.PhotoImage(file=punch_btn_img_path)

        # joke button
        self.joke_btn = tk.Button(
            btn_frame,
            image=self.joke_btn_img,
            borderwidth=0,
            bg="black",
            activebackground="black",
            command=self.handle_joke_button
        )
        self.joke_btn.grid(row=0, column=0, padx=20)

        # punchline button
        punch_btn = tk.Button(
            btn_frame,
            image=self.punch_btn_img,
            borderwidth=0,
            bg="black",
            activebackground="black",
            command=self.display_punchline
        )
        punch_btn.grid(row=0, column=1, padx=20)


    # JOKE HANDLING FUNCTIONS
    def handle_joke_button(self):
        """Controls the button changing: first time -> next joke."""
        self.display_setup()

        # After first click, change text
        if self.first_time:
            self.joke_btn.config(text="Next Joke")
            self.first_time = False

    def display_setup(self):
        """Pick a random joke and show its setup text."""
        self.current_setup, self.current_punchline = random.choice(self.jokes)
        self.terminal_display.config(text=self.current_setup)

    def display_punchline(self):
        """Display punchline of the current joke."""
        self.terminal_display.config(
            text=f"{self.current_setup}\n\n> {self.current_punchline}"
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
            fg="#00FF00",
            bg="black"
        ).pack(pady=10)

        tk.Button(
            menu,
            text="Restart",
            font=("Consolas", 11, "bold"),
            fg="black",
            bg="#00FF00",
            width=14,
            command=lambda: [menu.destroy(), self.splash_screen()]
        ).pack(pady=8)

        tk.Button(
            menu,
            text="Quit",
            font=("Consolas", 11, "bold"),
            fg="black",
            bg="#00FF00",
            width=14,
            command=self.root.quit
        ).pack(pady=5)


# RUN APPLICATION
root = tk.Tk()
JokeMatrix(root)
root.mainloop()
