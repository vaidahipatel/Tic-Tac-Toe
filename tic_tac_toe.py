import time

import pygame as pg
import tkinter as tk
import sys
from pygame.locals import QUIT, MOUSEBUTTONDOWN


# initialize global variables
player1 = 'x'
player2 = 'o'
XO = 'x'
winner = None
draw = False
width = 600
height = 600
black = (0, 0, 0)
line_color = '#334553'

# TicTacToe 3x3 board
TTT = [[None] * 3, [None] * 3, [None] * 3]


root = tk.Tk()
root.geometry("500x200")
root.title("Tic Tac Toe")
root["bg"] = '#000000'

name_var1 = tk.StringVar()
name_var2 = tk.StringVar()

name_label1 = tk.Label(root, text='Player - 1', font=('calibre', 16, 'bold'), bg='#000000', fg='#FF0000', pady=7)
name_entry1 = tk.Entry(root, textvariable=name_var1, font=('calibre', 14, 'normal'))
name_label2 = tk.Label(root, text='Player - 2', font=('calibre', 16, 'bold'), bg='#000000', fg='#00B3B3', pady=7)
name_entry2 = tk.Entry(root, textvariable=name_var2, font=('calibre', 14, 'normal'))


def submit():
    global player1, player2
    player1 = name_var1.get()
    player2 = name_var2.get()

    print("The name1 is : " + player1)
    print("The name2 is : " + player2)
    name_var1.set("")
    name_var2.set("")
    root.destroy()


sub_btn = tk.Button(root, text='Play Game', command=submit, font=('calibre', 10, 'normal'))
name_label1.pack()
name_entry1.pack()
name_label2.pack()
name_entry2.pack()
sub_btn.pack(pady=15)
root.mainloop()

# initializing pygame window
pg.init()
fps = 30
CLOCK = pg.time.Clock()
# this method is used to build the
# infrastructure of the display
# parameters = (width,height), depth, fps
screen = pg.display.set_mode((width, height + 100), 0, 32)
pg.display.set_caption("Tic Tac Toe")

# loading the images
opening = pg.image.load('front page.jpg')
x_img = pg.image.load('X.png')
o_img = pg.image.load('O.png')

# resizing images
x_img = pg.transform.scale(x_img, (120, 120))
o_img = pg.transform.scale(o_img, (120, 120))
opening = pg.transform.scale(opening, (width, height + 100))


def game_opening():  # opens the main tic tac toe game
    screen.blit(opening, (0, 0))
    pg.display.update()
    time.sleep(2)
    screen.fill(black)

    # Drawing vertical lines
    pg.draw.line(screen, line_color, (width / 3, 0), (width / 3, height), 7)
    pg.draw.line(screen, line_color, (width / 3 * 2, 0), (width / 3 * 2, height), 7)
    # Drawing horizontal lines
    pg.draw.line(screen, line_color, (0, height / 3), (width, height / 3), 7)
    pg.draw.line(screen, line_color, (0, height / 3 * 2), (width, height / 3 * 2), 7)
    draw_status()


def draw_status():
    global draw, XO, player1, player2, winner

    if winner is None:
        if XO == 'x':
            message = player1 + "'s Turn"
        else:
            message = player2 + "'s Turn"
    else:
        if winner == 'x':
            message = player1 + " won!"
        else:
            message = player2 + " won!"
    if draw:
        message = 'Game Draw!'

    font = pg.font.Font(None, 40)  
    # setting the font properties like
    # width and color of the text
    # render(text, antialias, color, background=None)
    # antialias for smooth edges
    text = font.render(message, 1, (255, 255, 255)) 

    # copy the rendered message onto the board
    screen.fill('#334553', (0, 600, 600, 100))
    text_rect = text.get_rect(center=(width / 2, 700 - 50))
    screen.blit(text, text_rect)
    pg.display.update()


def check_win():  # function for checking win
    global TTT, winner, draw

    # check for winning rows
    for row in range(0, 3):
        if (TTT[row][0] == TTT[row][1] == TTT[row][2]) and (TTT[row][0] is not None):
            # this row won
            winner = TTT[row][0]
            pg.draw.line(screen, '#f9005c', (0, (row + 1) * height / 3 - height / 6),
                         (width, (row + 1) * height / 3 - height / 6), 4)
            break

    # check for winning columns
    for col in range(0, 3):
        if (TTT[0][col] == TTT[1][col] == TTT[2][col]) and (TTT[0][col] is not None):
            # this column won
            winner = TTT[0][col]
            # draw winning line
            pg.draw.line(screen, '#f9005c', ((col + 1) * width / 3 - width / 6, 0),
                         ((col + 1) * width / 3 - width / 6, height), 4)
            break

    # check for diagonal winners
    if (TTT[0][0] == TTT[1][1] == TTT[2][2]) and (TTT[0][0] is not None):
        # game won diagonally left to right
        winner = TTT[0][0]
        pg.draw.line(screen, '#f9005c', (50, 50), (550, 550), 4)

    if (TTT[0][2] == TTT[1][1] == TTT[2][0]) and (TTT[0][2] is not None):
        # game won diagonally right to left
        winner = TTT[0][2]
        pg.draw.line(screen, '#f9005c', (550, 50), (50, 550), 4)

    if all([all(row) for row in TTT]) and winner is None:
        draw = True
    draw_status()


def drawXO(row, col):  # finds the position for drawing x or o
    global TTT, XO
    if row == 1:  # position of x-coordinate
        posx = 40  
    elif row == 2:
        posx = width / 3 + 40
    elif row == 3:
        posx = width / 3 * 2 + 40

    if col == 1:  # position of y-coordinate
        posy = 40
    elif col == 2:
        posy = height / 3 + 40
    elif col == 3:
        posy = height / 3 * 2 + 40

    TTT[row - 1][col - 1] = XO

    if XO == 'x':
        screen.blit(x_img, (posy, posx))  # displays image of x at the given particular coordinate
        XO = 'o'
    else:
        screen.blit(o_img, (posy, posx))  # displays image of o at the given particular coordinate
        XO = 'x'
    pg.display.update()


def userClick():
    # get coordinates of mouse click
    x, y = pg.mouse.get_pos()

    # get column of mouse click (1-3)
    if x < width / 3:
        col = 1
    elif x < width / 3 * 2:
        col = 2
    elif x < width:
        col = 3
    else:
        col = None

    # get row of mouse click (1-3)
    if y < height / 3:
        row = 1
    elif y < height / 3 * 2:
        row = 2
    elif y < height:
        row = 3
    else:
        row = None

    if row and col and TTT[row - 1][col - 1] is None:
        global XO

        # draw the x or o on screen
        drawXO(row, col)
        check_win()


def reset_game():  # reseting the game
    global TTT, winner, XO, draw
    time.sleep(2)
    XO = 'x'
    draw = False
    winner = None 
    TTT = [[None] * 3, [None] * 3, [None] * 3]  
    game_opening()


game_opening()

# run the game loop forever
while True:
    for event in pg.event.get():
        if event.type == QUIT:
            pg.quit()
            sys.exit()
        elif event.type == MOUSEBUTTONDOWN:
            # the user clicked; place an X or O
            userClick()
            if winner or draw:
                reset_game()

    pg.display.update()
    CLOCK.tick(fps)
