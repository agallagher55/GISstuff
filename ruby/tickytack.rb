# TIC TAC TOE
# Build a tic-tac-toe game on the command line where two human players can play against each other and the game is displayed in between turns.

# Think about how you would set up the different elements within the game… What should be a class? 
# Instance variable? Method? A few minutes of thought can save you from wasting an hour of coding.

# Build your game, taking care to not share information between classes any more than you have to.

# Get input from user1, add input to game, show game, get input from user2

# Classes
# Player, game

class Player
    def initialize(team)
        @team = team
    end

    def make_move(position) 
    end
end

class Game
    attr_accessor :spaces, :board

    def initialize
        puts "\nNew Game!"

        self.spaces = Hash.new(['A1', 'A2', 'A3', 'B1', 'B2', 'B3', 'C1', 'C2', 'C3'])
        self.spaces.default = ' '

        self.board = " #{spaces['A1']}| #{spaces['A2']}| #{spaces['A3']}\n========\n #{spaces['B1']}| #{spaces['B2']}| #{spaces['B3']}\n========\n #{spaces['C1']}| #{spaces['C2']}| #{spaces['C3']}"
        puts self.board
    end

    def show
        puts "\nSHOW FUNCTION"
        puts self.board
    end

    def make_move(team, position) 
        puts "\nMAKE_MOVE FUNCTION"
        puts "\n", spaces[position] = team
        puts "'#{team}' at #{position}"
        puts self.board
        return spaces[position] = team
    end
end

game1 = Game.new
game1.make_move('X', 'A1')
game1.show()

