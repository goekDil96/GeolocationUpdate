# -*- coding: utf-8 -*-

# GeolocationUpdate
# -----------------
# Know your limits! (created by auxilium)
#
# Author:   Dilara Goeksu
# Version:  0.1, copyright Wednesday, 01 December 2021
# Website:  https://github.com/Dilara Goeksu/Geolocation
# License:  Apache License 2.0 (see LICENSE file)


import logging
from .getconfig import get_config as _get_config
from . import getlimit # noqa F401
# import os
# import sys

# -*- coding: utf-8 -*-

# Geolocation
# -----------
# Know your limits! (created by auxilium)
#
# Author:   Dilara Goeksu
# Version:  0.1, copyright Wednesday, 27 October 2021
# Website:  https://github.com/Dilara Goeksu/Geolocation
# License:  Apache License 2.0 (see LICENSE file)

logging.getLogger(__name__).addHandler(logging.NullHandler())

__doc__ = 'Know your limits! (created by auxilium)'
__license__ = 'Apache License 2.0'


__author__ = 'Dilara Goeksu'
__email__ = 'dilara.goeksu@stud.h-da.de'
__url__ = 'https://github.com/Dilara Goeksu/Geolocation'

__date__ = 'Wednesday, 01 December 2021'
__version__ = '0.1'
__dev_status__ = '3 - Alpha'  # '4 - Beta'  or '5 - Production/Stable'

__dependencies__ = 'numpy',
__dependency_links__ = 'https://limits.pythonanywhere.com/limits.zip',
__data__ = ()
__scripts__ = ()
__theme__ = ''

# this is just an example to demonstrate the auxilium workflow


path_to_getlimit_file = _get_config()["path_to_getlimit_file"]
