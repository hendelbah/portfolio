import tkinter as tk
from tkinter import filedialog
import numpy as np
import imageio
from PIL import ImageTk, Image
from pathlib import Path
from wildfire.forest import Forest


class Application(tk.Frame):

    def __init__(self, master=None):
        super().__init__(master)
        self.master = master
        self.spawn_forest_prob = 0.7
        self.flame_powers = [0, 30, 60, 30, 0]
        self.time = 100
        self.terrain_size = [100, 100]
        self.scale = 2
        self.wind_course = 90
        self.wind_power = 0
        self.input_img_path = Path()
        self.output_dir = Path()
        self.generated_gif_count = 0
        self.forest = None
        self.canvas = None
        self.can_image = None
        self.pack(side='left')
        self.create_widgets()

    # noinspection PyAttributeOutsideInit
    def create_widgets(self):
        self.prob_label = tk.Label(self)
        self.prob_label["text"] = 'Probability'
        self.prob_label.grid(row=0, column=0, sticky='W')

        self.prob_entry = tk.Entry(self)
        self.prob_entry.insert(tk.END, str(self.spawn_forest_prob))
        self.prob_entry.grid(row=0, column=1, columnspan=2, padx=3, pady=3)

        self.power_label = tk.Label(self)
        self.power_label["text"] = 'Fire power values '
        self.power_label.grid(row=1, column=0, sticky='W')

        self.power_entry = tk.Entry(self)
        self.power_entry.insert(tk.END, ' '.join(map(str, self.flame_powers)))
        self.power_entry.grid(row=1, column=1, columnspan=2, padx=3, pady=3)

        self.time_label = tk.Label(self)
        self.time_label["text"] = 'Number of ticks '
        self.time_label.grid(row=2, column=0, sticky='W')

        self.time_entry = tk.Entry(self)
        self.time_entry.insert(tk.END, str(self.time))
        self.time_entry.grid(row=2, column=1, columnspan=2, padx=3, pady=3)

        self.scale_label = tk.Label(self)
        self.scale_label["text"] = 'GIF scale '
        self.scale_label.grid(row=3, column=0, sticky='W')

        self.scale_entry = tk.Entry(self)
        self.scale_entry.insert(tk.END, str(self.scale))
        self.scale_entry.grid(row=3, column=1, columnspan=2, padx=3, pady=3)

        self.height_label = tk.Label(self)
        self.height_label["text"] = 'Grid height '
        self.height_label.grid(row=4, column=0, sticky='W')

        self.height_entry = tk.Entry(self)
        self.height_entry.insert(tk.END, str(self.terrain_size[0]))
        self.height_entry.grid(row=4, column=1, columnspan=2, padx=3, pady=3)

        self.width_label = tk.Label(self)
        self.width_label["text"] = 'Grid width '
        self.width_label.grid(row=5, column=0, sticky='W')

        self.width_entry = tk.Entry(self)
        self.width_entry.insert(tk.END, str(self.terrain_size[1]))
        self.width_entry.grid(row=5, column=1, columnspan=2, padx=3, pady=3)

        self.wind_course_label = tk.Label(self)
        self.wind_course_label["text"] = 'Wind course'
        self.wind_course_label.grid(row=6, column=0, sticky='W')

        self.wind_course_entry = tk.Entry(self)
        self.wind_course_entry.insert(tk.END, str(self.wind_course))
        self.wind_course_entry.grid(row=6, column=1, columnspan=2, padx=3, pady=3)

        self.wind_power_label = tk.Label(self)
        self.wind_power_label["text"] = 'Wind power'
        self.wind_power_label.grid(row=7, column=0, sticky='W')

        self.wind_power_entry = tk.Entry(self)
        self.wind_power_entry.insert(tk.END, str(self.wind_power))
        self.wind_power_entry.grid(row=7, column=1, columnspan=2, padx=3, pady=3)

        self.input_img_label = tk.Label(self)
        self.input_img_label["text"] = 'Input image'
        self.input_img_label.grid(row=8, column=0, sticky='W')

        self.input_img_entry = tk.Entry(self)
        self.input_img_entry.insert(tk.END, str(self.input_img_path))
        self.input_img_entry.grid(row=8, column=1, columnspan=2, padx=3, pady=3)

        self.input_img_button = tk.Button(self, text="Open...", command=self.input_img_btn_click)
        self.input_img_button.grid(row=8, column=3, sticky='W')

        self.output_dir_label = tk.Label(self)
        self.output_dir_label["text"] = 'Output directory'
        self.output_dir_label.grid(row=9, column=0, sticky='W')

        self.output_dir_entry = tk.Entry(self)
        self.output_dir_entry.insert(tk.END, str(self.output_dir))
        self.output_dir_entry.grid(row=9, column=1, columnspan=2, padx=3, pady=3)

        self.output_dir_button = tk.Button(self, text="Set...", command=self.output_dir_btn_click)
        self.output_dir_button.grid(row=9, column=3, sticky='W')

        self.generate_button = tk.Button(self)
        self.generate_button["text"] = "Select initial fire"
        self.generate_button["command"] = self.select_fire
        self.generate_button.grid(row=10, column=1, columnspan=1, padx=3, pady=3)

        self.quit = tk.Button(self, text="Quit", command=self.master.destroy)
        self.quit.grid(row=11, column=3, padx=4, pady=4, sticky='NSWE')

    def input_img_btn_click(self):
        self.input_img_entry.delete(0, tk.END)
        self.input_img_entry.insert(tk.END, tk.filedialog.askopenfilename())

    def output_dir_btn_click(self):
        self.output_dir_entry.delete(0, tk.END)
        self.output_dir_entry.insert(tk.END, tk.filedialog.askdirectory())

    def calculate_gif(self):
        picture_array = np.zeros((self.time, (self.forest.height - 2) * self.forest.picture_scale,
                                  (self.forest.width - 2) * self.forest.picture_scale, 3), dtype=np.uint8)
        picture_array[0] = self.forest.picture
        for frame in range(1, self.time):
            self.forest.evolve_to_next_frame(self.flame_powers, self.wind_course, self.wind_power)
            print(str(round(frame / self.time * 100, 2)) + '% of frames processed')
            picture_array[frame] = self.forest.picture
        return picture_array

    def simulate_wildfire(self, event):
        x = (event.x - 2) // self.forest.picture_scale
        y = (event.y - 2) // self.forest.picture_scale
        self.forest.add_fire(y, x)
        gif = self.calculate_gif()
        print("GIF generation complete. Saving...")
        imageio.mimsave(self.output_dir / f'wildfire{self.generated_gif_count}.gif', gif)
        self.generated_gif_count += 1
        print("GIF saved")
        event.widget.destroy()
        self.pack(side='left')

    def select_fire(self):
        entered_height = int(self.height_entry.get())
        entered_width = int(self.width_entry.get())
        self.terrain_size = [entered_height, entered_width]
        self.time = int(self.time_entry.get())
        self.flame_powers = list(map(int, self.power_entry.get().split()))
        self.spawn_forest_prob = float(self.prob_entry.get())
        self.scale = int(self.scale_entry.get())
        self.wind_course = int(self.wind_course_entry.get())
        self.wind_power = float(self.wind_power_entry.get())
        self.input_img_path = Path(self.input_img_entry.get())
        self.output_dir = Path(self.output_dir_entry.get())
        image_proceeded = False
        if self.input_img_path.is_file():
            try:
                self.forest = Forest.from_image(self.input_img_path, self.scale)
                image_proceeded = True
            except Exception as e:
                print(e)
        else:
            print('No valid image file selected. Using random values instead')
        if not image_proceeded:
            self.forest = Forest.random(self.terrain_size, self.spawn_forest_prob, self.scale)
        self.can_image = ImageTk.PhotoImage(Image.fromarray(self.forest.picture, mode='RGB'))
        self.canvas = tk.Canvas(self.master, width=self.can_image.width(), height=self.can_image.height())
        self.canvas.create_image(0, 0, anchor=tk.NW, image=self.can_image)
        self.canvas.pack(side='left')
        self.canvas.bind("<Button-1>", self.simulate_wildfire)
