from image_processor import ImageProcessor
import tkinter as tk
import tkinter.filedialog
from PIL import ImageTk, Image

class app:

    def __init__(self, window, canvasx, canvasy):
        self.window = window
        self.fileString = ''
        self.tkImage = None
        self.img = None
        self.width = canvasx
        self.height = canvasy
        self.cellSize = tk.StringVar(value = 20)
        self.density = tk.StringVar(value = 70)

        # declare widgets
        self.sizeLabel = tk.Label(text="cell size")
        self.densityLabel = tk.Label(text="density percent")
        self.openFileBtn = tk.Button(text="select file", command=self.chooseFile)
        self.renderBtn = tk.Button(text="render", command=self.render)
        self.imageCanvas = tk.Canvas(self.window, width=self.width, height=self.height, background="black")
        self.sizeIn = tk.Entry(textvariable=self.cellSize)
        self.densityIn = tk.Entry(textvariable=self.density)


        # pack widgets
        self.openFileBtn.grid(column = 0, row = 1)
        self.renderBtn.grid(column = 2, row = 1)
        self.sizeLabel.grid(column = 0, row = 3)
        self.sizeIn.grid(column = 2, row = 3)
        self.densityLabel.grid(column = 0, row = 4)
        self.densityIn.grid(column = 2, row = 4)
        self.window.mainloop()

    def chooseFile(self):
        self.fileString = tkinter.filedialog.askopenfilename()
        self.img = Image.open(self.fileString)
        processor = ImageProcessor(self.img)
        processor.fitInside(self.width, self.height)
        self.tkImage = ImageTk.PhotoImage(processor.getImage())
        print("resize: done")
        self.imageCanvas.grid(column=0, row=2, columnspan=3)
        self.imageCanvas.create_image(1, 1, anchor='nw', image=self.tkImage)

    def render(self):
        if self.fileString == '' or self.tkImage is None:
            return
        else:
            self.imageCanvas.delete('all')
            processor = ImageProcessor(self.img)
            processor.fitInside(self.width, self.height)
            processor.makeIllusion(int(self.cellSize.get()), float(self.density.get()) / 100)
            self.tkImage = ImageTk.PhotoImage(processor.getImage())
            self.imageCanvas.create_image(1, 1, anchor='nw', image=self.tkImage)
            processor.saveImage("output/outImage.png")

if __name__ == '__main__':
    root = tk.Tk()
    myApp = app(root, 700, 700)
