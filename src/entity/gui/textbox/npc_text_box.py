import textwrap

import pygame

from entity.entity import Entity


class NpcTextBox(Entity):
    def __init__(self, messages: list[str], rect: tuple[int, int, int, int],
                 font_size: int, delay: int):
        super().__init__(rect[0], rect[1], rect[2], rect[3])
        self.messages = messages
        self.message_index = 0
        self.characters_to_display = 0
        self.font_size = font_size
        self.delay = delay
        self.time = pygame.time.get_ticks()
        self.font = pygame.font.Font(None, 36)

    def update(self, state: "GameState"):
        # print("textbox update")
        controller = state.controller

        # show characters of text one at a time, not whole message.
        text = self.messages[self.message_index]
        if self.characters_to_display < len(text):
            self.characters_to_display += 1

        # handle button press to see next message
        if controller.isTPressed and \
                pygame.time.get_ticks() - self.time > self.delay and \
                self.message_index < len(self.messages) - 1:
            self.time = pygame.time.get_ticks()
            self.message_index += 1
            self.characters_to_display = 0

        # print("is finished? " + str(self.is_finished()))

    def draw(self, state: "GameState"):
        # print("Textbox draw")
        text = self.messages[self.message_index]
        text_to_display = text[:self.characters_to_display]
        wrapped_text = textwrap.wrap(text_to_display, 60)
        # print("text: " + text_to_display)
        # print("position: " + str(self.position.toTuple()))
        for i, line in enumerate(wrapped_text):
            text_surface = state.FONT.render(line, True, (255, 255, 255))
            state.DISPLAY.blit(text_surface,
                         (self.position.x, self.position.y + (i * 40)))

        # state.DISPLAY.blit(font.render(
        #     f"player money: {state.player.money}",
        #     True, (5, 5, 5)), (150, 150))

    def is_finished(self) -> bool:
        return self.message_index == len(self.messages) - 1 and \
            pygame.time.get_ticks() - self.time > self.delay

    def reset(self):
        self.message_index = 0
        self.characters_to_display = 0
        self.time = pygame.time.get_ticks()