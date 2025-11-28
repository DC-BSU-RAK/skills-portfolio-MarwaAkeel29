import tkinter as tk # Main GUI framework for building all screens and buttons
from tkinter import messagebox #Popup for system messages
# Handles PNG & GIF loading + frame extraction for animated backgrounds
from PIL import Image, ImageTk, ImageSequence
# Picks random jokes + laughter sounds for unpredictable humor
import random
# Plays all sound effects (clicks, laughs, startup audio)
import pygame
# Used for building safe file paths for images, sounds, and icons
import os


# Handles GIF animation for all screens
class AnimatedGIF(tk.Label):

    def __init__(self, parent, gif_path):

        # Handles GIF animation for all screens
        gif = Image.open(gif_path)
        self.frames = []
        for frame in ImageSequence.Iterator(gif):
            img = ImageTk.PhotoImage(frame.copy().convert("RGBA"))
            duration = frame.info.get("duration", 80) # keeps original GIF timing
            self.frames.append((img, duration))

         # super() places the FIRST frame onto the label immediately
        super().__init__(parent, image=self.frames[0][0], borderwidth=0)

        self.idx = 0   # track frame pointer for animation loop
        self.animate() # start smooth autoplay

    def animate(self):
         # cycling frames gives the glitchy/hacker effect
        frame, delay = self.frames[self.idx]
        self.config(image=frame)
        self.idx = (self.idx + 1) % len(self.frames)
        self.after(delay, self.animate)

# created main class for the joke machine interface
class JokeMatrix:

    def __init__(self, root):
        self.root = root
        self.root.title("Joke Terminal v1.0")
        self.root.geometry("500x500")
        self.root.config(bg="black")
        pygame.mixer.init()

        #Window Icon (Favicon)
        icon_path = os.path.join(os.path.dirname(__file__), "icon", "Alexa.ico")
        try:
            self.root.iconbitmap(icon_path)
        except Exception:
            pass

        # slight startup delay → feels like a "boot sequence" 
        startup_sound_path = os.path.join(os.path.dirname(__file__), "sounds", "witch.mp3")
        self.root.after(2000, lambda: pygame.mixer.Sound(startup_sound_path).play())

        # slight startup delay → feels like a "boot sequence"
        sound_path = os.path.join(os.path.dirname(__file__), "sounds", "click.mp3")
        self.btn_sound = pygame.mixer.Sound(sound_path)

        # random laughs to keep punchline reactions fun
        self.laugh_sounds = [
        pygame.mixer.Sound(os.path.join(os.path.dirname(__file__), "sounds", "laugh1.mp3")),
        pygame.mixer.Sound(os.path.join(os.path.dirname(__file__), "sounds", "laugh2.mp3")),
        pygame.mixer.Sound(os.path.join(os.path.dirname(__file__), "sounds", "laugh3.mp3")),
        pygame.mixer.Sound(os.path.join(os.path.dirname(__file__), "sounds", "laugh4.mp3")),
        ]

        # store jokes
        self.jokes = []
        self.current_setup = ""
        self.current_punchline = ""

        # first_time determines whether to show FIRST joke button or NEXT button
        self.first_time = True

        # load jokes from txt file
        self.load_jokes()

        # open splash screen
        self.splash_screen()

    # load icon image
    def load_image(self, folder, name, sub=None):
        path = os.path.join(folder, name)
        img = tk.PhotoImage(file=path)  # Load image
        if sub:
            img = img.subsample(*sub)  # Resize via subsampling
        return img        


    # load all jokes from text file
    def load_jokes(self):
        """Reads jokes from randomJokes.txt and stores them."""
        file_path = os.path.join(os.path.dirname(__file__), "randomJokes.txt")

        with open(file_path, "r", encoding="utf-8") as file:
            for line in file:
                if "?" in line: # quick validation for joke structure
                    setup, punchline = line.strip().split("?")
                    self.jokes.append((setup + "?", punchline))

    def speak(self, text):
        """Convert text to audio & play non-blocking."""
        try:
            from gtts import gTTS
            tts = gTTS(text=text, lang="en")
            audio_path = os.path.join(os.path.dirname(__file__), "temp_joke.mp3")
            tts.save(audio_path)
            pygame.mixer.Sound(audio_path).play()  # NON-BLOCKING
        except Exception as e:
            print("Voice error:", e)


    # clear all widgets from screen
    def wipe(self):
        # clears screen before switching pages → prevents widget stacking
        for w in self.root.winfo_children():
            w.destroy()

    # play button click sound
    def play_click(self):
        self.btn_sound.play()

    # play random laugh sound
    def play_random_laugh(self):
        random.choice(self.laugh_sounds).play()            


    # display animated splash screen
    def splash_screen(self):
        self.wipe()

        # reset for next session
        self.first_time = True

        # animated background gif
        gif_path = os.path.join(os.path.dirname(__file__), "backgrounds", "hacker_bg.gif")
        self.bg = AnimatedGIF(self.root, gif_path)
        self.bg.place(x=0, y=0, relwidth=1, relheight=1)

        # initiate button (first user interaction)
        btn_img_path = os.path.join(os.path.dirname(__file__), "buttons", "initiate_btn.png")
        self.initiate_btn_img = tk.PhotoImage(file=btn_img_path).subsample(3,3)

        initiate_btn = tk.Button(
            self.root,
            image=self.initiate_btn_img,
            borderwidth=0,
            bg="black",
            activebackground="black",
            command=lambda: [pygame.mixer.stop(), # stop intro sound before page swap
                             self.play_click(), 
                             self.terminal_screen()]
        )
        initiate_btn.place(relx=0.5, rely=0.88, anchor="center")


    # load second page terminal UI
    def terminal_screen(self):
        self.wipe()

        # animated background gif for second page
        gif_path = os.path.join(os.path.dirname(__file__), "backgrounds", "terminal_bg.gif")
        self.bg2 = AnimatedGIF(self.root, gif_path)
        self.bg2.place(x=0, y=0, relwidth=1, relheight=1)

        # reset joke button state
        self.first_time = True

        # three-line navigation menu top-left
        sys_btn = tk.Button(
            self.root,
            text="☰",
            font=("Consolas", 12, "bold"),
            fg="black",
            bg="#00E5FF",
            command=lambda:[self.play_click(), self.system_menu()]
        )
        sys_btn.place(x=10, y=10)

        # Boot-up terminal lines 
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


        #FIRST JOKE BUTTON - it will appear once
        self.joke_btn_first = tk.Button(
            self.root,
            image=self.joke_first_img,
            borderwidth=0,
            bg="black",
            activebackground="black",
            command=lambda: [self.play_click(), 
                             self.handle_first_joke()]

        )
        self.joke_btn_first.place(x=103, y=356)

        #SECOND JOKE BUTTON - hidden initially 
        self.joke_btn_second = tk.Button(
            self.root,
            image=self.joke_second_img,
            borderwidth=0,
            bg="black",
            activebackground="black",
            command=lambda: [self.play_click(), 
                             self.handle_joke_button()]
        )
        self.joke_btn_second.place_forget()     

        #PUNCHLINE BUTTON
        self.punch_btn = tk.Button(
            self.root,
            image=self.punch_btn_img,
            borderwidth=0,
            bg="black",
            activebackground="black",
            command=lambda: [
            self.play_click(),
            self.display_punchline(), 
            # small delay makes laugh feel like Audience reacting 
            self.root.after(1000, self.play_random_laugh)  
        ]
        )
        self.punch_btn.place(x=265, y=357)


    # first-time joke button logic
    def handle_first_joke(self):
        """Runs only once → fetch joke, then swap to NEXT JOKE button."""
        self.display_setup()

        # Hide first joke button    
        self.joke_btn_first.place_forget()

        # Show second joke button
        self.joke_btn_second.place(x=93, y=360)

        self.first_time = False

    # next-joke button logic
    def handle_joke_button(self):
        self.display_setup()


    # show joke setup text
    def display_setup(self):
        """Pick a random joke and show its setup text."""
        self.current_setup, self.current_punchline = random.choice(self.jokes)

        self.terminal_display.config(
            text=f"<< JOKE RETRIEVED >>\n\n{self.current_setup}",
            fg="#00E5FF",
            wraplength=360,
            justify="left"      
        )
        self.speak(self.current_setup)


    # show punchline text
    def display_punchline(self):
    
        self.terminal_display.config(
            text=f"{self.current_setup}\n\n> {self.current_punchline}",
            fg="#00E5FF",
            wraplength=360,
            justify='left'
        )

        self.speak(self.current_punchline)
        self.root.after(1300, self.play_laugh_sound)



    # system menu popup window
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

        # restart → clears everything and replays startup
        tk.Button(
            menu,
            text="Restart",
            font=("Consolas", 11, "bold"),
            fg="black",
            bg="#00E5FF",
            width=14, 
            command=lambda:[self.play_click(), 
                            menu.destroy(), 
                            self.splash_screen()]
        ).pack(pady=8)

        tk.Button(
            menu,
            text="Quit",
            font=("Consolas", 11, "bold"),
            fg="black",
            bg="#00E5FF",
            width=14,
            command=lambda: [self.play_click(), 
                             self.root.quit()]
        ).pack(pady=5)

     # plays a short laughter clip after punchline (delayed)
    def play_laugh_sound(self):
        """Plays laugh sound only when called (delayed, non-blocking)."""
        try:
            laugh_path = os.path.join(os.path.dirname(__file__), "sounds", "laugh.mp3")
            pygame.mixer.Sound(laugh_path).play()
        except Exception as e:
            print("Laugh sound error:", e)


# RUN APPLICATION
root = tk.Tk()
JokeMatrix(root)
root.mainloop()
