from pathlib import Path
import pytest
from dotenv import load_dotenv
from disc_score_bot.apis.pdgaapi import PdgaApi

# Load PDGA credentials from cfg/token.env if present
load_dotenv(Path(__file__).resolve().parent.parent / "cfg" / "token.env")


@pytest.fixture(scope="module")
def api():
    """Authenticated PdgaApi session, skipped when credentials are unavailable."""
    pdga = PdgaApi()
    if pdga.login() is None:
        pytest.skip("PDGA credentials not available or rejected")
    yield pdga
    pdga.logout()


def test_pdga_login(api):
    assert api.is_authenticated is True
    assert api.sessid is not None
    assert api.session_name is not None
    assert api.token is not None


def test_pdga_connect(api):
    response = api.connect()
    assert response is not None


def test_pdga_players_by_number(api):
    response = api.players(pdga_number="1") # Steady Ed Headrick
    assert response is not None
    assert response.get("players")
    assert response["players"][0]["last_name"] == "Headrick"


def test_pdga_players_by_name(api):
    response = api.players(last_name="Headrick", limit=5)
    assert response is not None
    assert response.get("players") is not None


def test_pdga_player_statistics(api):
    response = api.player_statistics(year="2020", limit=5)
    assert response is not None
    assert response.get("players") is not None


def test_pdga_events(api):
    response = api.events(tier="NT", start_date="2021-01-01", end_date="2021-12-31", limit=5)
    assert response is not None
    assert response.get("events") is not None


def test_pdga_courses(api):
    response = api.courses(state_prov="VA", limit=5)
    assert response is not None
    assert response.get("courses") is not None


def test_pdga_requires_auth():
    """Unauthenticated calls must not hit the API."""
    pdga = PdgaApi()
    assert pdga.is_authenticated is False
    assert pdga.players(pdga_number="1") is None
    assert pdga.connect() is None
    assert pdga.logout() is None
