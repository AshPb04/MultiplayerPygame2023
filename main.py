import string
import random
from game import *
import pygame.sysfont
from characters import *
from GUI import *
import mysql.connector

################## connect to sql database ######################
connection = mysql.connector.connect(
    host='localhost',
    user='root',
    password='',
    database='multiplayer game'
)


class MainMenu:
    def __init__(self):
        pygame.init()
        self.__animation_increment = 50
        self.__clock_tick_rate = 60
        self.__screen = pygame.display.set_mode((960, 600))
        self.__db = connection.cursor()
        pygame.display.set_caption("Let's be Triangles!")


    def __loginpageDisplay(self):
        # Creating the objects needed for the login page GUI -> background, textboxes
        menu = Background("menu")
        newPlayer_text = Textbox("new player textbox", (480, 325), width=600, height=350,
                                 font=pygame.font.Font(None, 32),
                                 modX=130, modY=30, upper=False)
        nickname_text = Textbox("nickname textbox", (480, 500), width=600, height=350, font=pygame.font.Font(None, 32),
                                modX=130, modY=30, upper=False)
        return menu, newPlayer_text, nickname_text

    def __menupageDisplay(self):
        menu = Background("menu")
        new_game = Button("new game", (480, 300), width=600, height=400)
        return menu, new_game

    # registers the new user into the database and assigns a player ID for them
    def __newNickname(self, nickname):
        self.__db.execute("SELECT name FROM users;")
        all_players = self.__db.fetchall()
        for player in all_players:
            for name in player:
                if name == nickname:
                    return False
        player_count = len(all_players) + 1
        playerID = "00000" + str(player_count)
        if len(playerID) > 6 and player_count < 999999:
            while len(playerID) > 6:
                playerID = playerID[1:]
        if player_count >= 999999:
            print(True)
            playerID = playerID[5:]
        self.__db.execute(f"INSERT INTO users (playerID, name) VALUES ('{playerID}', '{nickname}');")
        connection.commit()
        return True

    # if a user is already registered it checks to see that the user is part of the database to be able to login
    def __nicknameValidation(self, nickname):
        self.__db.execute("SELECT name FROM users;")
        all_names = self.__db.fetchall()
        for names in all_names:
            for name in names:
                if name == nickname:
                    return True
        return False

    # first page that opens up that allows users to either register or login
    def loginScreen(self):
        menu, newPlayer_text, nickname_text =  self.__loginpageDisplay()
        clock = pygame.time.Clock()
        running = True
        new = False
        registered = False
        while running:
            mouse = pygame.mouse.get_pos()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False

                if event.type == pygame.MOUSEBUTTONDOWN:
                    new = newPlayer_text.interaction(mouse)
                    if not new:
                        new = False
                        registered = nickname_text.interaction(mouse)
                        if not registered:
                            registered = False

                if event.type == pygame.KEYDOWN:
                    if new:
                        if event.key == pygame.K_RETURN:
                            nickname = newPlayer_text.getText()
                            valid = self.__newNickname(nickname)
                            if valid:
                                newPlayer_text.remove_text()
                                self.__menuScreen(nickname)
                            else:
                                newPlayer_text.remove_text()
                        newPlayer_text.typing(event, 11)
                    if registered:
                        if event.key == pygame.K_RETURN:
                            nickname = nickname_text.getText()
                            valid = self.__nicknameValidation(nickname)
                            if valid:
                                nickname_text.remove_text()
                                self.__menuScreen(nickname)
                            else:
                                nickname_text.remove_text()
                        nickname_text.typing(event, 11)

            menu.setBackground(self.__screen)
            newPlayer_text.draw(self.__screen)
            nickname_text.draw(self.__screen)
            newPlayer_text.createSurface(self.__screen)
            nickname_text.createSurface(self.__screen)
            pygame.display.flip()
            clock.tick(self.__clock_tick_rate)
        pygame.quit()

    # validates whether a code inputted by the user is within the database
    def __codeValidation(self, gameCode):
        db.execute("SELECT gameCode FROM `games`;")
        all_codes = db.fetchall()
        for i in all_codes:
            for code in i:
                print(i)
                if code == gameCode:
                    return True
        return False

    # creates a code for a new game
    def __codeGenerator(self):
        letters = string.ascii_uppercase
        letter_code = "".join(random.choice(letters) for i in range(3))
        number = str(random.randrange(0, 10))
        index = random.randrange(0, 5)
        new_code = letter_code[:index] + number + letter_code[index:]
        self.__db.execute("SELECT gameCode FROM `games`;")
        all_codes = self.__db.fetchall()
        for i in all_codes:
            for code in i:
                if code == new_code:
                    self.__codeGenerator()
        return new_code

    def __menuScreen(self, nickname):
        menu, new_game = self.__menupageDisplay()
        print("SUCCESSFULLY LOGGED IN")
        db.execute(f"SELECT playerID FROM `users` WHERE name = '{nickname}';")
        playerID = db.fetchall()
        playerID = playerID[0][0]
        clock = pygame.time.Clock()
        running = True
        while running:
            for event in pygame.event.get():
                mouse = pygame.mouse.get_pos()
                if event.type == pygame.QUIT:
                    running = False
                if event.type == pygame.MOUSEBUTTONDOWN:
                    new = new_game.interaction(mouse)
                    if new:
                        gameCode = self.__codeGenerator()
            menu.setBackground(self.__screen)
            new_game.draw(self.__screen)
            pygame.display.flip()
            clock.tick(self.__clock_tick_rate)
        pygame.quit()
        
    def __startGame(self, playerID, gameCode):
        Game = LetsBeTriangles(playerID, gameCode)
        Game.waitingRoom()
        self.loginScreen()
        
