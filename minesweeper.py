import itertools
import random
import copy


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
        return set()

                

    def known_safes(self):
        """
        Returns the set of all cells in self.cells known to be safe.
        """
        if self.count == 0:
            return self.cells
        return set()


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

        self.mark_safe(cell)
        
        i,j = cell
        neighbours = set()

        for p in range(self.height):
            for q in range(self.width):
                if abs(p-i) <= 1 and abs(q-j) <= 1:
                    neighbours.add((p,q))
        neighbours.remove(cell)
        copied_neighbours = copy.deepcopy(neighbours)
        
        for neighbour in copied_neighbours:
            if neighbour in self.safes:
                neighbours.remove(neighbour)
            elif neighbour in self.mines:
                neighbours.remove(neighbour)
                count -= 1
        new_sentence = Sentence(neighbours, count)
        if new_sentence.cells != set():
            self.knowledge.append(new_sentence)

        #RG - sort the knowledge by sentence length
        #sorted(self.knowledge, key=len(Sentence(cells)))
        #RG....
        
        if len(self.knowledge) != 0:
            #new_knowledge = copy.deepcopy(self.knowledge)
            
            #self.knowledge = []
            #for z in new_knowledge:
                #if z not in self.knowledge:
                    #self.knowledge.append(z)
            
            
            copied_knowledge = copy.deepcopy(self.knowledge)
            copied_knowledge1 = copy.deepcopy(self.knowledge)
            
            for sentence in copied_knowledge1:
                #for x in sentence.known_mines():
                    #self.mark_mine(x)
            
                #for y in sentence.known_safes():
                    #self.mark_safe(y)
                    
                    #RG - compare copied_knowledge with Knowledge
                for sentence1 in copied_knowledge:
                    if len(sentence.cells) > len(sentence1.cells):
                        if sentence1.cells.issubset(sentence.cells) and sentence1.cells != sentence.cells:
                            new_sentence_cells = sentence1.cells.difference(sentence.cells)
                            new_sentence_count = sentence1.count - sentence.count
                            if new_sentence_cells != set():
                                self.knowledge.append(Sentence(new_sentence_cells, new_sentence_count))
                                
                        elif sentence.cells.issubset(sentence1.cells) and sentence1.cells != sentence.cells:
                            new_sentence_cells = sentence.cells.difference(sentence1.cells)
                            new_sentence_count = sentence.count -sentence1.count
                            if new_sentence_cells != set():
                                self.knowledge.append(Sentence(new_sentence_cells, new_sentence_count))
                
                for sentence1 in copied_knowledge:
                    if len(sentence.cells.intersection(sentence1.cells)) != 0:
                        new_sentence_cells = sentence.cells.intersection(sentence1.cells)
                        new_sentence_count = sentence.count
                        #print(" New cells {} ".format(new_sentence_cells))
                        #print("New KB {} " .format(self.knowledge[:].cells))
                        #for sentence2 in self.knowledge:
                            #if new_sentence_cells not in sentence2.cells:
                        self.knowledge.append(Sentence(new_sentence_cells, new_sentence_count))
                                #continue
                
                           
                           
                                                                                     

            
            # for sentence in copied_knowledge:
            #     if len(sentence.cells) < len(copied_knowledge[-1].cells):
            #         if copied_knowledge[-1].cells.issubset(sentence.cells) and copied_knowledge[-1].cells != sentence.cells:
            #             new_sentence_cells = copied_knowledge[-1].cells.difference(sentence.cells)
            #             new_sentence_count = copied_knowledge[-1].count - sentence.count
            #             if new_sentence_cells != set():
            #                 self.knowledge.append(Sentence(new_sentence_cells, new_sentence_count))
                        
                        
                    # elif sentence.cells.issubset(copied_knowledge[-1].cells) and copied_knowledge[-1].cells != sentence.cells:
                    #     new_sentence_cells = sentence.cells.difference(copied_knowledge[-1].cells)
                    #     new_sentence_count = sentence.count -copied_knowledge[-1].count
                    #     if new_sentence_cells != set():
                    #         self.knowledge.append(Sentence(new_sentence_cells, new_sentence_count))
        
        #RG moving logic to add to known_mines and known_safes at the end of adding knowledge logic
        
        new_knowledge = self.knowledge
        self.knowledge = []
        for z in new_knowledge:
            if z not in self.knowledge:
                self.knowledge.append(z)
        
        copied_new_knowledge = copy.deepcopy(self.knowledge)
        
        for sentence in copied_new_knowledge:
            for x in sentence.known_mines():
                self.mark_mine(x)
        
        copied_new_knowledge1 = copy.deepcopy(self.knowledge)
        for sentence in copied_new_knowledge1:
            for y in sentence.known_safes():
                self.mark_safe(y)
        
        
        
        sentences_to_remove = []
        for sentence in self.knowledge:
            if sentence.cells == set():
                sentences_to_remove.append(sentence)
        for sentence in sentences_to_remove:
            self.knowledge.remove(sentence)
        
        print("Number of sentenes in knowledge base: {}".format(len(self.knowledge)))
        print("Number of safe cells: {}".format(self.safes))
        for sentence in self.knowledge:
            print("{} = {}".format(sentence.cells, sentence.count))
            
    def make_safe_move(self):
        """
        Returns a safe cell to choose on the Minesweeper board.
        The move must be known to be safe, and not already a move
        that has been made.

        This function may use the knowledge in self.mines, self.safes
        and self.moves_made, but should not modify any of those values.
        """
        for safecell in self.safes:
            if safecell not in self.moves_made:
                return safecell
        return None

    def make_random_move(self):
        """
        Returns a move to make on the Minesweeper board.
        Should choose randomly among cells that:
            1) have not already been chosen, and
            2) are not known to be mines
        """
        random_moves = []
        
        for row in range(self.height):
            for col in range(self.width):
                if (row,col) not in self.moves_made and (row,col) not in self.mines:
                    random_moves.append((row,col))
        if len(random_moves) > 0:
            return random.choice(random_moves)
        return None
    
    