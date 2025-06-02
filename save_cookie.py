import tkinter as tk
from tkinter import filedialog, messagebox
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import time
import pickle
import threading
import os

# 默认值
DEFAULT_URL = "https://weibo.com"
DEFAULT_CHROMEDRIVER_PATH = r"E:\chromedriver-win64\chromedriver.exe"  # ← 修改为你的默认路径

def start_browser(chrome_path, url):
    options = Options()
    options.add_argument('--disable-blink-features=AutomationControlled')

    try:
        driver = webdriver.Chrome(executable_path=chrome_path, options=options)
        driver.get(url)
        messagebox.showinfo("提示", "请在60秒内完成登录微博")
        time.sleep(60)

        with open("weibo_cookies.pkl", "wb") as f:
            pickle.dump(driver.get_cookies(), f)

        messagebox.showinfo("成功", "Cookie 已保存为 weibo_cookies.pkl")
        driver.quit()
    except Exception as e:
        messagebox.showerror("错误", f"启动浏览器失败：\n{e}")

def on_start():
    chrome_path = path_entry.get().strip()
    url = url_entry.get().strip()
    if not chrome_path or not os.path.isfile(chrome_path):
        messagebox.showwarning("提示", "请正确填写 chromedriver 路径")
        return
    if not url:
        messagebox.showwarning("提示", "请输入微博网址")
        return
    threading.Thread(target=start_browser, args=(chrome_path, url), daemon=True).start()

def browse_path():
    path = filedialog.askopenfilename(title="选择 chromedriver.exe", filetypes=[("可执行文件", "*.exe")])
    if path:
        path_entry.delete(0, tk.END)
        path_entry.insert(0, path)

# GUI
root = tk.Tk()
root.title("微博 Cookie 保存器")
root.geometry("500x220")

# 微博地址输入
tk.Label(root, text="微博网址：").pack(pady=5)
url_entry = tk.Entry(root, width=60)
url_entry.insert(0, DEFAULT_URL)
url_entry.pack()

# chromedriver 路径输入
tk.Label(root, text="chromedriver.exe 路径：").pack(pady=5)
frame = tk.Frame(root)
frame.pack()
path_entry = tk.Entry(frame, width=45)
path_entry.insert(0, DEFAULT_CHROMEDRIVER_PATH)
path_entry.pack(side=tk.LEFT, padx=5)
browse_button = tk.Button(frame, text="浏览", command=browse_path)
browse_button.pack(side=tk.LEFT)

# 启动按钮
start_button = tk.Button(root, text="启动浏览器并保存 Cookie", command=on_start)
start_button.pack(pady=20)

root.mainloop()
