def algebraic_to_array_form(position):
    '''
    converts algebraic notation e.g H2 to the notation used in the program e.g. (6,7)
    :param position: STRING. position in algebraic notation
    :return: TUPLE of 2 INT
    '''
    col_part=position[0].lower()
    row_part=int(position[1])
    if col_part=="a":
        c=0
    elif col_part=="b":
        c=1
    elif col_part=="c":
        c=2
    elif col_part=="d":
        c=3
    elif col_part=="e":
        c=4
    elif col_part=="f":
        c=5
    elif col_part=="g":
        c=6
    elif col_part=="h":
        c=7
    r=(8-row_part)
    return (r,c)

def array_to_algebraic_form(position):
    '''
    convert from notation  used in the program to algebraic notation   e.g. H1
    :param position: TUPLE of 2 INT. Position in the format used in the program
    :return: STRING. Position if algebraic notation
    '''
    alpha="abcdefgh"
    row=position[0]
    col=position[1]
    al_col=alpha[col]
    al_row=8-row
    return f'{al_col}{al_row}'

def get_square_coordinates(START_OF_CELLS,SQUARE_LENGTH):
    '''
    returns the coordinates of each square ((top left), (top right), (bottom right),(bottom left)) on the board
    Used to draw onto the eight squares and identify which square has been clicked on. This function has been used once
    and then the output was explicitly assigned to a variabel so that the function doesn't have to be used again unless
    the board or its dimensions change
    :param START_OF_CELLS: TUPLE of 2 INT. x,y coordinates of the top left corner of the first square on the board.
    i.e. (0,0) or A8
    :param SQUARE_LENGTH: INT. Length of each square of the board
    :return: 8x8 ARRAY of 4x2 ARRAY of INT
    '''
    row = 0
    col = 0
    square_coordinates = [[[], [], [], [], [], [], [], []],
                          [[], [], [], [], [], [], [], []],
                          [[], [], [], [], [], [], [], []],
                          [[], [], [], [], [], [], [], []],
                          [[], [], [], [], [], [], [], []],
                          [[], [], [], [], [], [], [], []],
                          [[], [], [], [], [], [], [], []],
                          [[], [], [], [], [], [], [], []], ]
    end = False
    while not end:
        t_l = (START_OF_CELLS[0] + SQUARE_LENGTH * col, START_OF_CELLS[1] + SQUARE_LENGTH * row)
        t_r = (START_OF_CELLS[0] + SQUARE_LENGTH * (col + 1), START_OF_CELLS[1] + SQUARE_LENGTH * row)
        b_r = (START_OF_CELLS[0] + SQUARE_LENGTH * (col + 1), START_OF_CELLS[1] + SQUARE_LENGTH * (row + 1))
        b_l = (START_OF_CELLS[0] + SQUARE_LENGTH * (col), START_OF_CELLS[1] + SQUARE_LENGTH * (row + 1))
        square_coordinates[row][col] = [t_l, t_r, b_r, b_l]

        if col == 7 and row == 7:
            end = True
        elif col == 7:
            col = 0
            row += 1
        else:
            col += 1
    return square_coordinates