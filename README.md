# MD Redact

Generic tool to redact markdown files.

Will look for files named `SOLUTION.md` in a target directory and any of it's sub-directories OR target file, parse the file(s), remove blocks wrapped in tags, and create a new markdown file in the same location as the source `SOLUTION.md` file with the name `README.md`.

## Usage

### Source files

In the target file, wrap a block of markdown in commented tags:

```
<!-- $SOLUTION_START -->

Markdown text that you want to remove from `SOLUTION.md`

<!-- $SOLUTION_END -->
```

### CLI Usage

Use the tool with:

```bash
redact solution path/to/directory/
```

or
```bash
redact solution path/to/SOLUTION.md
```

### Quality checks

Enforces some quality checks. Will throw an error if a check fails:
- Tags must alternate: start, end, start, end, etc...
- An `end` tag must have the same indentation as a `start` tag
- The line immediately after a `start` tag must have the same indentation. TODO: this should be the next line with text on it.
- An `end` tag must have the same identation level as it's preceding `start` tag.
- There can be no orphan tags: for ever `start` tag, there must be an `end` tag.

## Notes

Unoptimised, inflexible, uncustomisable, and written in a hurry.
