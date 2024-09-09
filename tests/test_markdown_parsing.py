import pytest
import re

from redact.parse import process_markdown_file
from redact.errors import MarkdownParsingError


def test_output_simple():
    test_data = [
        "some text\n",
        "<!-- $SOLUTION_START -->\n",
        "remove me\n",
        "<!-- $SOLUTION_END -->\n",
        "some more text",
    ]
    test_output = "some text\nsome more text"

    assert process_markdown_file(test_data) == test_output


def test_output_indent():
    test_data = [
        "some text\n",
        "    <!-- $SOLUTION_START -->\n",
        "    remove me\n",
        "    <!-- $SOLUTION_END -->\n",
        "some more text",
    ]
    test_output = "some text\nsome more text"

    assert process_markdown_file(test_data) == test_output


def test_out_of_order():
    test_data_double_start = [
        "<!-- $SOLUTION_START -->\n",
        "<!-- $SOLUTION_START -->\n",
    ]
    match = re.escape(
        "Error in file `None`, at line 2: Encountered `<!-- $SOLUTION_START -->` without closing the previous block with `<!-- $SOLUTION_END -->`."
    )
    with pytest.raises(MarkdownParsingError, match=match):
        process_markdown_file(test_data_double_start)

    test_data_double_end = [
        "<!-- $SOLUTION_START -->\n",
        "<!-- $SOLUTION_END -->\n",
        "<!-- $SOLUTION_END -->\n",
    ]
    match = re.escape(
        "Error in file `None`, at line 3: Encountered `<!-- $SOLUTION_END -->` without closing the previous block with `<!-- $SOLUTION_START -->`."
    )
    with pytest.raises(MarkdownParsingError, match=match):
        process_markdown_file(test_data_double_end)


def test_end_as_first():
    test_data = [
        "<!-- $SOLUTION_END -->\n",
    ]
    match = re.escape(
        "Error in file `None`, at line 1: Encountered `<!-- $SOLUTION_END -->` without closing the previous block with `<!-- $SOLUTION_START -->`."
    )
    with pytest.raises(MarkdownParsingError, match=match):
        process_markdown_file(test_data)


def test_odd_pairs():
    test_data_odd_pairs = [
        "<!-- $SOLUTION_START -->\n",
        "<!-- $SOLUTION_END -->\n",
        "<!-- $SOLUTION_START -->\n",
    ]
    match = re.escape(
        "Error in file `None`: Unbalanced `<!-- $SOLUTION_START -->` and `<!-- $SOLUTION_END -->` tags."
    )
    with pytest.raises(MarkdownParsingError, match=match):
        process_markdown_file(test_data_odd_pairs)


def test_start_indent():
    test_data = [
        "<!-- $SOLUTION_START -->\n",
        "    this is some text\n",
        "   <!-- $SOLUTION_END -->\n",
    ]
    match = re.escape(
        "Error in file `None`, at line 2: Indentation mismatch after `<-- $SOLUTION_START -->`.\n"
        "Expected 0 spaces but found 4."
    )
    with pytest.raises(MarkdownParsingError, match=match):
        process_markdown_file(test_data)


def test_end_indent():
    test_data = [
        "    <!-- $SOLUTION_START -->\n",
        "    this is some text\n",
        "<!-- $SOLUTION_END -->\n",
    ]
    match = re.escape(
        "Error in file `None`, at line 3: Indentation mismatch before `<-- $SOLUTION_END -->`.\n"
        "Expected 4 spaces but found 0."
    )
    with pytest.raises(MarkdownParsingError, match=match):
        process_markdown_file(test_data)


def test_imbalance():
    test_data = [
        "<!-- $SOLUTION_START -->",
        "<!-- $SOLUTION_END -->",
        "<!-- $SOLUTION_START -->",
    ]
    match = re.escape(
        "Error in file `None`: Unbalanced `<!-- $SOLUTION_START -->` and `<!-- $SOLUTION_END -->` tags."
    )

    with pytest.raises(MarkdownParsingError, match=match):
        process_markdown_file(test_data)
