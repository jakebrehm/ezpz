import tkinter as tk
from tkinter import ttk


class ScrollableFrame(tk.Frame):

    def __init__(self, master, *args, cwidth=None, cheight=None, **kwargs):

        self.master = master

        self.frame = tk.Frame(master)
        self.frame.columnconfigure(0, weight=1)

        self.canvas = tk.Canvas(self.frame, bd=0, highlightthickness=0)
        self.canvas.grid(row=0, column=0, sticky='NSEW')
        if cwidth:
            self.canvas.config(width=cwidth)
        if cheight:
            self.canvas.config(height=cheight)

        self.scrollbar = tk.Scrollbar(self.frame)
        self.scrollbar.grid(row=0, column=1, sticky='NSE')

        super().__init__(master=self.canvas, *args, **kwargs)
        self.canvas.create_window(0, 0, window=self, anchor='nw', tags='window')
        self.columnconfigure(0, weight=1)
        if cwidth:
            self.columnconfigure(0, minsize=cwidth)

        self.update()
        self.bind('<Visibility>', self.update)
        self.bind('<Configure>', self.update)

    def scroll(self):

        def enter_canvas(event):
            self.canvas.bind_all('<MouseWheel>', scroll_canvas)

        def leave_canvas(event):
            self.canvas.unbind_all('<MouseWheel>')

        def scroll_canvas(event):
            self.canvas.yview_scroll(int(-1*(event.delta/1)), 'units')

        self.frame.bind('<Enter>', enter_canvas)
        self.frame.bind('<Leave>', leave_canvas)

    def update(self, event=None):
        self.update_idletasks()
        self.canvas.itemconfig(
            'window',
            width=self.canvas.winfo_width(),
        )
        self.canvas.config(yscrollcommand=self.scrollbar.set)
        self.canvas.config(scrollregion=self.canvas.bbox('all'))
        if self.canvas.bbox('all')[-1] > self.canvas.winfo_height():
            self.scrollbar['command'] = self.canvas.yview
            self.canvas.config(yscrollincrement=1)
            self.scroll()
        else:
            self.unbind('<Enter>')
            self.unbind('<Leave>')
            self.canvas.unbind_all('<MouseWheel>')

    def grid(self, *args, **kwargs):
        self.frame.grid(*args, **kwargs)
    
    def grid_remove(self):
        self.frame.grid_remove()


class ScrollableTab(ScrollableFrame):

    def __init__(self, notebook, title, *args, **kwargs):

        self.notebook = notebook

        master_name = self.notebook.winfo_parent()
        master = self.notebook._nametowidget(master_name)

        super().__init__(master, *args, **kwargs)

        self.notebook.add(self.frame, text=title)
    
    def grid(self, *args, **kwargs):
        _class = self.__class__.__name__
        method = self.grid.__name__
        raise AttributeError(f"'{_class}' object has no method '{method}'")
    
    def grid_remove(self):
        _class = self.__class__.__name__
        method = self.grid_remove.__name__
        raise AttributeError(f"'{_class}' object has no method '{method}'")
