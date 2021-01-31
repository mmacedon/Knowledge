import itertools
import random


class Minesweeper():
    """
    Minesweeper game representation
    """

    def __init__(self, height=8, width=8, mines=8):

        # Set initial width, height, and number of mines
        self.height = height
        self.width = width
        self.mines = set()

        # Initialize an empty field with no mines
        self.board = []
        for i in range(self.height):
            row = []
            for j in range(self.width):
                row.append(False)
            self.board.append(row)

        # Add mines randomly
        while len(self.mines) != mines:
            i = random.randrange(height)
            j = random.randrange(width)
            if not self.board[i][j]:
                self.mines.add((i, j))
                self.board[i][j] = True

        # At first, player has found no mines
        self.mines_found = set()

    def print(self):
        """
        Prints a text-based representation
        of where mines are located.
        """
        for i in range(self.height):
            print("--" * self.width + "-")
            for j in range(self.width):
                if self.board[i][j]:
                    print("|X", end="")
                else:
                    print("| ", end="")
            print("|")
        print("--" * self.width + "-")

    def is_mine(self, cell):
        i, j = cell
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
        if len(self.cells) == self.count:
            return self.cells
        else:
            return None

    def known_safes(self):
        """
        Returns the set of all cells in self.cells known to be safe.
        """
        if self.count == 0:
            return self.cells
        else:
            return None

    def mark_mine(self, cell):
        """
        Updates internal knowledge representation given the fact that
        a cell is known to be a mine.
        """
        if cell in self.cells:
            self.cells.remove(cell)
            self.count -= 1

    def mark_safe(self, cell):
        """
        Updates internal knowledge representation given the fact that
        a cell is known to be safe.
        """
        if cell in self.cells:
            self.cells.remove(cell)

class MinesweeperAI():
    """
    Minesweeper game player
    """

    def __init__(self, height=8, width=8):

        # Set initial height and width
        self.height = height
        self.width = width

        # Keep track of which cells have been clicked on
        self.moves_made = set()

        # Keep track of cells known to be safe or mines
        self.mines = set()
        self.safes = set()

        # List of sentences about the game known to be true
        self.knowledge = []

    def mark_mine(self, cell):
        """
        Marks a cell as a mine, and updates all knowledge
        to mark that cell as a mine as well.
        """
        self.mines.add(cell)
        for sentence in self.knowledge:
            sentence.mark_mine(cell)

    def mark_safe(self, cell):
        """
        Marks a cell as safe, and updates all knowledge
        to mark that cell as safe as well.
        """
        self.safes.add(cell)
        for sentence in self.knowledge:
            sentence.mark_safe(cell)

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
        #self.safes.remove(cell)

        cellX = cell[0]
        cellY = cell[1]
        neighboringCells = set()

        for i in range(-1, 2, 1):
            column = cellX + i
            if column < 0 or column > self.width - 1:
                continue
            for j in range(-1, 2, 1):
                row = cellY + j
                if row < 0 or row > self.height - 1:
                    continue
                if (column, row) in self.moves_made:
                    continue
                neighboringCells.add((column, row))

        newSentence = Sentence(neighboringCells, count)
        self.knowledge.append(newSentence)
        #Marking the Cell as Safe

        #Second Form of Interpretation
        #If one set is a subset of another
        if len(self.knowledge) == 0:
            for sentence1 in self.knowledge:
                for sentence2 in self.knowledge:
                    if sentence1.cells == sentence2.cells:
                        continue
                    elif sentence1.cells.issubset(sentence2.cells):
                        #See one is a subset of another
                         if len(sentence2.cells) == sentence2.count and len(sentence1.cells) == sentence1.count:
                             #Sentence1 is a subset of sentence2, and sentence1 == count1 and sentence2 == count2
                             self.knowledge.append(Sentence(sentence2.cells.difference(sentence1.cells), sentence2.count - sentence1.count))

        for sentence in self.knowledge:
            if sentence.count == 0:
                for cell in sentence.cells: self.safes.add(cell)
            elif len(sentence.cells) == sentence.count:
                for cell in sentence.cells: self.mines.add(cell)

        for cell in self.safes:
            self.mark_safe(cell)

        for cell in self.mines:
            self.mark_mine(cell)

    def make_safe_move(self):
        """
        Returns a safe cell to choose on the Minesweeper board.
        The move must be known to be safe, and not already a move
        that has been made.

        This function may use the knowledge in self.mines, self.safes
        and self.moves_made, but should not modify any of those values.
        """
        if len(self.safes) == 0:
            return None

        safe_move = self.safes.pop()
        return safe_move

    def make_random_move(self):
        """
        Returns a move to make on the Minesweeper board.
        Should choose randomly among cells that:
            1) have not already been chosen, and
            2) are not known to be mines
        """
        possibleMoves = 0

        for i in range(self.width):
            for j in range(self.height):
                if (i, j) not in self.moves_made and (i, j) not in self.mines and (i, j) not in self.safes:
                    possibleMoves += 1

        if possibleMoves == 0:
            return None

        move_made = False
        while not move_made:
            randomMoveX = random.randint(0, self.width - 1 )
            randomMoveY = random.randint(0, self.height - 1)
            move = (randomMoveX, randomMoveY)
            if move in self.moves_made or move in self.mines or move in self.safes:
                continue
            else:
                move_made = True

        return move
