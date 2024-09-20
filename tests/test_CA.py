'''My Test'''

import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from CA import get_num

def test_get_num():
    '''Test that get_num function works '''
    assert get_num("(3)PFOA400ppm_75075_50s_CA.xlsx") == 3
