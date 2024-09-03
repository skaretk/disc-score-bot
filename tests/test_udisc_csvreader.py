import datetime
import pytest
import sys
from pathlib import Path
from context import score
from score.udisc.udisc_csv_reader import UdiscCsvReader
from score.udisc.udisc_csv_types import UdiscCsvTypes
from score.udisc.udisc_scorecard import UdiscScorecard
from score.udisc.udisc_scorecard_old import UdiscScoreCardOld
from score.udisc.udisc_competition_scorecard import UdiscScoreCardCompetition
sys.path.insert(0, str(Path().cwd()))

SCORECARD_OLD_DATA = """PlayerName,CourseName,LayoutName,Date,Total,+/-,Hole1,Hole2,Hole3,Hole4,Hole5,Hole6,Hole7,Hole8,Hole9,Hole10,Hole11,Hole12,Hole13,Hole14,Hole15,Hole16,Hole17,Hole18
Par,Krokhol Disc Golf Course,Krokhol Gold Layout 2022,2022-01-01 23:59,60,,3,3,3,3,3,4,3,3,4,4,3,4,3,3,4,3,4,3
Player 1,Krokhol Disc Golf Course,Krokhol Gold Layout 2022,2022-01-01 23:59,94,34,4,6,6,6,5,7,4,7,5,5,7,6,5,4,5,3,5,4
Player 2,Krokhol Disc Golf Course,Krokhol Gold Layout 2022,2022-01-01 23:59,72,12,2,5,3,5,5,6,3,4,5,5,3,4,3,3,4,4,4,4
Player 3,Krokhol Disc Golf Course,Krokhol Gold Layout 2022,2022-01-01 23:597,83,23,4,5,4,5,5,6,4,3,5,4,6,5,4,5,7,2,5,4"""

SCORECARD_DATA = """PlayerName,CourseName,LayoutName,StartDate,EndDate,Total,+/-,RoundRating,Hole1,Hole2,Hole3,Hole4,Hole5,Hole6,Hole7,Hole8,Hole9,Hole10,Hole11,Hole12
Par,Bikkjestykket,Høst 2023,2024-06-16 1322,2024-06-16 1432,36,,,3,3,3,3,3,3,3,3,3,3,3,3
Player 1,Bikkjestykket,Høst 2023,2024-06-16 1322,2024-06-16 1432,30,-6,194,3,2,2,2,2,2,2,5,2,2,3,3
Player 2,Bikkjestykket,Høst 2023,2024-06-16 1322,2024-06-16 1432,38,2,138,3,3,2,3,3,3,3,4,3,4,3,4
Player 3,Bikkjestykket,Høst 2023,2024-06-16 1322,2024-06-16 1432,30,-6,194,2,3,2,3,2,2,2,2,3,3,3,3"""

LEAGUE_DATA = """division,position,name,relative_score,total_score,payout,hole_1,hole_2,hole_3,hole_4,hole_5,hole_6,hole_7,hole_8,hole_9,hole_10,hole_11,hole_12
MPO,1,"Man Player 1",-8,28,,3,2,2,2,2,2,3,2,3,2,3,2
MPO,2,"Man Player 2 ",1,37,,3,4,3,3,3,4,3,2,3,3,2,4
FPO,1,"Female Player 1",-6,30,,3,3,2,2,3,2,3,2,2,3,2,3
FPO,2,"Female Player 2",-5,31,,3,2,3,3,3,2,2,2,3,3,3,2
MP40,1,"Master Player 1",-3,33,,2,3,3,4,3,3,2,2,2,3,4,2"""

class CsvFile:
    def __init__(self, name, content):
        self.name = name + ".csv"
        self.content = content

FOLDER_DATA = [CsvFile("scorecard", SCORECARD_DATA),
               CsvFile("scorecard_old", SCORECARD_OLD_DATA),
               CsvFile("league", LEAGUE_DATA)]

def create_file(tmp_path, file_name, content):
    p = tmp_path / file_name
    p.write_text(content, encoding="utf-8")
    return p

@pytest.fixture(name="scorecard_file")
def scorecard_file_fixture(tmp_path: Path):
    return create_file(tmp_path, "2024-06-161322-Bikkjestykket-Hst2023-UDisc.csv", SCORECARD_DATA)

@pytest.fixture(name="scorecard_file_old")
def scorecard_old_file_fixture(tmp_path: Path):
    return create_file(tmp_path, "2022-01-011322-KrokholDiscGolfCourse-KrokholGoldLayout2022-UDisc.csv", SCORECARD_OLD_DATA)

@pytest.fixture(name="scorecard_file_league")
def scorecard_league_file_fixture(tmp_path: Path):
    return create_file(tmp_path, "test-competition_1999-12-31.csv", LEAGUE_DATA)

@pytest.fixture(name="scorecard_folder")
def scorecard_folder_fixture(tmp_path: Path):
    for csv_file in FOLDER_DATA:
        create_file(tmp_path, csv_file.name, csv_file.content)
    return tmp_path

def test_scorecard_folder(scorecard_folder: Path):
    for file in list(scorecard_folder.iterdir()):
        reader = UdiscCsvReader(file)
        assert reader.type in (UdiscCsvTypes.SCORECARD, UdiscCsvTypes.SCORECARD_OLD, UdiscCsvTypes.COMPETITION)

def test_udisc_csv_reader_scorecard_file(tmp_path: Path):
    p = create_file(tmp_path, "2024-06-161322-Bikkjestykket-Hst2023-UDisc.csv", SCORECARD_DATA)
    assert p.read_text(encoding="utf-8") == SCORECARD_DATA
    reader = UdiscCsvReader(p)
    assert reader.type == UdiscCsvTypes.SCORECARD

def test_udisc_csv_reader_old_scorecard(tmp_path: Path):
    p = create_file(tmp_path, "2022-01-011322-KrokholDiscGolfCourse-KrokholGoldLayout2022-UDisc.csv", SCORECARD_OLD_DATA)
    assert p.read_text(encoding="utf-8") == SCORECARD_OLD_DATA
    reader = UdiscCsvReader(p)
    assert reader.type == UdiscCsvTypes.SCORECARD_OLD

def test_udisc_csv_reader_competition(tmp_path: Path):
    p = create_file(tmp_path, "2022-01-011322-SomeLeague-UDisc.csv", LEAGUE_DATA)
    assert p.read_text(encoding="utf-8") == LEAGUE_DATA
    reader = UdiscCsvReader(p)
    assert reader.type == UdiscCsvTypes.COMPETITION

def test_udisc_scorecardreader(scorecard_file):
    reader = UdiscCsvReader(scorecard_file)
    scorecard = reader.parse()

    assert isinstance(scorecard, UdiscScorecard)
    assert scorecard.course.name == "Bikkjestykket"
    assert scorecard.course.url == "" # no course_url in the csv
    assert scorecard.course.layout == "Høst 2023"
    assert scorecard.date_time is not None
    assert scorecard.date_time_end is not None
    assert len(scorecard.divisions) == 1
    assert scorecard.divisions[0] == ""
    assert scorecard.par == 36
    assert len(scorecard.players) == 3
    for player in scorecard.players:
        assert isinstance(player.score, int)
        assert isinstance(player.rating, int)
        assert player.score_cards == 1
    assert len(scorecard.holes) == 12

def test_udisc_scorecardreader_old(scorecard_file_old):
    reader = UdiscCsvReader(scorecard_file_old)
    scorecard = reader.parse()

    assert isinstance(scorecard, UdiscScoreCardOld)
    assert scorecard.course.name == "Krokhol Disc Golf Course"
    assert scorecard.course.url == "" # no course_url in the csv
    assert scorecard.course.layout == "Krokhol Gold Layout 2022"
    assert scorecard.date_time is not None
    assert len(scorecard.divisions) == 1
    assert scorecard.divisions[0] == ""
    assert scorecard.par == 60
    assert len(scorecard.players) == 3
    for player in scorecard.players:
        assert isinstance(player.score, int)
        assert player.score_cards == 1
    assert len(scorecard.holes) == 18

def test_udisc_competition_scorecardreader(scorecard_file_league):
    reader = UdiscCsvReader(scorecard_file_league)
    scorecard = reader.parse()

    assert isinstance(scorecard, UdiscScoreCardCompetition)
    assert scorecard.name == "test-competition"
    assert scorecard.date_time == datetime.datetime(1999,12,31)
    assert scorecard.course.name is None # no coursename in the csv
    assert scorecard.course.url == "" # no course_url in the csv
    assert scorecard.course.layout is None
    assert scorecard.date_time is not None
    assert len(scorecard.divisions) == 3
    assert scorecard.divisions[0] == "MPO"
    assert scorecard.divisions[1] == "FPO"
    assert scorecard.divisions[2] == "MP40"
    assert scorecard.par is None # no par in the csv
    assert len(scorecard.players) == 5
    assert len(scorecard.holes) == 12
