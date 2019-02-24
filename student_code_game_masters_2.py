from game_master import GameMaster
from read import *
from util import *
import read

class TowerOfHanoiGame(GameMaster):

    def __init__(self):
        super().__init__()
        
    def produceMovableQuery(self):
        """
        See overridden parent class method for more information.

        Returns:
             A Fact object that could be used to query the currently available moves
        """
        return parse_input('fact: (movable ?disk ?init ?target)')

    def getGameState(self):
        """
        Returns a representation of the game in the current state.
        The output should be a Tuple of three Tuples. Each inner tuple should
        represent a peg, and its content the disks on the peg. Disks
        should be represented by integers, with the smallest disk
        represented by 1, and the second smallest 2, etc.

        Within each inner Tuple, the integers should be sorted in ascending order,
        indicating the smallest disk stacked on top of the larger ones.

        For example, the output should adopt the following format:
        ((1,2,5),(),(3, 4))

        Returns:
            A Tuple of Tuples that represent the game state
        """
        ### student code goes here

        # ask what ?x is on peg1, peg2, peg3 currently
        on_peg_1 = self.checkOnPeg("peg1")
        on_peg_2 = self.checkOnPeg("peg2")
        on_peg_3 = self.checkOnPeg("peg3")

        return tuple(on_peg_1),tuple(on_peg_2),tuple(on_peg_3)


    def checkOnPeg (self, check_peg):
        what_on_peg = self.kb.kb_ask(Fact(("on ?x "+check_peg).split()))
        on_check_peg = []

        if what_on_peg == False:
            pass

        else:
            for d in what_on_peg:
                disk = d.bindings[0].constant.element
                disk_num = int(disk[-1])
                on_check_peg.append(disk_num)
            on_check_peg.sort()
        return on_check_peg

    def makeMove(self, movable_statement):
        """
        Takes a MOVABLE statement and makes the corresponding move. This will
        result in a change of the game state, and therefore requires updating
        the KB in the Game Master.

        The statement should come directly from the result of the MOVABLE query
        issued to the KB, in the following format:
        (movable disk1 peg1 peg3)

        Args:
            movable_statement: A Statement object that contains one of the currently viable moves

        Returns:
            None
        """
        ### Student code goes here
        target_peg = movable_statement.terms[2].term.element
        from_peg = movable_statement.terms[1].term.element
        disks_on_target_peg = self.checkOnPeg(target_peg)[0]
        disks_on_from_peg = self.checkOnPeg(from_peg)[0]

        new_on = read.parse_input("fact: (on " + str(disks_on_target_peg) + " " + str(target_peg))
        old_on = read.parse_input("fact: (on " + str(disks_on_from_peg )+ " " +str(from_peg))
        new_top = read.parse_input("fact: (top " + str(disks_on_target_peg) + " " + str(target_peg))
        old_top = read.parse_input("fact: (top " + str(disks_on_from_peg) + " " + str(from_peg))
        new_empty = read.parse_input("fact: (empty " + str(target_peg))
        old_empty = read.parse_input("fact: (empty " + str(from_peg))

        self.kb.kb_assert(new_on)
        self.kb.kb_assert(new_top)
        self.kb.kb_retract(old_on)
        self.kb.kb_retract(old_top)

        if len(disks_on_target_peg)==0:
            # new peg update
            self.kb.kb_retract(new_empty)
            # old peg update
        if len(disks_on_from_peg) == 1:
            self.kb.kb_assert(old_empty)

    def reverseMove(self, movable_statement):
        """
        See overridden parent class method for more information.

        Args:
            movable_statement: A Statement object that contains one of the previously viable moves

        Returns:
            None
        """
        pred = movable_statement.predicate
        sl = movable_statement.terms
        newList = [pred, sl[0], sl[2], sl[1]]
        self.makeMove(Statement(newList))

class Puzzle8Game(GameMaster):

    def __init__(self):
        super().__init__()

    def produceMovableQuery(self):
        """
        Create the Fact object that could be used to query
        the KB of the presently available moves. This function
        is called once per game.

        Returns:
             A Fact object that could be used to query the currently available moves
        """
        return parse_input('fact: (movable ?piece ?initX ?initY ?targetX ?targetY)')

    def getGameState(self):
        """
        Returns a representation of the the game board in the current state.
        The output should be a Tuple of Three Tuples. Each inner tuple should
        represent a row of tiles on the board. Each tile should be represented
        with an integer; the empty space should be represented with -1.

        For example, the output should adopt the following format:
        ((1, 2, 3), (4, 5, 6), (7, 8, -1))

        Returns:
            A Tuple of Tuples that represent the game state
        """
        ### Student code goes here
        bindings_lst = self.kb.kb_ask(Fact("coordinate ?x pos1 pos1".split()))
        num1 = bindings_lst[0].bindings[0].constant.element
        bindings_lst = self.kb.kb_ask(Fact("coordinate ?x pos2 pos1".split()))
        num2 = bindings_lst[0].bindings[0].constant.element
        bindings_lst = self.kb.kb_ask(Fact("coordinate ?x pos3 pos1".split()))
        num3 = bindings_lst[0].bindings[0].constant.element
        bindings_lst = self.kb.kb_ask(Fact("coordinate ?x pos1 pos2".split()))
        num4 = bindings_lst[0].bindings[0].constant.element
        bindings_lst = self.kb.kb_ask(Fact("coordinate ?x pos2 pos2".split()))
        num5 = bindings_lst[0].bindings[0].constant.element
        bindings_lst = self.kb.kb_ask(Fact("coordinate ?x pos3 pos2".split()))
        num6 = bindings_lst[0].bindings[0].constant.element
        bindings_lst = self.kb.kb_ask(Fact("coordinate ?x pos1 pos3".split()))
        num7 = bindings_lst[0].bindings[0].constant.element
        bindings_lst = self.kb.kb_ask(Fact("coordinate ?x pos2 pos3".split()))
        num8 = bindings_lst[0].bindings[0].constant.element
        bindings_lst = self.kb.kb_ask(Fact("coordinate ?x pos3 pos3".split()))
        num9 = bindings_lst[0].bindings[0].constant.element

        tuple =((int(num1),int(num2),int(num3)),
                (int(num4),int(num5),int(num6)),
                (int(num7),int(num8),int(num9)))

        return tuple




    def makeMove(self, movable_statement):
        """
        Takes a MOVABLE statement and makes the corresponding move. This will
        result in a change of the game state, and therefore requires updating
        the KB in the Game Master.

        The statement should come directly from the result of the MOVABLE query
        issued to the KB, in the following format:
        (movable tile3 pos1 pos3 pos2 pos3)

        Args:
            movable_statement: A Statement object that contains one of the currently viable moves

        Returns:
            None
        """
        ### Student code goes here
        # pass

        terms = movable_statement.terms

        to_tile_new = Fact(["coordinate", terms[0],terms[3],terms[4]])
        to_tile_empty = Fact(["coordinate", "-1", terms[1],terms[2]])
        self.kb.kb_assert(to_tile_new)
        self.kb.kb_assert(to_tile_empty)

        from_tile_old = Fact(["coordinate", terms[0],terms[1],terms[2]])
        from_tile_empty = Fact(["coordinate", "-1",terms[3],terms[4]])
        self.kb.kb_retract(from_tile_old)
        self.kb.kb_retract(from_tile_empty)



    def reverseMove(self, movable_statement):
        """
        See overridden parent class method for more information.

        Args:
            movable_statement: A Statement object that contains one of the previously viable moves

        Returns:
            None
        """
        pred = movable_statement.predicate
        sl = movable_statement.terms
        newList = [pred, sl[0], sl[3], sl[4], sl[1], sl[2]]
        self.makeMove(Statement(newList))
