# MD Redact

Generic tool to redact markdown files.

Will look for files named `SOLUTION.md` in a target directory and any of it's sub-directories, parse the files, remove blocks wrapped in tags, and create a new markdown file in the same location as the source `SOLUTION.md` file with the name `README.md`.

## Usage

### Source files

In the target file, wrap a block of markdown in commented tags:

```markdown
`<!-- $SOLUTION_START -->`

Markdown text that you want to remove from `SOLUTION.md`

`<!-- $SOLUTION_END -->`
```

### CLI Usage

Use the tool with:

```bash
redact solution path/to/directory/
```

The tool does not accept file paths, only directory paths.


## Notes

Unoptimised, inflexible, uncustomisable,  and written in a hurry.
