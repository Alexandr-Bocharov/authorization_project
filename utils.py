def check_number(value):
    return all([char in "0123456789" for char in value]) and len(value) == 11


NULLABLE = {
    "blank": "True",
    "null": "True"
}