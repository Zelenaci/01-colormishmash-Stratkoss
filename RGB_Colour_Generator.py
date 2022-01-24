from os.path import basename, splitext
from tkinter import Scale,StringVar,Frame,Entry,Canvas,HORIZONTAL,END,LEFT,S
import tkinter as tk



class Application(tk.Tk):
    name = basename(splitext(basename(__file__))[0])
    name = "RGB Colour Generator"

    def __init__(self):
        super().__init__(className=self.name)
        self.title(self.name)
        self.bind("<Escape>", self.quit)


        self.RED_F = Frame(self)
        self.RED_F.pack()
        self.GREEN_F = Frame(self)
        self.GREEN_F.pack()
        self.BLUE_F = Frame(self)
        self.BLUE_F.pack()
      


        self.varR = StringVar()
        self.labelR = tk.Label(self.RED_F, text="R")
        self.labelR.pack(side=LEFT, anchor=S)
        self.scaleR = Scale(self.RED_F, from_=0, to=255, orient=HORIZONTAL, length= 256, variable=self.varR)
        self.scaleR.pack(side=LEFT, anchor=S)
        self.entryR = Entry(self.RED_F, width=8, textvariable=self.varR)
        self.entryR.pack(side=LEFT, anchor=S)



        self.varG = StringVar()
        self.labelG = tk.Label(self.GREEN_F, text="G")
        self.labelG.pack(side=LEFT)
        self.scaleG = Scale(self.GREEN_F, from_=0, to=255, orient = HORIZONTAL, length= 256, variable=self.varG)
        self.scaleG.pack(side=LEFT)
        self.entryG = Entry(self.GREEN_F, width=8, textvariable=self.varG)
        self.entryG.pack(side=LEFT, anchor=S)



        self.varB = StringVar()
        self.labelB = tk.Label(self.BLUE_F, text="B")
        self.labelB.pack(side=LEFT)
        self.scaleB = Scale(self.BLUE_F, from_=0, to=255, orient = HORIZONTAL, length= 256, variable=self.varB)
        self.scaleB.pack(side=LEFT)
        self.entryB = Entry(self.BLUE_F, width=8, textvariable=self.varB)
        self.entryB.pack(side=LEFT, anchor=S)




        self.varR.trace("w", self.change)
        self.varB.trace("w", self.change)
        self.varG.trace("w", self.change)



        self.canvasMain = Canvas(self, width=365, height=200, background= "#000000")
        self.canvasMain.pack()
        self.canvasMain.bind("<Button-1>", self.clickHandler)
        self.entryMain = Entry(self, text="#000000")
        self.entryMain.pack()

        self.buttonExit = tk.Button(self, text="SAVE AND QUIT", command=self.quit)
        self.buttonExit.pack()

        


        self.frameMem = Frame(self)
        self.frameMem.pack()
        self.canvasMem = []
        for row in range(3):
            for column in range(7):
                canvas = Canvas(self.frameMem, width=50, height=50, background="#ffffff")
                canvas.bind("<Button-1>", self.clickHandler)
                canvas.grid(row=row,column=column)
                self.canvasMem.append(canvas)

        
        self.load()

    def set_scales(self):
        color = self.canvasMain.cget("background")
        r=int(color[1:3],16)
        g=int(color[3:5],16)
        b=int(color[5:],16)
        self.varR.set(r)
        self.varG.set(g)
        self.varB.set(b)

    def load(self):
        try:
            with open("paleta.txt", "r") as f:
                colorMain = f.readline().strip()
                self.canvasMain.config(background=colorMain)
                self.set_scales()
                for canvas in self.canvasMem:
                    colorMem = f.readline().strip()
                    canvas.config(background=colorMem)
        except FileNotFoundError:
            print("Chyba při načítání souboru.")

    def change(self, var=None, index=None, mode=None):
        r = self.scaleR.get()
        g = self.scaleG.get()
        b = self.scaleB.get()
        colorcode = f"#{r:02x}{g:02x}{b:02x}"
        self.canvasMain.config(background=colorcode)
        self.entryMain.delete(0, END)
        self.entryMain.insert(0, colorcode)

    def clickHandler(self, event):
        if self.cget("cursor") != "pencil":
            self.config(cursor="pencil")
            self.color = event.widget.cget("background")
        else:
            self.config(cursor="")
            event.widget.config(background=self.color)

    def save(self):
        with open("paleta.txt", "w") as f:
            f.write(self.canvasMain.cget("background")+"\n")
            for canvas in self.canvasMem:
                f.write(canvas.cget("background")+"\n")

    def quit(self, event=None):
        self.save()
        super().quit()

app = Application()
app.mainloop()
