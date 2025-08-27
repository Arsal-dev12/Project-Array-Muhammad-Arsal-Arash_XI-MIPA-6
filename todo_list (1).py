
import tkinter as tk
from tkinter import ttk, messagebox
from datetime import datetime

# Aplikasi To-Do List Modern dengan Array
class ToDoApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Project Array Muhammad Arsal Arash - XI MIPA 6")
        self.root.geometry("700x500")
        self.root.configure(bg="#f4f6f9")

        # Data Array untuk menyimpan task
        self.tasks = []

        # Frame input
        input_frame = tk.Frame(self.root, bg="#f4f6f9")
        input_frame.pack(pady=10)

        tk.Label(input_frame, text="Task:", bg="#f4f6f9").grid(row=0, column=0, padx=5)
        self.task_entry = tk.Entry(input_frame, width=30)
        self.task_entry.grid(row=0, column=1, padx=5)

        tk.Label(input_frame, text="Deadline (YYYY-MM-DD):", bg="#f4f6f9").grid(row=0, column=2, padx=5)
        self.deadline_entry = tk.Entry(input_frame, width=15)
        self.deadline_entry.grid(row=0, column=3, padx=5)

        add_button = tk.Button(input_frame, text="Add Task", command=self.add_task, bg="#4CAF50", fg="white")
        add_button.grid(row=0, column=4, padx=5)

        delete_button = tk.Button(input_frame, text="Delete Selected", command=self.delete_task, bg="#E74C3C", fg="white")
        delete_button.grid(row=0, column=5, padx=5)

        # Treeview untuk menampilkan task
        self.tree = ttk.Treeview(self.root, columns=("Task", "Added", "Deadline", "Status"), show="headings", height=12)
        self.tree.heading("Task", text="Task")
        self.tree.heading("Added", text="Added On")
        self.tree.heading("Deadline", text="Deadline")
        self.tree.heading("Status", text="Status")

        self.tree.column("Task", width=200)
        self.tree.column("Added", width=120)
        self.tree.column("Deadline", width=120)
        self.tree.column("Status", width=80)

        self.tree.pack(pady=10)

        # Progress bar
        self.progress = ttk.Progressbar(self.root, orient="horizontal", length=500, mode="determinate")
        self.progress.pack(pady=10)

        # Label motivasi
        self.motivation_label = tk.Label(self.root, text="", bg="#f4f6f9", font=("Arial", 12, "italic"))
        self.motivation_label.pack()

        # Button selesaiin task
        done_button = tk.Button(self.root, text="Mark as Done", command=self.mark_done, bg="#3498DB", fg="white")
        done_button.pack(pady=5)

    def add_task(self):
        task_name = self.task_entry.get().strip()
        deadline = self.deadline_entry.get().strip()
        if not task_name:
            messagebox.showwarning("Warning", "Task tidak boleh kosong!")
            return
        try:
            if deadline:
                datetime.strptime(deadline, "%Y-%m-%d")
        except ValueError:
            messagebox.showwarning("Warning", "Format deadline harus YYYY-MM-DD")
            return

        added_date = datetime.now().strftime("%Y-%m-%d")
        self.tasks.append([task_name, added_date, deadline, "Pending"])
        self.refresh_table()
        self.task_entry.delete(0, tk.END)
        self.deadline_entry.delete(0, tk.END)

    def delete_task(self):
        selected_items = self.tree.selection()
        if not selected_items:
            messagebox.showwarning("Warning", "Pilih task yang ingin dihapus!")
            return
        for item in selected_items:
            values = self.tree.item(item, "values")
            for t in self.tasks:
                if t[0] == values[0] and t[1] == values[1]:
                    self.tasks.remove(t)
                    break
        self.refresh_table()

    def mark_done(self):
        selected_items = self.tree.selection()
        if not selected_items:
            messagebox.showwarning("Warning", "Pilih task yang ingin ditandai selesai!")
            return
        for item in selected_items:
            values = self.tree.item(item, "values")
            for t in self.tasks:
                if t[0] == values[0] and t[1] == values[1]:
                    t[3] = "Done"
        self.refresh_table()

    def refresh_table(self):
        for row in self.tree.get_children():
            self.tree.delete(row)
        for task in self.tasks:
            self.tree.insert("", tk.END, values=task)
        self.update_progress()

    def update_progress(self):
        if not self.tasks:
            self.progress["value"] = 0
            self.motivation_label.config(text="")
            return

        done_count = sum(1 for t in self.tasks if t[3] == "Done")
        total = len(self.tasks)
        percentage = (done_count / total) * 100
        self.progress["value"] = percentage

        if done_count == total:
            self.motivation_label.config(text="Yeayy 🎉 semua tugas selesai!")
        else:
            self.motivation_label.config(text=f"Sisa {total - done_count} tugas, ayo semangat! 💪")

if __name__ == "__main__":
    root = tk.Tk()
    app = ToDoApp(root)
    root.mainloop()
