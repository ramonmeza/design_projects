def capitalize_each_word(text: str, delimiter: str = " ") -> str:
    return delimiter.join(x.capitalize() for x in text.split(delimiter))
