'''My Test'''

import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from CV import check_files, extract_mvs

def test_check_files():
    '''Test that get_num function works '''
    assert check_files(['test.jpg', 'test.csv']) == False
    assert check_files(['test.xlsx', 'test.csv']) == True

def test_extract_rpm():
    assert extract_mvs('G_P_KOH40.0032gL_DMAB0.0475gL_20mVs_CV.xlsx') == '20mVs'