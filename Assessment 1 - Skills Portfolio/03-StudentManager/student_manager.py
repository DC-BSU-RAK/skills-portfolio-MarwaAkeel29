import tkinter as tk
from tkinter import ttk, messagebox
from PIL import Image, ImageTk
import os

class StudentManagerGUI:

    def __init__(self, root):
        self.root = root
        self.root.title("Student Work Management")
        self.root.geometry("850x550")
        self.root.resizable(False, False)

        #LOAD BACKGROUND IMAGE 
        bg_path = os.path.join(os.path.dirname(__file__), "background", "bg.png")
        self.bg_img = ImageTk.PhotoImage(Image.open(bg_path))
        bg_label = tk.Label(self.root, image=self.bg_img)
        bg_label.place(x=0, y=0, relwidth=1, relheight=1)

        #LOAD STUDENT FILE
        self.student_file = os.path.join(os.path.dirname(__file__), "studentMarks.txt")
        self.students = self.load_students()

        #SIDEBAR BUTTONs
        self.btn_dir = os.path.join(os.path.dirname(__file__), "buttons")
        self.create_sidebar_buttons()

        #MAIN RECORDS FRAME
        self.records_frame = tk.Frame(self.root, bg="#0F1A24")
        self.records_frame.place(x=230, y=180, width=600, height=310)


    # IMAGE LOADER WITH SUBSAMPLE
    def load_image(self, folder, name, sub=None):
        path = os.path.join(folder, name)
        img = tk.PhotoImage(file=path)
        if sub:
            img = img.subsample(*sub)
        return img
    
    
    # SIDEBAR BUTTONS 
    def create_sidebar_buttons(self):

        #VIEW ALL RECORD BUTTON
        self.btn_all_img = self.load_image(self.btn_dir, "all_btn.png", (2, 2))
       
        self.btn_all = tk.Button(self.root, image=self.btn_all_img, command=self.show_all_students,
                                 borderwidth=0, bg="#11676a", activebackground="black")
        self.btn_all.image = self.btn_all_img
        self.btn_all.place(x=10, y=112)


        #INDIVIDUAL RECORD BUTTON
        self.btn_ind_img = self.load_image(self.btn_dir, "individual_btn.png", (2, 2))

        self.btn_ind = tk.Button(
            self.root, image=self.btn_ind_img,
            command=self.show_individual_screen,
            borderwidth=0, bg="#11676a", activebackground="black"
        )
        self.btn_ind.image = self.btn_ind_img
        self.btn_ind.place(x=10, y=175)


        # SCORES BUTTON
        self.btn_scores_img = self.load_image(self.btn_dir, "scores_btn.png", (2, 2))

        self.btn_scores = tk.Button(
            self.root,
            image=self.btn_scores_img,
            command=self.show_scores_screen,   
            borderwidth=0,
            bg="#11676a",
            activebackground="black"
        )
        self.btn_scores.image = self.btn_scores_img
        self.btn_scores.place(x=10, y=235)
        

       
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
        style.configure("Treeview.Heading",
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
            

    #Individual record section
    def show_individual_screen(self):
        # clear old contents in record area
        for w in self.records_frame.winfo_children():
            w.destroy()

        form = tk.Frame(self.records_frame, bg="#0F1A24")
        form.pack(fill="both", expand=True)


        # Label
        tk.Label(
            form, text="Search Individual Student",
            font=("Consolas", 14, "bold"), fg="white",
            bg="#0F1A24"
        ).pack(pady=15)

        # Entry box
        entry = tk.Entry(form, font=("Consolas", 12), width=25)
        entry.pack(pady=15)

        # Search button
        def search():
            query = entry.get().strip()

            if not query:
                messagebox.showwarning("Input Missing", "Enter a name or student number!")
                return

            result = [
                s for s in self.students 
                if s["number"] == query or s["name"].lower() == query.lower()
            ]

            if not result:
                messagebox.showerror("Not Found", "No matching student found.")
                return
            
            # show only that student in table
            self.show_table(result)

        tk.Button(
            form,
            text="Search",
            font=("Consolas", 12, "bold"),
            command=search,
            bg="#1A2A35", fg="white",
            width=12
        ).pack(pady=15)

    
    #Score section (this includes Highest and lowest)
    def show_scores_screen(self):
        # clear old content
        for w in self.records_frame.winfo_children():
            w.destroy()

        frame = tk.Frame(self.records_frame, bg="#0F1A24")
        frame.pack(fill="both", expand=True, padx=20, pady=20)

        # find highest + lowest
        highest = max(self.students, key=lambda s: s["total"])
        lowest  = min(self.students, key=lambda s: s["total"])


        # Card creator function (records will be displayed as a card)
        def create_card(parent, title, student, color):
            card = tk.Frame(parent, bg="#1A2A35", padx=15, pady=15)
            card.pack(pady=10, fill="x")

            tk.Label(
                card,
                text=title,
                font=("Consolas", 16, "bold"),
                fg=color,
                bg="#1A2A35"
            ).pack(anchor="w")

            text = (
                f"Name: {student['name']}\n"
                f"Number: {student['number']}\n"
                f"Coursework Total: {student['coursework']}\n"
                f"Exam Marks: {student['exam']}\n"
                f"Overall Total: {student['total']}\n"
                f"Percentage: {student['percent']:.1f}%\n"
                f"Grade: {student['grade']}"
            )

            tk.Label(
                card,
                text=text,
                font=("Consolas", 12),
                fg="white",
                bg="#1A2A35",
                justify="left"
            ).pack(anchor="w")

        # Created highest & lowest cards
        create_card(
            frame,
            "Highest Scoring Student",
            highest,
            "#66FF7F"    
        )

        create_card(
            frame,
            "Lowest Scoring Student",
            lowest,
            "#FF6B6B"    
        )


    # BUTTON ACTIONS
    def show_all_students(self):
        self.show_table(self.students)

    def search_student_window(self):
        messagebox.showinfo("Search", "Individual search screen coming next")

    def show_highest(self):
        if self.students:
            top = max(self.students, key=lambda s: s["percent"])
            self.show_table([top])

    def show_lowest(self):
        if self.students:
            low = min(self.students, key=lambda s: s["percent"])
            self.show_table([low])



# RUN APP
if __name__ == "__main__":
    root = tk.Tk()
    StudentManagerGUI(root)
    root.mainloop()
