import tkinter as tk
from tkinter import scrolledtext
import create_csv.main as cm


class ImageGenerator:
    def __init__(self, root, pos_x, pos_y):
        self.root = root
        self.pos_x = pos_x
        self.pos_y = pos_y
        self.size_x = 50
        self.size_y = 20
        self.com = tk.Label(self.root, text='ニュース本文を入力してください。')
        self.com.grid(row=0, column=0, padx=5, pady=5)
        self.canvas = scrolledtext.ScrolledText(self.root, bd=5, width=self.size_x, height=self.size_y)
        self.canvas.grid(row=1, column=0, columnspan=2, padx=5, pady=5)
        # self.title = tk.Entry(self.root, bd=5)
        # self.title.grid(row=2, column=0, columnspan=2, padx=5, pady=5)
        self.button2 = tk.Button(self.root, text="推論", width=10, bg='white', command=self.predict)
        self.button2.grid(row=2, column=0, padx=5, pady=5)
        self.label = tk.Label(self.root, text='推論結果:')
        self.label.grid(row=2, column=1, padx=5, pady=5)

    def predict(self):
        text = self.canvas.get('1.0', 'end')
        if text is '\n':
            return
        result = cm.text_categorize(text)

        self.label['text'] = f'推論結果: {result}'
        self.label.update()
