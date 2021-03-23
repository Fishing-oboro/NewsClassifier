import tkinter as tk
import os
from tkinter import *
from tkinter import ttk
from tkinter import filedialog
from tkinter import scrolledtext
from tkinter import messagebox
import create_csv.main as cm


class ImageGenerator:
    def __init__(self, root, pos_x, pos_y):
        self.root = root
        self.pos_x = pos_x
        self.pos_y = pos_y
        self.size_x = 50
        self.size_y = 20
        self.url = 'statics'
        self.com = tk.Label(self.root, text='ニュース本文を入力してください。')
        self.com.grid(row=0, column=0, padx=5, pady=5)
        self.canvas = scrolledtext.ScrolledText(self.root, bd=5, width=self.size_x, height=self.size_y)
        self.canvas.grid(row=1, column=0, columnspan=2, padx=5, pady=5)

        self.frame1 = ttk.Frame(root, padding=10)
        self.frame1.grid(row=2, column=0, columnspan=1, padx=5, pady=5, sticky=E)
        ttl_label = ttk.Label(self.frame1, text="　　 タイトル＞＞", padding=(5, 2))
        ttl_label.pack(side=LEFT)
        self.entry1 = StringVar()
        ttl_entry = ttk.Entry(self.frame1, textvariable=self.entry1, width=30)
        ttl_entry.pack(side=LEFT)

        self.frame2 = ttk.Frame(root, padding=10)
        self.frame2.grid(row=3, column=0, columnspan=3, padx=5, sticky=E)
        dir_label = ttk.Label(self.frame2, text="保存先フォルダ＞＞", padding=(5, 2))
        dir_label.pack(side=LEFT)
        self.entry2 = StringVar()
        dir_entry = ttk.Entry(self.frame2, textvariable=self.entry2, width=30)
        dir_entry.pack(side=LEFT)
        dir_button = ttk.Button(self.frame2, text="参照", command=self.dir_dialog)
        dir_button.pack(side=LEFT)

        self.button2 = tk.Button(self.root, text="推論", width=10, bg='white', command=self.predict)
        self.button2.grid(row=4, column=0, padx=5, pady=5)
        self.label = tk.Label(self.root, text='推論結果:')
        self.label.grid(row=4, column=1, padx=5, pady=5)

    def predict(self):
        text = self.canvas.get('1.0', 'end')
        title = self.entry1.get()
        if text is '\n':
            return
        if title:
            result = cm.text_categorize(text, title=title, url=self.url)
        else:
            result = cm.text_categorize(text, url=self.url)
        self.label['text'] = f'推論結果: {result}'
        self.label.update()

    def dir_dialog(self):
        url = os.path.abspath(os.path.dirname(__file__))
        path = filedialog.askdirectory(initialdir=url)
        self.entry2.set(path)
        if path:
            messagebox.showinfo('info', f'{path}を保存先に指定しました')
            self.url = f'{path}/statics'
        else:
            messagebox.showerror('error', 'パスの指定がありません')
