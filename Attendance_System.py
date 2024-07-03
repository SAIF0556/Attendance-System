import tkinter as tk
from tkinter import messagebox, ttk, filedialog, font
import csv
from datetime import datetime
import os

class AttendanceSystem:
    def __init__(self, root):
        self.root = root
        self.root.title("Attendance System")
        self.root.state('zoomed')  # Open in full screen
        self.root.configure(bg="#1035ae")  # Deep blue color

        # Teacher's Info
        self.teacher_name = tk.StringVar()
        self.degree = tk.StringVar()
        self.semester = tk.StringVar()
        self.course_name = tk.StringVar()
        self.year = tk.StringVar()
        self.date = tk.StringVar()

        # Student Info
        self.students = []

        # GUI Setup
        self.setup_gui()

    def setup_gui(self):
        main_frame = tk.Frame(self.root, bg="#1035ae")
        main_frame.pack(fill="both", expand=True)

        canvas = tk.Canvas(main_frame, bg="#1035ae", highlightthickness=0)
        canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        scrollbar = tk.Scrollbar(main_frame, orient=tk.VERTICAL, command=canvas.yview)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        scrollable_frame = tk.Frame(canvas, bg="#1035ae")

        scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(
                scrollregion=canvas.bbox("all")
            )
        )

        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)

        def _on_mouse_wheel(event):
            canvas.yview_scroll(-1 * int(event.delta / 120), "units")

        canvas.bind_all("<MouseWheel>", _on_mouse_wheel)

        # Centered Logo Frame
        logo_frame = tk.Frame(scrollable_frame, bg="#1035ae")
        logo_frame.grid(row=0, column=0,pady=10,  sticky="n")

        logo_path = os.path.join(os.path.dirname(__file__), 'image.png')
        self.logo_img = tk.PhotoImage(file=logo_path)
        logo_label = tk.Label(logo_frame, image=self.logo_img, bg="#1035ae", height=95)
        logo_label.pack()

        teacher_frame = tk.LabelFrame(scrollable_frame, text="", bg="#1035ae", fg="white", padx=20, pady=20)
        teacher_frame.grid(row=1, column=0, padx=20, pady=20, sticky="ew")

        tk.Label(teacher_frame, text="Teacher's Name:", bg="#1035ae", fg="white", font=font.Font(size=16)).grid(row=0, column=0, sticky="w", pady=10, padx=10)
        tk.Entry(teacher_frame, textvariable=self.teacher_name, width=120, bg="white").grid(row=1, column=0, pady=10, padx=10)

        tk.Label(teacher_frame, text="Degree:", bg="#1035ae", fg="white", font=font.Font(size=16)).grid(row=0, column=1, sticky="w", pady=10, padx=10)
        tk.Entry(teacher_frame, textvariable=self.degree, width=120, bg="white").grid(row=1, column=1, pady=10, padx=10)

        tk.Label(teacher_frame, text="Semester:", bg="#1035ae", fg="white", font=font.Font(size=16)).grid(row=2, column=0, sticky="w", pady=10, padx=10)
        tk.Entry(teacher_frame, textvariable=self.semester, width=120, bg="white").grid(row=3, column=0, pady=10, padx=10)

        tk.Label(teacher_frame, text="Course Name:", bg="#1035ae", fg="white", font=font.Font(size=16)).grid(row=2, column=1, sticky="w", pady=10, padx=10)
        tk.Entry(teacher_frame, textvariable=self.course_name, width=120, bg="white").grid(row=3, column=1, pady=10, padx=10)

        # tk.Label(teacher_frame, text="Year:", bg="#1035ae", fg="white", font=font.Font(size=16)).grid(row=4, column=0, sticky="w", pady=10, padx=10)
        # tk.Entry(teacher_frame, textvariable=self.year, width=120, bg="white").grid(row=5, column=0, pady=10, padx=10)

        # tk.Label(teacher_frame, text="Date (YYYY-MM-DD):", bg="#1035ae", fg="white", font=font.Font(size=16)).grid(row=4, column=1, sticky="w", pady=10, padx=10)
        # tk.Entry(teacher_frame, textvariable=self.date, width=120, bg="white").grid(row=5, column=1, pady=10, padx=10)

        student_header_frame = tk.Frame(scrollable_frame, bg="#1035ae")
        student_header_frame.grid(row=2, column=0, padx=20, pady=20, sticky="nsew")

        label_style = {'bg': "#1035ae", 'fg': "white", 'width': 40, 'highlightbackground': 'white', 'highlightthickness': 1}

        tk.Label(student_header_frame, text="Roll Number", **label_style, font=font.Font(size=16)).grid(row=0, column=0, sticky='w')
        tk.Label(student_header_frame, text="Student Name", **label_style, font=font.Font(size=16)).grid(row=0, column=1)
        tk.Label(student_header_frame, text="Attendance", **label_style, font=font.Font(size=16)).grid(row=0, column=2)

        self.attendance_frame = tk.Frame(scrollable_frame, bg="#1035ae", width=140)
        self.attendance_frame.grid(row=3, column=0, padx=10, pady=20, sticky="w")

        self.student_entries = []
        self.roll_entries = []
        self.attendance_dropdowns = []

        # Buttons Frame at the Bottom
        buttons_frame = tk.Frame(scrollable_frame, bg="#1035ae")
        buttons_frame.grid(row=4, column=0, pady=20, sticky="s")

        tk.Button(buttons_frame, text="Load Students", command=self.load_students_from_file, bg="white", fg="#1035ae", font=font.Font(size=16)).pack(side=tk.LEFT, padx=10)
        tk.Button(buttons_frame, text="Save Attendance", command=self.save_attendance, bg="white", fg="#1035ae", font=font.Font(size=16)).pack(side=tk.LEFT, padx=10)

    def display_students(self):
        for widget in self.attendance_frame.winfo_children():
            widget.destroy()

        self.student_entries = []
        self.roll_entries = []
        self.attendance_dropdowns = []

        for i, (name, roll) in enumerate(self.students):
            roll_entry = tk.Entry(self.attendance_frame, width=53, bg="white", font=font.Font(size=13))
            roll_entry.insert(0, roll)
            roll_entry.grid(row=i, column=0, padx=10, pady=10)
            roll_entry.config(state='readonly')

            student_entry = tk.Entry(self.attendance_frame, width=53, bg="white", font=font.Font(size=13))
            student_entry.insert(0, name)
            student_entry.grid(row=i, column=1, padx=10, pady=10)
            student_entry.config(state='readonly')

            attendance_var = tk.StringVar()
            attendance_dropdown = ttk.Combobox(self.attendance_frame, values=["Present", "Absent"], width=53, state="readonly", font=font.Font(size=13))
            attendance_dropdown.grid(row=i, column=2, padx=10, pady=10)
            attendance_dropdown.current(1)

            self.student_entries.append(student_entry)
            self.roll_entries.append(roll_entry)
            self.attendance_dropdowns.append(attendance_dropdown)

    def save_attendance(self):
        current_month_folder = datetime.now().strftime('%Y_%m')
        os.makedirs(current_month_folder, exist_ok=True)

        # Get the date from the input
        input_date = self.date.get()

        # Generate filename with input date
        filename = f"{current_month_folder}/attendance_{input_date}.csv"
        
        with open(filename, mode='w', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(["Teacher's Name", "Degree", "Semester", "Course Name", "Year", "Date", "Time"])
            writer.writerow([self.teacher_name.get(), self.degree.get(), self.semester.get(), self.course_name.get(), self.year.get(), input_date, datetime.now().strftime("%H:%M:%S")])
            writer.writerow([])
            writer.writerow(["Student Name", "Roll Number", "Status"])
            for i, (name, roll) in enumerate(self.students):
                status = self.attendance_dropdowns[i].get()
                writer.writerow([name, roll, status])

        messagebox.showinfo("Saved", f"Attendance data saved to {filename}")

    def load_students_from_file(self):
        file_path = filedialog.askopenfilename(filetypes=[("CSV files", "*.csv"), ("All files", "*.*")])
        if file_path:
            with open(file_path, mode='r') as file:
                reader = csv.reader(file)
                next(reader)  # Skip the header row
                self.students = [(row[1], row[0]) for row in reader]
                self.display_students()

if __name__ == "__main__":
    root = tk.Tk()
    app = AttendanceSystem(root)
    root.mainloop()
