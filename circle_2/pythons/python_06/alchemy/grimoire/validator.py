


def validate_ingredients(ingredients: str) -> str:
    valid_words = ["fire", "water", "earth", "air"]

    ingreds = ingredients.lower().split()
    valid = True

    for word in ingreds:
        if word not in valid_words:
            valid = False
            break
    if valid == True:
        return f"{ingredients} - VALID"
    return f"{ingredients} - INVALID"
