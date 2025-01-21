def check_number(value):
    if not value:
        return False

    result = all([char in "0123456789" for char in value]) and len(value) == 11
    return result


NULLABLE = {
    "blank": "True",
    "null": "True"
}