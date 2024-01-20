import pygame

from entity.demon.demon1 import Demon1
from entity.npc.start_screen.cindy_long_hair import CindyLongHair
from entity.npc.rest_screen.quest_giver_janet import QuestGiverJanet
from screen.black_jack_jared_screen import BlackJackJaredScreen
from screen.black_jack_rumble_bill_screen import BlackJackRumbleBillScreen
from screen.black_jack_screen import BlackJackScreen
from screen.black_jack_thomas_screen import BlackJackThomasScreen
from screen.boss_screen import BossScreen
from screen.chilli_screen import ChilliScreen
from screen.coin_flip_fred_screen import CoinFlipFredScreen
from screen.coin_flip_sandy_screen import CoinFlipSandyScreen
from screen.coin_flip_screen import CoinFlipScreen
from screen.coin_flip_ted_screen import CoinFlipTedScreen
from constants import WINDOWS_SIZE, GREEN, BLUE
from controller import Controller
from entity.obstacle.obstacle import Obstacle
from screen.gambling_area_screen import GamblingAreaScreen
from screen.hedge_maze_screen import HedgeMazeScreen
from screen.hotel_room_screen import HotelRoomScreen
from screen.main_screen import MainScreen
from screen.opossumInACanIchi import OpossumInACanIchiScreen
from screen.opossum_in_a_can_nelly_screen import OpossumInACanNellyScreen
from screen.opossum_in_a_can_sally_screen import OpossumInACanSallyScreen
from screen.opossum_in_a_can_screen import OpossumInACanScreen
from entity.player.player import Player
from physics.vector import Vector
from screen.rest_screen import RestScreen
from screen.start_screen import StartScreen


class GameState:
    def __init__(self):
        # shared pygame constructs
        self.DISPLAY: pygame.Surface = pygame.display.set_mode(WINDOWS_SIZE)
        self.FONT = pygame.font.Font('freesansbold.ttf', 24)

        # Use in NPC only TODO remove
        self.TEXT_SURFACE = self.FONT.render('Casino', True, GREEN, BLUE)
        self.TEXT_SURFACE_RECT = self.TEXT_SURFACE.get_rect()

        # core game state
        self.controller: Controller = Controller()
        self.player: Player = Player(16 * 15, 16 * 22)
        self.demon_left: Demon1 = Demon1(0,0)
        self.cindy_long_hair: CindyLongHair = CindyLongHair(0,0)
        self.quest_giver_janet: QuestGiverJanet = QuestGiverJanet(0,0)
        self.npcs = []  # load npcs based on which screen (do not do here, but do in map load function (screen start())
        self.demons = []  # load npcs based on which screen (do not do here, but do in map load function (screen start())
        self.treasurechests = []
        # self.npcs = [CoinFlipFred(175, 138), SalleyOpossum(65, 28), ChiliWilley(311, 28)]
        self.obstacle = Obstacle(444, 999)

        self.isRunning: bool = True
        self.isPaused: bool = False
        self.delta: float = 0.0
        self.camera = Vector(0.0, 0.0)


        self.startScreen = StartScreen()
        self.chilliScreen = ChilliScreen()
        self.mainScreen = MainScreen()
        self.restScreen = RestScreen()
        self.gamblingAreaScreen = GamblingAreaScreen()
        self.hotelRoomScreen = HotelRoomScreen()
        self.bossScreen = BossScreen()
        # self.restScreen = RestScreen()
        self.hedgeMazeScreen = HedgeMazeScreen()
        # self.bossScreen = BossScreen()

        self.coinFlipScreen = CoinFlipScreen()
        self.coinFlipTedScreen = CoinFlipTedScreen()
        self.coinFlipFredScreen = CoinFlipFredScreen()
        self.coinFlipSandyScreen = CoinFlipSandyScreen()

        self.opossumInACanScreen = OpossumInACanScreen()
        self.opossumInACanNellyScreen = OpossumInACanNellyScreen()
        self.opossumInACanSallyScreen = OpossumInACanSallyScreen()
        self.opossumInACanIchiScreen = OpossumInACanIchiScreen()

        self.blackJackScreen = BlackJackScreen()
        self.blackJackThomasScreen = BlackJackThomasScreen()
        self.blackJackRumbleBillScreen = BlackJackRumbleBillScreen()
        self.blackJackJaredScreen = BlackJackJaredScreen()

        self.currentScreen = self.bossScreen
        # assign a value to currentScreen here
