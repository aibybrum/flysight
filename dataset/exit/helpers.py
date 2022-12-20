def closest_value(input_list, input_value):
    difference = lambda input_list : abs(input_list - input_value)
    res = min(input_list, key=difference)
    return res