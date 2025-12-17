import tkinter as tk

root = tk.Tk()
root.title("Simple Paint App")

canvas = tk.Canvas(root, bg="blue", width=900, height=700)
canvas.pack()

#Store prev mouse position
x_prev, y_prev = None, None

#Mouse press function
def on_mouse_click(event):
    global x_prev, y_prev
    x_prev = event.x
    y_prev = event.y

#Mouse drag function
def on_mouse_drag(event):
    global x_prev, y_prev
    canvas.create_line(x_prev, y_prev, event.x, event.y, width=2) #draw line

    x_prev, y_prev  = event.x, event.y  #update prev position

#Fix Mouse Movements
canvas.bind("<Button-1>", on_mouse_click)
canvas.bind("<B1-Motion>", on_mouse_drag)

#Start App
root.mainloop()


