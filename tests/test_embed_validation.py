import logging
import pytest
from nextcord import Embed
from disc_score_bot.utils.embed_validation import (
    validate_embed,
    validate_embed_total_length,
    validate_embed_title,
    validate_embed_description,
    validate_embed_no_of_fields,
    validate_embed_field_names,
    validate_embed_field_value,
    validate_embed_footer,
    validate_embed_author,
)

def generate_string(n: int) -> str:
    """Generate a string with n size"""
    return "x" * n

@pytest.fixture
def valid_embed() -> Embed:
    """Valid embed"""
    e = Embed()
    e.title = "Title"
    e.description = "Valid Description"
    e.color = 0x004899
    e.add_field(name="Valid Field", value="Valid Field Value")
    e.set_footer(text="Valid Footer")
    e.set_author(name="Valid Author")
    return e

def test_valid_embed(valid_embed):
    """Check Valid Embed"""
    assert validate_embed(valid_embed) is True

@pytest.mark.parametrize("length,expected", [(256, True), (257, False)])
def test_embed_title_boundaries(length, expected, caplog):
    """Title boundaries"""
    caplog.set_level(logging.ERROR)
    title = generate_string(length)
    assert validate_embed_title(title) is expected
    if not expected:
        assert "title too long" in caplog.text

def test_embed_title_none():
    """Test embed Title None"""
    assert validate_embed_title(None) is True

@pytest.mark.parametrize("length,expected", [(4096, True), (4097, False)])
def test_embed_description_boundaries(length, expected, caplog):
    """Description"""
    caplog.set_level(logging.ERROR)
    desc = generate_string(length)
    assert validate_embed_description(desc) is expected
    if not expected:
        assert "description too long" in caplog.text

def test_embed_description_none():
    """Test description OK"""
    assert validate_embed_description(None) is True

def test_embed_fields_max():
    """Test max fields"""
    e = Embed()
    for _ in range(25):
        e.add_field(name="n", value="v")
    assert validate_embed_no_of_fields(e.fields) is True

def test_embed_fields_too_many(caplog):
    """Test too many fields"""
    caplog.set_level(logging.ERROR)
    e = Embed()
    for _ in range(26):
        e.add_field(name="n", value="v")
    assert validate_embed_no_of_fields(e.fields) is False
    assert "too many fields!" in caplog.text

@pytest.mark.parametrize("length,expected", [(256, True), (257, False)])
def test_embed_field_name_boundaries(length, expected, caplog):
    """Test embed.field.name boundaries"""
    caplog.set_level(logging.ERROR)
    e = Embed()
    e.add_field(name=generate_string(length), value="ok")
    assert validate_embed_field_names(e.fields) is expected
    if not expected:
        assert "field.name too long" in caplog.text

@pytest.mark.parametrize("length,expected", [(1024, True), (1025, False)])
def test_embed_field_value_boundaries(length, expected, caplog):
    """Test embed.field.value boundaries"""
    caplog.set_level(logging.ERROR)
    e = Embed()
    e.add_field(name="ok", value=generate_string(length))
    assert validate_embed_field_value(e.fields) is expected
    if not expected:
        assert "field.value too long" in caplog.text

def test_embed_footer_ok_when_empty():
    """Test footer not set"""
    e = Embed()
    assert validate_embed_footer(e.footer) is True

@pytest.mark.parametrize("length,expected", [(2048, True), (2049, False)])
def test_embed_footer_boundaries(length, expected, caplog):
    """Test embed.footer boundaries"""
    caplog.set_level(logging.ERROR)
    e = Embed()
    e.set_footer(text=generate_string(length))
    assert validate_embed_footer(e.footer) is expected
    if not expected:
        assert "footer.text too long" in caplog.text

def test_embed_author_empty():
    """Test empty author"""
    e = Embed()
    assert validate_embed_author(e.author) is True

@pytest.mark.parametrize("length,expected", [(256, True), (257, False)])
def test_embed_author_boundaries(length, expected, caplog):
    """Test embed.author.name boundaries"""
    caplog.set_level(logging.ERROR)
    e = Embed()
    e.set_author(name=generate_string(length))
    assert validate_embed_author(e.author) is expected
    if not expected:
        assert "author.name too long" in caplog.text

@pytest.mark.parametrize("total_len,expected", [(6000, True), (6001, False)])
def test_validate_total_length_boundaries(total_len, expected, caplog):
    """Test embed total character boundaries (Discord limit = 6000)"""
    caplog.set_level(logging.ERROR)
    e = Embed(description=generate_string(total_len))
    assert validate_embed_total_length(e) is expected
    if not expected:
        assert "Embed size too long" in caplog.text
    else:
        assert "Embed size too long" not in caplog.text

def test_validate_embed_title_too_long(valid_embed, caplog):
    """Test embed.title too long"""
    caplog.set_level(logging.ERROR)
    valid_embed.title = generate_string(257)
    assert validate_embed(valid_embed) is False
    assert "title too long" in caplog.text

def test_validate_embed_field_value_too_long(valid_embed, caplog):
    """Test embed.field value too long"""
    caplog.set_level(logging.ERROR)
    valid_embed.clear_fields()
    valid_embed.add_field(name="ok", value=generate_string(1025))
    assert validate_embed(valid_embed) is False
    assert "field.value too long" in caplog.text

def test_validate_embed_too_many_fields(valid_embed, caplog):
    """Test embed.fields with too many fields"""
    caplog.set_level(logging.ERROR)
    valid_embed.clear_fields()
    for _ in range(26):
        valid_embed.add_field(name="n", value="v")
    assert validate_embed(valid_embed) is False
    assert "too many fields!" in caplog.text
