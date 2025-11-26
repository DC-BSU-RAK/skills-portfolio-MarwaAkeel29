import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageTk, ImageSequence
import random
import os
import pygame


# Class to load and animate GIF frames
class AnimatedGIF(tk.Label):

    def __init__(self, parent, gif_path=None, frames=None):
        # Initialize GIF widget (load from file or use preloaded frames)

        self.frames = []

        if frames:  
            # Use preloaded frames
            self.frames = frames
        elif gif_path:  
            # Load from file
            gif = Image.open(gif_path)
            for frame in ImageSequence.Iterator(gif):
                duration = frame.info.get('duration', 100)  # default 100ms
                self.frames.append((ImageTk.PhotoImage(frame.convert("RGBA")), duration))
        else:
            # No valid source provided
            raise ValueError("Either gif_path or frames must be provided.")

        # Set first frame on label
        super().__init__(parent, image=self.frames[0][0], borderwidth=0) # Label holds GIF frames
        self.idx = 0 # Current frame index
        self.animate() # Start animation loop

    def animate(self):
        # Display next frame in loop
        frame, duration = self.frames[self.idx] # Retrieve next frame
        self.config(image=frame)  # Display current frame
        self.idx = (self.idx + 1) % len(self.frames) # Loop frames continuously
        self.after(duration, self.animate)  # Schedule next frame update

    @staticmethod
    def preload_gif(gif_path):
        # Preload frames from GIF file to memory
        frames = []
        gif = Image.open(gif_path)
        for frame in ImageSequence.Iterator(gif):
            duration = frame.info.get('duration', 100)
            frames.append((ImageTk.PhotoImage(frame.convert("RGBA")), duration))
        return frames


# Main class for the Math Nebula game interface and logic
class MathNebula:

    # Initialization
    def __init__(self):
        self.root = tk.Tk() # Main window for entire game
        self.root.title("Mind Matrix: Space Arithmetic Quest") # Window title
        self.root.geometry("600x600") # Fixed window size for layout stability
        self.root.config(bg="#0B0C10") # Sets space-themed dark background
        self.root.resizable(False, False) # Prevents unwanted resizing


        self.root.protocol("WM_DELETE_WINDOW", self.quit_game)  # Ensures clean shutdown

        # chosen space rank/title (no real-name)
        self.space_title = "Cadet"   # default; will be overwritten by selection

        # Game state trackers
        self.mission_mode = "" # Stores difficulty level chosen
        self.current_question = 0 # Tracks active question index
        self.current_score = 0 # Stores accumulated score
        self.total_questions = 10 # Fixed number of challenges
        self.num_a = 0 # First random operand
        self.num_b = 0 # Second random operand
        self.operator_symbol = "" # Current + or - operator
        self.attempt_count = 0 # Tracks retries for scoring rules

        # Widgets that change during play
        self.mission_progress = None # Progress bar reference
        self.pilot_entry = None # Input field for answers
        self.feedback_label = None # User feedback text

        # Asset root folders
        self.script_dir = os.path.dirname(__file__) # Base location of script
        self.bg_dir = os.path.join(self.script_dir, "backgrounds") # Background images
        self.btn_dir = os.path.join(self.script_dir, "buttons") # Button images
        self.snd_dir = os.path.join(self.script_dir, "sounds") # Sound effects

        # Preload all GIFs once
        self.gifs = {}  # Stores GIF frames for reuse
        gif_names = [
            "bg_launch.gif",
            "mission_briefing.gif",
            "flight_bg.gif",
            "quiz_bg.gif",
            "results_bg.gif"
        ]

        for name in gif_names:
            path = os.path.join(self.bg_dir, name)
            frames = AnimatedGIF.preload_gif(path)  # preload frames from disk
            self.gifs[name] = frames  # store frames only, not Label yet


        # Initialize pygame mixer
        pygame.mixer.init()

        # Load background music
        bg_music_path = os.path.join(self.snd_dir, "space_ambience.mp3")
        pygame.mixer.music.load(bg_music_path)  # Load ambient music
        pygame.mixer.music.play(-1)  # loop forever
        pygame.mixer.music.set_volume(0.3) # Balanced background volume

        # Load sounds
        self.click_sound = pygame.mixer.Sound(os.path.join(self.snd_dir, "click.mp3")) # UI click
        self.correct_sound = pygame.mixer.Sound(os.path.join(self.snd_dir, "correct.mp3")) # Right answer tone
        self.wrong_sound = pygame.mixer.Sound(os.path.join(self.snd_dir, "wrong.mp3")) # Wrong answer alert
        self.game_sound = pygame.mixer.Sound(os.path.join(self.snd_dir, "game.wav"))  # Menu navigation effect


    def choose_title_screen(self):
        # Popup for rank selection
        title_win = tk.Toplevel(self.root)
        title_win.title("Select Space Rank")
        title_win.geometry("240x200") # Compact size for simple selection
        title_win.resizable(False, False)  # Prevent resizing

        # Center popup relative to main window
        self.root.update_idletasks()
        x = self.root.winfo_x() + (self.root.winfo_width() // 2) - 210
        y = self.root.winfo_y() + (self.root.winfo_height() // 2) - 190
        title_win.geometry(f"+{x}+{y}") # Center popup over main window

        # Load PNG background
        bg_path = os.path.join(self.bg_dir, "bg_launch.png")
        bg_img = ImageTk.PhotoImage(Image.open(bg_path).resize((420, 380))) # Resize to fit popup

        bg_label = tk.Label(title_win, image=bg_img) # Static background
        bg_label.image = bg_img
        bg_label.place(x=0, y=0, relwidth=1, relheight=1)


        SPACE_TITLES = [
            "Commander",   # classic top rank
            "Captain",   # familiar, strong
            "Navigator",   # skilled in direction
            "Astrogator",  # sci-fi term for star navigator
            "Cosmonaut",  # astronaut variant
            "Stellar",    # general space operative
            "Quantum",   # futuristic, techy
            "Vanguard",   # front-line explorer
            "Scout",    # reconnaissance role
            "Cadet"    # beginner rank
        ]

        # Stores selected title
        self.title_var = tk.StringVar(value=self.space_title)  

        dropdown = ttk.Combobox(
            title_win, 
            textvariable=self.title_var,
            values=SPACE_TITLES,
            font=("Consolas", 13),
            state="readonly", # Prevents typing unwanted values
            width=18,
            height=20
        )
        dropdown.place(relx=0.5, rely=0.50, anchor="center")  # Centers dropdown


        def save_and_close():
            self.space_title = self.title_var.get()  # Store chosen rank
            self.click_sound.play()  # UI feedback sound
            title_win.destroy()  # Close popup
            self.mission_instructions()  # Load next screen

        # Load continue button
        continue_img = self.load_image(self.btn_dir, "continue_btn.png", (3, 2))

        continue_btn = tk.Button(
            title_win,  # Parent is the popup window
            image=continue_img,
            command=save_and_close,  # call the inner function
            borderwidth=0,
            bg="#0B0C10",
            activebackground="#0B0C10"
        )
        continue_btn.image = continue_img
        continue_btn.place(relx=0.5, rely=0.75, anchor="center")

    def save_title_and_proceed(self):
        self.space_title = self.title_var.get() # Store rank explicitly
        self.mission_instructions()  # Continue workflow


    # Utility Helpers
    def add_profile_button(self):
        profile_img = self.load_image(self.btn_dir, "astronaut_profile.png", (2, 2))  # Small profile icon

        if hasattr(self, "profile_btn"):
            self.profile_btn.destroy()  # Remove previous button to avoid duplicates

        self.profile_btn = tk.Button(
            self.root,
            image=profile_img,
            command=self.open_profile_window, # Open player stats window
            borderwidth=0,
            bg="#0B0C10",
            activebackground="#0B0C10"
        )
        self.profile_btn.image = profile_img
        self.profile_btn.place(relx=0.99, rely=0.01, anchor="ne") # Top-right position

    def open_profile_window(self):
        profile_win = tk.Toplevel(self.root) # Small popup for profile info
        profile_win.title("Profile")
        profile_win.geometry("400x300")
        profile_win.resizable(False, False)

        # Background PNG
        bg_path = os.path.join(self.bg_dir, "profile_bg.png")
        bg_img = ImageTk.PhotoImage(Image.open(bg_path).resize((400, 300))) # Fit window size

        bg_label = tk.Label(profile_win, image=bg_img)  # Profile background
        bg_label.image = bg_img
        bg_label.place(x=0, y=0, relwidth=1, relheight=1)

        # Space Title / Rank 
        tk.Label(
            profile_win,
            text=f"Rank:{self.space_title}",
            font=("Consolas", 17, "bold"),
            fg="#66FCF1",
            bg="#000000"
        ).place(x=160, y=60) # Shows chosen rank

        # Score Display 
        tk.Label(
            profile_win,
            text=f"Score:{self.current_score}",
            font=("Consolas", 17, "bold"),
            fg="#66FCF1",
            bg="#000000"
        ).place(x=160, y=100) # Shows current score


        # Sound Toggle
        mute_img = self.load_image(self.btn_dir, "mute.png", (3, 3))  # Mute icon
        unmute_img = self.load_image(self.btn_dir, "unmute.png", (3, 3)) # Unmute icon

        self.is_muted = getattr(self, "is_muted", False)  # Track sound state

        def toggle_sound():
            if self.is_muted:
                pygame.mixer.music.set_volume(0.3) # Restore music
                sound_btn.config(image=mute_img)
                self.is_muted = False
            else:
                pygame.mixer.music.set_volume(0) # Silence game audio
                sound_btn.config(image=unmute_img)
                self.is_muted = True

        sound_btn = tk.Button(
            profile_win,
            image=mute_img if not self.is_muted else unmute_img, # Correct icon state
            command=toggle_sound,  # Toggle sound on click
            borderwidth=0,
            bg="#0B0C10",
            activebackground="#0B0C10"
        )
        sound_btn.place(relx=0.90, rely=0.07, anchor="ne")
    
    # Remove all widgets for new screen load
    def clear_screen(self):
        for w in self.root.winfo_children():
            w.destroy() 


    def animate_progress(self, target):
        current = self.mission_progress["value"]  # Current bar value
        if current < target:
            self.mission_progress["value"] += 1
            self.root.after(10, lambda: self.animate_progress(target))  # gradual update


    def load_image(self, folder, name, sub=None):
        path = os.path.join(folder, name)
        img = tk.PhotoImage(file=path)  # Load PNG image
        if sub:
            img = img.subsample(*sub)  # Resize via subsampling
        return img
    
    
    # Home Screen
    def launch_portal(self):
        self.clear_screen() # Reset screen for main menu

        bg = AnimatedGIF(
            self.root,
            frames=self.gifs["bg_launch.gif"]) # Play animated launch background
        bg.place(x=0, y=0, relwidth=1, relheight=1)
        self.bg_launch_ref = bg  # Prevent garbage collection

        # Shrink start button
        start_img = self.load_image(self.btn_dir, "start_btn.png", (4, 4)) 

        # Shrink exit button
        exit_img = self.load_image(self.btn_dir, "exit_btn.png", (4, 4))  

        # Add profile icon
        self.add_profile_button() 

        start_btn = tk.Button(
            self.root, 
            image=start_img, 
            command=lambda: [self.game_sound.play(), self.choose_title_screen()],  # Navigate to title screen
            borderwidth=0, 
            bg="#0B0C10", 
            activebackground="#0B0C10"
        )
        start_btn.image = start_img
        start_btn.place(relx=0.15, rely=0.97, anchor="sw") # Bottom left

        exit_btn = tk.Button(
            self.root, 
            image=exit_img, 
            command=lambda: [self.game_sound.play(), self.root.after(200, self.quit_game)], # Quit game
            borderwidth=0, 
            bg="#0B0C10", 
            activebackground="#0B0C10"
        )
        exit_btn.image = exit_img
        exit_btn.place(relx=0.85, rely=0.97, anchor="se")  # Bottom right

    # Mission Instructions
    def mission_instructions(self):
        self.clear_screen()  # Load fresh screen

        bg = AnimatedGIF(
            self.root, 
            frames=self.gifs["mission_briefing.gif"]) # Animated briefing background
        bg.place(x=0, y=0, relwidth=1, relheight=1)
        self.bg_brief_ref = bg

        # Profile accessible anytime
        self.add_profile_button() 

        # Explore button
        explore_img = self.load_image(self.btn_dir, "explore_btn.png", (3, 3)) 
        # Back button
        back_img = self.load_image(self.btn_dir, "back_btn.png", (3, 4)) 

        explore_btn = tk.Button(
            self.root, 
            image=explore_img, 
            command=lambda: [self.click_sound.play(), self.select_difficulty()], # Go to difficulty menu
            borderwidth=0, 
            bg="#0B0C10", 
            activebackground="#0B0C10"
        )
        explore_btn.image = explore_img
        explore_btn.place(relx=0.72, rely=0.90, anchor="center")  # Bottom center-right

        back_btn = tk.Button(
            self.root, 
            image=back_img, 
            command=lambda: [self.click_sound.play(), self.launch_portal()], # Return to main screen
            borderwidth=0, 
            bg="#0B0C10", 
            activebackground="#0B0C10"
        )
        back_btn.image = back_img
        back_btn.place(relx=0.29, rely=0.90, anchor="center")  # Bottom center-left

    # Difficulty Select
    def select_difficulty(self):
        self.clear_screen() # Refresh for difficulty selection

        bg = AnimatedGIF(
            self.root, 
            frames=self.gifs["flight_bg.gif"]) # Flying animation backdrop
        bg.place(x=0, y=0, relwidth=1, relheight=1)
        self.bg_flight_ref = bg

        # Hard mode planet
        advance = self.load_image(self.btn_dir, "planet_advance.png", (2, 2))  
        # Medium mode planet
        moderate = self.load_image(self.btn_dir, "planet_moderate.png", (2, 2)) 
        # Easy mode planet
        easy = self.load_image(self.btn_dir, "planet_easy.png", (2, 2)) 

        # Perfectly aligned buttons
        btnA = tk.Button(
            self.root, 
            image=advance, 
            command=lambda: [self.click_sound.play(), self.start_mission("Advanced")], # Hard mode start
            bd=0, 
            highlightthickness=0, 
            activebackground="#000000", 
            bg="#000000")
        btnA.image = advance
        btnA.place(x=55, y=115) # Pre-aligned coordinates

        btnM = tk.Button(
            self.root, 
            image=moderate, 
            command=lambda: [self.click_sound.play(), self.start_mission("Moderate")], # Medium mode start
            bd=0, 
            highlightthickness=0, 
            activebackground="#000000", 
            bg="#000000")
        btnM.image = moderate
        btnM.place(x=130, y=375)

        btnE = tk.Button(
            self.root, 
            image=easy, 
            command=lambda: [self.click_sound.play(), self.start_mission("Easy")],  # Easy mode start
            bd=0, 
            highlightthickness=0, 
            activebackground="#000000", 
            bg="#000000")
        btnE.image = easy
        btnE.place(x=355, y=485)

        back_img = self.load_image(self.btn_dir, "back_btn.png", (4, 4))
        back_btn = tk.Button(
            self.root, 
            image=back_img, 
            command=lambda: [self.game_sound.play(), self.mission_instructions()],  # Return to briefing
            borderwidth=0, 
            bg="#0B0C10", 
            activebackground="#0B0C10"
        )
        back_btn.image = back_img
        back_btn.place(relx=0.97, rely=0.98, anchor="se") # Bottom-right

    # Mission Start
    def start_mission(self, mode):
        self.mission_mode = mode  # Store current difficulty mode
        self.current_question = 0    # Reset question counter
        self.current_score = 0   # Reset score for new run
        self.next_question()  # Begin mission

    # Random Values
    def random_values(self):
        if self.mission_mode == "Easy":
            return random.randint(1, 9), random.randint(1, 9) # Simple numbers
        elif self.mission_mode == "Moderate":
            return random.randint(10, 99), random.randint(10, 99) # Medium numbers
        return random.randint(1000, 9999), random.randint(1000, 9999) # Hard numbers

    # HUD Display
    def display_top_info(self):
        top = tk.Frame(self.root, bg="") # Container for HUD
        top.pack(fill="x", pady=5, padx=15)
        
        left = tk.Frame(top, bg="") # Left HUD section
        left.pack(side="left")

         # Display difficulty level
        tk.Label(
            left,
            text=f"Mode: {self.mission_mode}", 
            font=("Consolas", 18, "bold"),
            fg="#66FCF1", 
            bg="#000000").pack()
        
         # Display current score
        tk.Label(
            left, 
            text=f"Score: {self.current_score}", 
            font=("Consolas", 18, "bold"),
            fg="#66FCF1", 
            bg="#000000").pack()

        right = tk.Frame(top, bg="") # Right HUD section
        right.pack(side="right")

        # Show question progress
        tk.Label(
            right, 
            text=f"Q {self.current_question + 1}/{self.total_questions}",
            font=("Consolas", 18, "bold"), 
            fg="#66FCF1", 
            bg="#0B0C10").pack()

        # Progress tracker bar
        self.mission_progress = ttk.Progressbar(
            right, 
            orient="horizontal",
            length=165, 
            mode="determinate")
        self.mission_progress.pack(pady=9, padx=(0, 7))
        self.animate_progress((self.current_question / self.total_questions) * 100)

    # Question Screen
    def next_question(self):
        self.clear_screen() # Reset screen layout

        bg = AnimatedGIF(
            self.root, 
            frames=self.gifs["quiz_bg.gif"]) # Animated quiz background
        bg.place(x=0, y=0, relwidth=1, relheight=1)
        self.bg_quiz_ref = bg

        self.display_top_info() # Show score + progress bar

        self.num_a, self.num_b = self.random_values() # Generate operands
        self.operator_symbol = random.choice(["+", "-"])  # Random operator
        self.attempt_count = 0 # Reset try counter per question

        hud = tk.Frame(self.root, bg="#000000") # HUD container
        hud.place(relx=0.5, rely=0.49, anchor="center")

        # Show math question
        tk.Label(
            hud,
            text=f"{self.num_a} {self.operator_symbol} {self.num_b} = ?",
            font=("Consolas", 27, "bold"),
            fg="#66FCF1",
            bg="#000000"
        ).pack(pady=(20, 18))

         # Input box for answers
        self.pilot_entry = tk.Entry(
            hud, 
            font=("Consolas", 20), 
            justify="center",
            width=12, 
            relief="flat", 
            bg="#485B63", 
            fg="#66FCF1",
            insertbackground="#66FCF1"
        )
        self.pilot_entry.pack(pady=(5, 14))

         # Area for hints and correctness
        self.feedback_label = tk.Label(
            hud, 
            text="", 
            font=("Consolas", 14),
            fg="#C5C6C7", 
            bg="#000000", 
            wraplength=260, 
            justify="center"
        )
        self.feedback_label.pack(pady=(5, 10))

        submit_img = self.load_image(self.btn_dir, "submit_btn.png", (2, 2)) # Submit button
        submit_btn = tk.Button(
            self.root, 
            image=submit_img, 
            command=lambda: [self.click_sound.play(), self.verify_answer()],  # play click sound first, Validate answer
            borderwidth=0,
            bg="#000000", 
            activebackground="#000000"
        )
        submit_btn.image = submit_img
        submit_btn.place(relx=0.4, rely=0.74, x=9, y=3)


    # Answer Check
    def verify_answer(self):
        inp = self.pilot_entry.get().strip() # Read user input

        if inp == "":
            self.feedback_label.config(text="Enter a number before submitting, cadet!", fg="#FF6961")
            self.wrong_sound.play()  # Alert for no input
            return
        
        try:
            inp = int(inp) # Convert input to integer
            correct = eval(f"{self.num_a} {self.operator_symbol} {self.num_b}") # calculation

            if inp == correct:
                self.current_score += 10 if self.attempt_count == 0 else 5  # Score logic
                self.feedback_label.config(text="Stellar precision!", fg="#45A29E")
                self.correct_sound.play()  # play correct sound
                self.root.after(1200, self.move_next)  # Auto-continue
                return

            self.attempt_count += 1  # One try consumed
            self.wrong_sound.play()  # play wrong sound

            if self.attempt_count == 1:
                self.feedback_label.config(text="Orbit misaligned, try again!", fg="#FF6961")
            else:
                self.feedback_label.config(text="Mission failed for this challenge.", fg="#FF6961")
                self.root.after(1200, self.move_next)

        except ValueError:
            self.feedback_label.config(text="Numbers only, space traveler!", fg="#FF6961")
            self.wrong_sound.play()   # Non-number input error

    # Next Question or Results                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                 
    def move_next(self):
        self.current_question += 1 # Advance question count
        if self.current_question < self.total_questions:
            self.next_question() # Continue mission
        else:
            self.display_results() # Show final results

    # Results Screen
    def display_results(self):
        self.clear_screen() # Reset screen layout

        bg = AnimatedGIF(self.root, frames=self.gifs["results_bg.gif"]) # Animated results backdrop
        bg.place(x=0, y=0, relwidth=1, relheight=1)
        self.bg_results_ref = bg

        self.add_profile_button() # Access profile even at end

        # Display score
        tk.Label(
            self.root, 
            text=f"Final Score: {self.current_score}/100",
            font=("Consolas", 20, "bold"), 
            fg="#66FCF1", 
            bg="#000000"
        ).place(relx=0.5, rely=0.47, anchor="center")

        if self.current_score >= 90:
            msg = "MISSION REPORT: Excellent control, Commander."
        elif self.current_score >= 70:
            msg = "COMMAND UPDATE: Strong navigation detected."
        elif self.current_score >= 50:
            msg = "STATUS: Acceptable trajectory. Further training advised."
        else:
            msg = "ALERT: System recalibration required. Debrief pending."

        # Performance message
        tk.Label(
            self.root, 
            text=msg, 
            font=("Consolas", 14, "bold"),
            fg="#C5C6C7", 
            bg="#000000", 
            wraplength=420, 
            justify="center"
        ).place(relx=0.5, rely=0.58, anchor="center")

        # Retry button
        play_img = self.load_image(self.btn_dir, "relaunch_btn.png", (3, 3)) 
        # Quit button 
        quit_img = self.load_image(self.btn_dir, "space_exit_btn.png", (3, 3)) 

        play_btn = tk.Button(
            self.root, 
            image=play_img, 
            command=lambda: [self.game_sound.play(), self.launch_portal()],  # click sound, Restart game
            borderwidth=0, 
            highlightthickness=0, 
            bg="#000000", 
            activebackground="#000000"
        )
        play_btn.image = play_img
        play_btn.place(relx=0.25, rely=0.93, anchor="center")

        quit_btn = tk.Button(
            self.root, 
            image=quit_img, 
            command=lambda: [self.game_sound.play(), self.root.after(150, self.quit_game)],  # click sound, Exit game
            borderwidth=0, 
            highlightthickness=0, 
            bg="#FFFFFF", 
            activebackground="#000000" 
        )
        quit_btn.image = quit_img
        quit_btn.place(relx=0.75, rely=0.93, anchor="center")

    # Stop music and close game
    def quit_game(self):
        pygame.mixer.music.stop()  # Stop background music
        self.root.destroy()  # Close window safely

    # Start Game Loop
    def run(self):
        self.launch_portal() # Load home screen first
        self.root.mainloop()  # Start GUI loop


# Launch App
if __name__ == "__main__":
    MathNebula().run()  #Run game application
