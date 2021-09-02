import tkinter as tk
import numpy as np
import imageio
import random
from tkinter import filedialog
from PIL import ImageTk, Image

direction_shifts = {0: [-1, 0],  # north
                    1: [-1, 1],  # north-east
                    2: [0, 1],  # east
                    3: [1, 1],  # south-east
                    4: [1, 0],  # south
                    5: [1, -1],  # south-west
                    6: [0, -1],  # west
                    7: [-1, -1]}  # north-west

DIRT_ID = 0
TREE_ID = 1
FLAME0_ID = 2
FLAME1_ID = 3
FLAME2_ID = 4
FLAME3_ID = 5
FLAME4_ID = 6

pallet = {DIRT_ID: [190, 175, 135],
          TREE_ID: [120, 190, 0],
          FLAME0_ID: [225, 190, 0],
          FLAME1_ID: [240, 160, 0],
          FLAME2_ID: [255, 175, 0],
          FLAME3_ID: [225, 145, 0],
          FLAME4_ID: [195, 130, 0]}


###################################################################################################################


class Forest:
    def __init__(self, initial_state, scale=1):
        self.state_array = initial_state
        self.height = initial_state.shape[0]
        self.width = initial_state.shape[1]
        self._flames = []
        self.picture_scale = scale if scale > 0 else 1
        # 1 pixel around the edges of Forest.state is cut on the Forest.picture (what height - 2 stays for)
        self.picture = np.zeros(((self.height - 2) * self.picture_scale,
                                 (self.width - 2) * self.picture_scale, 3), dtype=np.uint8)
        if self.picture_scale > 1:
            for picture_y in range(self.picture.shape[0]):
                for picture_x in range(self.picture.shape[1]):
                    state_array_y = picture_y // self.picture_scale + 1
                    state_array_x = picture_x // self.picture_scale + 1
                    self.picture[picture_y, picture_x] = pallet[self.state_array[state_array_y, state_array_x]]
        else:
            for x in range(self.height - 2):
                for y in range(self.width - 2):
                    self.picture[x, y] = pallet[self.state_array[x + 1, y + 1]]

    def add_fire(self, flame=None):
        """

        :param flame:
        :return:
        """
        flame = [] if flame is None else flame
        new_flame = []

        if 2 <= len(flame) < 4:
            new_flame = [flame[0], flame[1], 2, list(range(8))]
        elif len(flame) == 4:
            new_flame = flame
        elif not flame:
            new_flame = [self.state_array.shape[0] // 2,
                         self.state_array.shape[1] // 2, 2, list(range(8))]
        if 1 < new_flame[2] < 7:
            self._flames.append(new_flame)
        self.state_array[new_flame[0], new_flame[1]] = new_flame[2]
        self.changeFrame(new_flame[0], new_flame[1], new_flame[2])

    def changeFrame(self, x, y, value):
        if self.picture_scale > 1:
            X = (x - 1) * self.picture_scale
            Y = (y - 1) * self.picture_scale
            color = pallet[value]
            for x1 in range(self.picture_scale):
                for y1 in range(self.picture_scale):
                    self.picture[X + x1, Y + y1] = color
        else:
            self.picture[x - 1, y - 1] = pallet[value]

    def calculateNextState(self, flamePowers, windCourse, windPower):
        def odd(o):
            if o in [1, 3, 5, 7]:
                return 1
            else:
                return 0

        def revO(o):
            if o < 4:
                o += 4
            else:
                o -= 4
            return (o)

        prevFlames = self._flames
        self._flames = []
        for flame in prevFlames:
            nextFlameO = []
            if flame[2] < 6:
                power = flamePowers[flame[2] - 2]
                for o in flame[3]:
                    newP = [flame[0] + direction_shifts[o][0], flame[1] + direction_shifts[o][1]]
                    if 0 < newP[0] < self.height - 1 and 0 < newP[1] < self.width - 1:
                        if self.state_array[newP[0], newP[1]] == 1:
                            diagonalMultiplier = 1 - odd(o) * 0.65
                            if windPower > 0:
                                windAngle = abs(windCourse - o * 45)
                                if windAngle > 180:
                                    windAngle = 360 - windAngle
                                if windAngle >= 90:
                                    windMultiplier = (
                                                             1.4 - windAngle / 180) ** windPower
                                else:
                                    windMultiplier = (
                                                             1.9 - windAngle / 90) ** windPower
                            else:
                                windMultiplier = 1
                            if random.randint(1, 100) <= power * diagonalMultiplier * windMultiplier:
                                newFlame = list(range(8))
                                newFlame.pop(revO(o))
                                self.add_fire([newP[0], newP[1], 2, newFlame])
                            else:
                                nextFlameO.append(o)
                flame[2] += 1
            else:
                flame[2] = 0
            self.add_fire([flame[0], flame[1], flame[2], nextFlameO])


###################################################################################################################


class Application(tk.Frame):
    treshold = 140
    spawnForestProb = 0.7
    flamePowers = [0, 30, 60, 30]
    time = 100
    terrainSize = [100, 100]
    scale = 2
    windCourse = 90
    windPower = 0
    inputImgPath = ''
    outputDir = ''
    generatedGifCount = 0

    def __init__(self, master=None):
        super().__init__(master)
        self.master = master
        self.pack(side='left')
        self.create_widgets()

    def create_widgets(self):
        self.probLabel = tk.Label(self)
        self.probLabel["text"] = 'Probability'
        self.probLabel.grid(row=0, column=0, sticky='W')

        self.probEntry = tk.Entry(self)
        self.probEntry.insert(tk.END, str(self.spawnForestProb))
        self.probEntry.grid(row=0, column=1, columnspan=2, padx=3, pady=3)

        self.powerLabel = tk.Label(self)
        self.powerLabel["text"] = 'Fire power values '
        self.powerLabel.grid(row=1, column=0, sticky='W')

        self.powerEntry = tk.Entry(self)
        self.powerEntry.insert(tk.END, str(self.flamePowers).replace(
            '[', '').replace(',', '').replace(']', ''))
        self.powerEntry.grid(row=1, column=1, columnspan=2, padx=3, pady=3)

        self.timeLabel = tk.Label(self)
        self.timeLabel["text"] = 'Number of ticks '
        self.timeLabel.grid(row=2, column=0, sticky='W')

        self.timeEntry = tk.Entry(self)
        self.timeEntry.insert(tk.END, str(self.time))
        self.timeEntry.grid(row=2, column=1, columnspan=2, padx=3, pady=3)

        self.scaleLabel = tk.Label(self)
        self.scaleLabel["text"] = 'GIF scale '
        self.scaleLabel.grid(row=3, column=0, sticky='W')

        self.scaleEntry = tk.Entry(self)
        self.scaleEntry.insert(tk.END, str(self.scale))
        self.scaleEntry.grid(row=3, column=1, columnspan=2, padx=3, pady=3)

        self.heightLabel = tk.Label(self)
        self.heightLabel["text"] = 'Gif height '
        self.heightLabel.grid(row=4, column=0, sticky='W')

        self.heightEntry = tk.Entry(self)
        self.heightEntry.insert(tk.END, str(self.terrainSize[0]))
        self.heightEntry.grid(row=4, column=1, columnspan=2, padx=3, pady=3)

        self.widthLabel = tk.Label(self)
        self.widthLabel["text"] = 'Gif width '
        self.widthLabel.grid(row=5, column=0, sticky='W')

        self.widthEntry = tk.Entry(self)
        self.widthEntry.insert(tk.END, str(self.terrainSize[1]))
        self.widthEntry.grid(row=5, column=1, columnspan=2, padx=3, pady=3)

        self.windCourseLabel = tk.Label(self)
        self.windCourseLabel["text"] = 'Wind course'
        self.windCourseLabel.grid(row=6, column=0, sticky='W')

        self.windCourseEntry = tk.Entry(self)
        self.windCourseEntry.insert(tk.END, str(self.windCourse))
        self.windCourseEntry.grid(
            row=6, column=1, columnspan=2, padx=3, pady=3)

        self.windPowerLabel = tk.Label(self)
        self.windPowerLabel["text"] = 'Wind power m/s'
        self.windPowerLabel.grid(row=7, column=0, sticky='W')

        self.windPowerEntry = tk.Entry(self)
        self.windPowerEntry.insert(tk.END, str(self.windPower))
        self.windPowerEntry.grid(row=7, column=1, columnspan=2, padx=3, pady=3)

        self.inputImgLabel = tk.Label(self)
        self.inputImgLabel["text"] = 'Input image'
        self.inputImgLabel.grid(row=8, column=0, sticky='W')

        self.inputImgEntry = tk.Entry(self)
        self.inputImgEntry.insert(tk.END, str(self.inputImgPath))
        self.inputImgEntry.grid(row=8, column=1, columnspan=2, padx=3, pady=3)

        self.inputImgButton = tk.Button(
            self, text="Open...", command=self.inputImgBtnClick)
        self.inputImgButton.grid(row=8, column=3, sticky='W')

        self.outputDirLabel = tk.Label(self)
        self.outputDirLabel["text"] = 'Output Directory'
        self.outputDirLabel.grid(row=9, column=0, sticky='W')

        self.outputDirEntry = tk.Entry(self)
        self.outputDirEntry.insert(tk.END, str(self.outputDir))
        self.outputDirEntry.grid(row=9, column=1, columnspan=2, padx=3, pady=3)

        self.outputDirButton = tk.Button(
            self, text="Set...", command=self.outputDirBtnClick)
        self.outputDirButton.grid(row=9, column=3, sticky='W')

        self.generateButton = tk.Button(self)
        self.generateButton["text"] = "Select fire"
        self.generateButton["command"] = self.selectFire
        self.generateButton.grid(
            row=10, column=1, columnspan=1, padx=3, pady=3)

        self.quit = tk.Button(self, text="Quit", command=self.master.destroy)
        self.quit.grid(row=11, column=3, padx=4, pady=4, sticky='NSWE')

        # self.coefEntry = tk.Entry(self)
        # self.coefEntry.insert(tk.END,str(self.treshold))
        # self.coefEntry.grid(row=12,column=1,columnspan=2,padx=3,pady=3)

    def inputImgBtnClick(self):
        self.inputImgEntry.delete(0, tk.END)
        self.inputImgEntry.insert(tk.END, filedialog.askopenfilename())

    def outputDirBtnClick(self):
        self.outputDirEntry.delete(0, tk.END)
        self.outputDirEntry.insert(tk.END, filedialog.askdirectory())

    def createRandomState(self):
        randomState = np.random.choice([0, 1], size=self.terrainSize, p=[
            1 - self.spawnForestProb, self.spawnForestProb])
        # randomForestState = ForestState(randomState, scale)
        return randomState

    def createImageState(self, imagepath):
        pic = imageio.imread(imagepath)
        # 2 is not blue
        # 1 is not green
        # 0 is not red
        notred = pic[:, :, 0]
        notgreen = pic[:, :, 1]
        notblue = pic[:, :, 2]
        # here happens black magic process of deciding which pixels
        # represent forest and which don't
        GREEN = (notred + notblue - notgreen) / 2
        RED = (notblue + notgreen - notred) / 2
        BLUE = (notgreen + notred - notblue) / 2
        # the greener and the bluer pixel is, the 'foresty' it is.
        pic = np.clip((GREEN * 5 + RED - BLUE), 0, 256)
        imageState = pic
        for x in range(imageState.shape[0]):
            for y in range(imageState.shape[1]):
                if imageState[x, y] < self.treshold:
                    imageState[x, y] = 1
                else:
                    imageState[x, y] = 0
        imageio.imsave('./usedcolormask.png', pic)
        return imageState

    def calculateGif(self, fs):
        colored = [[[[]]]]
        colored = np.zeros((self.time, (fs.height - 2) * fs.picture_scale,
                            (fs.width - 2) * fs.picture_scale, 3), dtype=np.uint8)
        colored[0] = fs.picture
        for t in range(1, self.time):
            fs.calculateNextState(
                self.flamePowers, self.windCourse, self.windPower)
            print(str(round(t / self.time * 100, 2)) + '% of ticks processed')
            colored[t] = fs.picture
        print("GIF generation complete. Saving...")
        return colored

    def generateGIF(self, event):
        x = (event.x - 2) // self.forestState.picture_scale
        y = (event.y - 2) // self.forestState.picture_scale
        self.forestState.add_fire([y, x])
        colored = self.calculateGif(self.forestState)
        imageio.mimsave(
            self.outputDir + '/wildfire{0}.gif'.format(self.generatedGifCount), colored)
        self.generatedGifCount += 1
        print("GIF saved")
        event.widget.delete('all')
        self.canvas.configure(width=0)
        self.pack(side='left')

    def selectFire(self):
        enteredHeight = int(self.heightEntry.get())
        enteredWidth = int(self.widthEntry.get())
        self.terrainSize = [enteredHeight, enteredWidth]
        self.time = int(self.timeEntry.get())
        # self.treshold = int(self.coefEntry.get())
        self.flamePowers = list(map(int, self.powerEntry.get().split()))
        self.spawnForestProb = float(self.probEntry.get())
        self.scale = int(self.scaleEntry.get())
        self.windCourse = int(self.windCourseEntry.get())
        self.windPower = float(self.windPowerEntry.get())
        self.inputImgPath = self.inputImgEntry.get()
        self.outputDir = self.outputDirEntry.get()
        if self.outputDir == '':
            self.outputDir = '.'
        self.state = self.createRandomState()
        if self.inputImgPath == '':
            print('No image selected. Using random values instead')
        else:
            try:
                self.state = self.createImageState(self.inputImgPath)
                self.enteredScale = 1
            except Exception as e:
                print(e)
        self.forestState = Forest(self.state, self.scale)
        self.img = ImageTk.PhotoImage(
            Image.fromarray(self.forestState.picture, mode='RGB'))
        try:
            self.canvas.destroy()
        except Exception as e:
            print(e)
        self.canvas = tk.Canvas(
            root, width=self.img.width(), height=self.img.height())
        self.canvas.pack(side='left')
        self.can_img = self.canvas.create_image(
            0, 0, anchor=tk.NW, image=self.img)
        self.canvas.bind("<Button-1>", self.generateGIF)


root = tk.Tk()
root.title('Cellular automatons: Wildfire')
app = Application(master=root)

app.mainloop()
