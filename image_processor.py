import numpy as np
from PIL import Image

class ImageProcessor:

    def __init__(self, image):
        self.image = image
        self.imageArray = np.asarray(self.image)
        self.width = self.imageArray.shape[0]
        self.height = self.imageArray.shape[1]
        self.channels = self.imageArray.shape[2]

    def greyScale(self):
        for i in range(self.width):
            for j in range(self.height):
                average = 0
                for k in range(self.channels):
                    average += self.imageArray[i][j][k]
                average /= self.channels
                for k in range(self.channels):
                    self.imageArray[i][j][k] = average

    def twoTone(self, percent):
        limit = int((percent * 255) / 100)
        for i in range(self.width):
            for j in range(self.height):
                average = 0
                for k in range(self.channels):
                    average += self.imageArray[i][j][k]
                average /= self.channels
                for k in range(self.channels):
                    if average < limit:
                        average = 0
                    else:
                        average = 255
                    self.imageArray[i][j][k] = average

    def changeBrightness(self, percent):  # dont use this it does not work
        change = int((percent * 255) / 100)
        for i in range(self.width):
            for j in range(self.height):
                for k in range(self.channels):
                    self.imageArray[i][j][k] += change

    def setSize(self, width, height, channels = 3):
        newArray = np.ndarray((width, height, channels), dtype=np.uint8)
        for i in range(width):
            for j in range(height):
                for k in range(channels):
                    newArray[i][j][k] = self.imageArray[int((i / width) * self.width)][int((j / height) * self.height)][k]
        self.__setNewArray(newArray)

    def fitInside(self, width, height, channels = 3):
        if self.width > self.height:
            ratio = width / self.width
            self.setSize(width, int(self.height * ratio), channels)
        else:
            ratio = height / self.height
            self.setSize(int(self.width * ratio), height, channels)

    def makeIllusion(self, cell_size, density):
        self.greyScale()
        cell_width = cell_height = cell_size
        for cell_x in range(0, self.width, cell_width):
            for cell_y in range(0, self.height, cell_height):
                average = 0
                for pixX in range(cell_width):
                    for pixY in range(cell_height):
                        try:
                            average += self.imageArray[cell_x + pixX][cell_y + pixY][0]
                        except IndexError:
                            pass
                average /= cell_width * cell_height * 255
                centerX = cell_x + cell_width/2
                centerY = cell_y + cell_height/2

                for pixX in range(cell_width):
                    for pixY in range(cell_height):
                        if ((centerX - (cell_x + pixX))**2) + ((centerY - (cell_y + pixY))**2) < (cell_width * average * density)**2:
                            color = [255, 255, 255]
                        else:
                            color = [0, 0, 0]

                        try:
                            self.imageArray[cell_x + pixX][cell_y + pixY] = color
                        except IndexError:
                            pass

    def __setNewArray(self, newArray):
        shape = newArray.shape
        self.imageArray = newArray
        self.width = shape[0]
        self.height = shape[1]
        self.channels = shape[2]

    def reset(self):
        self.imageArray = np.asarray(self.image)
        self.__setNewArray(self.imageArray)

    def getArray(self):
        return self.imageArray

    def export(self):
        return Image.fromarray(self.imageArray)
    
    def getImage(self):
        return Image.fromarray(self.imageArray)

    def saveImage(self, filename):
        saveImage = Image.fromarray(self.imageArray)
        saveImage.save(filename)

if __name__ == '__main__':
    filename = "images/christmas-tree.jpg"
    image = Image.open(filename)
    processor = ImageProcessor(image)
    processor.makeIllusion(17, 0.45)
    processor.saveImage("outImage.png")