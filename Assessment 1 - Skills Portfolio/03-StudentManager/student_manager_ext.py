import tkinter as tk           # Core GUI framework — builds all windows, frames, buttons for the manager
from tkinter import ttk, messagebox   # ttk → styled widgets (treeview tables), messagebox → alerts & confirmations
from PIL import Image, ImageTk    # Loads / converts background images & button icons for smooth UI rendering
import os    # Helps locate resource folders (icons, backgrounds, text files)


class StudentManagerGUI:

    def __init__(self, root):
        self.root = root
        self.root.title("Student Work Management")
        self.root.geometry("850x600")
        self.root.resizable(False, False)

        #Window Icon (Favicon)
        icon_path = os.path.join(os.path.dirname(__file__), "icon", "Student_Manager.ico")
        try:
            self.root.iconbitmap(icon_path)
        except Exception:
            pass

        #LOAD BACKGROUND IMAGE 
        self.bg_main_path = os.path.join(os.path.dirname(__file__), "background", "bg_1.png")
        self.bg_score_path = os.path.join(os.path.dirname(__file__), "background", "bg_2.png")
        self.bg_edit_path = os.path.join(os.path.dirname(__file__), "background", "bg_3.png")

        # Load both now (prevents garbage-collection)
        self.bg_main_img = ImageTk.PhotoImage(Image.open(self.bg_main_path))
        self.bg_score_img = ImageTk.PhotoImage(Image.open(self.bg_score_path))
        self.bg_edit_img = ImageTk.PhotoImage(Image.open(self.bg_edit_path))

        # Create ONE background label that we will update later
        self.bg_label = tk.Label(self.root, image=self.bg_main_img)
        self.bg_label.place(x=0, y=0, relwidth=1, relheight=1)

        #LOAD STUDENT FILE
        self.student_file = os.path.join(os.path.dirname(__file__), "studentMarks_ext.txt")
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
    
    # Switches background based on screen mode → lets app visually change between 
    # main, score view, and edit pages without recreating widgets
    def set_background(self, mode):
        if mode == "main":
            self.bg_label.config(image=self.bg_main_img)
            self.bg_label.image = self.bg_main_img
        elif mode == "score":
            self.bg_label.config(image=self.bg_score_img)
            self.bg_label.image = self.bg_score_img
        elif mode == "edit":
            self.bg_label.config(image=self.bg_edit_img)
            self.bg_label.image = self.bg_edit_img

    
    # Shows or hides main-page elements (search bar, sort, summary)
    # Used when switching to edit/score screens to keep layout clean and distraction-free
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
            
    
    # Builds all sidebar buttons (view all, scores, manage)
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

        # EXTENSION MENU BUTTON
        self.btn_ext_img = self.load_image(self.btn_dir, "manage_btn.png", (2, 2))

        self.btn_ext = tk.Button(
            self.root,
            image=self.btn_ext_img,
            command=self.open_extension_menu,
            borderwidth=0,
            bg="#0F1A24",
            activebackground="black"
        )
        self.btn_ext.image = self.btn_ext_img
        self.btn_ext.place(x=1, y=255)   

        #Save button for Add student page
        self.save_btn_img = self.load_image(self.btn_dir, "save_btn.png", (3, 3))

        # UPDATE BUTTON IMAGE
        self.update_btn_img = self.load_image(self.btn_dir, "update_btn.png", (3, 3))

        # DELETE BUTTON IMAGE
        self.delete_btn_img = self.load_image(self.btn_dir, "delete_btn.png", (3, 3))
   
     
    # Reads studentMarks_ext.txt, converts raw text into usable student dictionaries
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
                try: # calculates totals/percentages, and prepares all data for UI display
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

    # Converts percentage into final letter grade → used when loading, adding, or updating students
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

        # Groups all sorting choices in one clean place instead of separate buttons
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

        # Works for name, percentage, exam, cw, total, and student number
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


    # Builds the main TreeView table each time data changes
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

        # Clears old rows, applies custom theme, and inserts formatted student rows
        for s in dataset:
            tree.insert("", "end",
                        values=(s["number"], s["name"], s["coursework"], s["exam"],
                                s["total"], f"{s['percent']:.1f}%", s["grade"]))
            
    def show_summary(self):
        # Clear old content
        for w in self.summary_frame.winfo_children():
            w.destroy()

        # Shows quick stats below the table (student count + average %)
        count = len(self.students)
        avg = sum(s['percent'] for s in self.students) / count if count else 0

        # Auto updates whenever records are changed
        text = f"Total Students: {count}   |   Average Percentage: {avg:.2f}%"

        tk.Label(
            self.summary_frame,
            text=text,
            font=("Consolas", 11, "bold"),
            bg="#0F1A24",
            fg="#F2F8FA"
        ).pack(anchor="w", padx=11)

    # Live search system → filters students as the user types
    def run_search(self, *args):
        query = self.search_var.get().strip().lower()

        if query == "":
            # Empty search → show all
            self.show_table(self.students)
            return
        
        # Matches by student number or name for fast lookup
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

        # RESET FRAME SIZE
        self.records_frame.place(x=230, y=230, width=600, height=310)

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


    # Opens manage menu (add / delete / update)
    # Keeps student modification actions grouped and accessible
    def open_extension_menu(self):
        menu = tk.Menu(
            self.root,
            tearoff=0,
            bg="#1A2A35",
            fg="white",
            activebackground="#335566",
            activeforeground="white",
            font=("Consolas", 15, "bold")  
        )

        menu.add_command(
            label="Add Student", 
            command=self.add_student_window)
        menu.add_separator()
        menu.add_command(
            label="Delete Student", 
            command=self.delete_student_window)
        menu.add_separator()
        menu.add_command(
            label="Update Student", 
            command=self.update_student_window)

        # open menu near extension button
        menu.tk_popup(self.btn_ext.winfo_rootx(), self.btn_ext.winfo_rooty() + 35)


    # Returns user to main records page with full table + summary
    def show_all_students(self):
        self.set_background("main")

        # Resets background, UI elements, and table data
        self.records_frame.place(x=230, y=230, width=600, height=310)
        self.toggle_main_ui(True)    # to SHOW search, sort, summary again
        self.show_table(self.students)
        self.show_summary() #show the summary frame 


    # Builds the Add Student form on BG3 layout
    def add_student_window(self):
        # Switch to BG3
        self.set_background("edit")
        self.toggle_main_ui(False)

        # Resize + reposition records frame 
        self.records_frame.place(x=297, y=190, width=450, height=387)

        # Clear old content
        for w in self.records_frame.winfo_children():
            w.destroy()

        # Created centered form inside frame
        form = tk.Frame(self.records_frame, bg="#0F1A24")
        form.place(relx=0.5, rely=0.5, anchor="center")

        labels = ["Student Number:", "Name:", "CW1 Marks:", "CW2 Marks:", "CW3 Marks:", "Exam Marks:"]
        self.add_entries = {}

        # Creates labeled input fields and a save button inside the frame
        for i, text in enumerate(labels):
            tk.Label(
                form, text=text, font=("Consolas", 12),
                fg="white", bg="#0F1A24"
            ).grid(row=i, column=0, sticky="w", pady=6, padx=10)

            entry = tk.Entry(form, font=("Consolas", 12), width=20)
            entry.grid(row=i, column=1, pady=6, padx=10)
            self.add_entries[text] = entry

        # Save Button Image
        save_btn = tk.Button(
            form,
            image=self.save_btn_img,
            borderwidth=0,
            bg="#0F1A24",
            activebackground="#0F1A24",
            command=self.save_new_student
        )
        save_btn.grid(row=len(labels), column=0, columnspan=2, pady=15)


    # Validates all entered marks + name + number
    def save_new_student(self):

        #Extract Raw Inputs
        num = self.add_entries["Student Number:"].get().strip()
        name = self.add_entries["Name:"].get().strip()
        cw1 = self.add_entries["CW1 Marks:"].get().strip()
        cw2 = self.add_entries["CW2 Marks:"].get().strip()
        cw3 = self.add_entries["CW3 Marks:"].get().strip()
        exam = self.add_entries["Exam Marks:"].get().strip()

        fields = [num, name, cw1, cw2, cw3, exam]

        #Empty field validation
        if any(f == "" for f in fields):
            messagebox.showerror("Missing Information",
                                "Please fill all the fields before saving.")
            return

        #Student Number validation
        if not num.isdigit():
            messagebox.showerror("Invalid Student Number",
                                "Student Number must contain digits only.")
            return

        #Name validation
        if any(ch.isdigit() for ch in name):
            messagebox.showerror("Invalid Name",
                                "Name must contain letters only, not numbers.")
            return

        #Marks must be valid numbers
        try:
            cw1 = int(cw1)
            cw2 = int(cw2)
            cw3 = int(cw3)
            exam = int(exam)
        except:
            messagebox.showerror("Invalid Marks",
                                "Marks must be numbers only (0–100).")
            return

        #Marks 0–100 range validation
        for m in (cw1, cw2, cw3, exam):
            if not (0 <= m <= 100):
                messagebox.showerror("Invalid Marks",
                                    "All marks must be between 0 and 100.")
                return

        #Confirm popup
        confirm = messagebox.askyesno(
            "Confirm New Student",
            f"Add this student?\n\n"
            f"Number: {num}\n"
            f"Name: {name}\n"
            f"CW1={cw1}, CW2={cw2}, CW3={cw3}\n"
            f"Exam={exam}"
        )
        if not confirm:
            return

        # Calculates totals, grade, appends to text file, updates memory, and refreshes UI
        coursework_total = cw1 + cw2 + cw3
        total = coursework_total + exam
        percent = total / 160 * 100
        grade = self.calc_grade(percent)

        #Append to file
        with open(self.student_file, "a") as f:
            f.write(f"\n{num},{name},{cw1},{cw2},{cw3},{exam}\n")

        #Update memory
        self.students.append({
            "number": num,
            "name": name,
            "cw1": cw1,
            "cw2": cw2,
            "cw3": cw3,
            "coursework": coursework_total,
            "exam": exam,
            "total": total,
            "percent": percent,
            "grade": grade
        })

        messagebox.showinfo("Success ✔", "Student added successfully!")
        self.show_all_students()


    # Popup window for deleting students
    def delete_student_window(self):
        self.delete_win = tk.Toplevel(self.root)
        self.delete_win.title("Delete Student")
        self.delete_win.geometry("400x300")
        self.delete_win.resizable(False, False)
        self.delete_win.configure(bg="#0F1A24")

        tk.Label(
            self.delete_win, 
            text="Delete Student", 
            font=("Consolas", 16, "bold"),
            fg="white", 
            bg="#0F1A24"
        ).pack(pady=15)

        # USER INPUT
        tk.Label(
            self.delete_win, text="Enter Name or Student Number:",
            font=("Consolas", 12), fg="white", bg="#0F1A24"
        ).pack()

        self.del_search_var = tk.StringVar()
        self.del_search_var.trace("w", self.filter_delete_results)

        # Includes live search + dropdown to choose exactly one matching student
        self.del_search_entry = tk.Entry(
            self.delete_win, 
            textvariable=self.del_search_var,
            font=("Consolas", 12),
            width=25
        )
        self.del_search_entry.pack(pady=5)

        # DROPDOWN (MATCHED RESULTS)
        tk.Label(
            self.delete_win, text="Matching Students:",
            font=("Consolas", 12), fg="white", bg="#0F1A24"
        ).pack(pady=(10, 2))

        self.del_combo = ttk.Combobox(
            self.delete_win, 
            font=("Consolas", 12),
            state="readonly",
            width=28
        )
        self.del_combo.pack()

        # DELETE BUTTON
        delete_btn = tk.Button(
            self.delete_win,
            image=self.delete_btn_img,
            borderwidth=0,
            bg="#0F1A24",
            activebackground="#0F1A24",
            command=self.confirm_and_delete
        )
        delete_btn.pack(pady=25)


    # Filters students in realtime based on typed text
    def filter_delete_results(self, *args):
        query = self.del_search_var.get().lower().strip()

        if query == "":
            self.del_combo["values"] = []
            return

        results = []

        #Only shows matches in the dropdown (name or number starts with input)
        for s in self.students:
            if s["number"].lower().startswith(query) or s["name"].lower().startswith(query):
                results.append(f"{s['number']} - {s['name']}")

        # update dropdown
        self.del_combo["values"] = results

        # auto-select first ONLY if results exist
        if results:
            self.del_combo.current(0)
        else:
            self.del_combo.set("")   # clears displayed selection


    # Confirms and removes selected student from memory + file
    def confirm_and_delete(self):
        selected = self.del_combo.get()

        if selected == "":
            messagebox.showerror("No Student Selected", "Please select a valid student from the list.")
            return

        # extract the real student number from dropdown
        student_num = selected.split(" - ")[0].strip()

        # final check: check if num exists in list
        match = next((s for s in self.students if s["number"] == student_num), None)
        if not match:
            messagebox.showerror("Invalid Selection", "The selected student does not exist.")
            return

        # confirm popup
        ok = messagebox.askyesno(
            "Confirm Delete",
            f"Are you sure you want to delete student:\n{selected}?"
        )
        if not ok:
            return

        # remove from memory
        self.students = [s for s in self.students if s["number"] != student_num]

        # rewrite full file
        with open(self.student_file, "w") as f:
            for s in self.students:
                # store exactly as originally read
                cw1 = cw2 = cw3 = s["coursework"] // 3
                f.write(f"{s['number']},{s['name']},{cw1},{cw2},{cw3},{s['exam']}\n")

        messagebox.showinfo("Deleted Successfully", "Student record has been removed.")
        self.delete_win.destroy()
        self.show_all_students()


    # Opens update window with search bar + auto-filling form fields
    def update_student_window(self):
        # TopLevel Window
        self.update_win = tk.Toplevel(self.root)
        self.update_win.title("Update Student")
        self.update_win.geometry("480x420")
        self.update_win.resizable(False, False)
        self.update_win.configure(bg="#0F1A24")

        tk.Label(
            self.update_win,
            text="Update Student Record",
            font=("Consolas", 16, "bold"),
            fg="white",
            bg="#0F1A24"
        ).pack(pady=15)

        # SEARCH BAR
        tk.Label(
            self.update_win,
            text="Search by Name or Student Number:",
            font=("Consolas", 12),
            fg="white",
            bg="#0F1A24"
        ).pack()

        self.update_search_var = tk.StringVar()
        self.update_search_var.trace("w", self.filter_update_results)

        self.update_search_entry = tk.Entry(
            self.update_win,
            textvariable=self.update_search_var,
            font=("Consolas", 12),
            width=30
        )
        self.update_search_entry.pack(pady=6)

        # DROPDOWN
        tk.Label(
            self.update_win,
            text="Matching Students:",
            font=("Consolas", 12),
            fg="white",
            bg="#0F1A24"
        ).pack()

        self.update_combo = ttk.Combobox(
            self.update_win,
            font=("Consolas", 12),
            width=33,
            state="readonly"
        )
        self.update_combo.pack(pady=5)
        self.update_combo.bind("<<ComboboxSelected>>", self.fill_update_fields)

        # FORM FRAME
        form = tk.Frame(self.update_win, bg="#0F1A24")
        form.pack(pady=10)

        labels = ["Student Number:", "Name:", "CW1 Marks:",
                "CW2 Marks:", "CW3 Marks:", "Exam Marks:"]
        self.update_entries = {}

        # Lets user modify any student record
        for i, text in enumerate(labels):
            tk.Label(
                form,
                text=text,
                font=("Consolas", 12),
                fg="white",
                bg="#0F1A24"
            ).grid(row=i, column=0, sticky="w", padx=5, pady=5)

            entry = tk.Entry(form, font=("Consolas", 12), width=20)
            entry.grid(row=i, column=1, padx=5, pady=5)
            self.update_entries[text] = entry

        # UPDATE BUTTON
        tk.Button(
            self.update_win,
            text="Save Changes",
            font=("Consolas", 12, "bold"),
            bg="#4CAF50",
            fg="white",
            width=14,
            command=self.confirm_update_student
        ).pack(pady=15)


    # Filters students for update window dropdown
    def filter_update_results(self, *args):
        query = self.update_search_var.get().lower().strip()

        # Clear dropdown when empty
        if not query:
            self.update_combo["values"] = []
            return

        results = []

        for s in self.students:
            num = s["number"].lower()
            name = s["name"].lower()

            # FILTER:
            # Supports full number match or name starting with query
            if num == query or name.startswith(query):
                results.append(f"{s['number']} - {s['name']}")

        self.update_combo["values"] = results

        if results:
            self.update_combo.current(0)

    # Opens update window with search bar + auto-filling form fields
    def update_student_window(self):
        self.update_win = tk.Toplevel(self.root)
        self.update_win.title("Update Student")
        self.update_win.geometry("450x480")
        self.update_win.resizable(False, False)
        self.update_win.configure(bg="#0F1A24")

        tk.Label(self.update_win, text="Update Student Record",
                font=("Consolas", 16, "bold"),
                fg="white", bg="#0F1A24").pack(pady=15)

        #SEARCH FIELD
        tk.Label(self.update_win, text="Search by Name or Number:",
                font=("Consolas", 12), fg="white",
                bg="#0F1A24").pack()

        self.update_search_var = tk.StringVar()
        self.update_search_var.trace("w", self.filter_update_results)

        self.update_search_entry = tk.Entry(
            self.update_win, textvariable=self.update_search_var,
            font=("Consolas", 12), width=30
        )
        self.update_search_entry.pack(pady=5)

        # Dropdown
        tk.Label(self.update_win, text="Matching Students:",
                font=("Consolas", 12), fg="white",
                bg="#0F1A2A").pack(pady=(8,2))

        self.update_combo = ttk.Combobox(
            self.update_win, state="readonly",
            font=("Consolas", 12), width=32
        )
        self.update_combo.pack()
        self.update_combo.bind("<<ComboboxSelected>>", self.fill_update_fields)

        #FORM FIELDS (This section includes auto-fill)

        form = tk.Frame(self.update_win, bg="#0F1A24")
        form.pack(pady=12)

        labels = ["Student Number:", "Name:", "CW1:", "CW2:", "CW3:", "Exam:"]
        self.update_entries = {}

        for i, txt in enumerate(labels):
            tk.Label(form, text=txt, font=("Consolas", 12),
                    fg="white", bg="#0F1A24").grid(row=i, column=0,
                                                    sticky="w", pady=6, padx=10)

            e = tk.Entry(form, font=("Consolas", 12), width=20)
            e.grid(row=i, column=1, pady=6)
            self.update_entries[txt] = e

        #UPDATE BUTTON    
        update_btn = tk.Button(
                self.update_win,
                image=self.update_btn_img,
                borderwidth=0,
                bg="#0F1A24",
                activebackground="#0F1A24",
                command=self.save_updated_student
            ).pack(pady=15)


    # Auto-fills the update form with the selected student's exact values
    def fill_update_fields(self, event):
        selected = self.update_combo.get()
        if not selected:
            return

        num = selected.split(" - ")[0]

        # Find selected student
        for s in self.students:
            if s["number"] == num:
                self.update_entries["Student Number:"].delete(0, tk.END)
                self.update_entries["Student Number:"].insert(0, s["number"])

                self.update_entries["Name:"].delete(0, tk.END)
                self.update_entries["Name:"].insert(0, s["name"])

                # saved only coursework sum; so rewrite split values from file
                # reload raw exact CW values from file
                with open(self.student_file) as f:
                    for line in f:
                        p = line.strip().split(",")
                        if p[0] == num:
                            cw1, cw2, cw3 = p[2], p[3], p[4]
                            exam = p[5]

                self.update_entries["CW1:"].delete(0, tk.END)
                self.update_entries["CW1:"].insert(0, cw1)

                self.update_entries["CW2:"].delete(0, tk.END)
                self.update_entries["CW2:"].insert(0, cw2)

                self.update_entries["CW3:"].delete(0, tk.END)
                self.update_entries["CW3:"].insert(0, cw3)

                self.update_entries["Exam:"].delete(0, tk.END)
                self.update_entries["Exam:"].insert(0, exam)
                break

    # Validates changes, rewrites the record inside text file
    def save_updated_student(self):
        # Extract inputs
        num = self.update_entries["Student Number:"].get().strip()
        name = self.update_entries["Name:"].get().strip()
        cw1 = self.update_entries["CW1:"].get().strip()
        cw2 = self.update_entries["CW2:"].get().strip()
        cw3 = self.update_entries["CW3:"].get().strip()
        exam = self.update_entries["Exam:"].get().strip()

        # Basic validation
        if not num or not name or not cw1 or not cw2 or not cw3 or not exam:
            messagebox.showerror("Missing Fields", "Please fill all fields.")
            return

        # Check duplicate student number
        selected = self.update_combo.get()
        old_number = selected.split(" - ")[0]

        if num != old_number:
            for s in self.students:
                if s["number"] == num:
                    messagebox.showerror("Duplicate Number",
                                        "A student with this number already exists.")
                    return

        try:
            cw1, cw2, cw3, exam = int(cw1), int(cw2), int(cw3), int(exam)
        except:
            messagebox.showerror("Invalid Marks", "Enter valid numbers for marks.")
            return

        # Confirm popup
        ok = messagebox.askyesno(
            "Confirm Update",
            f"Update record for {old_number}?",
        )
        if not ok:
            return

        # Update file (rewrite)
        new_lines = []
        with open(self.student_file) as f:
            for line in f:
                p = line.strip().split(",")
                if p[0] == old_number:
                    new_lines.append(f"{num},{name},{cw1},{cw2},{cw3},{exam}\n")
                else:
                    new_lines.append(line)

        with open(self.student_file, "w") as f:
            f.writelines(new_lines)

        # Update internal list
        self.students = self.load_students()

        messagebox.showinfo("Success", "Student updated successfully!")
        self.update_win.destroy()
        self.show_all_students()


# RUN APP
if __name__ == "__main__":
    root = tk.Tk()
    StudentManagerGUI(root)
    root.mainloop()
