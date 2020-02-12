import tkinter as tk

window = tk.Tk()
greeting = tk.Label(
    text="Hello, Tkinter",
    foreground="black",  # Set the text color to white
    background="yellow",  # Set the background color to black
    width=15,
    height=10
)
greeting.pack()

window.mainloop()
