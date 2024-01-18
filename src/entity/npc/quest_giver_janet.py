import math

import pygame

from entity.npc.npc import Npc
from entity.gui.textbox.npc_text_box import NpcTextBox


#### NOTE: BOTH JANET AND BILLY BOTH NEED HEDGE HOG AND WATER WILL NEED TO CHANGE IN FUTURE
####
####
class QuestGiverJanet(Npc):
    def __init__(self, x: int, y: int):
        super().__init__(x, y)
        self.queststart1 = NpcTextBox(
            ["I have a quest for you, get a score of 500 in opossum in a can from nelly OR sandy", "there are two people here you can do this from, be sure to complete the quest beforehand. Once you defeate someone you cant fight them."],
            (50, 450, 50, 45), 30, 500)
        self.questfinish1 = NpcTextBox(
            ["Janet: Wow you really got hte 500 points!!! Hope you enjoy your reward"],
            (50, 450, 50, 45), 30, 500)
        self.queststart2 = NpcTextBox(
            ["Janet: If you want more from me you need to be more suave, get a Spirit of 1 and come back and talk to me."],
            (50, 450, 50, 45), 30, 500)
        self.questfinish2 = NpcTextBox(
            ["Janet: Your chariasma is magnetic I'll talk to you now and reward you!"],
            (50, 450, 50, 45), 30, 500)
        self.queststart3 = NpcTextBox(
            ["Janet: Can you find my hedge hog friend Nurgle? We just seperated right before you talked to me. ",  "He loves to dig around in the trash, he's so cute, plump, white, looks very sickly"],
            (50, 450, 50, 45), 30, 500)

        self.questfinish3 = NpcTextBox(
            ["Janet:Thank you so much for finding my drinking buddy. ", "I'll teach you the ultimate black jack technique"],
            (50, 450, 50, 45), 30, 500)
        self.choices = ["Yes", "No"]
        self.menu_index = 0
        self.input_time = pygame.time.get_ticks()
        self.find_hog = False

        self.state_start_time = pygame.time.get_ticks()  # initialize start_time to the current time
        self.state = "waiting"  # states = "waiting" | "talking" | "finished"
        self.textboxstate = "textbox1" # state = "textbox1" | "textbox2" | "textbox3" | "textbox4" | "textbox5"
        self.talkfirstfivehundred = False
        self.quest2counter = False
        self.quest3counter = False

    def update(self, state: "GameState"):
        # print("current state is:" + str(self.textboxstate))

        if self.state == "waiting":
            if state.opossumInACanScreen.five_hundred_points == True and self.talkfirstfivehundred == True:
                self.textboxstate = "textbox2"
                self.talkfirstfivehundred = False
                # print("am I getting reset?")
                # if self.talkfirstfivehundred == True:
                #     print("fjasd;fjkdls")


            if state.player.spirit == 1 and self.quest2counter == True:
                # print("time for the 2nd quest")
                self.textboxstate = "textbox4"
                self.find_hog = True

            if "Nurgle the hedge hog" in state.player.items and self.quest3counter == True:
                print("Hi")
                self.textboxstate = "textbox6"







            # if "Nurgle the hedge hog" in state.player.items and self.talkfirstbeforehandoverhog == True:
            #
            #     self.textboxstate = "textbox2"
            #     print(self.textboxstate)
            #
            # if "Water Bottle" in state.player.items and self.talkfirstbeforehandoverwater == True:
            #     self.textboxstate = "textbox4"
            #     print(self.textboxstate)

            player = state.player

            # print("waiting")
            # if value is below 88 it wont activate for some reason
            min_distance = math.sqrt(
                (player.collision.x - self.collision.x) ** 2 + (
                            player.collision.y - self.collision.y) ** 2)
            #
            # if min_distance < 25:
            #     print("nooo")

            self.update_waiting(state)

        elif self.state == "talking":
            # self.textbox.reset()
            # self.textbox.message_index = 0

            self.update_talking(state)

    def update_waiting(self, state: "GameState"):
        player = state.player
        # print(self.state)
        min_distance = math.sqrt(
            (player.collision.x - self.collision.x) ** 2 + (
                        player.collision.y - self.collision.y) ** 2)

        if min_distance < 10:
            print("nooo")

        if state.controller.isTPressed and (
                pygame.time.get_ticks() - self.state_start_time) > 500:
            distance = math.sqrt(
                (player.collision.x - self.collision.x) ** 2 + (
                            player.collision.y - self.collision.y) ** 2)
            # print("distance: " + str(distance))

            if distance < 40:
                # print("start state: talking")
                # print("10")

                self.state = "talking"

                self.state_start_time = pygame.time.get_ticks()
                # the below is where kenny had it
                if self.textboxstate == "textbox1":
                    # print("Textbox1")
                    self.queststart1.reset()
                elif self.textboxstate == "textbox2":
                    # print("Textbox2")
                    self.questfinish1.reset()
                elif self.textboxstate == "textbox3":

                    self.queststart2.reset()

                elif self.textboxstate == "textbox4":
                    self.questfinish2.reset()
                elif self.textboxstate == "textbox5":
                    self.queststart3.reset()
                elif self.textboxstate == "textbox6":
                    self.questfinish3.reset()

    def update_talking(self, state: "GameState"):
        current_time = pygame.time.get_ticks()

        # Update and check the state of the appropriate text box
        if self.textboxstate == "textbox1":
            self.queststart1.update(state)
            if state.controller.isTPressed and (current_time - self.input_time > 500):
                if self.queststart1.is_finished():
                    self.state = "waiting"
                    self.state_start_time = current_time
                    self.input_time = current_time  # Update last input time
                    self.talkfirstfivehundred = True


        elif self.textboxstate == "textbox2":
            self.questfinish1.update(state)
            if state.controller.isTPressed and (current_time - self.input_time > 500):
                print("Hi")
                if self.questfinish1.is_finished():
                    # state.player.items.remove("Nurgle the hedge hog")
                    # if "janet reward 1" not in state.player.items:
                    #     state.player.items.append("janet reward 1")
                    print(self.textboxstate)

                    self.textboxstate = "textbox3"
                    print(self.textboxstate)

                    # self.talkfirstbeforehandoverhog = False

                    self.state = "waiting"
                    self.state_start_time = current_time
                    self.input_time = current_time  # Update last input time
                    print(self.textboxstate)



        elif self.textboxstate == "textbox3":
            print("am i here??????")

            self.queststart2.update(state)
            if state.controller.isTPressed and (current_time - self.input_time > 500):
                if self.queststart2.is_finished():

                    self.state = "waiting"
                    self.state_start_time = current_time
                    self.input_time = current_time  # Update last input time
                    # self.talkfirstfivehundred = True
                    self.quest2counter = True




        elif self.textboxstate == "textbox4":
            self.questfinish2.update(state)
            if state.controller.isTPressed and (current_time - self.input_time > 500):
                if self.questfinish2.is_finished():
                    # state.player.items.remove("Water Bottle")
                    print("we are in textbox4")
                    self.quest2counter = False



                    self.state = "waiting"
                    self.state_start_time = current_time
                    self.input_time = current_time  # Update last input time
                    self.textboxstate = "textbox5"

        elif self.textboxstate == "textbox5":
            self.queststart3.update(state)
            if state.controller.isTPressed and (current_time - self.input_time > 500):
                if self.queststart3.is_finished():
                    self.state = "waiting"
                    self.state_start_time = current_time
                    self.input_time = current_time  # Update last input time
                    self.find_hog = True
                    self.quest3counter = True

        elif self.textboxstate == "textbox6":
            self.questfinish3.update(state)
            if state.controller.isTPressed and (current_time - self.input_time > 500):
                if self.questfinish3.is_finished():
                    self.state = "waiting"
                    self.state_start_time = current_time
                    self.input_time = current_time  # Update last input time
                    self.find_hog = True
                    self.quest3counter = True





    def draw(self, state):
        rect = (
        self.collision.x + state.camera.x, self.collision.y + state.camera.y,
        self.collision.width, self.collision.height)
        pygame.draw.rect(state.DISPLAY, self.color, rect)

        if self.state == "waiting":
            pass
        elif self.state == "talking":
            # print("is talking")
            if self.textboxstate == "textbox1":
                self.queststart1.draw(state)
            elif self.textboxstate == "textbox2":
                self.questfinish1.draw(state)
            elif self.textboxstate == "textbox3":
                self.queststart2.draw(state)
            elif self.textboxstate == "textbox4":
                self.questfinish2.draw(state)
            elif self.textboxstate == "textbox5":
                self.queststart3.draw(state)
                self.find_hog = True
            elif self.textboxstate == "textbox6":
                self.questfinish3.draw(state)
                self.find_hog = True

