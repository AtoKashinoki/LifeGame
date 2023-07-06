"""
    pygame entity objects management module
"""
# import module
import pygame


class Entities:
    """
        class about entities objects management
    """
    modes: tuple[type, ...] = (list, dict)

    def __init__(self, manage_mode: type = list):
        """
            setup variables.
        :param manage_mode: entities variable type
        """
        if manage_mode not in self.modes:
            raise TypeError(f"Invalid mode name -> mode = {manage_mode}\n<Available mode: {self.modes}>")
        self.__entities = manage_mode()

    def add_Entity(self, entity, key: str | tuple = None) -> None:
        """
            add entity object in management datas.
        :param entity: surface object to add
        :param key: key of surface to add
        :return: None
        """
        entities_type = type(self.__entities)
        if entities_type is list:
            self.__entities.append(entity)
            return
        if entities_type is dict:
            self.__entities[key] = entity
            return

    def add_Entities(self, entities: tuple or list, keys: tuple or list[str or tuple, ...] = None) -> None:
        """
            add entities objects in management datas.
        :param entities: entities objects to add
        :param keys: key of surfaces to add
        :return: None
        """
        if keys is None:
            keys = [f"{i}" for i in range(len(entities))]
        for i, entities in enumerate(entities):
            self.add_Entity(entities, keys[i])
        return

    def get_Entity(self, key: int | str | tuple) -> any:
        """
            return entity object.
        :param key: key of entity to get
        :return: entity object
        """
        return self.__entities[key]

    def update(self, key: int | str | tuple, *arguments) -> None:
        """
            execution update function of entities.
        :param key: key of entity to update.
        :param arguments: update function arguments
        :return: None
        """
        self.get_Entity(key).update(*arguments)
        return

    def all_update(self, *arguments) -> None:
        """
            execution update function of all entities.
        :param arguments: update function arguments
        :return: None
        """
        entities_type = type(self.__entities)
        if entities_type is list:
            for i in range(len(self.__entities)):
                self.update(i, *arguments)
            return
        if entities_type is dict:
            for key in self.__entities:
                self.update(key, *arguments)
            return
        return

    def draw(self, surface: pygame.Surface, key: int | str | tuple, *arguments) -> None:
        """
            execution draw function of entities.
        :param surface: screen surface
        :param key: key of entity to draw.
        :param arguments: draw function arguments
        :return: None
        """
        self.get_Entity(key).draw(surface, *arguments)
        return

    def all_draw(self, surface: pygame.Surface, *arguments) -> None:
        """
            execution update function of all entities.
        :param surface: screen surface
        :param arguments: update function arguments
        :return: None
        """
        entities_type = type(self.__entities)
        if entities_type is list:
            for i in range(len(self.__entities)):
                self.draw(surface, i, *arguments)
            return
        if entities_type is dict:
            for key in self.__entities:
                self.draw(surface, key, *arguments)
            return
        return
