# 🎓 Student Manager App – Coursework & Exam Management System

A beautifully designed Tkinter-based student records manager that handles coursework marks, exam marks, summaries, sorting, searching, and full CRUD (Create, Read, Update, Delete) operations.

This project includes two versions:

- **Basic Version** → View, Search, Sort, Score Analysis  
- **Extension Version** → Add / Delete / Update / Sort Student Records (fully reflected in text file)

All wrapped inside a clean UI with custom buttons, background images, and an elegant sidebar navigation.

---

## 📘 What Is Student Manager App?

The Student Manager App is a complete GUI system built to manage a class of students and their marks.

It includes:

### ⭐ Basic Version

- Load data from `studentMarks.txt`
- Display all students in a styled table
- Live search bar (filters instantly)
- Sorting system (Name, Number, %, CW, Exam, Total…)
- Score screen: Highest & Lowest scoring cards
- Summary section (Count + Class Average)
- Beautiful custom background images + sidebar UI
- Smart background switching (main ↔ score)
- Custom favicon support

### ⭐ Extension Version

Adds full record management:

- ✔ Sort students  
- ✔ Add a student  
- ✔ Delete a student  
- ✔ Update a student  

All edits rewrite and update the text file, ensuring persistent, real data modification.  
This makes the system a real, working student database.

---

## ✨ Features

### 🧮 Student Data Handling

- Reads marks from `.txt` file  
- Computes:  
  - Coursework total  
  - Overall total  
  - Percentage  
  - Letter grade (A–F)  

### 🔍 Live Search System

- Type ANY letter or number  
- Instantly filters results  
- Works for both names and student numbers  
- No button press needed   

### 🏆 Scores Page

- Highest scoring student card  
- Lowest scoring student card  
- Two-column layout  
- Auto-resizable & well centered  
- Uses alternate background image  

### 🧩 Extension Features

#### ⇅ Sorting Menu (also included in basic)

- Clean dropdown menu with:  
  - Name (A–Z / Z–A)  
  - Percentage (Low → High / High → Low)  
  - Coursework  
  - Exam  
  - Total score  
  - Student number  

#### ➕ Add Student

- Full form: Student No, Name, CW1/2/3, Exam  
- Validations:  
  - Required fields  
  - Numbers only  
  - Marks 0–100  
  - No digit inside student name  
- Confirmation popup  
- Automatically calculates totals & grade  
- Appends into `studentMarks_ext.txt`  
- Refreshes table instantly  

#### 🗑️ Delete Student

- Clean top-level popup  
- Type name or number → auto-suggestions  
- Dropdown shows all matched students  
- Confirmation box  
- Rewrites entire text file after deletion  
- Refreshes table instantly  

#### ✏️ Update Student

- Search bar + suggestion dropdown  
- Auto-fills all fields:  
  - Number, Name, CW1, CW2, CW3, Exam  
- Editable student number (duplicate check included)  
- Confirmation popup  
- Safely rewrites updated record  
- Reloads table immediately  

---

## 🎮 How to Use (Full Guide)

### 1️⃣ Launch App

- The main dashboard loads with:  
  - Background image  
  - Sidebar controls  
  - Records table  
  - Search bar  
  - Sort button  
  - Summary area  

### 2️⃣ View All Students

- Press **VIEW ALL** (sidebar)  
- Table loads full dataset with computed totals  

### 3️⃣ Search

- Start typing:  
  - `1`  
  - `jo`  
  - `ama`  
  - `10`  
- Results update instantly  

### 4️⃣ Sort Records

- Press **SORT** → choose:  
  - Name A–Z  
  - Percentage High–Low  
  - Exam Marks  
  - Total Marks  
  …and more  

### 5️⃣ View Scores

- Press **SCORES**  
- Background switches  
- Search + Sort hide  
- Highest and Lowest cards appear  

### 6️⃣ Extension Menu

- Press **Manage**:  
  - Add Student  
  - Delete Student  
  - Update Student  

#### Add Student

- Fill all fields  
- Click **Save**  
- Confirmation popup  
- Added to text file + table  

#### Delete Student

- Type a letter → shows dropdown results  
- Select student  
- Press **Delete**  
- Confirm action  
- Removed from file + table  

#### Update Student

- Search student  
- Dropdown shows exact matches  
- Auto-fill form  
- Edit fields (including number)  
- Save changes  
- All changes update the file permanently  

---

## ⚙️ Tech Stack

- Python 3.x  
- Tkinter – GUI framework  
- Pillow (PIL) – Loads images, renders PNG backgrounds  
- ttk – Styled tables (Treeview)  
- OS module – Handles paths for icons, backgrounds, text files  
- OOP Architecture – Clean, modular, extendable design  

---

## 🖼️ UI Highlights

- Multiple background images  
- Separate themes for:  
  - Main page  
  - Score page  
  - Extension management  
- Custom buttons (PNG)  
- Custom favicon (`Student.ico`)  
- Live search bar  
- Responsive card layouts
