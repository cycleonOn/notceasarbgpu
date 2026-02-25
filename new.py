import tkinter as tk
from tkinter import ttk, messagebox
import random
import string
import pyperclip  # pip install pyperclip


class PasswordGeneratorApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Генератор паролей")
        self.root.geometry("400x350")
        self.root.resizable(False, False)

       
        self.root.configure(bg="#1e1e2f")

       
        title_label = tk.Label(root, text="Генератор паролей", font=("Arial", 16, "bold"), bg="#1e1e2f", fg="#ffffff")
        title_label.pack(pady=10)

       
        length_frame = tk.Frame(root, bg="#1e1e2f")
        length_frame.pack(pady=10)
        tk.Label(length_frame, text="Длина пароля:", bg="#1e1e2f", fg="#ffffff").pack(side=tk.LEFT, padx=5)

        self.length_var = tk.IntVar(value=12)
        self.length_spin = ttk.Spinbox(length_frame, from_=8, to=32, textvariable=self.length_var, width=5)
        self.length_spin.pack(side=tk.LEFT)

        
        tk.Label(root, text="Сложность:", bg="#1e1e2f", fg="#ffffff").pack(pady=5)
        self.complexity_var = tk.StringVar(value="medium")
        ttk.Radiobutton(root, text="Простая (только буквы)", variable=self.complexity_var, value="low").pack()
        ttk.Radiobutton(root, text="Средняя (буквы и цифры)", variable=self.complexity_var, value="medium").pack()
        ttk.Radiobutton(root, text="Сложная (всё подряд)", variable=self.complexity_var, value="high").pack()

        
        generate_btn = ttk.Button(root, text="Сгенерировать пароль", command=self.generate_password)
        generate_btn.pack(pady=15)

       
        self.password_entry = ttk.Entry(root, width=35, font=("Consolas", 12))
        self.password_entry.pack(pady=5)

        
        copy_btn = ttk.Button(root, text="Копировать", command=self.copy_to_clipboard)
        copy_btn.pack(pady=5)

    def generate_password(self):
        length = self.length_var.get()
        complexity = self.complexity_var.get()

        if length < 8 or length > 32:
            messagebox.showerror("Ошибка", "Длина пароля должна быть от 8 до 32 символов!")
            return

        chars = string.ascii_letters
        if complexity == "medium":
            chars += string.digits
        elif complexity == "high":
            chars += string.digits + string.punctuation

        password = ''.join(random.choice(chars) for _ in range(length))
        self.password_entry.delete(0, tk.END)
        self.password_entry.insert(0, password)

    def copy_to_clipboard(self):
        password = self.password_entry.get()
        if password:
            pyperclip.copy(password)
            messagebox.showinfo("Скопировано", "Пароль успешно скопирован в буфер обмена!")
        else:
            messagebox.showwarning("Пусто", "Сначала сгенерируйте пароль.")


if __name__ == "__main__":
    root = tk.Tk()
    app = PasswordGeneratorApp(root)
    root.mainloop()
