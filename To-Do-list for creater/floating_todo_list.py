import tkinter as tk
from tkinter import messagebox, simpledialog, ttk
from datetime import datetime
import json

class FloatingToDoList:
    def __init__(self, root):
        self.root = root
        self.root.title("Floating To-Do List")
        self.root.geometry("400x500")
        self.root.minsize(300, 400)  # Set minimum size
        self.root.attributes("-topmost", True)  # Keep window on top
        self.root.configure(bg='lightblue')  # Background color

        self.tasks = []

        # Create a text area for the to-do list
        self.text_area = tk.Text(root, wrap='word', bg='white', fg='black')
        self.text_area.pack(expand=True, fill='both')

        # Create a search bar
        self.search_var = tk.StringVar()
        self.search_entry = ttk.Entry(root, textvariable=self.search_var)
        self.search_entry.pack(side='top', fill='x', padx=10, pady=5)
        self.search_entry.bind("<KeyRelease>", self.search_tasks)

        # Create a frame for buttons
        self.button_frame = ttk.Frame(root)
        self.button_frame.pack(side='top', fill='x', padx=10, pady=5)

        # Create buttons with styling
        self.style = ttk.Style()
        self.style.configure("TButton", padding=3, relief="flat", background="lightgreen", foreground="black", font=("Arial", 7, "bold"))

        self.add_button = ttk.Button(self.button_frame, text="Add Task", command=self.add_task)
        self.add_button.pack(side='left', fill='x', expand=True)

        self.remove_button = ttk.Button(self.button_frame, text="Remove Task", command=self.remove_task)
        self.remove_button.pack(side='left', fill='x', expand=True)

        self.complete_button = ttk.Button(self.button_frame, text="Complete Task", command=self.complete_task)
        self.complete_button.pack(side='left', fill='x', expand=True)

        self.save_button = ttk.Button(self.button_frame, text="Save Tasks", command=self.save_tasks)
        self.save_button.pack(side='left', fill='x', expand=True)

        self.load_button = ttk.Button(self.button_frame, text="Load Tasks", command=self.load_tasks)
        self.load_button.pack(side='left', fill='x', expand=True)

        # Transparency and Movability
        self.root.wm_attributes("-alpha", 0.9)  # Set transparency
        self.root.bind("<Button-1>", self.start_move)
        self.root.bind("<B1-Motion>", self.move_window)

    def start_move(self, event):
        self.x = event.x
        self.y = event.y

    def move_window(self, event):
        x = self.root.winfo_x() - self.x + event.x
        y = self.root.winfo_y() - self.y + event.y
        self.root.geometry(f"+{x}+{y}")

    def ai_suggest_tasks(self, user_input):
        # Simple AI task suggestions based on user input
        suggestions = [
            "Buy groceries",
            "Finish project report",
            "Call the doctor",
            "Schedule a meeting",
            "Read a book",
            "Exercise for 30 minutes",
            "Prepare for the presentation"
        ]
        return [task for task in suggestions if user_input.lower() in task.lower()]

    def add_task(self):
        task = simpledialog.askstring("Add Task", "Enter a new task:")
        if task:
            # Get AI suggestions based on user input
            ai_suggestions = self.ai_suggest_tasks(task)
            if ai_suggestions:
                suggestion_message = "AI Suggestions:\n" + "\n".join(ai_suggestions)
                messagebox.showinfo("Suggestions", suggestion_message)

            priority = simpledialog.askstring("Task Priority", "Enter priority (High, Medium, Low):")
            due_date = simpledialog.askstring("Due Date", "Enter due date (YYYY-MM-DD):")
            self.tasks.append({"task": task, "priority": priority, "due_date": due_date, "completed": False})
            self.update_text_area()

    def remove_task(self):
        selected_task = simpledialog.askstring("Remove Task", "Enter the task to remove:")
        for task in self.tasks:
            if task["task"] == selected_task:
                self.tasks.remove(task)
                self.update_text_area()
                return
        messagebox.showerror("Error", "Task not found.")

    def complete_task(self):
        selected_task = self.text_area.get("1.0", tk.END).strip().split('\n')
        if selected_task:
            task_to_complete = simpledialog.askstring("Complete Task", "Enter the task to complete:")
            for task in self.tasks:
                if task["task"] == task_to_complete:
                    task["completed"] = True
                    self.update_text_area()
                    return
            messagebox.showerror("Error", "Task not found.")

    def search_tasks(self, event):
        search_term = self.search_var.get().lower()
        filtered_tasks = [task for task in self.tasks if search_term in task["task"].lower()]
        self.text_area.delete("1.0", tk.END)
        for task in filtered_tasks:
            self.text_area.insert(tk.END, f"{task['task']} (Priority: {task['priority']}, Due: {task['due_date']})\n")

    def save_tasks(self):
        with open("tasks.json", "w") as f:
            json.dump(self.tasks, f)
        messagebox.showinfo("Success", "Tasks saved successfully.")

    def load_tasks(self):
        try:
            with open("tasks.json", "r") as f:
                self.tasks = json.load(f)
            self.update_text_area()
            messagebox.showinfo("Success", "Tasks loaded successfully.")
        except FileNotFoundError:
            messagebox.showerror("Error", "No saved tasks found.")

    def update_text_area(self):
        self.text_area.delete("1.0", tk.END)
        for task in self.tasks:
            self.text_area.insert(tk.END, f"{task['task']} (Priority: {task['priority']}, Due: {task['due_date']})\n")

if __name__ == "__main__":
    root = tk.Tk()
    app = FloatingToDoList(root)
    root.mainloop()
