def deslugify(slug):
    # Split the slug on hyphens, capitalize the first letter of each word, and join them back together
    words = slug.split('-')
    deslugified_name = ' '.join(word.capitalize() for word in words)
    return deslugified_name