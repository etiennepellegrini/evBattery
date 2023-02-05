
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

import evBattery
#
# Place all imports before here.
# ======================================================================

stats = evBattery.vehicle()
print(stats)

with jsonlines.open("../data/car_stats.jsonl", mode="a") as writer:
    writer.write(stats)
