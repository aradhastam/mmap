import socket
from tqdm import tqdm
import tkinter as tk
from tkinter import messagebox
import threading

# تابعی برای چک کردن پورت‌ها
def check_ports(target_ip, start_port, end_port, result_label, progress_bar):
    open_ports = []
    for port in tqdm(range(start_port, end_port + 1), desc="Scanning Ports", unit="port"):
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(1)
        result = sock.connect_ex((target_ip, port))
        if result == 0:
            open_ports.append(port)
        sock.close()
        progress_bar['value'] = (port - start_port + 1) / (end_port - start_port + 1) * 100
        root.update_idletasks()

    if open_ports:
        result_label.config(text=f"پورت‌های باز: {open_ports}")
    else:
        result_label.config(text="هیچ پورت بازی پیدا نشد.")

# تابع برای اجرای بررسی در یک ترد جداگانه برای گرافیک
def start_scan():
    target = entry_target.get()
    try:
        start_port = int(entry_start_port.get())
        end_port = int(entry_end_port.get())
    except ValueError:
        messagebox.showerror("خطا", "پورت‌ها باید اعداد صحیح باشند.")
        return
    
    try:
        target_ip = socket.gethostbyname(target)
    except socket.gaierror:
        messagebox.showerror("خطا", "آدرس سایت وارد شده معتبر نیست.")
        return
    
    result_label.config(text="در حال بررسی...")
    progress_bar['value'] = 0
    thread = threading.Thread(target=check_ports, args=(target_ip, start_port, end_port, result_label, progress_bar))
    thread.start()

# تابع برای اجرای ترمینال
def terminal_scan():
    target = input("آدرس سایت (دامنه یا IP): ")
    try:
        start_port = int(input("پورت شروع: "))
        end_port = int(input("پورت پایان: "))
    except ValueError:
        print("پورت‌ها باید اعداد صحیح باشند.")
        return

    try:
        target_ip = socket.gethostbyname(target)
    except socket.gaierror:
        print("آدرس سایت وارد شده معتبر نیست.")
        return

    open_ports = check_ports_terminal(target_ip, start_port, end_port)
    if open_ports:
        print(f"پورت‌های باز برای {target} ({target_ip}): {open_ports}")
    else:
        print(f"هیچ پورت بازی پیدا نشد.")

# تابع برای چک کردن پورت‌ها در ترمینال (بدون گرافیک)
def check_ports_terminal(target_ip, start_port, end_port):
    open_ports = []
    for port in tqdm(range(start_port, end_port + 1), desc="Scanning Ports", unit="port"):
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(1)
        result = sock.connect_ex((target_ip, port))
        if result == 0:
            open_ports.append(port)
        sock.close()
    return open_ports

# منوی انتخاب گرافیک یا ترمینال
def choose_mode():
    choice = input("آیا می‌خواهید از رابط گرافیکی استفاده کنید؟ (y/n): ").strip().lower()
    if choice == 'y':
        start_gui()
    elif choice == 'n':
        terminal_scan()
    else:
        print("لطفاً 'y' یا 'n' وارد کنید.")
        choose_mode()

# تنظیمات پنجره گرافیکی
def start_gui():
    global root, entry_target, entry_start_port, entry_end_port, result_label, progress_bar

    root = tk.Tk()
    root.title("بررسی پورت‌های سایت")

    # ورودی‌ها
    label_target = tk.Label(root, text="آدرس سایت یا IP:")
    label_target.pack()
    entry_target = tk.Entry(root, width=30)
    entry_target.pack()

    label_start_port = tk.Label(root, text="پورت شروع:")
    label_start_port.pack()
    entry_start_port = tk.Entry(root, width=30)
    entry_start_port.pack()

    label_end_port = tk.Label(root, text="پورت پایان:")
    label_end_port.pack()
    entry_end_port = tk.Entry(root, width=30)
    entry_end_port.pack()

    # دکمه شروع اسکن
    scan_button = tk.Button(root, text="شروع اسکن", command=start_scan)
    scan_button.pack()

    # نوار لود
    progress_bar = tk.Progressbar(root, orient="horizontal", length=300, mode="determinate")
    progress_bar.pack(pady=10)

    # برچسب برای نمایش نتایج
    result_label = tk.Label(root, text="")
    result_label.pack()

    # اجرای رابط گرافیکی
    root.mainloop()

# فراخوانی منوی انتخاب
choose_mode()
