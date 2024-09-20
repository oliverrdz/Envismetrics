'''My Test'''

import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from HDV import check_files, rpm_to_rads


def test_rpm_to_rads():
    assert rpm_to_rads(20) - 2.094 < 0.01