def clean_string(string):
    string = ''.join(letter for letter in string if letter.isalnum())
    string = string.lower()

    return string


def remove_spaces_string(string):
    string = string.replace(" ", "_")
    string = string.replace("-", "_")
    string = string.lower()

    return string


def clean_string_heading(string):
    string = ' '.join(letter for letter in string if letter.isalnum())
    string = string.title()

    return string


def title_rc(string):
    string = string.replace("_and_", " & ")
    string = string.replace("_", " ")
    string = string.title()

    return string
