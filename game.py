from GUI import *
from game_classes import *
from network import Network


class LetsBeTriangles:
    def __init__(self, playerID, gameCode):
        self.__gameCode = gameCode
        self.__playerID = playerID
        self.__network = Network()
        self.__player = self.__network.getGame()
        self.__playerNum = self.__player.getPlayerNum()
        ################# CREATING WINDOW ##############################
        pygame.init()
        self.__animation_increment = 50
        self.__clock_tick_rate = 60
        self.__screen = pygame.display.set_mode((960, 600))
        pygame.display.set_caption("Let's be Triangles!")
        ################ CREATING OBJECTS FOR GAME #####################
        self.__itemLists = []
        self.__createItems()
        self.__backgrounds = self.__createBackgrounds()
        if self.__playerNum == 1:
            self.__waitingRoom = Background("waiting room 1")
        else:
            self.__waitingRoom = Background("waiting room 2")
        self.__welcome = Dialogue(text=["Welcome to the game, Let's Be Triangles!!!",
                                        "You and your friend have known each other for some time huh."
                                        "ever since you were born."
                                        "You both had a perfect childhood for",
                                        "the most part; small town, tight knit community.",
                                        "Shame what happened to your parents when you were both 15."
                                        "But they couldn't help but be geniuses, revolutionists maybe.",
                                        "Left to look after yourself from then on, but this is the week, you'll both"
                                        "(maybe)"
                                        "reach your lifelong dreams of becoming what",
                                        "you've always wanted to be, Triangles."],
                                  choices=0)
        # Other variables needed for game
        self.__startGame = False
        self.__Money = 0


    def __createItems(self):
        shop1_items = {"name": "shop 1",
                       "curtain blue": 10, "laptop cable 1": 25, "laptop cable 2": 15, "bowl": 5, "door": 50}
        shop2_items = {"name": "shop 2",
                       "apple": 2, "tomato soup": 10, "lettuce": 5, "chocolate cake": 30, "5l water": 10, "5l oil": 25}
        contraband = {"name": "shady guy",
                      "battery": 100, "wire 1": 30, "wire 2": 35}
        train = {"name": "train station",
                 "train ticket": 2}
        itemLists = [shop1_items, shop2_items, contraband, train]
        for itemList in itemLists:
            itemList = Items(itemList, itemList["name"])
            self.__itemLists.append(itemList)

    def __createBackgrounds(self):
        garden = Background("garden")
        # right from garden
        livingRoom = Background("house")
        hallway = Background("hallway")
        basement = Background("basement")

        # left from garden
        town = Background("town")
        trainStation = Background("train station")
        trainStation.addItemList(self.__itemLists[2])
        street = Background("city street")
        queue = Background("queue")
        lab = Background("lab")

        # shops
        shop1 = Background("shop 1")
        shop1.addItemList(self.__itemLists[0])
        shop2 = Background("shop 2")
        shop2.addItemList(self.__itemLists[1])
        shady_guy = Background("black market")
        shady_guy.addItemList(self.__itemLists[3])

        return [garden, livingRoom, hallway, basement,
                town, trainStation, street, queue, lab,
                shop1, shop2, shady_guy]

    def waitingRoom(self):
        self.__player.isReady()
        clock = pygame.time.Clock()
        running = True
        while running:
            clock.tick(60)
            p2 = self.__network.send(self.__player)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
            if p2.ready():
                break
            self.__waitingRoom.setBackground(self.__screen)
            pygame.display.flip()
            clock.tick(self.__clock_tick_rate)
        self.__gardenScreen(480)

    def __updateScreen(self, index, player2, location, text, choices):  # Updates screen when there are changes
        # waits if second player is not in the game yet
        apple = False
        if apple:
            self.__waitingRoom.setBackground(self.__screen)
        else:
            self.__backgrounds[index].setBackground(self.__screen) # setting background
            if player2.getLocation() == location:  # draws second player only if it's in the same location
                player2.draw(self.__screen)
                self.__player.draw(self.__screen)
            else:
                self.__player.draw(self.__screen)
            # displays welcome text
            if location == "garden":
                if not self.__startGame:
                    self.__welcome.draw(self.__screen)
            # displays dialogue needed for each scene
            if text is not None:
                dialogue = Dialogue(text, choices)
                dialogue.draw(self.__screen)
            # displays money amount
            if self.__player.getMoney() < player2.getMoney():
                self.__Money = self.__player.getMoney()
            else:
                self.__Money = player2.getMoney()
            moneyDisplay = Text(f"SHARED BANK ACCOUNT: {str(self.__Money)} shaples",
                                font=pygame.font.SysFont("freesansbold.ttf", 25),
                                pos=(15, 575))
            moneyDisplay.displayText(self.__screen)
        pygame.display.flip()

    def __addDialogue(self, text, choices, player2):
        pass

    def __gardenScreen(self, pos):
        clock = pygame.time.Clock()
        self.__player.setPos(pos)
        self.__player.setLocation("garden")
        running = True
        while running:
            clock.tick(60)
            p2 = self.__network.send(self.__player)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
            self.__player.move()
            x = self.__player.getPos()
            if x >= 1050:
                self.__livingroomScreen(0)
            if x <= 0:
                self.__townScreen(1050)
                pass
            self.__updateScreen(0, p2, "garden", None, 0)

            clock.tick(self.__clock_tick_rate)


    def __livingroomScreen(self, pos):
        self.__startGame = True
        clock = pygame.time.Clock()
        self.__player.setPos(pos)
        self.__player.setLocation("living room")
        running = True
        while running:
            clock.tick(60)
            p2 = self.__network.send(self.__player)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
            self.__player.move()
            x = self.__player.getPos()
            if x >= 1050:
                self.__hallwayScreen(0)
            if x <= 0:
                self.gardenScreen(1050)
            self.__updateScreen(1, p2, "living room", ["Home sweet home, 20 years and it never feels old"], 0)
            clock.tick(self.__clock_tick_rate)


    def __hallwayScreen(self, pos):
        clock = pygame.time.Clock()
        self.__player.setPos(pos)
        self.__player.setLocation("hallway")
        running = True
        while running:
            clock.tick(60)
            p2 = self.__network.send(self.__player)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
            self.__player.move()
            x = self.__player.getPos()
            if x >= 1050:
                if self.__player.getBasementAccess() is None:
                    self.__basementScreen(0)
                    self.__player.setBasementAccess(True)
                    p2.setBasementAccess(False)
                else:
                    if self.__player.getBasementAccess():
                        self.__basementScreen(0)
                    else:
                        self.__player.setPos(1050)
                print(self.__player.getBasementAccess(), p2.getBasementAccess())
            if x <= 0:
                self.__livingroomScreen(1050)
            self.__updateScreen(2, p2, "hallway", None, 0)
            clock.tick(self.__clock_tick_rate)


    def __basementScreen(self, pos):
        clock = pygame.time.Clock()
        self.__player.setPos(pos)
        self.__player.setLocation("basement")
        running = True
        while running:
            clock.tick(60)
            p2 = self.__network.send(self.__player)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
            self.__player.move()
            x = self.__player.getPos()
            if x >= 1050:
                self.__player.setPos(1050)
            if x <= 0:
               self.__hallwayScreen(1050)
            self.__updateScreen(3, p2, "basement", None, 0)
            clock.tick(self.__clock_tick_rate)


    def __townScreen(self, pos):
        self.__startGame = True
        clock = pygame.time.Clock()
        self.__player.setPos(pos)
        self.__player.setLocation("town")
        running = True
        while running:
            clock.tick(60)
            p2 = self.__network.send(self.__player)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_UP:
                        position = self.__player.getPos()
                        if position < 525:
                            if p2.getLocation() == "shop 1":
                                self.__townScreen(263)
                            else:
                                self.__shop1Screen()
                        elif position >= 525:
                            if p2.getLocation() == "shop 2":
                                self.__townScreen(60)
                            else:
                                self.__shop2Screen()
            self.__player.move()
            x = self.__player.getPos()
            if x >= 1050:
                self.gardenScreen(0)
            if x <= 0:
                self.__trainScreen(1050)
            self.__updateScreen(4, p2, "town",
                                ["The towns not really a town.",
                                 "It's more like a collection, or maybe a pair of two shops.",
                                 "Huh, there's a flyer here:",
                                 "'Shape Changing procedure City Centre popup'",
                                 "'Price reduction up to 50% off on procedures'"],
                                0)

            clock.tick(self.__clock_tick_rate)


    def __shop1Screen(self):
        clock = pygame.time.Clock()
        self.__player.setLocation("shop 1")
        buyBox = Textbox("buy box", (850, 500), 400, 250, pygame.font.Font(None, 25), 0, 8, True)
        running = True
        while running:
            clock.tick(60)
            p2 = self.__network.send(self.__player)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_DOWN:
                        self.__townScreen(263)
            self.__backgrounds[9].setBackground(self.__screen)
            buyBox.draw(self.__screen)
            buyBox.createSurface(self.__screen)
            pygame.display.flip()
            clock.tick(self.__clock_tick_rate)


    def __shop2Screen(self):
        clock = pygame.time.Clock()
        self.__player.setLocation("shop 2")
        running = True
        while running:
            clock.tick(60)
            p2 = self.__network.send(self.__player)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_DOWN:
                        self.__townScreen(788)
            self.__backgrounds[10].setBackground(self.__screen)
            pygame.display.flip()
            clock.tick(self.__clock_tick_rate)


    def __trainScreen(self, pos):
        clock = pygame.time.Clock()
        self.__player.setPos(pos)
        self.__player.setLocation("train")
        running = True
        while running:
            clock.tick(60)
            p2 = self.__network.send(self.__player)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
            self.__player.move()
            x = self.__player.getPos()
            if x >= 1050:
                self.__townScreen(0)
            if x <= 0:
                self.__streetScreen(1050)
            self.__updateScreen(5, p2, "train",
                                ["Ahhh the NSRS, reliable", " AND only 5 shaples to get to the City"],
                                0)
            clock.tick(self.__clock_tick_rate)


    def __streetScreen(self, pos):
        clock = pygame.time.Clock()
        self.__player.setPos(pos)
        self.__player.setLocation("street")
        running = True
        while running:
            clock.tick(60)
            p2 = self.__network.send(self.__player)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_UP:
                        position = self.__player.getPos()
                        if (position > 400) and (position < 800):
                            self.__blackmarketScreen()
            self.__player.move()
            x = self.__player.getPos()
            if x >= 1050:
                self.__trainScreen(0)
            if x <= 0:
                self.__queueScreen(1050)
            self.__updateScreen(6, p2, "street", None, 0)
            clock.tick(self.__clock_tick_rate)


    def __blackmarketScreen(self):
        clock = pygame.time.Clock()
        running = True
        while running:
            clock.tick(60)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_DOWN:
                        self.__streetScreen(525)
            self.__backgrounds[11].setBackground(self.__screen)
            pygame.display.flip()
            clock.tick(self.__clock_tick_rate)


    def __queueScreen(self, pos):
        clock = pygame.time.Clock()
        self.__player.setPos(pos)
        self.__player.setLocation("queue")
        running = True
        while running:
            clock.tick(60)
            p2 = self.__network.send(self.__player)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
            self.__player.move()
            x = self.__player.getPos()
            if x >= 1050:
                self.__streetScreen(0)
            if x <= 0:
                self.__labScreen(1050)
            self.__updateScreen(7, p2, "queue",
                                ["Security Guard: 'THE QUEUE WILL BE CLOSING SHORTLY DUE TO LENGTH.",
                                 "Security Guard: 'WE ARE REACHING MAXIMUM CAPACITY."
                                 " QUEUE TIMES ARE 5 HOURS TO THE DOOR.'",
                                 "Security Guard: 'OUT OF LINE BACK OF THE LINE NO EXCEPTIONS'"],
                                0)
            clock.tick(self.__clock_tick_rate)


    def __labScreen(self, pos):
        clock = pygame.time.Clock()
        self.__player.setPos(pos)
        self.__player.setLocation("lab")
        running = True
        while running:
            clock.tick(60)
            p2 = self.__network.send(self.__player)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
            self.__player.move()
            x = self.__player.getPos()
            if x >= 1050:
                self.__queueScreen(0)
            if x <= 0:
                self.__player.setPos(0)
            self.__updateScreen(8, p2, "lab", ["This is it, your dream.",
                                               "Was it worth it?",
                                               "I guess it wasn't just you and your friends dream.",
                                               "Like parent like child."], 0)
            clock.tick(self.__clock_tick_rate)


