import tkinter as tk
from tkinter import ttk, messagebox
from PIL import Image, ImageTk
import os

class StudentManagerGUI:

    def __init__(self, root):
        self.root = root
        self.root.title("Student Work Management")
        self.root.geometry("850x600")
        self.root.resizable(False, False)

        #LOAD BACKGROUND IMAGE 
        self.bg_main_path = os.path.join(os.path.dirname(__file__), "background", "bg.png")
        self.bg_score_path = os.path.join(os.path.dirname(__file__), "background", "bg_score.png")

        # Load both now (prevents garbage-collection)
        self.bg_main_img = ImageTk.PhotoImage(Image.open(self.bg_main_path))
        self.bg_score_img = ImageTk.PhotoImage(Image.open(self.bg_score_path))

        # Create ONE background label that we will update later
        self.bg_label = tk.Label(self.root, image=self.bg_main_img)
        self.bg_label.place(x=0, y=0, relwidth=1, relheight=1)

        #LOAD STUDENT FILE
        self.student_file = os.path.join(os.path.dirname(__file__), "studentMarks.txt")
        self.students = self.load_students()

        #SIDEBAR BUTTONs
        self.btn_dir = os.path.join(os.path.dirname(__file__), "buttons")
        self.create_sidebar_buttons()

        #MAIN RECORDS FRAME
        self.records_frame = tk.Frame(self.root, bg="#0F1A24")
        self.records_frame.place(x=230, y=230, width=600, height=310)

        # SEARCH BAR
        self.search_var = tk.StringVar()
        self.search_var.trace("w", self.run_search)  # Live search

        self.search_entry = tk.Entry(
            self.root,
            textvariable=self.search_var,
            font=("Consolas", 12),
            bd=0,
            bg="white"
        )
        self.search_entry.place(x=325, y=180, width=187, height=25)

        #SUMMARY FRAME 
        self.summary_frame = tk.Frame(self.root, bg="#0F1A24")
        self.summary_frame.place(x=230, y=543, width=600, height=40)

    # IMAGE LOADER WITH SUBSAMPLE
    def load_image(self, folder, name, sub=None):
        path = os.path.join(folder, name)
        img = tk.PhotoImage(file=path)
        if sub:
            img = img.subsample(*sub)
        return img
    
    def set_background(self, mode):
        if mode == "main":
            self.bg_label.config(image=self.bg_main_img)
            self.bg_label.image = self.bg_main_img
        else:
            self.bg_label.config(image=self.bg_score_img)
            self.bg_label.image = self.bg_score_img

    def toggle_main_ui(self, visible=True):
        """Show or hide main-page widgets: search, sort, summary."""
        if visible:
            #all geometry places to be shown only for first page
            self.search_entry.place(x=325, y=180, width=187, height=25)
            self.sort_button.place(x=805, y=180)
            self.summary_frame.place(x=230, y=543, width=600, height=40)
        else:
            self.search_entry.place_forget() #used forget function so it does'nt deletes it but removes temporarily
            self.sort_button.place_forget()
            self.summary_frame.place_forget()
            
    
    # SIDEBAR BUTTONS 
    def create_sidebar_buttons(self):

        #VIEW ALL RECORD BUTTON
        self.btn_all_img = self.load_image(self.btn_dir, "all_btn.png", (2, 2))
       
        self.btn_all = tk.Button(
            self.root, 
            image=self.btn_all_img, 
            command=self.show_all_students,
            borderwidth=0, 
            bg="#0F1A24", 
            activebackground="black")
        self.btn_all.image = self.btn_all_img
        self.btn_all.place(x=10, y=138)

        # SCORES BUTTON
        self.btn_scores_img = self.load_image(self.btn_dir, "scores_btn.png", (2, 2))

        self.btn_scores = tk.Button(
            self.root,
            image=self.btn_scores_img,
            command=self.show_scores_screen,   
            borderwidth=0,
            bg="#0F1A24",
            activebackground="black"
        )
        self.btn_scores.image = self.btn_scores_img
        self.btn_scores.place(x=0, y=195)

        # SORT BUTTON IMAGE
        self.sort_btn_img = self.load_image(self.btn_dir, "sort_btn.png", (8, 8))

        self.sort_button = tk.Button(
            self.root,
            image=self.sort_btn_img,
            command=self.open_sort_menu,
            borderwidth=0,
            bg="#0F1A24",
            activebackground="#0F1A24"
        )
        self.sort_button.image = self.sort_btn_img
        self.sort_button.place(x=805, y=180)   
     

    # LOADING STUDENTS FROM TEXT FILE
    def load_students(self):
        students = []
        if not os.path.exists(self.student_file):
            messagebox.showerror("Error", "studentMarks.txt not found!")
            return students

        with open(self.student_file, "r") as f:
            for line in f:
                parts = line.strip().split(",")
                if len(parts) != 6:
                    continue

                num, name, c1, c2, c3, exam = parts
                try:
                    cw_total = int(c1) + int(c2) + int(c3)
                    exam = int(exam)
                    total = cw_total + exam
                    percent = total / 160 * 100

                    students.append({
                        "number": num,
                        "name": name,
                        "coursework": cw_total,
                        "exam": exam,
                        "total": total,
                        "percent": percent,
                        "grade": self.calc_grade(percent)
                    })
                except:
                    continue

        return students

    def calc_grade(self, p):
        if p >= 70: return "A"
        if p >= 60: return "B"
        if p >= 50: return "C"
        if p >= 40: return "D"
        return "F"
    
    #Created Sort Menu with varieties of commands 
    def open_sort_menu(self):
        menu = tk.Menu(
            self.root, 
            tearoff=0, 
            bg="#1A2A35", 
            fg="white",
            activebackground="#335566", 
            activeforeground="white",
            font=("Consolas", 11))

        menu.add_command(label="Name (A → Z)",
                        command=lambda: self.sort_records("name_asc"))
        menu.add_command(label="Name (Z → A)", 
                         command=lambda: self.sort_records("name_desc"))
        menu.add_separator() #Added a seperator for clean grouped menu displays

        menu.add_command(label="Percentage (Low → High)",
                         command=lambda: self.sort_records("percent_asc"))
        menu.add_command(label="Percentage (High → Low)",
                         command=lambda: self.sort_records("percent_desc"))
        menu.add_separator()

        menu.add_command(label="Student Number",
                         command=lambda: self.sort_records("number"))
        menu.add_command(label="Coursework Marks",
                         command=lambda: self.sort_records("cw"))
        menu.add_command(label="Exam Marks",
                         command=lambda: self.sort_records("exam"))
        menu.add_command(label="Total Marks",
                         command=lambda: self.sort_records("total"))

        # popup under the sort button
        menu.tk_popup(self.sort_button.winfo_rootx(), self.sort_button.winfo_rooty() + 35)

    #Crested sort records function that links to command menu for specific tasks
    def sort_records(self, mode):
        data = self.students.copy()

        if mode == "name_asc":
            data.sort(key=lambda s: s["name"].lower())
        elif mode == "name_desc":
            data.sort(key=lambda s: s["name"].lower(), reverse=True)
        elif mode == "percent_asc":
            data.sort(key=lambda s: s["percent"])
        elif mode == "percent_desc":
            data.sort(key=lambda s: s["percent"], reverse=True)
        elif mode == "number":
            data.sort(key=lambda s: int(s["number"]))
        elif mode == "cw":
            data.sort(key=lambda s: s["coursework"], reverse=True)
        elif mode == "exam":
            data.sort(key=lambda s: s["exam"], reverse=True)
        elif mode == "total":
            data.sort(key=lambda s: s["total"], reverse=True)

        self.show_table(data)


    # TREEVIEW TABLE DISPLAY
    def show_table(self, dataset):
        # Clear old widgets 
        for w in self.records_frame.winfo_children():
            w.destroy()

        # Table columns names
        columns = ("Number", "Name", "CW", "Exam", "Total", "Percent", "Grade")

        # Created TreeView (used this idea from minerva linkedin course)
        tree = ttk.Treeview(
            self.records_frame,
            columns=columns,
            show="headings",
            selectmode="browse"
        )

        # created a custom Style
        style = ttk.Style()
        style.configure(
            "Treeview",
            rowheight=28,
            background="#0F1A24",
            fieldbackground="#0F1A24",
            foreground="white",
            borderwidth=0
        )
        style.configure(
            "Treeview.Heading",
            font=("Consolas", 10, "bold"),
            foreground="black")

        tree.pack(side="left", fill="both", expand=True)

        # Attached scrollbar 
        scroll = ttk.Scrollbar(self.records_frame, orient="vertical", command=tree.yview)
        scroll.pack(side="right", fill="y")
        tree.configure(yscrollcommand=scroll.set)

        # Column widths for the rectangle in bg image
        widths = [80, 150, 70, 70, 80, 90, 70]

        for (col, w) in zip(columns, widths):
            tree.heading(col, text=col)
            tree.column(col, width=w, anchor="center")

        # Insert rows
        for s in dataset:
            tree.insert("", "end",
                        values=(s["number"], s["name"], s["coursework"], s["exam"],
                                s["total"], f"{s['percent']:.1f}%", s["grade"]))
            
    def show_summary(self):
        # Clear old content
        for w in self.summary_frame.winfo_children():
            w.destroy()

        count = len(self.students)
        avg = sum(s['percent'] for s in self.students) / count if count else 0

        text = f"Total Students: {count}   |   Average Percentage: {avg:.2f}%"

        tk.Label(
            self.summary_frame,
            text=text,
            font=("Consolas", 11, "bold"),
            bg="#0F1A24",
            fg="#F2F8FA"
        ).pack(anchor="w", padx=11)

    def run_search(self, *args):
        query = self.search_var.get().strip().lower()

        if query == "":
            # Empty search → show all
            self.show_table(self.students)
            return

        result = [
            s for s in self.students
            if query in s["number"].lower()
            or query in s["name"].lower()
        ]

        self.show_table(result)
    
    #Score section (this includes Highest and lowest)
    def show_scores_screen(self):

        self.set_background("score")
        self.toggle_main_ui(False)     # to HIDE search, sort, summary

        # Clear old content
        for w in self.records_frame.winfo_children():
            w.destroy()

        # Frame to hold cards
        cards_frame = tk.Frame(self.records_frame, bg="#0F1A24")
        cards_frame.pack(fill="both", expand=True, padx=5, pady=5)

        # Configure 2 equal columns
        cards_frame.grid_columnconfigure(0, weight=1)
        cards_frame.grid_columnconfigure(1, weight=1)

        # Find highest + lowest
        highest = max(self.students, key=lambda s: s["total"])
        lowest  = min(self.students, key=lambda s: s["total"])

        # created a Card creator function 
        def create_card(parent, title, student, color, column):
            card = tk.Frame(parent, bg="#1A2A35", padx=10, pady=12)
            card.grid(row=0, column=column, sticky="nsew", padx=5, pady=5)

            # Made card expand to fill vertical space
            parent.grid_rowconfigure(0, weight=1)

            tk.Label(
                card,
                text=title,
                font=("Consolas", 14, "bold"),
                fg=color,
                bg="#1A2A35"
            ).pack(anchor="w", pady=(0,10))

            text = (
                f"Name: {student['name']}\n\n"
                f"Number: {student['number']}\n\n"
                f"Coursework Total: {student['coursework']}\n\n"
                f"Exam Marks: {student['exam']}\n\n"
                f"Overall Total: {student['total']}\n\n"
                f"Percentage: {student['percent']:.1f}%\n\n"
                f"Grade: {student['grade']}"
            )

            tk.Label(
                card,
                text=text,
                font=("Consolas", 11),
                fg="white",
                bg="#1A2A35",
                justify="left"
            ).pack(anchor="w")

        # Create cards side by side so it appears clean
        create_card(cards_frame, "Highest Scoring Student", highest, "#66FF7F", column=0)
        create_card(cards_frame, "Lowest Scoring Student", lowest, "#FF6B6B", column=1)


    # view all function linked to button
    def show_all_students(self):
        self.set_background("main")
        self.toggle_main_ui(True)       # to SHOW search, sort, summary again
        self.show_table(self.students)
        self.show_summary() #show the summary frame 



# RUN APP
if __name__ == "__main__":
    root = tk.Tk()
    StudentManagerGUI(root)
    root.mainloop()
