# display some sort of count so the player knows how many more incorrect guesses he/she has before the game ends. 
# You should also display which correct letters have already been chosen (and their position in the word, e.g. _ r o g r a _ _ i n g) and 
# which incorrect letters have already been chosen.

# June 18, 2019
# Alex Gallagher

# Add function to guess word
# Keep track of score for self
# Play again function

def play_game()
    puts "Starting Game..."
    filename = "6desk.txt"

    # Randomly select a word between 5 and 12 characters long for the secret word.
    def rand_line(file, min, max)
        words = File.readlines(file)
        suitable = Array.new()
        
        words.each do |word|
            if word.length >= min && word.length <= max
                suitable.push(word)
            end
        end
        rand_word = suitable[rand(0..suitable.length)].chomp.upcase
    end

    puts "\nShortest Word Length: "
    usermin = gets.chomp.to_i

    puts "Longest Word Length: "
    usermax = gets.chomp.to_i

    secret_word = rand_line(filename, usermin, usermax)
    puts "\nSECRET WORD: #{secret_word}\n"

    # Global Variables
    number_right = 0

    guessed = Array.new()
    guessed_right = Array.new()

    hidden_word = "_"*secret_word.length
    win = false

    uniq_chars = secret_word.chars.uniq

    # Difficulty
    puts "\nPlease choose your difficulty: Easy, Medium, Hard, Expert"
    answer = gets.chomp.upcase
    # Avoid typos by only grabbing first two letters
    case answer[0..1]
    when "EA"
        guesses = secret_word.length + 8
    when "ME"
        guesses = secret_word.length + 6
    when "HA"
        guesses = secret_word.length + 4
    when "EX"
        guesses = secret_word.length + 2
    else
        # Default = MEDIUM
        guesses = secret_word.length + 6
    end

    puts "Secret word has #{secret_word.length} letters (#{uniq_chars.length} unique)"

    while guesses > 0 && win == false
        puts "\nSECRET WORD: #{hidden_word}"
        puts "\tGuessed: #{guessed.join(", ")}"
        puts "\tGuessed Right: #{guessed_right.join("-")}"
        puts "\tGuesses Remaining: #{guesses}"

        puts "\nGuess a letter: "
        guessed_letter = gets.strip().upcase
        
        # Check if guess has been guessed
        if guessed.include?(guessed_letter) == false 
            
            # Check if guess is in word
            if secret_word.include?guessed_letter
                puts "\t#{guessed_letter} is in the secret word!"
                guessed_right.push(guessed_letter)
                number_right += 1

                # Update hidden word with guessed letter
                chars = secret_word.split('')
                chars.each_with_index {|c, i|
                    if c == guessed_letter
                        hidden_word[i] = c
                    end
                }
            else
                puts "\t#{guessed_letter} is wrong. HA."
            end

            guessed.push(guessed_letter)
            guesses -= 1

            # Check for Win 
            if number_right == uniq_chars.length
                puts "\nWINNER!"
                puts "You Guessed the secret word! --> #{secret_word}\n"
                win = true
            else
                if guesses == 0
                    puts "\nNo more guesses left. You lose.\nGame Over --> The word was: '#{secret_word}'\n"
                end
            end
        else
            puts "#{guessed_letter} has already been guessed!"
        end
    end
end

play_game

# Play again?
puts "Would you like to play again? (Y/N)"
play_again = gets.chomp.upcase
if play_again == "Y"
    play_game
else
    puts "Adios, amigo."
end
