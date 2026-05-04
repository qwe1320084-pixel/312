import tkinter as tk
from tkinter import ttk, messagebox
import random
import string
import json
import os

class PasswordGenerator:
    def __init__(self, root):
        self.root = root
        self.root.title("Random Password Generator")
        self.root.geometry("600x500")
        self.root.resizable(False, False)
        
        self.history_file = "history.json"
        self.history = self.load_history()
        
        self.create_widgets()
        self.update_history_table()
    
    # ------------------- Настройка интерфейса -------------------
    def create_widgets(self):
        # Рамка параметров
        frame_settings = ttk.LabelFrame(self.root, text="Настройки пароля", padding=10)
        frame_settings.pack(fill="x", padx=10, pady=5)
        
        # Ползунок длины
        ttk.Label(frame_settings, text="Длина пароля:").grid(row=0, column=0, sticky="w")
        self.length_var = tk.IntVar(value=12)
        self.length_scale = ttk.Scale(frame_settings, from_=4, to=32, orient="horizontal",
                                      variable=self.length_var, command=self.update_length_label)
        self.length_scale.grid(row=0, column=1, padx=10, pady=5, sticky="ew")
        self.length_label = ttk.Label(frame_settings, text="12")
        self.length_label.grid(row=0, column=2, padx=5)
        
        # Чекбоксы
        self.use_digits = tk.BooleanVar(value=True)
        self.use_letters = tk.BooleanVar(value=True)
        self.use_special = tk.BooleanVar(value=False)
        
        ttk.Checkbutton(frame_settings, text="Цифры (0-9)", variable=self.use_digits).grid(row=1, column=0, sticky="w")
        ttk.Checkbutton(frame_settings, text="Буквы (A-Z, a-z)", variable=self.use_letters).grid(row=1, column=1, sticky="w")
        ttk.Checkbutton(frame_settings, text="Спецсимволы (!@#$%^&*)", variable=self.use_special).grid(row=1, column=2, sticky="w")
        
        # Кнопка генерации
        self.generate_btn = ttk.Button(frame_settings, text="Сгенерировать пароль", command=self.generate_password)
        self.generate_btn.grid(row=2, column=0, columnspan=3, pady=10)
        
        # Поле вывода пароля
        ttk.Label(self.root, text="Сгенерированный пароль:").pack(anchor="w", padx=10)
        self.password_var = tk.StringVar()
        self.password_entry = ttk.Entry(self.root, textvariable=self.password_var, font=("Courier", 12), state="readonly")
        self.password_entry.pack(fill="x", padx=10, pady=5)
        
        # Кнопка копирования
        self.copy_btn = ttk.Button(self.root, text="Копировать в буфер", command=self.copy_to_clipboard)
        self.copy_btn.pack(pady=5)
        
        # История
        ttk.Label(self.root, text="История паролей:").pack(anchor="w", padx=10, pady=(10,0))
        frame_history = ttk.Frame(self.root)
        frame_history.pack(fill="both", expand=True, padx=10, pady=5)
        
        columns = ("#", "Пароль", "Длина", "Символы")
        self.tree = ttk.Treeview(frame_history, columns=columns, show="headings")
        self.tree.heading("#", text="№")
        self.tree.heading("Пароль", text="Пароль")
        self.tree.heading("Длина", text="Длина")
        self.tree.heading("Символы", text="Символы")
        self.tree.column("#", width=40)
        self.tree.column("Пароль", width=250)
        self.tree.column("Длина", width=60)
        self.tree.column("Символы", width=150)
        
        scrollbar = ttk.Scrollbar(frame_history, orient="vertical", command=self.tree.yview)
        self.tree.configure(yscrollcommand=scrollbar.set)
        self.tree.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
        
        # Кнопка очистки истории
        self.clear_btn = ttk.Button(self.root, text="Очистить историю", command=self.clear_history)
        self.clear_btn.pack(pady=5)
    
    def update_length_label(self, event=None):
        self.length_label.config(text=str(self.length_var.get()))
    
    # ------------------- Логика генерации -------------------
    def generate_password(self):
        length = self.length_var.get()
        use_digits = self.use_digits.get()
        use_letters = self.use_letters.get()
        use_special = self.use_special.get()
        
        # Проверка: хотя бы один тип символов выбран
        if not (use_digits or use_letters or use_special):
            messagebox.showerror("Ошибка", "Выберите хотя бы один тип символов!")
            return
        
        chars = ""
        if use_digits:
            chars += string.digits
        if use_letters:
            chars += string.ascii_letters
        if use_special:
            chars += "!@#$%^&*"
        
        # Генерация пароля
        password = ''.join(random.choice(chars) for _ in range(length))
        self.password_var.set(password)
        
        # Сохранение в историю
        symbols = []
        if use_digits: symbols.append("цифры")
        if use_letters: symbols.append("буквы")
        if use_special: symbols.append("спецсимволы")
        symbols_str = ", ".join(symbols)
        
        self.history.append({
            "password": password,
            "length": length,
            "symbols": symbols_str
        })
        self.save_history()
        self.update_history_table()
    
    # ------------------- История (JSON) -------------------
    def load_history(self):
        if os.path.exists(self.history_file):
            try:
                with open(self.history_file, "r", encoding="utf-8") as f:
                    return json.load(f)
            except:
                return []
        return []
    
    def save_history(self):
        with open(self.history_file, "w", encoding="utf-8") as f:
            json.dump(self.history, f, indent=4, ensure_ascii=False)
    
    def update_history_table(self):
        for row in self.tree.get_children():
            self.tree.delete(row)
        for idx, item in enumerate(self.history, start=1):
            self.tree.insert("", "end", values=(idx, item["password"], item["length"], item["symbols"]))
    
    def clear_history(self):
        if messagebox.askyesno("Подтверждение", "Очистить всю историю?"):
            self.history = []
            self.save_history()
            self.update_history_table()
    
    # ------------------- Копирование -------------------
    def copy_to_clipboard(self):
        pwd = self.password_var.get()
        if pwd:
            self.root.clipboard_clear()
            self.root.clipboard_append(pwd)
            messagebox.showinfo("Успех", "Пароль скопирован в буфер обмена!")
        else:
            messagebox.showwarning("Внимание", "Нет пароля для копирования.")

# ------------------- Запуск приложения -------------------
if __name__ == "__main__":
    root = tk.Tk()
    app = PasswordGenerator(root)
    root.mainloop()
