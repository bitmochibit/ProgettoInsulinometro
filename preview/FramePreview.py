import tkinter as tk

class MainApplication(tk.Frame):
    def __init__(self, parent, *args, **kwargs):
        tk.Frame.__init__(self, parent, *args, **kwargs)
        self.parent = parent
        setupTitleBar(self)


        mainFrame = tk.Frame(self, bg="#F1F2F7",)
        bottomFrame = tk.Frame(self, bg="#F9F8FD")

        mainFrame.pack(side="top", fill="both", expand=True)
        bottomFrame.pack(side="bottom", fill="both", expand=True)

def setupTitleBar(self):
    root.overrideredirect(True)  # turns off title bar, geometry
    root.geometry('800x600+200+200')  # set new geometry

    titleBar = tk.Frame(self, bg="#F1F2F7", relief="raised", bd=0)
    titleBar.pack(side="top", fill="x", expand=False)

    closeButton = tk.Button(titleBar, text="X", command=self.destroy)
    closeButton.pack(side="right")




if __name__ == "__main__":
    root = tk.Tk()
    root.geometry("800x600")
    MainApplication(root).pack(side="top", fill="both", expand=True)
    root.mainloop()