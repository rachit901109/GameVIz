import random
EASY_BOARD, EASY_MINES = (9,9), 10
MEDIUM_BOARD, MEDIUM_MINES = (16,16), 40
HARD_BOARD, HARD_MINES = (16,30), 99
DIRECTIONS = [(0,1), (0,-1), (1,0), (-1,0), (1,1), (-1,-1), (1,-1), (-1,1)]

def get_cell(position, column):
    return (position//column, position%column)

class Minesweeper():
    """
    Minesweeper game representation
    """
    def __init__(self, board, mines=8):

        # Set initial width, height, and number of mines
        self.height = board[0]
        self.width = board[1]
        self.mines = set()
        self.all_cells = set([get_cell(i, self.width) for i in range(self.height*self.width)])

        # Initialize an empty field with no mines
        self.board = [[False for _ in range(self.width)] for _ in range(self.height)]

        # Add mines randomly
        random_cells = random.sample(list(self.all_cells), mines)
        for cell in random_cells:
            self.mines.add(cell)
            self.board[cell[0]][cell[1]] = True

        # At first, player has found no mines
        self.mines_found = set()

    def print_board(self):
        """
        Prints a text-based representation
        of where mines are located.
        """
        for i in range(self.height):
            print("---" * (self.width))
            for j in range(self.width):
                if self.board[i][j]:
                    print("|X ", end="")
                else:
                    count_mines = self.nearby_mines((i,j))
                    print(f"|{count_mines} ", end="")
            print("|")
        print("---" * (self.width))

    def is_mine(self, cell):
        i, j = cell[0], cell[1]
        return self.board[i][j]

    def nearby_mines(self, cell):
        """
        Returns the number of mines that are
        within one row and column of a given cell,
        not including the cell itself.
        """

        # Keep count of nearby mines
        count = 0

        # Loop over all cells within one row and column
        for i in range(cell[0] - 1, cell[0] + 2):
            for j in range(cell[1] - 1, cell[1] + 2):

                # Ignore the cell itself
                if (i, j) == cell:
                    continue

                # Update count if cell in bounds and is mine
                if 0 <= i < self.height and 0 <= j < self.width:
                    if self.board[i][j]:
                        count += 1

        return count

    def won(self):
        """
        Checks if all mines have been flagged.
        """
        return self.mines_found == self.mines


class Sentence():
    """
    Logical statement about a Minesweeper game
    A sentence consists of a set of board cells,
    and a count of the number of those cells which are mines.
    """

    def __init__(self, cells, count):
        self.cells = set(cells)
        self.count = count

    def __eq__(self, other):
        return self.cells == other.cells and self.count == other.count

    def __str__(self):
        return f"{self.cells} = {self.count}"

    def known_mines(self):
        """
        Returns the set of all cells in self.cells known to be mines.
        """
        # if count of cell (non-zero) is equal to no. of surrounding cell, then all of them must be mines
        if len(self.cells) == self.count and self.count!=0:
            print(f"Mine found at: {self.cells}")
            return self.cells
        return set()

    def known_safes(self):
        """
        Returns the set of all cells in self.cells known to be safe.
        """
        # if cell count is 0 all surrounding cells are safe
        if self.count == 0:
            print(f"Safe cells at: {self.cells}")
            return self.cells
        return set()

    def mark_mine_sent(self, cell):
        """
        Updates internal knowledge representation given the fact that
        a cell is known to be a mine.
        """
        # if a cell is marked as mine we remove it from our set of cells and decrease the count
        print(f"marking mine at {cell} in all sentences")
        if cell in self.cells:
            # print(f"Marked mine at cell: {cell}")
            # print(f"Before removing mine: {self}")
            self.cells.remove(cell)
            self.count = max(0, self.count-1)
            # print(f"After removing mine: {self}")

    def mark_safe_sent(self, cell):
        """
        Updates internal knowledge representation given the fact that
        a cell is known to be safe.
        """
        # if cell is known to be safe we remove it from set of cell and do not decrease the count
        print(f"removing safe cell {cell} from sentences")
        if cell in self.cells:
            # print(f"Safe cell marked at: {cell}")
            # print(f"Before removing safe cell: {self}")
            self.cells.remove(cell)
            # print(f"After removing safe cell: {self}")


class MinesweeperAI():
    """
    Minesweeper game player
    """

    def __init__(self, board):

        # Set initial height and width
        self.height = board[0]
        self.width = board[1]
        self.all_cells = set([get_cell(i, self.width) for i in range(self.height*self.width)])

        # Keep track of which cells have been clicked on
        self.moves_made = set()

        # Keep track of cells known to be safe or mines
        self.mines = set()
        self.safes = set()

        # List of sentences about the game known to be true
        self.knowledge = []

    def isvalid(self, i, j):
        if i>=0 and i<self.height and j>=0 and j<self.width:
            return True
        return False
    
    def draw_known_board(self, game):
        for i in range(self.height):
            print("---" * (self.width))
            for j in range(self.width):
                if (i,j) in self.moves_made:
                    count_mines = game.nearby_mines((i,j))
                    print(f"|{count_mines} ", end="")
                elif (i,j) in self.mines:
                    print("|F ", end="")
                else:
                    print("|  ", end="")
            print("|")
        print("---" * (self.width))
        
    def mark_mine_ai(self, cell):
        """
        Marks a cell as a mine, and updates all knowledge
        to mark that cell as a mine as well.
        """
        self.mines.add(cell)
        for sentence in self.knowledge:
            sentence.mark_mine_sent(cell)

    def mark_safe_ai(self, cell):
        """
        Marks a cell as safe, and updates all knowledge
        to mark that cell as safe as well.
        """
        self.safes.add(cell)
        for sentence in self.knowledge:
            sentence.mark_safe_sent(cell)

    def add_knowledge(self, cell, count):
        """
        Called when the Minesweeper board tells us, for a given
        safe cell, how many neighboring cells have mines in them.

        This function should:
            1) mark the cell as a move that has been made
            2) mark the cell as safe
            3) add a new sentence to the AI's knowledge base
               based on the value of `cell` and `count`
            4) mark any additional cells as safe or as mines
               if it can be concluded based on the AI's knowledge base
            5) add any new sentences to the AI's knowledge base
               if they can be inferred from existing knowledge
        """
        self.moves_made.add(cell)
        self.mark_safe_ai(cell)

        set_cells = set()
        # add new sentence
        for dir in DIRECTIONS:
            row = cell[0]+dir[0]
            col = cell[1]+dir[1]

            if self.isvalid(row, col):
                if (row,col) in self.mines:
                    count = max(0, count-1)
                elif (row,col) not in self.safes:
                    set_cells.add((row, col))

        new_sent = Sentence(set_cells, count)
        print(f"New sentence added at cell:{cell}--> {new_sent}")            
        self.knowledge.append(new_sent)

        # Iteratively update the knowledge base and infer new sentences based on existing sentences in the knowledge base
        update_knowlege = True
        while update_knowlege:
            update_knowlege = False

            safe_cells = set()
            mine_cells = set()
            # make set of safe cells and mines
            for sent in self.knowledge:
                safe_cells = safe_cells.union(sent.known_safes())
                mine_cells = mine_cells.union(sent.known_mines())
            # if found safe cells and mines mark them
            if safe_cells:
                update_knowlege = True
                print("getting true in safe cells")
                for cell in safe_cells:
                    self.mark_safe_ai(cell)
            if mine_cells:
                update_knowlege = True
                print("getting true in mine cells")
                for mine in mine_cells:
                    self.mark_mine_ai(mine)

            # remove empty sentences from knowledge base
            empty = Sentence(set(),0)
            self.knowledge[:] = [x for x in self.knowledge if x!= empty]

            # infer new sentences from existing knowledge base
            for sent1 in self.knowledge:
                for sent2 in self.knowledge:
                    if sent1!=sent2 and sent1.cells.issubset(sent2.cells):
                        new_sent = Sentence(sent2.cells-sent1.cells, max(0,sent2.count-sent1.count))
                        if len(new_sent.cells) == 0:
                            print("cell length 0 encountered")
                            return 
                        if new_sent not in self.knowledge:
                            update_knowlege = True
                            print("getting true in new sent")
                            self.knowledge.append(new_sent)
                            print(f"New sentence infered: {new_sent} from {sent1} and {sent2}")

        print(f"known mines: {self.mines}\nknown safe cells remaining: {self.safes-self.moves_made}")
        print("printing knowledge base:-")
        print('-'*20)
        for sent in self.knowledge:
            print(sent)
        print('-'*20)

    def make_safe_move(self):
        """
        Returns a safe cell to choose on the Minesweeper board.
        The move must be known to be safe, and not already a move
        that has been made.

        This function may use the knowledge in self.mines, self.safes
        and self.moves_made, but should not modify any of those values.
        """
        safe_moves = self.safes - self.moves_made
        if safe_moves:
            rand_safe_move = random.choice(list(safe_moves))
            print(f"Making random safe move:\nSafe moves: {safe_moves}\nRandom safe move choosen: {rand_safe_move}")
            return rand_safe_move
        return None

    def make_random_move(self):
        """
        Returns a move to make on the Minesweeper board.
        Should choose randomly among cells that:
            1) have not already been chosen, and
            2) are not known to be mines
        """
        remain_cells = list(self.all_cells - self.moves_made - self.mines)
        if remain_cells:
            rand_cell = random.choice(remain_cells)
            print(f"Random choosen cell: {rand_cell}")
            return rand_cell
        return None
        

if __name__ == '__main__':
    game = Minesweeper(MEDIUM_BOARD, MEDIUM_MINES)
    ai = MinesweeperAI(MEDIUM_BOARD)
    print(f"Initial Board:")
    game.print_board()
    print(game.mines, ai.safes, sep='\n')

    while True:
        # input("press enter to make next move...")

        ai_move = ai.make_safe_move()
        if ai_move is None:
            print("ai making random move")
            ai_move = ai.make_random_move()
        else:
            print("ai making safe move")
        
        if game.is_mine(ai_move):
            print(f"ai clicked a mine at cell: {ai_move}")
            break
        else:
            ai.add_knowledge(ai_move, game.nearby_mines(ai_move))
            ai.draw_known_board(game)

        if len(game.mines) == len(ai.mines):
            ai_move = ai.make_safe_move()
            while ai_move is not None:
                # print('found it')
                ai.add_knowledge(ai_move, game.nearby_mines(ai_move))
                ai.draw_known_board(game)
                ai_move = ai.make_safe_move()
            print(f"ai won")
            break