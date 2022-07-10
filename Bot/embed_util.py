from numpy import diff


def difficulty_color(difficulty: int):
    DIFF_MAPPING = {
        0 : 0x00b8a3,
        1 : 0xffc01e,
        2 : 0xff375f
    }
    return DIFF_MAPPING[difficulty]
