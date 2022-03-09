import os
import sys
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), os.getcwd())))

import context
from context import discs

def test_pdga_sql_get_discs():
    pdga_sql = discs.PdgaSql()
    results = pdga_sql.get_discs()
    assert len(results) != 0

def test_pdga_sql_search_manufacturer():
    pdga_sql = discs.PdgaSql()
    results = pdga_sql.search_manufacturer("Innova")
    assert len(results) != 0
