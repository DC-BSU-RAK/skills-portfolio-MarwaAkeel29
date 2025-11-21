import tkinter as tk
from tkinter import ttk, messagebox
import os

class StudentManager:
    def __init__(self, root):
        self.root = root
        self.root.title("Student Records Manager")
        self.root.geometry("850x500")
        self.root.config(bg="#0B0C10")

        # Path to student file
        self.student_file = os.path.join(os.path.dirname(__file__), "studentMarks.txt")
        self.students = self.load_students()  # Load student data

        self.create_sidebar()  # Create left sidebar buttons

        # Notebook for tabs
        self.notebook = ttk.Notebook(self.root)
        self.notebook.place(x=160, y=20, width=670, height=450)

        # Tabs
        self.all_tab = tk.Frame(self.notebook, bg="#1F2833")
        self.individual_tab = tk.Frame(self.notebook, bg="#1F2833")
        self.highest_tab = tk.Frame(self.notebook, bg="#1F2833")
        self.lowest_tab = tk.Frame(self.notebook, bg="#1F2833")

        self.notebook.add(self.all_tab, text="All Students")
        self.notebook.add(self.individual_tab, text="Individual Student")
        self.notebook.add(self.highest_tab, text="Highest Mark")
        self.notebook.add(self.lowest_tab, text="Lowest Mark")

    # Load student data from file
    def load_students(self):
        students = []
        if not os.path.exists(self.student_file):
            messagebox.showerror("Error", f"No file found: {self.student_file}")
            return students

        with open(self.student_file, "r") as f:
            for line in f:
                parts = line.strip().split(",")
                if len(parts) != 6:
                    continue
                number, name, cw1, cw2, cw3, exam = parts
                try:
                    cw_total = float(cw1) + float(cw2) + float(cw3)
                    exam = float(exam)
                    total = cw_total + exam
                    pct = total / 160 * 100
                    students.append({
                        "name": name,
                        "number": number,
                        "coursework": cw_total,
                        "exam": exam,
                        "total": total,
                        "percentage": pct,
                        "grade": self.calculate_grade(pct)
                    })
                except ValueError:
                    continue
        return students

    # Calculate grade from percentage
    def calculate_grade(self, pct):
        if pct >= 70: return "A"
        if pct >= 60: return "B"
        if pct >= 50: return "C"
        if pct >= 40: return "D"
        return "F"

    # Sidebar buttons
    def create_sidebar(self):
        sidebar = tk.Frame(self.root, bg="#1C1C1C")
        sidebar.place(x=0, y=0, width=160, height=500)
        tk.Button(sidebar, text="All Students", width=18, command=self.show_all_students).pack(pady=10)
        tk.Button(sidebar, text="Individual", width=18, command=self.show_individual).pack(pady=10)
        tk.Button(sidebar, text="Highest", width=18, command=self.show_highest).pack(pady=10)
        tk.Button(sidebar, text="Lowest", width=18, command=self.show_lowest).pack(pady=10)

    # Create a table in a tab with given data
    def create_table(self, parent, data):
        for w in parent.winfo_children():
            w.destroy()
        columns = ("Number", "Name", "Coursework", "Exam", "Total", "Percentage", "Grade")
        tree = ttk.Treeview(parent, columns=columns, show="headings")
        tree.pack(fill="both", expand=True)
        for col in columns:
            tree.heading(col, text=col)
            tree.column(col, anchor="center")
        for s in data:
            tree.insert("", "end", values=(s['number'], s['name'], s['coursework'], s['exam'],
                                           s['total'], f"{s['percentage']:.2f}%", s['grade']))
        scrollbar = ttk.Scrollbar(parent, orient="vertical", command=tree.yview)
        tree.configure(yscroll=scrollbar.set)
        scrollbar.pack(side="right", fill="y")

    # Show all students
    def show_all_students(self):
        self.notebook.select(self.all_tab)
        if not self.students:
            for w in self.all_tab.winfo_children():
                w.destroy()
            tk.Label(self.all_tab, text="No students found.", fg="white", bg="#1F2833").pack(pady=20)
            return
        self.create_table(self.all_tab, self.students)

    # Show individual student search
    def show_individual(self):
        self.notebook.select(self.individual_tab)
        for w in self.individual_tab.winfo_children():
            w.destroy()
        tk.Label(self.individual_tab, text="Enter Student Name or Number:", bg="#1F2833", fg="#66FCF1").pack(pady=10)
        entry = tk.Entry(self.individual_tab)
        entry.pack(pady=5)
        result_frame = tk.Frame(self.individual_tab, bg="#1F2833")
        result_frame.pack(fill="both", expand=True, pady=10)

        def search():
            val = entry.get().strip()
            filtered = [s for s in self.students if s['name'] == val or s['number'] == val]
            if not filtered:
                for w in result_frame.winfo_children():
                    w.destroy()
                tk.Label(result_frame, text="Student not found!", fg="white", bg="#1F2833").pack(pady=20)
                return
            self.create_table(result_frame, filtered)

        tk.Button(self.individual_tab, text="Search", command=search).pack(pady=5)

    # Show student with highest percentage
    def show_highest(self):
        self.notebook.select(self.highest_tab)
        if not self.students:
            for w in self.highest_tab.winfo_children():
                w.destroy()
            tk.Label(self.highest_tab, text="No students found.", fg="white", bg="#1F2833").pack(pady=20)
            return
        self.create_table(self.highest_tab, [max(self.students, key=lambda x: x['percentage'])])

    # Show student with lowest percentage
    def show_lowest(self):
        self.notebook.select(self.lowest_tab)
        if not self.students:
            for w in self.lowest_tab.winfo_children():
                w.destroy()
            tk.Label(self.lowest_tab, text="No students found.", fg="white", bg="#1F2833").pack(pady=20)
            return
        self.create_table(self.lowest_tab, [min(self.students, key=lambda x: x['percentage'])])

if __name__ == "__main__":
    root = tk.Tk()
    StudentManager(root)
    root.mainloop()
