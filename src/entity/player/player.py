import json
from typing import Tuple

import pygame

from constants import TILE_SIZE, RED, SCREEN_WIDTH, SCREEN_HEIGHT, PLAYER_OFFSET, BLUEBLACK
from entity.entity import Entity


class Player(Entity):
    def __init__(self, x: float, y: float):
        super().__init__(x, y, TILE_SIZE, TILE_SIZE)
        self.color: Tuple[int, int, int] = RED
        self.walk_speed = 3.5
        self.money = 500
        # self.image = pygame.image.load(
        #     "/Users/stevenhalla/code/casino_hell/assets/images/SNES - Harvest Moon - Jack.png")
        self.character_sprite_down_image = pygame.image.load(
            "/Users/stevenhalla/code/casino_hell/assets/images/SNES - Harvest Moon - Jack.png").convert_alpha()

        self.character_sprite_left_image= pygame.image.load(
            "/Users/stevenhalla/code/casino_hell/assets/images/SNES - Harvest Moon - Jack.png").convert_alpha()

        self.character_sprite_up_image= pygame.image.load(
            "/Users/stevenhalla/code/casino_hell/assets/images/SNES - Harvest Moon - Jack.png").convert_alpha()

        # need to put in a max for stamina and focus

        self.exp = 0
        self.inn_badge = False
        self.level = 1
        self.body = 0
        self.mind = 0
        self.spirit = 0
        self.luck = 0
        self.food = 0
        self.perception = 0
        self.stamina_points = 55
        self.stamina_increase = self.body * 1 * self.level

        self.stamina_guard = False

        self.max_stamina_points = 100 + self.stamina_increase
        self.focus_points = 100
        self.max_focus_points = 100
        self.perks = []
        self.items = []

        self.magicinventory = [ ]
        self.companions = []
        self.canMove = True
        self.level3janetreward = False

        self.hasRabies = False


        self.rabies1time = False
        self.rabiesImmunity = False
        self.level2checker = False
        self.level3checker = False
        self.level4checker = False
        #conflip glasses gives player + 20 gold
        # need ingame menus that explain rules, minues to stamina,and other info
        self.close_status_screen = False

        self.days = 0

        self.isBossWorthy = False
        self.realBarKeep = False




    def to_dict(self, state: "GameState") -> dict:
        return {
            "level": self.level,
            "exp": self.exp,
            "stamina_points": self.stamina_points,
            "max_stamina_points": self.max_stamina_points,
            "focus_points": self.focus_points,
            "max_focus_points": self.max_focus_points,
            "companions": self.companions,
            "items": self.items,
            "magicinventory": self.magicinventory,
            "body": self.body,
            "mind": self.mind,
            "spirit": self.spirit,
            "perception": self.perception,
            "luck": self.luck,
            "money": self.money,
            "rabies": self.hasRabies,
            "immunity": self.rabiesImmunity,
            "level3reward": self.level3janetreward,
            "food": self.food,
            "days": self.days,
            "cutscene1": state.restScreen.barscene1,
            "cutscene2": state.restScreen.barscene2,

            "quest1complete": state.gamblingAreaScreen.five_hundred_opossums,

            "coinfliptedmoney": state.coinFlipTedScreen.coinFlipTedMoney,
            "coinflipfredmoney": state.coinFlipFredScreen.coinFlipFredMoney,

            "opossumnellymoney": state.opossumInACanNellyScreen.nellyOpossumMoney,
            "opossumsallymoney": state.opossumInACanSallyScreen.sallyOpossumMoney,

            "blackjackthomasmoney": state.blackJackThomasScreen.cheater_bob_money,
            "blackjackrumblebillmoney": state.blackJackRumbleBillScreen.cheater_bob_money,

            # Add more stats as needed
        }



    def update(self, state: "GameState"):





        controller = state.controller
        controller.update()

        # if controller.isPPressed:
        #     controller.isPPressed = False
        #     self.draw_player_stats(state)

        if controller.isOPressed:
            print("Your inventory for items: " + str(self.items))
            print("Your inventory for magic: " + str(self.magicinventory))
            print("Your body is: " + str(self.body))
            print("Your mind is: " + str(self.mind))
            print("Your spirit is: " + str(self.spirit))
            print("Your luck is: " + str(self.luck))
            print("Your perception is: " + str(self.perception))
            print("Your Hp  is: " + str(self.stamina_points) + "/" + str(self.max_stamina_points))
            print("Your Mp  is: " + str(self.focus_points) + "/" + str(self.max_focus_points))
            print("Your EXP is : " + str(self.exp))
            print("Your Level is : " + str(self.level))
            print("has rabies status: " + str(self.hasRabies))
            print("immune status: " + str(self.rabiesImmunity))
            print("food: " + str(self.food))

            controller.isOPressed = False

        if self.exp > 300 and self.level2checker == False:
            print("grats you leveld up to level 2")
            self.level = 2

            if self.spirit < 1:
                self.max_stamina_points += 10 + (self.stamina_increase)
                self.max_focus_points += 10
                self.spirit += 1
            self.level2checker = True
            return

        if self.exp > 320 and self.level3checker == False:
            print("grats you leveld up to level 3")
            # if "shield" not in self.magicinventory:
            if "shield" not in state.player.magicinventory:
                self.magicinventory.append("shield")
                self.max_stamina_points += 10
                self.max_focus_points += 10
            self.level3checker = True
            self.level = 3

            return


        # Define canMove before the for loop
        for npc in state.npcs:
            if npc.isSpeaking:
                self.canMove = False
                break

        if self.canMove:
            if controller.isLeftPressed:
                self.velocity.x = -self.walk_speed
            elif controller.isRightPressed:
                self.velocity.x = self.walk_speed
            else:
                # hard stop
                # self.velocity.x = 0  # default velocity to zero unless key pressed
                # slow stop
                self.velocity.x *= 0.65  # gradually slow the x velocity down
                if abs(self.velocity.x) < 0.15:  # if x velocity is close to zero, just set to zero
                    self.velocity.x = 0

            if controller.isUpPressed:
                self.velocity.y = -self.walk_speed
            elif controller.isDownPressed:
                self.velocity.y = self.walk_speed
            else:
                # hard stop
                # self.velocity.y = 0  # default velocity to zero unless key pressed
                # slow stop
                self.velocity.y *= 0.65  # gradually slow the y velocity down
                if abs(self.velocity.y) < 0.15:  # if y velocity is close to zero, just set to zero
                    self.velocity.y = 0

        else:  # if can not move, set velocity to zero
            self.velocity.x = 0
            self.velocity.y = 0

        # move player by velocity
        # note that if we have any collisions later we will undo the movements.
        # TODO test collision BEFORE moving
        self.setPosition(self.position.x + self.velocity.x,
                         self.position.y + self.velocity.y)



        if self.isOverlap(state.obstacle):
            self.undoLastMove()




        for npc in state.npcs:
            # print("p(" + str(state.player.collision.x) + "," + str(state.player.collision.x) + "),n(" + str(npc.collision.x) + "," + str(npc.collision.x) + ")")
            if self.collision.isOverlap(npc.collision) :



                # print("collide with npc: " + str(npc.collision.toTuple()))
                # print("moogle pants")

                self.undoLastMove()
                break

        for treasurechests in state.treasurechests:
            # print("p(" + str(state.player.collision.x) + "," + str(state.player.collision.x) + "),n(" + str(npc.collision.x) + "," + str(npc.collision.x) + ")")
            if self.collision.isOverlap(treasurechests.collision) :
                print("collide with chests: " + str(treasurechests.collision.toTuple()))
                self.undoLastMove()
                break

        for demon in state.demons:
            # print("p(" + str(state.player.collision.x) + "," + str(state.player.collision.x) + "),n(" + str(npc.collision.x) + "," + str(npc.collision.x) + ")")
            if self.collision.isOverlap(
                    demon.collision) :
                print("collide with npc: " + str(demon.collision.toTuple()))
                self.undoLastMove()
                break


    def draw(self, state):

        # down image
        # sprite_rect = pygame.Rect(22, 120, 24, 26)
        # sprite = self.character_sprite_down_image.subsurface(sprite_rect)
        # scaled_sprite = pygame.transform.scale(sprite, (50, 50))
        # sprite_x = self.collision.x + state.camera.x - 20
        # sprite_y = self.collision.y + state.camera.y - 10
        # state.DISPLAY.blit(scaled_sprite, (sprite_x, sprite_y))

        # left image
        # sprite_rect = pygame.Rect(22, 146, 24, 26)
        # sprite = self.character_sprite_left_image.subsurface(sprite_rect)
        # scaled_sprite = pygame.transform.scale(sprite, (50, 50))
        # sprite_x = self.collision.x + state.camera.x - 20
        # sprite_y = self.collision.y + state.camera.y - 10
        # state.DISPLAY.blit(scaled_sprite, (sprite_x, sprite_y))

        # #up image
        # sprite_rect = pygame.Rect(22, 172, 24, 26)
        # sprite = self.character_sprite_up_image.subsurface(sprite_rect)
        # scaled_sprite = pygame.transform.scale(sprite, (50, 50))
        # sprite_x = self.collision.x + state.camera.x - 20
        # sprite_y = self.collision.y + state.camera.y - 10
        # state.DISPLAY.blit(scaled_sprite, (sprite_x, sprite_y))
        sprite_rect = pygame.Rect(22, 146, 24, 26)
        sprite = self.character_sprite_left_image.subsurface(sprite_rect)
        scaled_sprite = pygame.transform.scale(sprite, (50, 50))
        flipped_sprite = pygame.transform.flip(scaled_sprite, True, False)
        sprite_x = self.collision.x + state.camera.x - 20
        sprite_y = self.collision.y + state.camera.y - 10
        state.DISPLAY.blit(flipped_sprite, (sprite_x, sprite_y))

    def draw_player_stats(self, state):
        # Create a black surface of size 600x600
        stats_surface = pygame.Surface((620, 580))
        state.DISPLAY.fill(BLUEBLACK)

        # Set the font for the text
        font = pygame.font.Font(None, 36)

        # Define the stats to display

        stats = [
            f"Level: {self.level}     Exp: {self.exp}",
            f"money: {self.money}",
            f"Stamina: {self.stamina_points}/{self.max_stamina_points}",
            f"Magic Points: {self.focus_points}/{self.max_focus_points}",
            f"Magic spells: {self.magicinventory}",
            f"Mind: {self.mind} Body: {self.body} Spirit: {self.spirit}",
            f"Perception:" f" {self.perception} Luck: {self.luck}",
            f"Day: {self.days}",
            f"Food: {self.food}",
        ]

        # Add Items to the stats list, one item per line
        for companion in self.companions:
            stats.append(f"Companions: {companion}")
        for item in self.items:
            stats.append(f"Item: {item}")


        # Draw each stat on the stats_surface
        for i, stat in enumerate(stats):
            text = font.render(stat, True, (255, 255, 255))  # White color for the text
            stats_surface.blit(text, (50, 30 + i * 40))  # Adjust the position as needed

        # You can adjust these values to position the box as you like
        box_x = SCREEN_WIDTH / 2 - 300  # Center the box in the middle of the screen width
        box_y = SCREEN_HEIGHT / 2 - 290  # Center the box in the middle of the screen height

        # Display the stats surface on the main display
        state.DISPLAY.blit(stats_surface, (box_x, box_y))

        border_color = (255, 255, 255)  # White color
        border_rect = pygame.Rect(box_x, box_y, 580, 580)  # The rectangle that represents the border
        border_thickness = 5  # Adjust the thickness as needed
        pygame.draw.rect(state.DISPLAY, border_color, border_rect, border_thickness)

        # if state.controller.isLPressed:
        #     state.controller.isLPressed = False
        #     print("L is pressed")
        #     # Call the load_game function when the L key is pressed
        #     self.load_game(state)

    def load_game(self, state):

        # Define the file path
        file_path = '/Users/stevenhalla/code/casino_hell/assets/save_data.json'

        # Read the JSON string from the file
        try:
            with open(file_path, 'r') as file:
                player_data_json = file.read()

            # Convert JSON string to a dictionary
            player_data = json.loads(player_data_json)

            # Update player's stats with the loaded data
            state.player.level = player_data['level']
            state.player.exp = player_data['exp']
            state.player.stamina_points = player_data['stamina_points']
            state.player.max_stamina_points = player_data['max_stamina_points']
            state.player.focus_points = player_data['focus_points']
            state.player.max_focus_points = player_data['max_focus_points']
            state.player.companions = player_data['companions']
            state.player.items = player_data['items']
            state.player.magicinventory = player_data['magicinventory']
            state.player.body = player_data['body']
            state.player.mind = player_data['mind']
            state.player.spirit = player_data['spirit']
            state.player.perception = player_data['perception']
            state.player.luck = player_data['luck']
            state.player.money = player_data['money']
            state.player.hasRabies = player_data['rabies']
            state.player.rabiesImmunity = player_data['immunity']
            state.player.level3janetreward = player_data['level3reward']
            state.player.food = player_data['food']
            state.player.days = player_data['days']
            state.restScreen.barscene1 = player_data['cutscene1']
            state.restScreen.barscene2 = player_data['cutscene2']

            state.gamblingAreaScreen.five_hundred_opossums = player_data['quest1complete']





            state.coinFlipTedScreen.coinFlipTedMoney = player_data['coinfliptedmoney']
            state.coinFlipFredScreen.coinFlipFredMoney = player_data['coinflipfredmoney']

            state.opossumInACanNellyScreen.nellyOpossumMoney = player_data['opossumnellymoney']
            state.opossumInACanSallyScreen.sallyOpossumMoney = player_data['opossumsallymoney']

            state.blackJackThomasScreen.cheater_bob_money = player_data['blackjackthomasmoney']
            state.blackJackRumbleBillScreen.cheater_bob_money = player_data['blackjackrumblebillmoney']


            innkeeper_position_x = 16 * 22
            innkeeper_position_y = 16 * 11
            state.player.setPosition(innkeeper_position_x, innkeeper_position_y)

            # Switch to the restScreen
            state.currentScreen = state.restScreen
            state.restScreen.start(state)
            # ... more stats as needed

            print("Game loaded successfully.")

        except Exception as e:
            print(f"Failed to load game: {e}")





