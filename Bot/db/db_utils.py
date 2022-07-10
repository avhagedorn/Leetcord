def standardize_difficulty(difficulty):
    mapping = {
        0 : "Easy",
        1 : "Medium",
        2 : "Hard",
        "Easy" : 0,
        "Medium" : 1,
        "Hard" : 2
    }

    return mapping[difficulty]
