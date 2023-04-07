import os
import tkinter as tk

class FileExplorer(tk.Frame):
    
    def __init__(self, master, folder_path, *args, **kwargs):
        tk.Frame.__init__(self, master, *args, **kwargs)
        self.master = master
        self.folder_path = folder_path
        self.file_listbox = tk.Listbox(self, width=50)
        self.scrollbar = tk.Scrollbar(self, orient='vertical', command=self.file_listbox.yview)
        self.file_listbox.config(yscrollcommand=self.scrollbar.set)
        self.file_listbox.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        self.scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.populate_files()

    def populate_files(self):
        for file in os.listdir(self.folder_path):
            if os.path.splitext(file)[1] == ".mp3":
                self.file_listbox.insert(tk.END, file)