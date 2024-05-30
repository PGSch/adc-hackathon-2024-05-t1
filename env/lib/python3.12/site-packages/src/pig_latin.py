import re


def pig_latin(text):
    def translate(word):
        vowels = "aeiou"
        if word[0] in vowels:
            return word + "way"
        else:
            consonants = ""
            for letter in word:
                if letter not in vowels:
                    consonants += letter
                else:
                    break
            return word[len(consonants) :] + consonants + "ay"

    def translate_with_punctuation(word):
        match = re.match(r"([a-zA-Z]+)([^a-zA-Z]*)", word)
        if match:
            translated_word = translate(match.group(1)) + match.group(2)
            return translated_word
        return word

    words = text.split()
    translated_words = [translate_with_punctuation(word) for word in words]
    return " ".join(translated_words)


# Unit tests
assert pig_latin("hello") == "ellohay"
assert pig_latin("world") == "orldway"
assert pig_latin("apple") == "appleway"
assert pig_latin("123") == "123"
assert pig_latin("hello world!") == "ellohay orldway!"
