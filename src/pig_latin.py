import re


def pig_latin(text):
    def convert_word(word):
        # Handle words with internal digits or special characters
        if re.search(r"[0-9]", word):
            return word + "way"
        # Check if the word starts with a vowel
        if re.match(r"^[aeiou]", word, re.I):
            return word + "way"
        else:
            # Extract the initial consonants and the rest of the word
            match = re.match(r"^([^aeiou]+)(.*)", word, re.I)
            if match:
                # Special case for words like "myth"
                if not re.search(r"[aeiou]", match.group(2), re.I):
                    return word + "ay"
                return match.group(2) + match.group(1) + "ay"
            return word + "ay"

    def preserve_capitalization(original, transformed):
        if original.istitle():
            return transformed.capitalize()
        elif original.isupper():
            return transformed.upper()
        return transformed

    def process_hyphenated(word):
        parts = word.split("-")
        transformed_parts = [
            preserve_capitalization(part, convert_word(part)) for part in parts
        ]
        return "-".join(transformed_parts)

    def process_contraction(word):
        parts = word.split("'")
        if len(parts) > 1:
            converted_part = convert_word(parts[0])
            transformed_contraction = (
                preserve_capitalization(parts[0], converted_part) + "'" + parts[1]
            )
            return transformed_contraction
        return word + "ay"

    words = re.findall(r"\b[\w\']+\b|[-.,!?;@\s]+", text)
    result = []

    for word in words:
        if re.match(r"\b[\w\']+\b", word):
            if "-" in word:
                result.append(process_hyphenated(word))
            elif "'" in word:
                result.append(process_contraction(word))
            else:
                result.append(preserve_capitalization(word, convert_word(word)))
        else:
            result.append(word)

    return "".join(result)


# Ensure to run this function with the pytest framework to verify corrections have been implemented properly.
