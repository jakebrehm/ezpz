import os
import tkinter as tk
from tkinter import filedialog as fd
from tkinter import ttk


class InputObject(tk.Frame):

    def __init__(self, master, multiple=False, width=None, filetypes=None,
                 abbreviate=False):

        self._master = master
        self._width = width
        self._multiple = multiple
        self._filetypes = filetypes
        self._abbreviate = abbreviate

        super().__init__(master)
        self.columnconfigure(0, weight=1)

        self._inputs = []

        self._label_text = 'Input location:'
        self._button_text = 'Browse...'
        self._dialog_title = 'Select files:'

        self.label = None
        self.field = None
        self.button = None

    def get(self):
        return self._inputs
    
    def clear(self):
        self.field['state'] = 'normal'
        self.field.delete(0, 'end')
        self.field['state'] = 'disabled' if self._multiple else 'readonly'
        self._inputs = []

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
            self.field.xview_moveto(1)

    def _format_item(self, path, abbreviate=False, suffix=''):
        return f' {os.path.basename(path) if abbreviate else path}{suffix}'
    
    @property
    def label_text(self):
        return self._label_text
    
    @label_text.setter
    def label_text(self, value):
        self._label_text = value
        if self.label:
            self.label['text'] = value
    
    @property
    def button_text(self):
        return self._button_text
    
    @button_text.setter
    def button_text(self, value):
        self._button_text = value
        if self.button:
            self.button['text'] = value
    
    @property
    def dialog_title(self):
        return self._dialog_title
    
    @dialog_title.setter
    def dialog_title(self, value):
        self._dialog_title = value


class InputEntry(InputObject):

    def __init__(self, master, width=None, filetypes=None, abbreviate=False):
        
        super().__init__(master, False, width, filetypes, abbreviate)
    
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


class InputList(InputObject):

    def __init__(self, master, width=None, filetypes=None, abbreviate=False):
        
        super().__init__(master, True, width, filetypes, abbreviate)

        self.label = None

        self.field = tk.Listbox(
            self,
            state='disabled',
            height=5,
            width=width,
            justify='center',
        )
        self.field.grid(row=0, column=0, padx=(0, 2), sticky='EW')

        controls = tk.Frame(self)
        controls.grid(row=0, column=1, sticky='NSEW')
        controls.rowconfigure(0, weight=1)
        self.button = ttk.Button(
            controls,
            takefocus=0,
            text=self._button_text,
            command=self._browse,
        )
        self.button.grid(row=0, column=0, sticky='NSEW')

    def _browse(self):
    
        dialog = fd.askopenfilenames
        filepaths = dialog(title=self._dialog_title)
        if filepaths:
            self._inputs = list(filepaths)
            self.field['state'] = 'normal'
            self.field.delete(0, 'end')
            for path in self._inputs:
                filepath = self._format_item(path, self._abbreviate)
                self.field.insert('end', filepath)

            self.field['state'] = 'disabled'
            self.field['justify'] = 'left'


class OutputEntry(InputEntry):

    def __init__(self, master, width=None, filetypes=None, abbreviate=False,
                 directory=False, default=None):

        self._directory = directory
        self._default = None

        if filetypes is None:
            filetypes = tuple()
        if default is None:
            default = tuple()

        super().__init__(master, width, filetypes, abbreviate)

        self._output = []

    def _browse(self):

        function = fd.askdirectory if self._directory else fd.asksaveasfilename
        kwargs = {'title': self._dialog_title}
        if not self._directory:
            kwargs['filetypes'] = self._filetypes
            kwargs['defaultextension'] = self._default
        
        output = function(**kwargs)
        if output:
            self._output = [output]
            output = self._format_item(output, self._abbreviate).strip()

            self.field['state'] = 'normal'
            self.field.delete(0, 'end')

            self.field.insert(0, output)

            self.field['state'] = 'readonly'
            self.field.update_idletasks()
            self.field.xview_moveto(1)

    def get(self):
        return self._output

    def clear(self):
        super().clear()
        self._output = []