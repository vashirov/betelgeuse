# coding=utf-8
"""Tests for :mod:`betelgeuse.parser`."""
import pytest

from betelgeuse import parser


def test_parse_docstring():
    """Check ``parse_docstring`` parser result."""
    docstring = """
    :field1: value1
    :field2: value2
    :field3:
        * item 1
        * item 2
    """
    assert parser.parse_docstring(docstring) == {
        'field1': 'value1',
        'field2': 'value2',
        'field3': '<ul class="simple">\n<li><p>item 1</p></li>\n'
                  '<li><p>item 2</p></li>\n</ul>\n',
    }


@pytest.mark.parametrize('docstring', ('', None))
def test_parse_none_docstring(docstring):
    """Check ``parse_docstring`` returns empty dict on empty input."""
    assert parser.parse_docstring(docstring) == {}


def test_parse_docstring_special_characters():
    """Check ``parse_docstring`` parser result."""
    docstring = """
    Description with an special character like é

    :field1: value with an special character like é
    """
    assert parser.parse_docstring(docstring) == {
        u'field1': u'value with an special character like é',
    }


@pytest.mark.parametrize('string', ('', None))
def test_parse_rst_empty_string(string):
    """Check ``parse_rst`` returns empty string on empty input."""
    assert parser.parse_rst(string) == ''


def test_parse_rst_translator_class():
    """Check if ``parse_rst`` uses a custom translator_class."""
    docstring = """
    :field1: value1
    :field2: value2
    :field3:
    """
    expected = (
        '<main>\n'
        '<blockquote>\n'
        '<table class="field-list simple">\n'
        '<tr><th>field1</th>\n'
        '<td><p>value1</p>\n'
        '</td>\n'
        '</tr>\n'
        '<tr><th>field2</th>\n'
        '<td><p>value2</p>\n'
        '</td>\n'
        '</tr>\n'
        '<tr><th>field3</th>\n'
        '<td><p></p></td>\n'
        '</tr>\n'
        '</table>\n'
        '</blockquote>\n'
        '</main>\n'
    )
    assert parser.parse_rst(
        docstring, parser.TableFieldListTranslator) == expected


def test_parse_rst_special_characters():
    """Check if ``parse_rst`` plays nice with special characters."""
    assert parser.parse_rst(u'String with special character like é') == (
        u'<main>\n'
        u'<p>String with special character like é</p>\n'
        u'</main>\n'
    )
