import tkinter as tk

class View():
    r = tk.Tk()
    r.geometry("1024x768+30+30")
    button = tk.Button(r, text='Stop', width=25, command=r.destroy)

    def __init__(self):
        self.r.title('Counting Seconds')
        self.button.pack()

        l = tk.Label(self.r,
                     text="test",
                     fg='Black')
        l.place(x=20, y=30 + 2 * 30, width=500, height=25)

        listbox = tk.Listbox(self.r)

        listbox.place(x = 0, y = 0, width = 500, height=500)

        listbox.insert(tk.END, "a list entry")

        for item in ["one", "two", "three", "four"]:
            listbox.insert(tk.END, item)


    def run(self):
        self.r.mainloop()







