def calculate_reward_for_corridor(lower: int, upper: int, perfect: int, number: float) -> float:
    if number < lower or number > upper:
        result = -1
    #else:
    #    result = 1
    else:
        if number == perfect:
            result = 1
        elif number < perfect:
            result = (number - lower) / (perfect - lower)
        else:
            result = (upper-number) / (upper - perfect)
    return result


def calculate_roofed_reward(power_output: float) -> float:
    if power_output >= 700:
        result = 700 / power_output
    else:
        result = power_output / 700
    return result
