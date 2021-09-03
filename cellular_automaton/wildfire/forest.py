import numpy as np
import random
import imageio

DIRT_ID = 0
TREE_ID = 1
INITIAL_FLAME_ID = 2
FLAME1_ID = 3
FLAME2_ID = 4
FLAME3_ID = 5
FINAL_FLAME_ID = 6

pallet = {DIRT_ID: [190, 175, 135],
          TREE_ID: [120, 190, 0],
          INITIAL_FLAME_ID: [225, 190, 0],
          FLAME1_ID: [240, 160, 0],
          FLAME2_ID: [255, 175, 0],
          FLAME3_ID: [225, 145, 0],
          FINAL_FLAME_ID: [195, 130, 0]}

direction_shifts = {0: [-1, 0],  # north
                    1: [-1, 1],  # north-east
                    2: [0, 1],  # east
                    3: [1, 1],  # south-east
                    4: [1, 0],  # south
                    5: [1, -1],  # south-west
                    6: [0, -1],  # west
                    7: [-1, -1]}  # north-west


class Flame:
    """
    A class used to store i `burning` cell data for the algorithm

    Attributes
    ----------
    x: int
        x coordinate on the grid
    y: int
        x coordinate on the grid
    sub_state: int
        a substate of `burning` cell
    dirs: list of int
        list of possible directions to look for `tree` cell
        to spread the fire
    """

    def __init__(self, y: int, x: int, sub_state: int = INITIAL_FLAME_ID, dirs: list[int] = None):
        if dirs is None:
            dirs = list(range(8))
        self.x = x
        self.y = y
        self.sub_state = sub_state
        self.dirs = dirs

    def evolve(self, dirs: list[int] = None):
        """
        Proceed flame to the next substage or if it is last - turn into `dirt`\n
        :param dirs: set dirs attribute to certain value
        """
        if self.sub_state >= FINAL_FLAME_ID:
            self.sub_state = DIRT_ID
            self.dirs = []
        else:
            if dirs is not None:
                self.dirs = dirs
            self.sub_state += 1


class Forest:
    """
    A class used to maintain forest grid

    Attributes
    ----------
    grid: np.Array
        A grid that represents forest condition, it stores ids of each cell state
    height: int
        Height on the grid
    width: int
        Width on the grid
    picture_scale: int
        Picture scale relative to grid
    picture: np.Array
        Scaled picture, it stores rgb array of cell colors
    """

    def __init__(self, initial_state, scale):
        self.grid = initial_state
        self.height = initial_state.shape[0]
        self.width = initial_state.shape[1]
        self._flames = []
        self.picture_scale = scale if scale > 0 else 1
        # 1 pixel around the edges of Forest.condition is cut on the Forest.picture (what height - 2 stays for)
        # this is scaled self.condition array with rgb arrays in cells
        self.picture = np.zeros(((self.height - 2) * self.picture_scale,
                                 (self.width - 2) * self.picture_scale, 3), dtype=np.uint8)
        self._translate_grid_to_picture()

    def _translate_grid_to_picture(self):
        for grid_y in range(1, self.grid.shape[0] - 1):
            for grid_x in range(1, self.grid.shape[1] - 1):
                self._translate_cell_to_picture(grid_y, grid_x)

    def _translate_cell_to_picture(self, condition_y: int, condition_x: int):
        color = pallet[self.grid[condition_y, condition_x]]
        if self.picture_scale > 1:
            picture_cell_x = (condition_x - 1) * self.picture_scale
            picture_cell_y = (condition_y - 1) * self.picture_scale
            for cell_x in range(self.picture_scale):
                for cell_y in range(self.picture_scale):
                    self.picture[picture_cell_y + cell_y, picture_cell_x + cell_x] = color
        else:
            self.picture[condition_x - 1, condition_y - 1] = color

    @classmethod
    def random(cls, size: list[int, int], tree_probability: float, scale=1):
        """
        Create instance with randomly generated initial grid\n
        :param size: grid size
        :param tree_probability: probability of tree spawn
        :param scale: picture scale relative to grid
        :return: Forest instance
        """
        random_state = np.random.choice([0, 1], size=size, p=[1 - tree_probability, tree_probability])
        return cls(random_state, scale)

    @classmethod
    def from_image(cls, image_path, scale=1):
        """
        Create instance using some image as pattern\n
        :param image_path:
        :param scale: picture scale relative to grid
        :return: Forest instance
        """
        threshold = 140  # a threshold for considering pixel as a "river"
        pic = imageio.imread(image_path)
        # 2 is not blue
        # 1 is not green
        # 0 is not red
        not_red = pic[:, :, 0]
        not_green = pic[:, :, 1]
        not_blue = pic[:, :, 2]
        # here happens black magic process of deciding which pixels
        # represent forest and which don't
        green = (not_red + not_blue - not_green) / 2
        red = (not_blue + not_green - not_red) / 2
        blue = (not_green + not_red - not_blue) / 2
        # the greener and the bluer pixel is, the 'foresty' it is.
        image_state = np.clip((green * 5 + red - blue), 0, 256)
        for x in range(image_state.shape[0]):
            for y in range(image_state.shape[1]):
                if image_state[x, y] < threshold:
                    image_state[x, y] = 1
                else:
                    image_state[x, y] = 0
        imageio.imsave('usedcolormask.png', pic)
        return cls(image_state, scale)

    def add_fire(self, flame: Flame or int = None, x: int = None):
        """
        Add new `burning` cell to grid\n
        :param Flame|int flame: Flame instance as source or just y coordinate to ignite
        :param int|None x: x coordinate to ignite bu only if flame is int
        """
        if flame is None:
            flame = Flame(self.grid.shape[1] // 2, self.grid.shape[0] // 2)
        elif isinstance(flame, int):
            flame = Flame(flame, x)
        if 1 < flame.sub_state < 7:
            self._flames.append(flame)
        self.grid[flame.y, flame.x] = flame.sub_state
        self._translate_cell_to_picture(flame.y, flame.x)

    @staticmethod
    def _reverse_direction(dir_arg: int):
        if dir_arg < 4:
            dir_arg += 4
        else:
            dir_arg -= 4
        return dir_arg

    def evolve_to_next_frame(self, flame_powers, wind_course, wind_power):
        """
        Proceed all `burning` cells to change frame\n
        :param flame_powers: chances of tree ignition for each burning cell
        :param wind_course: the direction of the wind
        :param wind_power: the speed of the wind
        """
        prev_flames = self._flames
        self._flames = []
        for flame in prev_flames:
            flame_next_dirs = []
            power = flame_powers[flame.sub_state - 2]
            for direction in flame.dirs:
                shift = direction_shifts[direction]
                new_flame = Flame(flame.y + shift[0], flame.x + shift[1])
                if 0 < new_flame.y < self.height - 1 and 0 < new_flame.x < self.width - 1:
                    if self.grid[new_flame.y, new_flame.x] == TREE_ID:
                        diagonal_multiplier = 1 - (direction % 2) * 0.65
                        if wind_power > 0:
                            wind_angle = abs(wind_course - direction * 45)
                            if wind_angle > 180:
                                wind_angle = 360 - wind_angle
                            if wind_angle >= 90:
                                wind_multiplier = (1.4 - wind_angle / 180) ** wind_power
                            else:
                                wind_multiplier = (1.9 - wind_angle / 90) ** wind_power
                        else:
                            wind_multiplier = 1
                        if random.randint(1, 100) <= power * diagonal_multiplier * wind_multiplier:
                            new_flame.dirs.pop(self._reverse_direction(direction))
                            self.add_fire(new_flame)
                        else:
                            flame_next_dirs.append(direction)
            flame.evolve(flame_next_dirs)
            self.add_fire(flame)
