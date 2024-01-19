import pygame
import random
import math
from typing import Tuple

from entity.entity import Entity
from constants import GREEN, PURPLE
from physics.rectangle import Rectangle

class Demon(Entity):
    def __init__(self, x: int, y: int):
        super().__init__(x, y, 16, 16)
        self.color: Tuple[int, int, int] = GREEN
        self.last_move_time = pygame.time.get_ticks()
        self.move_interval = 3000  # 3 seconds in milliseconds
        self.move_distance = 32  # distance to move each step
        self.last_color_change_time = pygame.time.get_ticks()
        self.color_change_interval = 3000

    def move_randomly(self, state):
        current_time = pygame.time.get_ticks()
        if current_time - self.last_move_time > self.move_interval:
            self.last_move_time = current_time
            direction = random.choice(['up', 'down', 'left', 'right'])

            # Adjust position based on direction
            if direction == 'up':
                self.position.y -= self.move_distance
            elif direction == 'down':
                self.position.y += self.move_distance
            elif direction == 'left':
                self.position.x -= self.move_distance
            elif direction == 'right':
                self.position.x += self.move_distance

            # Update the collision rectangle's position
            self.collision.x = self.position.x
            self.collision.y = self.position.y

        super().update(state)  # Call update at the end

    def LOSLeft(self, state):
        current_time = pygame.time.get_ticks()
        if current_time - self.last_color_change_time > self.color_change_interval:
            self.last_color_change_time = current_time
            if self.color == GREEN:
                self.color = PURPLE
            else:
                self.color = GREEN

        # Define the LOS range to the left of the demon
        los_range = 50  # Adjust this value as needed

        # Calculate the left boundary of the LOS range
        los_left_boundary = self.collision.x - los_range

        # Check if the player's position falls within the LOS range
        if state.player.collision.x < self.collision.x and \
                self.collision.x > los_left_boundary:
            print("Player is in LOS!")  # Print statement when the player is in LOS

            # Check if the player is to the left of the demon
            if state.player.collision.x < self.collision.x:
                print("I see you to the left")  # Print statement when the player is to the left

        # Store the LOS range for drawing
        self.los_range = los_range

    def update(self, state):
        super().update(state)
        # Reset velocity after moving

    def draw(self, state):
        rect = (
            self.collision.x + state.camera.x, self.collision.y + state.camera.y,
            self.collision.width, self.collision.height)
        pygame.draw.rect(state.DISPLAY, self.color, rect)

        if self.color == GREEN and hasattr(self, 'los_rect'):
            # Offset the LOS rect by the camera position for correct positioning on the screen
            los_rect_screen = self.los_rect.move(state.camera.x, state.camera.y)
            pygame.draw.rect(state.DISPLAY, (255, 255, 255), los_rect_screen, 1)
