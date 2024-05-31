# Implementing the final correction to the pig_latin function based on the detailed description provided above.


def pig_latin(text):
    import string

    vowels = "aeiouAEIOU"
    punctuation = string.punctuation.replace(
        "-", ""
    )  # Exclude hyphen as it will be handled separately
    digits = string.digits

    def translate_word(word):
        # Initial segmentation to separate leading and trailing punctuation and digits
        initial_punct = ""
        while word and (word[0] in punctuation):
            initial_punct += word[0]
            word = word[1:]

        final_punct = ""
        while word and (word[-1] in punctuation):
            final_punct = word[-1] + final_punct
            word = word[:-1]

        if not word:  # Return early if no alphabetic characters are left
            return initial_punct + word + final_punct

        if any(char.isdigit() for char in word):  # Check if any digit is in the word
            return initial_punct + word + final_punct + "way"

        # Check if the word starts with a vowel and translate accordingly
        if word[0] in vowels:
            return initial_punct + word + "way" + final_punct

        # Find the position of the first vowel for consonant handling
        first_vowel_index = len(word)
        for index, char in enumerate(word):
            if char in vowels:
                first_vowel_index = index
                break

        # Handle words that start with consonants
        if first_vowel_index == len(word):  # No vowels in the word
            return initial_punct + word + final_punct + "way"
        else:
            translated = word[first_vowel_index:] + word[:first_vowel_index] + "ay"
            return initial_punct + translated + final_punct

    return " ".join(translate_word(word) for word in text.split())
