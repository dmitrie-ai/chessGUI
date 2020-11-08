import pygame  # used to draw onto screen, render text etc
default_font="comicsansms"

class Button:
    '''
    A simple implementation of a button
    '''
    def __init__(self, x, y, width, height, btn_color, text, text_color,font=default_font,font_size=20):
        '''
        :param x: INT. x coordinate of the top left corner of the button.
        :param y: INT. y coordinate of the top left corner of the button. top left of window is (0,0)
        :param width: INT. width of button in pixels
        :param height: INT. height of button in pixels
        :param btn_color: TUPLE OF 3 INT RGB
        :param text: STRING
        :param text_color: TUPLE OF 3 INT RGB
        :param font: STRING. Default to the default font set above for consistency
        :param font_size: INT .default to 20
        '''
        self.font=font
        self.font_size=font_size
        self.x = x
        self.y = y
        self.btn_color = btn_color
        self.text_color = text_color
        self.text = text
        self.height = height
        self.width = width
        self.__rect = pygame.Rect(x, y, width, height) #region of screen where the button will be

    def get_text(self):
        return  self.text

    def draw(self, game_display):
        '''
        draws the button onto the screen
        :param game_display: pygame.display object.
        '''
        pygame.draw.rect(game_display, self.btn_color, self.__rect)
        font = pygame.font.SysFont(self.font, self.font_size)
        text = font.render(self.text, 1, self.text_color)
        game_display.blit(text, (
        self.x + (self.width / 2 - text.get_width() / 2), (self.y + (self.height / 2 - text.get_height() / 2))))

    def update(self):#updates the region of space where the button is so that the button is displayed.
        pygame.display.update(self.__rect)

    def is_over(self, pos):
        '''
        Checks whether a cartesian position is in in the button region.
        Used to check whether the cursor was on the button when the user clicked it.
        :param pos: TUPLE of INTEGER. (x,y) coordinate
        :return: BOOL.
        '''
        if pos[0] > self.x and pos[0] < self.x + self.width:
            if pos[1] > self.y and pos[1] < self.y + self.height:
                return True
        return False

    def erase(self,game_display,color=(0,0,0)):
        '''
        Paints over the button region with the same colour as the background so it isn't visible.
        :param game_display: pygame.display object
        :param color: TUPLE of 3 INT RGB. Colour of the background. Set to black by default but the colour of
        the background changes, it will have to be changed
        '''
        pygame.draw.rect(game_display, color, self.__rect) # draw rectangle of background colour on top of button region
        pygame.display.update(self.__rect)


class Label:
    '''
    Simple implementation of label. Display text onto the screen
    '''
    def __init__(self, text, color, x, y, size,font=default_font):
        '''
        :param text: STRING. TExt to be displayed
        :param color: TUPLE OF 3 INT RGB
        :param x: INT. x coordinate of the top left of the text
        :param y: INT. y coordinate of the top left of the text. Top left of window =(0,0)
        :param size: INT. font size of text
        :param font: STRING. Set to the default font specified above for consistency
        '''
        self.text = text
        self.x = x
        self.y = y
        self.color = color
        self.font_size = size
        self.font=font
        self.font = pygame.font.SysFont(self.font, self.font_size)
        self.text_width, self.text_height = self.font.size(text) # width and height of the text in the specified font and font size
        self.__rect = pygame.Rect(self.x, self.y, self.text_width, self.text_height)#region of window where the text will be

    def get_text(self):
        return self.text

    def draw(self, game_display):
        '''
        draws the text onto the screen
        :param game_display: pygame.display object
        '''
        text = self.font.render(self.text, 1, self.color)
        game_display.blit(text, (self.x, self.y))

    def update(self):# update region of window to show the text
        pygame.display.update(self.__rect)

    def erase(self, game_display,color=(0,0,0)):
        '''

        Paints over the label region with the same colour as the background so it isn't visible.
        :param game_display: pygame.display object
        :param color: TUPLE of 3 INT RGB. Colour of the background. Set to black by default but the colour of
        the background changes, it will have to be changed
        '''
        pygame.draw.rect(game_display, color, self.__rect) # draw rectangle of background colour on top of label region
        pygame.display.update(self.__rect)


