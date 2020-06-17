import os
import tkinter as tk
from tkinter import ttk
from tkinter import filedialog as fd


class InputEntry(tk.Frame):

    def __init__(self, master, multiple=False, width=None, filetypes=None,
                 abbreviate=False):

        self._master = master
        self._multiple = multiple
        self._width = width
        self._filetypes = filetypes
        self._abbreviate = abbreviate

        super().__init__(master)

        self._inputs = []

        self._label_text = 'Input location:'
        self._button_text = 'Browse...'
        self._dialog_title = 'Select files:'

        self.label = ttk.Label(self, text=self._label_text)
        self.label.grid(row=0, column=0, sticky='EW')

        self.field = ttk.Entry(self, takefocus=0, width=width, state='readonly')
        self.field.grid(row=1, column=0, padx=(0, 2), sticky='EW')

        self.button = ttk.Button(
            self,
            takefocus=0,
            text=self._button_text,
            command=self._browse,
        )
        self.button.grid(row=1, column=1, sticky='NSEW')

        self.columnconfigure(0, weight=1)

    def get(self):
        return self._inputs if self._multiple else self._inputs[0]
    
    def clear(self):
        self.field['state'] = 'normal'
        self.field.delete(0, 'end')
        self.field['state'] = 'disabled' if self._multiple else 'readonly'

    def _browse(self):

        dialog = fd.askopenfilenames if self._multiple else fd.askopenfilename
        filepaths = dialog(title=self._dialog_title)
        if filepaths:
            self._inputs = list(filepaths) if self._multiple else [filepaths]
            self.field['state'] = 'normal'
            self.field.delete(0, 'end')
            for path in self._inputs:
                filepath = self._format_item(path, self._abbreviate, suffix=';')
                self.field.insert('end', filepath)
            self.field.delete(len(self.field.get())-1, 'end')

            self.field['state'] = 'readonly'
            self.field.update_idletasks()
            self.field.xview_moveto(1))
        
        # if self._post_command:
        #     pass # add post command functionality
    
    def _format_item(self, path, abbreviate=False, suffix=''):
        return f' {os.path.basename(path) if abbreviate else path}{suffix}'