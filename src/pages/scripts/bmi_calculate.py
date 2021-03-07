from math import pow

def calculate_BMI(weight: float, height: float) -> float:
    """
    calculate_BMI calculates the BMI of the user.

    :param weight: the weight of the user in kilograms
    :param height: the height of the user in meters
    :return: the output for the body mass index calculated by the formula below
                Weight(kg) / Height(m)^2
    """
    # Validating that the height and weight are not negative numbers
    if (weight < 0 or height < 0):
        return -1
    if(height > 3):
        return -1
    # Rounding the result to 2 decimal places
    return round((weight / pow(height, 2)), 2)

def calculate_Imperial_BMI(weight: float, height: float) -> float:
    """
    calculate_BMI calculates the BMI of the user based on pounds and inches.

    :param weight: the weight of the user in pounds
    :param height: the height of the user in inches
    :return: the output for the body mass index calculated by the formula below
                [Weight(lbs) / Height(inches)^2] * 703
    """
    # Validating that the height and weight are not negative numbers
    if (weight < 0 or height < 0):
        return -1

    # Rounding the result to 2 decimal places
    return round(((weight / pow(height, 2)) * 703), 2)
