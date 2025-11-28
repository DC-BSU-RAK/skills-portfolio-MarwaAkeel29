# 🤖 Alexa JokeMatrix – Animated Joke Terminal 

A futuristic, glitchy AI-themed joke generator built using Tkinter, Pillow, Pygame, and optional gTTS voice playback.

JokeMatrix simulates a sci-fi “humor core booting sequence,” complete with animated backgrounds, startup sounds, neon terminal text, punchline timing, and dynamic audio reactions.

---

## 🎭 What Is JokeMatrix?

Alexa JokeMatrix is a fully animated joke machine that feels like you're interacting with a secret hacker-terminal AI that tells jokes.

It features:

- Animated GIF background loops
- Joke retrieval from `.txt` file
- Punchline reveal system
- Sound effects for clicks, jokes, and laughs
- Boot-up loading animations
- Built-in speech (optional)
- Super clean UI logic + class structure
- Custom favicon support

It’s fun, fast, futuristic, and extremely aesthetic.

---

## ✨ Features

###🌀 **Animated Interface**

- Smooth animated GIF backgrounds using `ImageSequence`
- Startup splash with glitchy terminal vibes
- Hacker-style neon cyan UI text
- Responsive button-based navigation

###🎤 **Smart Joke Delivery System**

- Loads jokes from `randomJokes.txt`
- Random joke selection each time
- Setup and punchline shown separately
- Time-delayed laughter reaction for comedic effect
- Optional AI-generated voice reading the joke

###🔊 **Audio Engine**

- Startup sound plays after a short boot delay
- Click sound for every button
- Random laughter sound each time
- Non-blocking playback via `pygame.mixer`

###🧩 **Clean Class Architecture**

- `AnimatedGIF` → handles all GIF animations
- `JokeMatrix` → manages UI screens, jokes, sounds
- `wipe()` → clears widgets cleanly before loading new screens
- Logical splitting of "setup phase" and "punchline phase"
---

## 🎮 How to Play (Full Guide)

1️⃣ **Launch the App**  
The system boots with a startup delay, just like a real AI loading its humor engine. You’ll hear a short startup sound after a moment.

2️⃣ **Press INITIATE**  
This takes you from the splash screen into the animated hacker terminal.

3️⃣ **Load Your First Joke**  
Press `LOAD JOKE` (only appears the first time). The joke setup is retrieved and shown in neon terminal format.

4️⃣ **Reveal the Punchline**  
Press `PUNCHLINE`:
- Punchline appears
- AI voice speaks it
- A laugh sound plays after a short comedic delay

5️⃣ **Load More Jokes**  
After the first joke, the button becomes `NEXT JOKE`. Each click pulls a brand-new joke from the text file.

6️⃣ **System Menu**  
Tap the ☰ icon at the top-left:  
You can:
- 🔄 Restart the entire session
- ❌ Quit the program
---

### ⚙️ **Tech Stack**

- **Python 3.x** – Core runtime
- **Tkinter** – GUI framework 
- **Pillow (PIL)** – Handles PNGs, GIFs, and frame-by-frame animation
- **Pygame** – Sound engine for clicks, laughs, and startup audio
- **gTTS** – Enables text-to-speech playback for jokes
- **os** – safe file paths for images, sounds, and icons
- **OOP Architecture** – Clean, modular, easily extendable
  

