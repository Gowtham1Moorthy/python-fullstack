import random

def deslugify(slug):
    # Split the slug on hyphens, capitalize the first letter of each word, and join them back together
    words = slug.split('-')
    deslugified_name = ' '.join(word.capitalize() for word in words)
    return deslugified_name

def randomize_numbers(input_number):
    #checks if value is a two digit number
    if not (1 <= input_number <= 99):
        raise ValueError("Input Number must be a two-digit number.")
    
    #This generates the two random digits
    digit1 = random.randint(0,6)
    digit2 = random.randint(0,9)

    randomized_number = digit1 * 10 + digit2

    return randomized_number