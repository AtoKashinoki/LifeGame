"""

    Life game program

"""
# import module
import sys
import pygame as pg
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

    def main(self, master: pg.Surface) -> bool | None:
        """
            main application process.
        :param master: main screen surface object
        :return: reboot bool and None
        """
        # setup variables
        frame_count = 0
        clock = pg.time.Clock()

        # main loop
        done = False
        while not done:
            # event check process
            key_pressed_list = pg.key.get_pressed()
            for event in pg.event.get():
                # quit click
                if event.type == pg.QUIT:
                    return

                # key down process
                if event.type == pg.KEYDOWN:
                    # reboot application
                    if event.key == pg.K_DELETE:
                        return True

                # key up process
                if event.type == pg.KEYUP:
                    pass

            # collision detection process

            # update process

            pg.display.update()

            # count and tick process
            frame_count += 1
            clock.tick(20)

        return


if __name__ == '__main__':
    app = Application()
    sys.exit()
