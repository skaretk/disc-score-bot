import sqlite3
from discs.pdgaapproveddisc import PdgaApprovedDisc

class PdgaSql():
    """Pdga SQL database with approved discs"""
    def __init__(self):
        self.db_name = 'cfg/pdga_approved_discs.db'

    def create_table(self):
        """Create table if not exists"""
        con = sqlite3.connect(self.db_name)
        con.execute("""CREATE TABLE IF NOT EXISTS pdga(
            MANUFACTURER TEXT,
            MODEL TEXT,
            APPROVED TEXT,
            URL TEXT);""")
        con.close()

    def get_discs(self):
        """Get all discs in the database"""
        con = sqlite3.connect(self.db_name)
        cur = con.cursor()
        cur.execute('SELECT * FROM pdga')
        results = cur.fetchall()
        con.close()
        discs = self.parse_results(results)

        return discs

    def search_manufacturer(self, manufacturer):
        """Seach for manufacturer"""
        con = sqlite3.connect(self.db_name)
        cur = con.cursor()
        cur.execute('SELECT * FROM pdga WHERE MANUFACTURER LIKE ?', ('%'+manufacturer+'%',))
        results = cur.fetchall()
        con.close()
        discs = self.parse_results(results)

        return discs

    def add_approved_disc(self, disc):
        """Add new approved disc"""
        sql = """INSERT INTO pdga(MANUFACTURER, MODEL, APPROVED, URL)
            VALUES (?, ?, ?, ?) """
        data = (disc.manufacturer, disc.name, disc.approved_date, disc.url)
        con = sqlite3.connect(self.db_name)
        cur = con.cursor()
        cur.execute(sql, data)
        con.commit()
        con.close()

    def parse_results(self, results):
        """Parse results, return list of discs"""
        discs = []
        for result in results:
            disc = PdgaApprovedDisc()
            disc.manufacturer = result[0]
            disc.name = result[1]
            disc.approved_date = result[2]
            disc.url = result[3]
            discs.append(disc)

        return discs
