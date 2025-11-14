import tkinter as tk
from tkinter import ttk
import random
import os

#Main Window Setup
galaxy = tk.Tk()
galaxy.title("Mind Matrix: Space Arithmetic Quest")
galaxy.geometry("600x600")
galaxy.config(bg="#0B0C10")


#Global State Values
mission_mode = ""
current_question = 0
current_score = 0
total_questions = 10
mission_progress = None
pilot_answer = None
feedback_label = None


#Quick Label Helper
def create_label(parent, text, font=("Consolas", 12), fg="#C5C6C7", pady=0, anchor=None):
    label = tk.Label(parent, text=text, font=font, fg=fg, bg="#0B0C10")
    label.pack(pady=pady, anchor=anchor)
    return label

#Quick Button Helper
def create_button(parent, text, command, pady=0):
    button = ttk.Button(parent, text=text, command=command)
    button.pack(pady=pady)
    return button

#Remove all widgets on screen
def clear_galaxy():
    for w in galaxy.winfo_children():
        w.destroy()


#Progress Bar Animation
def animate_progress(target):
    current = mission_progress["value"]
    if current < target:
        mission_progress["value"] += 1
        galaxy.after(10, lambda: animate_progress(target))


# Home (Launch Portal)
def launch_portal():
    clear_galaxy()

    script_dir = os.path.dirname(__file__)
    bg_path = os.path.join(script_dir, "backgrounds", "bg_launch.png")
    bg_image = tk.PhotoImage(file=bg_path)

    bg_label = tk.Label(galaxy, image=bg_image)
    bg_label.image = bg_image
    bg_label.place(x=0, y=0, relwidth=1, relheight=1)

    # Load start/exit button images
    start_img = tk.PhotoImage(file=os.path.join(script_dir, "buttons", "start_btn.png")).subsample(4,4)
    exit_img = tk.PhotoImage(file=os.path.join(script_dir, "buttons", "exit_btn.png")).subsample(4,4)

    # Start Mission Button
    start_button = tk.Button(
        galaxy,
        image=start_img,
        command=mission_instructions,
        borderwidth=0,
        highlightthickness=0,
        bg="#0B0C10",
        activebackground="#0B0C10",
    )
    start_button.image = start_img
    start_button.place(relx=0.15, rely=0.9, anchor="sw")

    # Exit Button
    exit_button = tk.Button(
        galaxy,
        image=exit_img,
        command=galaxy.destroy,
        borderwidth=0,
        highlightthickness=0,
        bg="#0B0C10",
        activebackground="#0B0C10",
    )
    exit_button.image = exit_img
    exit_button.place(relx=0.85, rely=0.9, anchor="se")


# Mission Instructions
def mission_instructions():
    clear_galaxy()

    script_dir = os.path.dirname(__file__)
    bg_path = os.path.join(script_dir, "backgrounds", "mission_briefing.png")
    bg_image = tk.PhotoImage(file=bg_path)

    bg_label = tk.Label(galaxy, image=bg_image)
    bg_label.image = bg_image
    bg_label.place(x=0, y=0, relwidth=1, relheight=1)

    # Load buttons
    explore_img = tk.PhotoImage(file=os.path.join(script_dir, "buttons", "explore_btn.png")).subsample(4,3)
    back_img = tk.PhotoImage(file=os.path.join(script_dir, "buttons", "back_btn.png")).subsample(4,4)

    # Continue Button
    explore_btn = tk.Button(
        galaxy,
        image=explore_img,
        bg="#0B0C10",
        activebackground="#0B0C10",
        borderwidth=0,
        highlightthickness=0,
        command=select_difficulty
    )
    explore_btn.image = explore_img
    explore_btn.place(relx=0.72, rely=0.74, anchor="center")

    # Back Button
    back_btn = tk.Button(
        galaxy,
        image=back_img,
        bg="#0B0C10",
        activebackground="#0B0C10",
        borderwidth=0,
        highlightthickness=0,
        command=launch_portal
    )
    back_btn.image = back_img
    back_btn.place(relx=0.29, rely=0.75, anchor="center")


# Difficulty Selection
def select_difficulty():
    clear_galaxy()

    script_dir = os.path.dirname(__file__)
    bg_path = os.path.join(script_dir, "backgrounds", "flight_bg.png")
    bg_image = tk.PhotoImage(file=bg_path)

    bg_label = tk.Label(galaxy, image=bg_image)
    bg_label.image = bg_image
    bg_label.place(x=0, y=0, relwidth=1, relheight=1)

    # Load planet buttons
    advance_img = tk.PhotoImage(file=os.path.join(script_dir, "buttons", "planet_advance.png")).subsample(2,2)
    moderate_img = tk.PhotoImage(file=os.path.join(script_dir, "buttons", "planet_moderate.png")).subsample(2,2)
    easy_img = tk.PhotoImage(file=os.path.join(script_dir, "buttons", "planet_easy.png")).subsample(2,2)

    # Planet Buttons
    advance_btn = tk.Button(
        galaxy, image=advance_img, bd=0, highlightthickness=0,
        activebackground="#000000",
        command=lambda: start_mission("Advanced")
    )
    advance_btn.image = advance_img   # <<< MUST ADD
    advance_btn.place(x=55, y=115)

    moderate_btn = tk.Button(
        galaxy, image=moderate_img, bd=0, highlightthickness=0,
        activebackground="#000000",
        command=lambda: start_mission("Moderate")
    )
    moderate_btn.image = moderate_img  # <<< MUST ADD
    moderate_btn.place(x=130, y=375)

    easy_btn = tk.Button(
        galaxy, image=easy_img, bd=0, highlightthickness=0,
        activebackground="#000000",
        command=lambda: start_mission("Easy")
    )
    easy_btn.image = easy_img  # <<< MUST ADD
    easy_btn.place(x=355, y=485)


    # Return Button
    return_img = tk.PhotoImage(file=os.path.join(script_dir, "buttons", "back_btn.png")).subsample(4,4)
    return_btn = tk.Button(
        galaxy,
        image=return_img,
        bg="#0B0C10",
        activebackground="#0B0C10",
        borderwidth=0,
        highlightthickness=0,
        command=mission_instructions
    )
    return_btn.image = return_img
    return_btn.place(relx=0.97, rely=0.98, anchor="se")


# Start Mission
def start_mission(level):
    global mission_mode, current_question, current_score
    mission_mode = level
    current_question = 0
    current_score = 0
    next_question()


# Random Values by Difficulty
def random_values():
    if mission_mode == "Easy":
        return random.randint(1, 9), random.randint(1, 9)
    elif mission_mode == "Moderate":
        return random.randint(10, 99), random.randint(10, 99)
    else:
        return random.randint(1000, 9999), random.randint(1000, 9999)


# HUD (Mode + Score + Progress)
def display_top_info():
    top_frame = tk.Frame(galaxy, bg="", highlightthickness=0, bd=0)
    top_frame.pack(fill="x", pady=5, padx=15)

    left_frame = tk.Frame(top_frame, bg="", highlightthickness=0, bd=0)
    left_frame.pack(side="left")

    create_label(left_frame, f"Mode: {mission_mode}", font=("Consolas", 18, "bold"), fg="#66FCF1")
    create_label(left_frame, f"Score: {current_score}", font=("Consolas", 18, "bold"), fg="#66FCF1")

    right_frame = tk.Frame(top_frame, bg="", highlightthickness=0, bd=0)
    right_frame.pack(side="right")

    create_label(right_frame, f"Q {current_question+1}/{total_questions}",
                 font=("Consolas", 18, "bold"), fg="#66FCF1")

    global mission_progress
    mission_progress = ttk.Progressbar(right_frame, orient="horizontal", length=165, mode="determinate")
    mission_progress.pack(pady=9, padx=(0,7))

    animate_progress((current_question / total_questions) * 100)


# Question + Input Screen
def next_question():
    clear_galaxy()
    global num_a, num_b, operator_symbol, pilot_entry, feedback_label, attempt_count

    script_dir = os.path.dirname(__file__)
    bg_path = os.path.join(script_dir, "backgrounds", "quiz_bg.png")
    quiz_bg = tk.PhotoImage(file=bg_path)

    bg_label = tk.Label(galaxy, image=quiz_bg)
    bg_label.image = quiz_bg
    bg_label.place(x=0, y=0, relwidth=1, relheight=1)

    display_top_info()

    # Submit Button Image
    submit_img = tk.PhotoImage(
        file=os.path.join(script_dir, "buttons", "submit_btn.png")
    ).subsample(2,2)

    hud_frame = tk.Frame(galaxy, bg="#000000")
    hud_frame.place(relx=0.5, rely=0.49, anchor="center")

    num_a, num_b = random_values()
    operator_symbol = random.choice(["+", "-"])
    attempt_count = 0

    tk.Label(
        hud_frame,
        text=f"{num_a} {operator_symbol} {num_b} = ?",
        font=("Consolas", 27, "bold"),
        fg="#66FCF1",
        bg="#000000"
    ).pack(pady=(20,18))

    pilot_entry = tk.Entry(
        hud_frame,
        font=("Consolas", 20),
        justify="center",
        width=12,
        relief="flat",
        bg="#485B63",
        fg="#66FCF1",
        insertbackground="#66FCF1"
    )
    pilot_entry.pack(pady=(5,14))

    feedback_label = tk.Label(
        hud_frame,
        text="",
        font=("Consolas", 14),
        fg="#C5C6C7",
        bg="#000000",
        wraplength=260,
        justify="center"
    )
    feedback_label.pack(pady=(5,10))

    submit_btn = tk.Button(
        galaxy,
        image=submit_img,
        command=verify_answer,
        borderwidth=0,
        highlightthickness=0,
        bg="#000000",
        activebackground="#000000"
    )
    submit_btn.image = submit_img
    submit_btn.place(relx=0.4, rely=0.74, x=9, y=3)


# Verify Answer + Attempts
def verify_answer():
    global current_score, current_question, attempt_count

    user_input = pilot_entry.get().strip()

    if user_input == "":
        feedback_label.config(text="Enter a number before submitting, cadet!", fg="#FF6961")
        return

    try:
        user_input = int(user_input)
        correct_answer = eval(f"{num_a} {operator_symbol} {num_b}")

        success_msgs = [
            "Stellar precision!", "Cosmic calculation!", "Spot on, navigator!",
            "Perfect orbit!", "Galaxy-level accuracy!"
        ]

        retry_msgs = [
            "Orbit misaligned, try again!", "Not quite there, pilot!",
            "Adjust your cosmic trajectory!", "Recalculate coordinates!",
            "Steady... reattempt your landing!"
        ]

        if user_input == correct_answer:
            current_score += 10 if attempt_count == 0 else 5
            feedback_label.config(text=random.choice(success_msgs), fg="#45A29E")
            galaxy.after(1200, move_next)
            return

        attempt_count += 1

        if attempt_count == 1:
            feedback_label.config(text=random.choice(retry_msgs), fg="#FF6961")
        else:
            feedback_label.config(text="Mission failed for this challenge.", fg="#FF6961")
            galaxy.after(1200, move_next)

    except ValueError:
        feedback_label.config(text="Numbers only, space traveler!", fg="#FF6961")


# Move to Next or Finish
def move_next():
    global current_question
    current_question += 1
    if current_question < total_questions:
        next_question()
    else:
        display_results()


# Results Page
def display_results():
    clear_galaxy()

    script_dir = os.path.dirname(__file__)
    bg_path = os.path.join(script_dir, "backgrounds", "results_bg.png")
    bg_image = tk.PhotoImage(file=bg_path)

    bg_label = tk.Label(galaxy, image=bg_image)
    bg_label.image = bg_image
    bg_label.place(x=0, y=0, relwidth=1, relheight=1)

    score_label = tk.Label(
        galaxy,
        text=f"Final Score: {current_score}/100",
        font=("Consolas", 20, "bold"),
        fg="#66FCF1",
        bg="#000000"
    )
    score_label.place(relx=0.5, rely=0.47, anchor="center")

    if current_score >= 90:
        feedback = "MISSION REPORT: Excellent control, Commander."
    elif current_score >= 70:
        feedback = "COMMAND UPDATE: Strong navigation detected."
    elif current_score >= 50:
        feedback = "STATUS: Acceptable trajectory. Further training advised."
    else:
        feedback = "ALERT: System recalibration required. Debrief pending."

    feedback_label = tk.Label(
        galaxy,
        text=feedback,
        font=("Consolas", 14, "bold"),
        fg="#C5C6C7",
        bg="#000000",
        wraplength=420,
        justify="center"
    )
    feedback_label.place(relx=0.5, rely=0.58, anchor="center")

    play_img = tk.PhotoImage(file=os.path.join(script_dir, "buttons", "relaunch_btn.png")).subsample(3,3)
    quit_img = tk.PhotoImage(file=os.path.join(script_dir, "buttons", "space_exit_btn.png")).subsample(3,3)

    play_btn = tk.Button(
        galaxy,
        image=play_img,
        borderwidth=0,
        highlightthickness=0,
        bg="#000000",
        activebackground="#000000",
        command=launch_portal
    )
    play_btn.image = play_img
    play_btn.place(relx=0.25, rely=0.93, anchor="center")

    quit_btn = tk.Button(
        galaxy,
        image=quit_img,
        borderwidth=0,
        highlightthickness=0,
        bg="#000000",
        activebackground="#000000",
        command=galaxy.destroy
    )
    quit_btn.image = quit_img
    quit_btn.place(relx=0.75, rely=0.93, anchor="center")


# Run App
launch_portal()
galaxy.mainloop()
