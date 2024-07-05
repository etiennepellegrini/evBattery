# ======================================================================
#
# Section 392 Navigation and Mission Design
#
# Copyright (C) 2021, California Institute of Technology.
# U.S. Government Sponsorship under NASA Contract NAS7-03001 is acknowledged.
#
# ======================================================================

""" placeholder Docstring."""

__version__ = '0.1'
__author__ = 'Etienne Pellegrini (392M)'

# ======================================================================
# Place all imports after here.
#
import jsonlines
import matplotlib.dates as mdates
import matplotlib.pyplot as plt

#
# Place all imports before here.
# ======================================================================

# ----------------------------------------------------------------------
# Read data
# ----------------------------------------------------------------------

stats = {}

with jsonlines.open("../data/car_stats.jsonl", mode="r") as reader:
    for line in reader:
        for key in line.keys():
            stats[key] = stats.get(key, []) + [line[key]]

# --- Post-process dates
date_num = []
for date in stats["date"]:
    date_num.append(mdates.datestr2num(date))

stats["date_num"] = date_num

# ----------------------------------------------------------------------
# Plots
# ----------------------------------------------------------------------
def plot(x, y):

    # Ensure compatible lengths
    if len(x) > len(y):
        x = x[-len(y):]
    elif len(x) < len(y):
        y = y[-len(x):]

    # Create fig
    fig, ax = plt.subplots()

    # Plot
    ax.plot(x, y)
    ax.xaxis.set_major_locator(mdates.MonthLocator(bymonth=(1, 7)))
    ax.xaxis.set_minor_locator(mdates.MonthLocator())

    plt.tight_layout()


# ----------------------------------------------------------------------
plot(stats["date_num"], stats["max_range"])
plot(stats["date_num"], stats["odometer"])

plt.show()
