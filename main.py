import pygame
import random
import time
from sprite import *
from settings import *

        

class Game:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption(title)
        self.clock = pygame.time.Clock()
        self.shuffle_time = 0
        self.start_shuffle = False
        self.previous_choice = ""
        self.start_game = False
        self.start_timer = False
        self.elapsed_time = 0
        self.high_score = float(self.get_high_scores()[0])
        self.last_move = ""

    def get_high_scores(self):
        with open("high_score.txt", "r") as file:
            scores = file.read().splitlines()
        return scores

    def save_score(self):
        with open("high_score.txt", "w") as file:
            file.write(str("%.3f\n" % self.high_score))

    def create_game(self):
        grid = [[x + y * GAME_SIZE for x in range(1, GAME_SIZE + 1)] for y in range(GAME_SIZE)]
        grid[-1][-1] = 0
        return grid

    def shuffle(self):
        possible_moves = []
        for row, tiles in enumerate(self.tiles):
            for col, tile in enumerate(tiles):
                if tile.text == "empty":
                    if tile.right():
                        possible_moves.append("right")
                    if tile.left():
                        possible_moves.append("left")
                    if tile.up():
                        possible_moves.append("up")
                    if tile.down():
                        possible_moves.append("down")
                    break
            if len(possible_moves) > 0:
                break

        if self.previous_choice == "right":
            possible_moves.remove("left") if "left" in possible_moves else possible_moves
        elif self.previous_choice == "left":
            possible_moves.remove("right") if "right" in possible_moves else possible_moves
        elif self.previous_choice == "up":
            possible_moves.remove("down") if "down" in possible_moves else possible_moves
        elif self.previous_choice == "down":
            possible_moves.remove("up") if "up" in possible_moves else possible_moves

        choice = random.choice(possible_moves)
        self.previous_choice = choice
        if choice == "right":
            self.tiles_grid[row][col], self.tiles_grid[row][col + 1] = self.tiles_grid[row][col + 1], \
                                                                       self.tiles_grid[row][col]
        elif choice == "left":
            self.tiles_grid[row][col], self.tiles_grid[row][col - 1] = self.tiles_grid[row][col - 1], \
                                                                       self.tiles_grid[row][col]
        elif choice == "up":
            self.tiles_grid[row][col], self.tiles_grid[row - 1][col] = self.tiles_grid[row - 1][col], \
                                                                       self.tiles_grid[row][col]
        elif choice == "down":
            self.tiles_grid[row][col], self.tiles_grid[row + 1][col] = self.tiles_grid[row + 1][col], \
                                                                       self.tiles_grid[row][col]

    def draw_tiles(self):
        self.tiles = []
        for row, x in enumerate(self.tiles_grid):
            self.tiles.append([])
            for col, tile in enumerate(x):
                if tile != 0:
                    self.tiles[row].append(Tile(self, col, row, str(tile)))
                else:
                    self.tiles[row].append(Tile(self, col, row, "empty"))

    def new(self):
        self.all_sprites = pygame.sprite.Group()
        self.tiles_grid = self.create_game()
        self.tiles_grid_completed = self.create_game()
        self.elapsed_time = 0
        self.start_timer = False
        self.start_game = False
        self.buttons_list = []
        self.buttons_list.append(Button(500, 100, 200, 50, "Shuffle", WHITE, BLACK))
        self.buttons_list.append(Button(500, 170, 200, 50, "Reset", WHITE, BLACK))
        self.buttons_list.append(Button(500, 240, 200, 50, "DFS", WHITE, BLACK))
        self.draw_tiles()

    def run(self):
        self.playing = True
        while self.playing:
            self.clock.tick(FPS)
            self.events()
            self.update()
            self.draw()

    def update(self):
        if self.start_game:
            if self.tiles_grid == self.tiles_grid_completed:
                self.start_game = False
                if self.high_score > 0:
                    self.high_score = self.elapsed_time if self.elapsed_time < self.high_score else self.high_score
                else:
                    self.high_score = self.elapsed_time
                self.save_score()

            if self.start_timer:
                self.timer = time.time()
                self.start_timer = False
            self.elapsed_time = time.time() - self.timer

        if self.start_shuffle:
            self.shuffle()
            self.draw_tiles()
            self.shuffle_time += 1
            if self.shuffle_time > 0:
                self.start_shuffle = False
                self.start_game = True
                self.start_timer = True

        self.all_sprites.update()

    def draw_grid(self):
        for row in range(-1, GAME_SIZE * TILESIZE, TILESIZE):
            pygame.draw.line(self.screen, LIGHTGREY, (row, 0), (row, GAME_SIZE * TILESIZE))
        for col in range(-1, GAME_SIZE * TILESIZE, TILESIZE):
            pygame.draw.line(self.screen, LIGHTGREY, (0, col), (GAME_SIZE * TILESIZE, col))

    def draw(self):
        self.screen.fill(BGCOLOUR)
        self.all_sprites.draw(self.screen)
        self.draw_grid()
        for button in self.buttons_list:
            button.draw(self.screen)
        UIElement(550, 35, "%.3f" % self.elapsed_time).draw(self.screen)
        UIElement(430, 300, "High Score - %.3f" % (self.high_score if self.high_score > 0 else 0)).draw(self.screen)
        UIElement(430, 500, "Last move: " + self.last_move).draw(self.screen)
        pygame.display.flip()

    # My functions:
    # def DFS(self, moves, initial_state, lastMove):
    #     if(len(moves) <= DPS_MAX_DEPTH):
    #         curState = initial_state
    #         curMove = ""
    #         while curState != self.tiles_grid_completed:
    #             possibleMoves = self.getSwapableTiles()
    #             random.shuffle(possibleMoves)
    #             for move in possibleMoves:
    #                 cur0Row, cur0Col = self.get0TilePos()
    #                 row, col = self.getTilePos(move)
    #                 curMove = self.swapTilesOnBoard(row, col, curState)
    #                 if(lastMove == curMove):
    #                     self.swapTilesOnBoard(cur0Row, cur0Col, curState)
    #                 else:
    #                     lastMove = curMove
    #                     moves.append(move)
    #                     self.DFS(moves, curState, lastMove)
    #                     if(len(moves) >= 1):
    #                         moves.pop()
    #         return moves
                    
    # def traceBackMoves(self, moves):
    #     # if(len(moves) == 0):
    #     #     UIElement(500, 200, "No solution for DFS").draw(self.screen)
    #     # else:
    #     moves.reverse()
    #     for move in moves:
    #             self.swapTiles(move)
    #             self.draw_tiles()
    #             # time.sleep(1)        
    class Node:
        def __init_(self, state, way):
            self.state = state
            self.way = way

        def isGoal(self):
            grid = [[x + y * GAME_SIZE for x in range(1, GAME_SIZE + 1)] for y in range(GAME_SIZE)]
            grid[-1][-1] = 0
            return self.state == grid
        def 
    def DFS(self, start):
        start_state = self.Node(start, "")
        frontier = [].append(start_state)
        explored = []
        depth = 0
        while(len(frontier) != 0):
            possibleStates = []
            if(frontier[-1].isGoal()):


        

    def moveDown(self, row, col):
        self.tiles_grid[row][col], self.tiles_grid[row + 1][col] = self.tiles_grid[row + 1][col], self.tiles_grid[row][col]

    def moveUp(self, row, col):
        self.tiles_grid[row][col], self.tiles_grid[row - 1][col] = self.tiles_grid[row - 1][col], self.tiles_grid[row][col]

    def moveLeft(self, row, col):
        self.tiles_grid[row][col], self.tiles_grid[row][col - 1] = self.tiles_grid[row][col - 1], self.tiles_grid[row][col]

    def moveRight(self, row, col):
        self.tiles_grid[row][col], self.tiles_grid[row][col + 1] = self.tiles_grid[row][col + 1], self.tiles_grid[row][col]

    def getTilePos(self, search_tile):
            for row, tiles in enumerate(self.tiles):
                for col, tile in enumerate(tiles):
                    if(self.tiles_grid[row][col] == search_tile):
                        return (row, col)
                    
    #Get the blank tile row and col positions
    def get0TilePos(self):
        return self.getTilePos(0)

    def swapTilesOnBoard(self, tileRow, tileCol, board):
        if(self.isSwapable(tileRow, tileCol)):
            blankRow, blankCol = self.get0TilePos()
            tempTile = board[tileRow][tileCol]
            board[tileRow][tileCol] = board[blankRow][blankCol]
            board[blankRow][blankCol] = tempTile
            if(tileRow < blankRow and tileCol == blankCol):
                return "Up"
            elif(tileRow > blankRow and tileCol == blankCol):
                return "Down"
            elif(tileRow == blankRow and tileCol < blankCol):
                return "Left"
            elif(tileRow == blankRow and tileCol > blankCol):
                return "Right"
        return "Invalid"
            
    #Swap a tile with the blank tile
    def swapTiles(self, tileRow, tileCol):
        return self.swapTilesOnBoard(tileRow, tileCol, self.tiles_grid)

    #check if a tile is adjacent to the blank tile (doesn't count diagonal placement)
    def isSwapable(self, tileRow, tileCol):
        for tile in self.getSwapableTiles():
            if(self.tiles_grid[tileRow][tileCol] == tile):
                return True
        return False

    #get all tiles that can be swaped with the blank tile
    def getSwapableTiles(self):
        swapableTiles = []
        blankRow, blankCol = self.get0TilePos()
        if(blankRow > 0):
            swapableTiles.append(self.tiles_grid[blankRow - 1][blankCol])
        if(blankRow < GAME_SIZE - 1):
            swapableTiles.append(self.tiles_grid[blankRow + 1][blankCol])
        if(blankCol > 0):
            swapableTiles.append(self.tiles_grid[blankRow][blankCol - 1])
        if(blankCol < GAME_SIZE - 1):
            swapableTiles.append(self.tiles_grid[blankRow][blankCol + 1])
        return swapableTiles

    

    def events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit(0)

            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_x, mouse_y = pygame.mouse.get_pos()
                for row, tiles in enumerate(self.tiles):
                    for col, tile in enumerate(tiles):
                        if tile.click(mouse_x, mouse_y):
                            if(self.tiles_grid[row][col] != 0):
                                self.last_move = self.swapTiles(row, col)

                            self.draw_tiles()

                for button in self.buttons_list:
                    if button.click(mouse_x, mouse_y):
                        if button.text == "Shuffle":
                            self.shuffle_time = 0
                            self.start_shuffle = True
                            # moves = []
                            # self.DFS(moves, self.tiles_grid, "")
                            # self.traceBackMoves(moves)
                        if button.text == "Reset":
                            self.new()
                        # if button.text == "DFS":
                        #     pass

    
    

game = Game()
while True:
    game.new()
    game.run()
