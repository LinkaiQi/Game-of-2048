import random

class Game2048:
    #---------------------------------------------------------------------------
    # constructor: initializes the empty grid with 2 "2"s in random tiles
    #---------------------------------------------------------------------------
    def __init__(self, row=4, col=4):
        self.row = row                         # number of rows in grid
        self.col = col                         # number of columns in grid
        self.score = 0                         # initialize the game score

        self.grid=[]                           # initialize the grid with 0s

        # ##### You need here to initialize you matix representing the grid
        for r in range(row):
            a_row = []
            for c in range(col):
                a_row.append(0)
            self.grid.append(a_row)

        # ##### with zeros. Don't forget row lines and col columns

        self.RandomFillTile(2)                 #initialize 2 tiles with a 2
        self.RandomFillTile(2)

    #---------------------------------------------------------------------------
    # generates a 2 or 4 randomly with 3 times more chance to get a 2
    #---------------------------------------------------------------------------
    def random2or4(self):
        if random.random() > 0.90:
            return 4
        else: return 2


    #---------------------------------------------------------------------------
    # retrieving the current score
    #---------------------------------------------------------------------------
    def getScore(self):
        return self.score

    #---------------------------------------------------------------------------
    # adding "new" to the current score
    #---------------------------------------------------------------------------
    def setScore(self, new):
        self.score+=new

    #---------------------------------------------------------------------------
    # Obtaining the number of empty tiles
    #---------------------------------------------------------------------------
    def getNbEmptyTiles(self):
        empty=0

        # ##### You should return the number of tiles that are empty
        for row_n in range(self.row):
            for col_n in range(self.col):
                if self.grid[row_n][col_n] == 0:
                    empty = empty + 1

        #empty_list = self.getListEmptyTiles()
        #return len(empty_list)
        # ##### i.e. they contain zeros.

        return empty

    #---------------------------------------------------------------------------
    # Obtaining the list of empty tiles in a list of pairs (of coordinates i,j)
    #---------------------------------------------------------------------------
    def getListEmptyTiles(self):
        emptyTiles=[]

        # ##### You should return a list of pairs where each pair
        for row_n in range(self.row):
            for col_n in range(self.col):
                if self.grid[row_n][col_n] == 0:
                    emptyTiles.append((row_n, col_n))
        # ##### is the x,y coordinates of a tile that is empty

        return emptyTiles

    #---------------------------------------------------------------------------
    # Selecting a rambom empty tile and filling it with "init"
    #---------------------------------------------------------------------------
    def RandomFillTile(self, init):
        emptyTiles=self.getListEmptyTiles()
        if len(emptyTiles) !=0:
            tile=random.randint(0,len(emptyTiles)-1)
            (i,j)=emptyTiles[tile]
            self.grid[i][j]=init

    #---------------------------------------------------------------------------
    # printing the current game grid, score and number of empty tiles
    #---------------------------------------------------------------------------
    def print(self):
        for row in range(self.row * 2 + 1):
            if row % 2 == 0:
                print("-"*29)
            else:
                row_n = (row // 2)
                print("|",end='')
                for element in self.grid[row_n]:
                    str_l = len(str(element))
                    if element == 0:
                        print(" "*5, "|",end='')
                    else:
                        print(" "*(4-str_l), str(element), "|",end='')
                print("")
        print("Current Score: ", self.score, "|| Empty cells: ",\
         self.getNbEmptyTiles())
        print("-"*37)


    #---------------------------------------------------------------------------
    # check if the grid is collapsible horizontally or vertically
    #---------------------------------------------------------------------------
    def collapsible(self):
        if (self.getNbEmptyTiles() != 0):
            return True
        elif self.isMergeable() == True:
            return True
        collaps=False

        # ##### You should check whether there is a possibility to merge
        # ##### adjacent tiles and assign True to collaps if it is the case


        return collaps

    #---------------------------------------------------------------------------
    # check if the grid contains 2048
    #---------------------------------------------------------------------------
    def win(self):

        # ##### return true is the value 2048 exists in the grid
        # ##### return false otherwise
        for row_n in range(self.row):
            for col_n in range(self.col):
                if self.grid[row_n][col_n] == 2048:
                    return True
        return False

    #---------------------------------------------------------------------------
    # collapses the columns to the left and updates the grid and score
    #---------------------------------------------------------------------------
    def slideLeft(self):
        changed = False                       # indicates if there were tiles that slid
        # shift
        for col in range(self.col-1):
            for row in range(self.row):
                if self.grid[row][col] == 0:
                    for c in range(col+1, self.col):
                        if self.grid[row][c] != 0:
                            self.grid[row][col] = self.grid[row][c]
                            self.grid[row][c] = 0
                            changed = True
                            break

        # merge
        for col in range(0, self.col-1):
            for row in range(self.row):
                if self.grid[row][col] != 0 and self.grid[row][col] == self.grid[row][col+1]:
                    changed = True
                    self.grid[row][col] = self.grid[row][col] * 2
                    self.grid[row][col+1] = 0
                    self.score = self.score + self.grid[row][col]

                    # move the following tiles forward
                    c = col + 1
                    while c < self.col-1:
                        self.grid[row][c] = self.grid[row][c+1]
                        self.grid[row][c+1] = 0
                        c = c + 1


        return changed


    #---------------------------------------------------------------------------
    # collapses the columns to the right and updates the grid and score
    #---------------------------------------------------------------------------
    def slideRight(self):
        changed = False                        # indicates if there were tiles that slid

        self.rotate()
        self.rotate()
        changed = self.slideLeft()
        self.rotate()
        self.rotate()

        return changed


    #---------------------------------------------------------------------------
    # collapses the rows upwards and updates the grid and score
    #---------------------------------------------------------------------------
    def slideUp(self):
        changed = False                        # indicates if there were tiles that slid

        self.rotate()
        self.rotate()
        self.rotate()
        changed = self.slideLeft()
        self.rotate()

        return changed

    #---------------------------------------------------------------------------
    # collapses the rows downwards and updates the grid and score
    #---------------------------------------------------------------------------
    def slideDown(self):
        changed = False                        # indicates if there were tiles that slid

        self.rotate()
        changed = self.slideLeft()
        self.rotate()
        self.rotate()
        self.rotate()

        return changed

    def isMergeable(self):
        Mergeable = False
        for row_n in range(self.row):
            for col_n in range(self.col):
                if col_n < self.col - 1:
                    if self.grid[row_n][col_n] == self.grid[row_n][col_n + 1]:
                        Mergeable = True
                if row_n < self.row - 1:
                    if self.grid[row_n][col_n] == self.grid[row_n + 1][col_n]:
                        Mergeable = True
        return Mergeable

    def rotate(self):
        reversed_grid = list(reversed(self.grid))

        # create a empty list to store the rotated grid
        rotated_grid = []
        for i in range(self.col):
            rotated_grid.append([])
        # rotate
        for row_n in range(self.row):
            for col_n in range(self.col):
                rotated_grid[col_n].append(reversed_grid[row_n][col_n])

        self.grid = rotated_grid
        # swape col_n and row_n
        saved = self.col
        self.col = self.row
        self.row = saved


#-End of Class Game2048---------------------------------------------------------

my_game = Game2048()
# ##### write here your main program to play the game
end_of_game = False
while not end_of_game:
    my_game.print()
    if my_game.win():
        print("Congratulations! You win.")
        end_of_game = True
        break
    if my_game.collapsible() == False:
        print("Sorry! Game Over. You lose.")
        end_of_game = True
        break

    user_in = input()
    if user_in == "a":
        if my_game.slideLeft() == True:
            num = my_game.random2or4()
            my_game.RandomFillTile(num)
    elif user_in == "w":
        if my_game.slideUp() == True:
            num = my_game.random2or4()
            my_game.RandomFillTile(num)
    elif user_in == "s":
        if my_game.slideDown() == True:
            num = my_game.random2or4()
            my_game.RandomFillTile(num)
    elif user_in == "d":
        if my_game.slideRight() == True:
            num = my_game.random2or4()
            my_game.RandomFillTile(num)
    elif user_in == "q":
        end_of_game = True
