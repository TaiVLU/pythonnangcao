import tkinter as tk
from tkinter import ttk

root = tk.Tk()
root.title("Form Tính Toán")

menu = tk.Menu(root)
root.config(menu=menu)

file_menu = tk.Menu(menu, tearoff=0)
menu.add_cascade(label="Tính Toán", menu=file_menu)
file_menu.add_command(label="Lưu Kết Quả")
file_menu.add_command(label="Xem Kết Quả")

tab_control = ttk.Notebook(root)

tab1 = ttk.Frame(tab_control)  # Tab Cộng/Trừ
tab2 = ttk.Frame(tab_control)  # Tab Nhân/Chia

tab_control.add(tab1, text='Cộng/Trừ')
tab_control.add(tab2, text='Nhân/Chia')

tab_control.pack(expand=1, fill='both')

frame1 = tk.Frame(tab1)
frame1.pack(padx=10, pady=10)

tk.Label(frame1, text="Nhập số a:").grid(row=0, column=0, padx=5, pady=5)
entry_a1 = tk.Entry(frame1)
entry_a1.grid(row=0, column=1, padx=5, pady=5)

tk.Label(frame1, text="Nhập số b:").grid(row=1, column=0, padx=5, pady=5)
entry_b1 = tk.Entry(frame1)
entry_b1.grid(row=1, column=1, padx=5, pady=5)

result_label1 = tk.Label(frame1, text="Kết quả: ")
result_label1.grid(row=2, column=0, columnspan=2, pady=5)

def tinh_cong_tru():
    a = float(entry_a1.get())
    b = float(entry_b1.get())
    ket_qua_cong = a + b
    ket_qua_tru = a - b
    result_label1.config(text=f"Cộng: {ket_qua_cong}, Trừ: {ket_qua_tru}")

tk.Button(frame1, text="Tính Cộng/Trừ", command=tinh_cong_tru).grid(row=3, column=0, columnspan=2, pady=5)

frame2 = tk.Frame(tab2)
frame2.pack(padx=10, pady=10)

tk.Label(frame2, text="Nhập số a:").grid(row=0, column=0, padx=5, pady=5)
entry_a2 = tk.Entry(frame2)
entry_a2.grid(row=0, column=1, padx=5, pady=5)

tk.Label(frame2, text="Nhập số b:").grid(row=1, column=0, padx=5, pady=5)
entry_b2 = tk.Entry(frame2)
entry_b2.grid(row=1, column=1, padx=5, pady=5)

result_label2 = tk.Label(frame2, text="Kết quả: ")
result_label2.grid(row=2, column=0, columnspan=2, pady=5)

def tinh_nhan_chia():
    a = float(entry_a2.get())
    b = float(entry_b2.get())
    if b != 0:
        ket_qua_nhan = a * b
        ket_qua_chia = a / b
        result_label2.config(text=f"Nhân: {ket_qua_nhan}, Chia: {ket_qua_chia:.2f}")
    else:
        result_label2.config(text="Lỗi: Không thể chia cho 0")

tk.Button(frame2, text="Tính Nhân/Chia", command=tinh_nhan_chia).grid(row=3, column=0, columnspan=2, pady=5)

root.mainloop()
