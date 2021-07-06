def average_repeats(repeats):

    """Average the repeat readings of volume taken during the experiment"""

    return sum(repeats) / len(repeats)

def make_cumulative_series(x):

    """Find the cumulative totals of a series, useful for graph plotting"""

    cumulative_totals = []
    sum_x = 0 
    for i in x:
        sum_x += i 
        cumulative_totals.append(sum_x)

    return cumulative_totals


