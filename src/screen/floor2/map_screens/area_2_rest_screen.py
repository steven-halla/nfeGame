import pygame
import pytmx

from constants import PLAYER_OFFSET, BLUEBLACK
from entity.npc.area2.area_2_rest_screen.Stew import Stew
from entity.npc.area2.area_2_rest_screen.alex import Alex
from entity.npc.area2.area_2_rest_screen.alice import Alice
from entity.npc.area2.area_2_rest_screen.area_2_rest_to_boss_area import Area2RestToBossArea
from entity.npc.area2.area_2_rest_screen.area_2_rest_to_gambling_area import Area2RestToGamblingArea
from entity.npc.area2.area_2_rest_screen.area_2_rest_to_nugget_area import Area2RestToNuggetArea
from entity.npc.area2.area_2_rest_screen.area_2_rest_to_rib_demon_maze_area import Area2RestToRibDemonMazeArea
from entity.npc.area2.area_2_rest_screen.clara import Clara
from entity.npc.area2.area_2_rest_screen.johnathon import Johnathon
from entity.npc.area2.area_2_gambling_screen.lunky import Lunky
from entity.npc.area2.area_2_rest_screen.karn import Karn
from entity.npc.area2.area_2_rest_screen.natasha import Natasha
from entity.npc.area2.area_2_gambling_screen.nibblet import Nibblet
from entity.npc.area2.area_2_rest_screen.paul import Paul

from entity.player.player import Player
from game_constants.events import Events
from screen.examples.screen import Screen
from physics.rectangle import Rectangle



class Area2RestScreen(Screen):

    def __init__(self):
        super().__init__("Casino MainScreen")
        self.chili_pit_flag = False
        self.tiled_map = pytmx.load_pygame("./assets/map/restarea.tmx")
        self.y_up_move = False
        self.powerpotiongotten = False
        self.y_down_move = False
        self.x_left_move = False
        self.x_right_move = False
        self.player = Player(333, 555)
        self.hedge_hog_counter = 0
        move_player_down_flag = False
        self.npcs = []  # Initialize the NPCs list as empty
        self.clock = pygame.time.Clock()  # Initialize the clock
        self.music_file =  "/Users/stevenhalla/code/casino_hell/assets/music/relax_screen.mp3"

        self.music_volume = 0.5  # Adjust as needed
        self.initialize_music()

    def stop_music(self):
        pygame.mixer.music.stop()

    def initialize_music(self):
        # Initialize the mixer
        pygame.mixer.init()

        # Load the music file
        pygame.mixer.music.load(self.music_file)

        # Set the volume for the music (0.0 to 1.0)
        pygame.mixer.music.set_volume(self.music_volume)

        # Play the music, -1 means the music will loop indefinitely
        pygame.mixer.music.play(-1)

    def start(self, state: "GameState"):

        if (Events.QUEST_1_COIN.value in state.player.level_two_npc_state and
                Events.QUEST_1_BADGE.value in state.player.level_two_npc_state and
                Events.QUEST_1_COMPLETE.value not in state.player.level_two_npc_state):
            print("yoyoyo")
            state.player.level_two_npc_state.append(Events.QUEST_1_COMPLETE.value)

        print("this is for our nugget area")
        print(str(state.area_2_gambling_area_to_rest_point))

        if state.area_2_gambling_area_to_rest_point == True:
            print("hdshfa;ljflksja;f")
            player_start_x = 16 * 16  # Desired X coordinate
            player_start_y = 16 * 1  # Desired Y coordinate
            state.player.setPosition(player_start_x, player_start_y)
            state.area_2_gambling_area_to_rest_point = False
        if state.area_2_nugget_area_to_rest_point == True:
            print("hdshfa;ljflksja;f")
            player_start_x = 16 * 94  # Desired X coordinate
            player_start_y = 16 * 1  # Desired Y coordinate
            state.player.setPosition(player_start_x, player_start_y)
            state.area_2_nugget_area_to_rest_point = False



        self.stop_music()
        if state.musicOn == True:
            self.initialize_music()
        super().start(state)
        state.npcs.clear()



        state.npcs = [
            Alice(16 * 5, 16 * 15),
            Johnathon(16 * 15, 16 * 15),
            Nibblet(16 * 25, 16 * 15),
            Alex(16 * 26, 16 * 45),
            Lunky(16 * 36, 16 * 45),
            Natasha(16 * 70, 16 * 45),
            Clara(16 * 80, 16 * 45),
            Stew(16 * 90, 16 * 45),
            Paul(16 * 100, 16 * 45),
            Karn(16 * 60, 16 * 45),
            # below are doors
            Area2RestToGamblingArea(16 * 17, 16 * 0),
            Area2RestToNuggetArea(16 * 95, 16 * 0),
            Area2RestToRibDemonMazeArea(16 * 15, 16 * 49),
            Area2RestToBossArea(16 * 64, 16 * 49),

        ]

    def update(self, state: "GameState"):


        controller = state.controller
        player = state.player
        obstacle = state.obstacle
        controller.update()


        for npc in state.npcs:
            npc.update(state)


        if controller.isExitPressed is True:
            state.isRunning = False

        if controller.isUpPressed:

            self.y_up_move = True

            self.y_down_move = False
            self.x_left_move = False
            self.x_right_move = False

        elif controller.isDownPressed:
            self.y_down_move = True
            self.y_up_move = False
            self.x_left_move = False
            self.x_right_move = False

        elif controller.isLeftPressed:
            self.x_left_move = True
            self.y_up_move = False
            self.y_down_move = False
            self.x_right_move = False

        elif controller.isRightPressed:
            self.x_right_move = True
            self.y_up_move = False
            self.y_down_move = False
            self.x_left_move = False

        else:
            self.y_up_move = False
            self.y_down_move = False
            self.x_left_move = False
            self.x_right_move = False

        player.update(state)

        # check map for collision
        if self.tiled_map.layers:
            tile_rect = Rectangle(0, 0, 16, 16)
            collision_layer = self.tiled_map.get_layer_by_name("collision")

            for x, y, image in collision_layer.tiles():
                tile_rect.x = x * 16
                tile_rect.y = y * 16
                if state.player.collision.isOverlap(tile_rect):
                    state.player.undoLastMove()
                for demon in state.demons:
                    if demon.collision.isOverlap(tile_rect):
                        demon.undoLastMove()


        state.camera.x = PLAYER_OFFSET[0] - state.player.collision.x
        state.camera.y = PLAYER_OFFSET[1] - state.player.collision.y



    def draw(self, state: "GameState"):

        state.DISPLAY.fill(BLUEBLACK)


        if self.tiled_map.layers:
            tile_width = self.tiled_map.tilewidth
            tile_height = self.tiled_map.tileheight

            # Get the background layer
            bg_layer = self.tiled_map.get_layer_by_name("bg")
            # Iterate over the tiles in the background layer
            for x, y, image in bg_layer.tiles():
                # Calculate the position of the tile in pixels
                pos_x = x * tile_width + state.camera.x
                pos_y = y * tile_height + state.camera.y

                scaled_image = pygame.transform.scale(image, (
                tile_width * 1.3, tile_height * 1.3))

                state.DISPLAY.blit(scaled_image, (pos_x, pos_y))

            # Get the collision layer
            collision_layer = self.tiled_map.get_layer_by_name("collision")
            for x, y, image in collision_layer.tiles():
                # Calculate the position of the tile in pixels
                pos_x = x * tile_width + state.camera.x
                pos_y = y * tile_height + state.camera.y

                scaled_image = pygame.transform.scale(image, (
                tile_width * 1.3, tile_height * 1.3))

                state.DISPLAY.blit(scaled_image, (pos_x, pos_y))



        for npc in state.npcs:
            npc.draw(state)



        state.obstacle.draw(state)

        state.player.draw(state)



        if state.controller.isPPressed == True:

            state.player.draw_player_stats(state)

            if state.controller.isBPressed == True:
                if state.controller.isPPressed:
                    state.controller.isPPressed = False
                    return

        # Update the display
        pygame.display.update()
