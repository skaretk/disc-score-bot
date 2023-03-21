import datetime
from unittest.mock import mock_open, patch
import os
import sys
from context import score
from score.files.udisccsvreader import UdiscCsvReader, UdiscCsvTypes
from score.scorecard_udisc import ScorecardUdisc
from score.scorecard_udisc_competition import ScorecardUdiscCompetition
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), os.getcwd())))

mocked_scorecard = mock_open(read_data="""PlayerName,CourseName,LayoutName,Date,Total,+/-,Hole1,Hole2,Hole3,Hole4,Hole5,Hole6,Hole7,Hole8,Hole9,Hole10,Hole11,Hole12,Hole13,Hole14,Hole15,Hole16,Hole17,Hole18
Par,Krokhol Disc Golf Course,Krokhol Gold Layout 2022,2022-01-01 23:59,60,,3,3,3,3,3,4,3,3,4,4,3,4,3,3,4,3,4,3
Player 1,Krokhol Disc Golf Course,Krokhol Gold Layout 2022,2022-01-01 23:59,94,34,4,6,6,6,5,7,4,7,5,5,7,6,5,4,5,3,5,4
Player 2,Krokhol Disc Golf Course,Krokhol Gold Layout 2022,2022-01-01 23:59,72,12,2,5,3,5,5,6,3,4,5,5,3,4,3,3,4,4,4,4
Player 3,Krokhol Disc Golf Course,Krokhol Gold Layout 2022,2022-01-01 23:597,83,23,4,5,4,5,5,6,4,3,5,4,6,5,4,5,7,2,5,4""")

mocked_league = mock_open(read_data="""division,position,name,relative_score,total_score,payout,hole_1,hole_2,hole_3,hole_4,hole_5,hole_6,hole_7,hole_8,hole_9,hole_10,hole_11,hole_12
MPO,1,"Man Player 1",-8,28,,3,2,2,2,2,2,3,2,3,2,3,2
MPO,2,"Man Player 2 ",1,37,,3,4,3,3,3,4,3,2,3,3,2,4
FPO,1,"Female Player 1",-6,30,,3,3,2,2,3,2,3,2,2,3,2,3
FPO,2,"Female Player 2",-5,31,,3,2,3,3,3,2,2,2,3,3,3,2
MP40,1,"Master Player 1",-3,33,,2,3,3,4,3,3,2,2,2,3,4,2""")

def test_udisc_csv_reader_scorecard():
    with patch('builtins.open', mocked_scorecard):
        reader = UdiscCsvReader("", mocked_scorecard)
        assert reader.type == UdiscCsvTypes.SCORECARD

def test_udisc_csv_reader_competition():
    with patch('builtins.open', mocked_league):
        reader = UdiscCsvReader("", mocked_league)
        assert reader.type == UdiscCsvTypes.COMPETITION

def test_udisc_scorecardreader():
    with patch('builtins.open', mocked_scorecard):
        reader = UdiscCsvReader("", mocked_scorecard)
        scorecard = reader.parse()

    assert isinstance(scorecard, ScorecardUdisc)
    assert scorecard.course.name == "Krokhol Disc Golf Course"
    assert scorecard.course.url == "" # no course_url in the csv
    assert scorecard.course.layout == "Krokhol Gold Layout 2022"
    assert scorecard.date_time is not None
    assert len(scorecard.divisions) == 1
    assert scorecard.divisions[0] == ""
    assert scorecard.par == 60
    assert len(scorecard.players) == 3
    assert len(scorecard.holes) == 18

def test_udisc_competition_scorecardreader():
    with patch('builtins.open', mocked_league):
        reader = UdiscCsvReader("", mocked_league)
        reader.file = "test-competition_1999-12-31"
        scorecard = reader.parse()

    assert isinstance(scorecard, ScorecardUdiscCompetition)
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
