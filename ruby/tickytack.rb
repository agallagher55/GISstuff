# TIC TAC TOE
# Build a tic-tac-toe game on the command line where two human players can play against each other and the board is displayed in between turns.

# Think about how you would set up the different elements within the game… What should be a class? 
# Instance variable? Method? A few minutes of thought can save you from wasting an hour of coding.

# Build your game, taking care to not share information between classes any more than you have to.

# Get input from user1, add input to board, show board, get input from user2

# Classes
# Player, Board

class Player
    def initialize(team)
        @team = team
    end

    def make_move(position)
        
    end
end

class Board
    @@spaces = Hash.new(['A1', 'A2', 'A3', 'B1', 'B2', 'B3', 'C1', 'C2', 'C3'])
    @@spaces.default = ' '
    @@spaces['A1'] = 'X'

    def initialize
        puts " #{@@spaces['A1']}| #{}| #{}\n========\n  #{}| #{}|\n========\n  #{}| #{}| #{}"
    end
end

Board.new