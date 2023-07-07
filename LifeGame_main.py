"""

    Life game program

"""
# import module
import sys
import pygame as pg
from PGM.Entities import *
import numpy as np


class Application:
    """
        LifeGame application class
    """
    version = "1.1.0"
    master_size = np.array((900, 600))

    def __init__(self):
        """
            application boot and shut down process
        """
        done = False
        while not done:

            # starting process
            #  setup app variables

            #  setup pygame
            pg.init()
            pg.display.set_caption(f"LifeGame ver.{self.version}")
            master = pg.display.set_mode(self.master_size)

            # execution main
            reboot_bool = self.main(master)

            # ending process
            pg.quit()

            # reboot process
            if reboot_bool is True:
                continue
            break

        return

    class Cell:
        """
            class about LifeGame's one cell.
        """
        def __init__(self, index: tuple[int, int],
                     cell_size: int = 9,
                     cell_life_color: tuple[int, int, int] = (0, 255, 0),
                     cell_death_color: tuple[int, int, int] = (0, 0, 0)):
            """
                setup cell process.
            :param cell_size: cell's width and height
            :param cell_life_color: life cells color
            :param cell_death_color: death cells color
            """
            super().__init__()

            # variables
            self.__index = index
            self.__size: list[int, int] = [cell_size for i in range(2)]
            self.__color: dict[str: list[int, int, int], str: list[int, int, int]] = \
                dict(zip(
                    ["life", "death"],
                    [list(color) for color in [cell_life_color, cell_death_color]]
                ))
            self.__state = False
            self.__pre_state = False

            # surface
            self.__surfaces = dict()
            for key in self.__color.keys():
                surface = pg.Surface(self.__size)
                pg.draw.rect(surface, self.__color[key], (0, 0, *self.__size))
                self.__surfaces[key] = surface
            self.__surface = self.__surfaces["death"]
            self.__rect = self.__surface.get_rect()
            self.__rect[:-2] = np.array(self.__index) * (np.array(self.__size) + 1)

            return

        def check_state(self, cells, progression) -> None:
            if progression:
                cell_count = 0
                for cell in cells:
                    if cell.get_pre_state():
                        cell_count += 1

                if cell_count <= 1:
                    self.__state = False
                elif cell_count == 3:
                    self.__state = True
                elif cell_count >= 4:
                    self.__state = False
            return

        def update(self):
            if self.__state:
                state = "life"
            else:
                state = "death"
            self.__surface = self.__surfaces[state]
            self.__pre_state = self.__state
            return

        def draw(self, master: pg.Surface, diff: list | tuple = (0, 0)) -> None:
            rect = np.array(self.__rect)
            rect[:-2] = rect[:-2] + np.array(diff)
            master.blit(self.__surface, rect)
            return

        def left_click(self) -> None:
            self.__state = True
            return

        def right_click(self) -> None:
            self.__state = False
            return

        def get_pre_state(self):
            return self.__pre_state

    class Cells(Entities):
        """
            Cells manage class
        """
        def __init__(self, mode: type):
            """
                setup process
            :param mode: management data type
            """
            super().__init__(mode)
            self.motion_bool = False
            self.click = 0
            return

        def Click(self, mouse_pos, cell_size, click, motion_bool=True) -> None:
            """
                execution left click process
            :param mouse_pos: mouse's x,y
            :param cell_size: cell size
            :param click: button click
            :param motion_bool: motion
            :return: None
            """
            self.motion_bool = motion_bool
            self.click = click
            index = tuple(np.array(mouse_pos) // (cell_size+1))
            try:
                if click == 1:
                    super().get_Entity(index).left_click()
                    return
                if click == 3:
                    super().get_Entity(index).right_click()
            except KeyError:
                pass
            return

        def all_update_(self, mouse_pos, cell_size, cells_shape, progression, frame_count, frame_rate) -> None:
            if frame_count % frame_rate == 0:
                self.all_check_state(cells_shape, progression)
            index = tuple(np.array(mouse_pos) // (cell_size + 1))
            get_E = super().get_Entity
            try:
                if self.motion_bool:
                    if self.click == 1:
                        get_E(index).left_click()
                    elif self.click == 3:
                        get_E(index).right_click()
                super().all_update()
            except KeyError:
                return
            return

        def all_check_state(self, cells_shape, progression):
            def check_cells(_GE, _x, _y) -> list:
                cells = list()
                for diff_y in range(_y - 1, _y + 2):
                    for diff_x in range(_x - 1, _x + 2):
                        if (diff_x, diff_y) != (_x, _y):
                            try:
                                cells.append(_GE(tuple([diff_x, diff_y])))
                            except KeyError:
                                pass
                return cells

            GE = super().get_Entity
            for y in range(cells_shape[1]):
                for x in range(cells_shape[0]):
                    GE(tuple([x, y])).check_state(check_cells(GE, x, y), progression)
            return

    def main(self, master: pg.Surface) -> bool | None:
        """
            main application process.
        :param master: main screen surface object
        :return: reboot bool and None
        """
        # setup variables
        frame_count = 0
        clock = pg.time.Clock()
        frame_rate = 16
        progression = False

        cell_size = 9
        num_x, num_y = self.master_size // cell_size

        # setup cells
        cells = self.Cells(dict)
        [[cells.add_Entity(self.Cell((x, y), cell_size=cell_size), (x, y))
          for x in range(num_x)]
         for y in range(num_y)]

        # main loop
        done = False
        while not done:
            # event check process
            key_pressed_list = pg.key.get_pressed()
            mouse_pos = pg.mouse.get_pos()
            for event in pg.event.get():
                # quit click
                if event.type == pg.QUIT:
                    return

                # key down process
                if event.type == pg.KEYDOWN:
                    # reboot application
                    if event.key == pg.K_DELETE:
                        return True

                    # game progression
                    if event.key == pg.K_SPACE:
                        if progression:
                            progression = False
                        else:
                            progression = True

                    # reset game
                    if event.key == pg.K_r:
                        cells = self.Cells(dict)
                        [[cells.add_Entity(self.Cell((x, y), cell_size=cell_size), (x, y))
                          for x in range(num_x)]
                         for y in range(num_y)]

                # key up process
                if event.type == pg.KEYUP:
                    pass

                # mouse down process
                if event.type == pg.MOUSEBUTTONDOWN:
                    if event.button == 1:
                        cells.Click(mouse_pos, cell_size, 1)
                    if event.button == 3:
                        cells.Click(mouse_pos, cell_size, 3)

                # mouse up process
                if event.type == pg.MOUSEBUTTONUP:
                    if event.button == 1:
                        cells.Click(mouse_pos, cell_size, 1, False)
                    if event.button == 3:
                        cells.Click(mouse_pos, cell_size, 3, False)

            # collision detection process

            # update process
            cells.all_update_(mouse_pos, cell_size, (num_x, num_y), progression, frame_count, frame_rate)

            # draw process
            master.fill((191, 191, 191), (0, 0, *self.master_size))
            cells.all_draw(master)

            pg.display.update()

            # count and tick process
            frame_count += 1
            clock.tick(64)

        return


if __name__ == '__main__':
    app = Application()
    sys.exit()
