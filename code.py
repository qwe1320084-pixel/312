import tkinter as tk
from tkinter import ttk, messagebox

# Фиксированные курсы (примерные значения)
EXCHANGE_RATES = {
    'USD': 0.0108,  # 1 рубль = 0.0108 USD
    'EUR': 0.0100,  # 1 рубль = 0.0100 EUR
    'GBP': 0.0092   # 1 рубль = 0.0092 GBP
}

def convert_currency():
    try:
        amount_rub = float(entry_rub.get())
        selected_currency = currency_var.get()
        rate = EXCHANGE_RATES[selected_currency]
        result = amount_rub * rate
        label_result.config(text=f"{result:.2f} {selected_currency}")
    except ValueError:
        messagebox.showerror("Ошибка", "Пожалуйста, введите корректное число.")
    except KeyError:
        messagebox.showerror("Ошибка", "Выберите валюту из списка.")

# Создание окна
root = tk.Tk()
root.title("Конвертер валют")
root.geometry("350x150")

# Ввод суммы в рублях
tk.Label(root, text="Сумма в рублях:").pack(pady=5)
entry_rub = tk.Entry(root)
entry_rub.pack(pady=5)

# Выпадающий список валют
tk.Label(root, text="Выберите валюту:").pack(pady=5)
currency_var = tk.StringVar()
currency_dropdown = ttk.Combobox(root, textvariable=currency_var, values=list(EXCHANGE_RATES.keys()))
currency_dropdown.current(0)  # По умолчанию USD
currency_dropdown.pack(pady=5)

# Кнопка конвертации
tk.Button(root, text="Конвертировать", command=convert_currency).pack(pady=10)

# Поле для вывода результата
label_result = tk.Label(root, text="", font=("Arial", 14))
label_result.pack(pady=10)

root.mainloop()
