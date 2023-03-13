import pygame
import mysql.connector

################## connect to sql database ######################
connection = mysql.connector.connect(
    host='localhost',
    user='root',
    password='',
    database='multiplayer game'
)
db = connection.cursor()

################################################ CLASSES ################################################


# retrieves image files from background and converts them so that it can be set a background
# background name can also be retrieved
class Background:
    def __init__(self, name):
        self.__name = name
        db.execute(f"SELECT imgFile FROM `backgrounds` WHERE name = '{name}';")
        self.__image = db.fetchall()
        self.__image = self.__image[0][0]
        self.__items = None
    def setBackground(self, screen):
        screen.fill((0, 0, 0))
        background_image = pygame.image.load(self.__image).convert()
        background_image = pygame.transform.smoothscale(background_image, (960, 600))
        screen.blit(background_image, (0, 0))
    def getBackground(self):
        return self.__name
    def addItemList(self, itemList):
        self.__items = itemList
    def getItemList(self):
        return self.__items


# button class for all buttons that converts the image file  to display on screen and keeps track of interactions


class Button:
    def __init__(self, name, pos, width, height):
        self.__x = pos[0]
        self.__y = pos[1]
        db.execute(f"SELECT imgFile FROM `buttons` WHERE name = '{name}';")
        self.__imgFile = db.fetchall()
        self.__imgFile = self.__imgFile[0][0]
        self.__image = pygame.image.load(self.__imgFile).convert_alpha()
        self.__image = pygame.transform.smoothscale(self.__image, (width, height))
        self.__rect = self.__image.get_rect(center=(self.__x, self.__y))
    def draw(self, screen):
        screen.blit(self.__image, self.__rect)
    def interaction(self, pos):
        x, y = pos
        if pygame.mouse.get_pressed()[0]:
            if self.__rect.collidepoint(x, y):
                return True


# a child from Button
# creates viable texting surface and displays users typing inputs
class Textbox(Button):
    def __init__(self, name, pos, width, height, font, modX, modY, upper):
        super().__init__(name, pos, width, height)
        self.__x = pos[0]
        self.__y = pos[1]
        self.__font = font
        self.__userText = ""
        self.__textX = self.__x - modX
        self.__textY = self.__y + modY
        self.__upper = upper
    def createSurface(self, screen):
        text_surface = self.__font.render(self.__userText, True, (000, 000, 000))
        screen.blit(text_surface, (self.__textX, self.__textY))
    def typing(self, event, limit):
        if event.key == pygame.K_BACKSPACE:
            self.__userText = self.__userText[:-1]
        else:
            if len(self.__userText) <= limit:
                if self.__upper:
                    self.__userText += event.unicode.upper()
                else:
                    self.__userText += event.unicode
    def remove_text(self):
        self.__userText = ""
    def getText(self):
        return self.__userText


class Text:
    def __init__(self, text, font, pos):
        self.__text = text
        self.__font = font
        self.__x = pos[0]
        self.__y = pos[1]
    def displayText(self, screen):
        text_surface = self.__font.render(self.__text, True, (000, 000, 000))
        screen.blit(text_surface, (self.__x, self.__y))


class Dialogue(Text):
    def __init__(self, text, choices):
        super().__init__(text=text, font=pygame.font.SysFont("freesansbold.ttf", 25), pos=(20, 20))
        self.__box = pygame.image.load("C:/Users/Asha Pangan/OneDrive/NEAimg/dialogueBox.png").convert_alpha()
        self.__box = pygame.transform.smoothscale(self.__box, (1000, 500))
        self.__x = 10
        self.__y = 8
        self.__font = pygame.font.SysFont("freesansbold.ttf", 23)
        self.__text = text
        self.__choices = choices
        self.__rect = self.__box.get_rect(center=(460, 90))
    def displayText(self, screen):
        text_surface = []
        for line in self.__text:
            text_surface.append(self.__font.render(line, True, (000, 000, 000)))
        for line in range(len(text_surface)):
            screen.blit(text_surface[line], (self.__x, self.__y + (line * 15) + (4 * line)))
    def draw(self, screen):
        screen.blit(self.__box, self.__rect)
        self.displayText(screen)
    def interaction(self, event):
        pass


