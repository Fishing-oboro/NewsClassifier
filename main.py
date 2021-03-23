import tkinter as tk
from news import ImageGenerator

root = tk.Tk()
root.wm_geometry("%dx%d+%d+%d" % (450, 450, 10, 10))
root.config(bg='white')
root.title('ニュース記事分類')
ImageGenerator(root, 10, 10)
root.mainloop()
