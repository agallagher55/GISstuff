
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

secret_word = rand_line(filename, 5, 12).upcase
puts secret_word

# display some sort of count so the player knows how many more incorrect guesses he/she has before the game ends. 
# You should also display which correct letters have already been chosen (and their position in the word, e.g. _ r o g r a _ _ i n g) and 
# which incorrect letters have already been chosen.

guesses = 5
number_right = 0
guessed = Array.new()

uniq_chars = secret_word.chars.uniq
uniq_chars.pop
puts "Unique Chars: #{uniq_chars}"
puts "uniq_chars.length: #{uniq_chars.length}"
puts "Number Right: #{number_right}"

while guesses > 0
    puts "\tGuessed: #{guessed}"
    puts "\tNumber Right: #{number_right}"
    puts "\tGuesses Remaining: #{guesses}"

    puts "\nGuess a letter: "
    guessed_letter = gets.chomp.upcase
    
    # Check if guess is in word
    if guessed.include?(guessed_letter) == false 

        if secret_word.include?guessed_letter
            puts "\t#{guessed_letter} is in the secret word!"
            number_right += 1
        else
            puts "\t#{guessed_letter} is wrong. HA"
        end

        guessed.push(guessed_letter)
        guesses -= 1

        # Check for Win 
        if number_right = uniq_chars.length
            puts "WINNER!"
        else
            puts "\tYou have #{guesses} more guesses"

            if guesses == 0
                puts "Game Over"
            end
        end
    else
        puts "#{guessed_letter} has already been guessed!"
    end

end