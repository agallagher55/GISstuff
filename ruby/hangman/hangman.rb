
puts "Initializing!"
filename = "5desk.txt"

# Randomly select a word between 5 and 12 characters long for the secret word.
def rand_line(file, len1, len2)
    words = File.readlines(file)
    suitable = Array.new()
    
    words.each do |word|
        if word.length > len1 && word.length < len2
            suitable.push(word)
        end
    end

    rand_word = suitable[rand(0..suitable.length)]
end

secret_word = rand_line(filename, 3, 6).upcase.chomp
puts "\nSECRET WORD: #{secret_word}\n"

# display some sort of count so the player knows how many more incorrect guesses he/she has before the game ends. 
# You should also display which correct letters have already been chosen (and their position in the word, e.g. _ r o g r a _ _ i n g) and 
# which incorrect letters have already been chosen.

# Global Variables
guesses = 5
number_right = 0

guessed = Array.new()
guessed_right = Array.new()

hidden_word = "_"*secret_word.length
win = false

uniq_chars = secret_word.chars.uniq
# uniq_chars.pop

puts "Unique Chars: #{uniq_chars}"
puts "Number of Unique Characters: #{uniq_chars.length}"
puts "Secret word has #{secret_word.length} letters"

while guesses > 0 && win == false
    puts "\nSECRET WORD: #{hidden_word}"
    puts "\tGuessed: #{guessed.join(", ")}"
    puts "\tGuessed Right: #{guessed_right.join("-")}"
    puts "\tGuesses Remaining: #{guesses}"

    puts "\nGuess a letter: "
    guessed_letter = gets.chomp.upcase
    
    # Check if guess is in word
    if guessed.include?(guessed_letter) == false 

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
                puts "No more guesses left. You lose.\nGame Over"
            end
        end
    else
        puts "#{guessed_letter} has already been guessed!"
    end
end