# TIC TAC TOE
# Build a tic-tac-toe game on the command line where two human players can play against each other and the game is displayed in between turns.

# Think about how you would set up the different elements within the game… What should be a class? 
# Instance variable? Method? A few minutes of thought can save you from wasting an hour of coding.

# Build your game, taking care to not share information between classes any more than you have to.

# Classes
# Player, game

class Player
    attr_accessor :team, :number, :wins
    @@count = 0

    def initialize
        puts "Choose your team: "
        self.team = gets.chomp

        @@count += 1
        number = @@count

        wins = 0
    end
end

class Game
    attr_accessor :spaces, :board, :moves

    def initialize
        puts "\nNew Game!"

        self.moves = 0

        self.spaces = Hash.new(['A1', 'A2', 'A3', 'B1', 'B2', 'B3', 'C1', 'C2', 'C3'])
        self.spaces.default = ' '

        self.board = " #{spaces['A1']}| #{spaces['A2']}| #{spaces['A3']}\n========\n #{spaces['B1']}| #{spaces['B2']}| #{spaces['B3']}\n========\n #{spaces['C1']}| #{spaces['C2']}| #{spaces['C3']}"
        puts self.board
    end

    def show
        puts "\n", self.board
    end

    def update_board
        self.board = " #{spaces['A1']}| #{spaces['A2']}| #{spaces['A3']}\n========\n #{spaces['B1']}| #{spaces['B2']}| #{spaces['B3']}\n========\n #{spaces['C1']}| #{spaces['C2']}| #{spaces['C3']}"
    end

    def make_move(team) 
        puts "\n#{team}'s turn! Choose your move: "
        position = gets.chomp.upcase
        valid = false
        
        until valid
            if ["X", "O"].include?(self.spaces[position])
                puts "\t**SORRY, can't go there!"
                puts "\tChoose a new move: "
                position = gets.chomp.upcase
            else
                valid = true
                self.spaces[position] = team
                self.moves += 1
        end

        puts "\n'#{team}' at #{position}"
        puts "Total moves remaining: #{9 - @moves}"
        
        update_board
        show
        end
    end
end

player1 = Player.new
player2 = Player.new
game1 = Game.new

while game1.moves < 9
    game1.make_move(player1.team)
    game1.make_move(player2.team)
end

# game1.make_move('X')
# game1.make_move('O')

## check for win

