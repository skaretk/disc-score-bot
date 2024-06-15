import sys
from pathlib import Path
from context import discs
from pdga.pdgaapproveddiscssql import PdgaSql
sys.path.insert(0, str(Path().cwd()))

def test_pdga_sql_get_discs():
    pdga_sql = PdgaSql()
    results = pdga_sql.get_discs()
    assert len(results) != 0

def test_pdga_sql_search_manufacturer():
    pdga_sql = PdgaSql()
    results = pdga_sql.search_manufacturer("Innova")
    assert len(results) != 0
