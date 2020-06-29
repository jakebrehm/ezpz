import tkinter as tk
from tkinter import ttk


class Application(tk.Frame):

    def __init__(self, *args, padding=None, **kwargs):

        self._padding = padding

        self._root = tk.Tk(*args, **kwargs)
        self._root.rowconfigure(0, weight=1)
        self._root.columnconfigure(0, weight=1)

        super().__init__(master=self._root)

        self.grid(row=0, column=0, padx=padding, pady=padding, sticky='NSEW')
        self.rowconfigure(0, weight=1)
        self.columnconfigure(0, weight=1)

    def geometry(self, width, height, center=False):
        self._root.geometry(f'{width}x{height}')
        if center:
            CenterWindow(self._root)

    def mainloop(self):
        self._root.mainloop()
    
    @property
    def root(self):
        return self._root


def CenterWindow(window):
    if isinstance(window, Application):
        window = window.root
    window.update()
    X_POSITION = ( window.winfo_screenwidth() - window.winfo_width() ) // 2
    Y_POSITION = ( window.winfo_screenheight() - window.winfo_height() ) // 2
    window.geometry(f'+{X_POSITION}+{Y_POSITION}')


def GetRoot(widget):
    root = widget.nametowidget(widget.winfo_toplevel())
    while not isinstance(root, tk.Tk):
        root = root.nametowidget(root.winfo_parent())
    return root