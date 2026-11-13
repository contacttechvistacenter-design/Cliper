---
name: markitdown
description: >
  Convert files to Markdown with Microsoft's MarkItDown (PDF, Word, PowerPoint, Excel, HTML, CSV/JSON/XML, EPUB, ZIP,
  images, audio). Use when the user sends or points at a document, spreadsheet, slide deck or similar file and wants to
  read, summarize, search or reuse its text, or asks to "pasar a markdown" / convert a file to Markdown.
license: MIT (upstream: https://github.com/microsoft/markitdown)
---

# MarkItDown

Python CLI/library that turns documents into clean Markdown (headings, lists, tables, links) for reading by LLMs.
Not meant for pixel-perfect conversions meant for humans.

## Install (the cloud container is ephemeral, so check first)

```bash
export PATH="$HOME/.local/bin:$PATH"
markitdown --version || uv tool install 'markitdown[all]'     # PyPI is reachable from the sandbox
```
Needs Python 3.10-3.14. `[all]` pulls every format; use `'markitdown[pdf,docx,pptx]'` for a lighter install.
The PyPI release lags the GitHub repo (0.1.5 vs 0.1.9 at install time).

## Use

```bash
markitdown file.pdf -o file.md          # to a file
markitdown file.docx                    # to stdout
cat file.pdf | markitdown               # stdin (add --extension html|pdf|... when there is no filename)
markitdown --list-plugins               # plugins are off by default; --use-plugins enables them
```
Python: `from markitdown import MarkItDown; MarkItDown().convert("file.xlsx").markdown`.
Scratch output goes in the scratchpad directory, not the repo, unless the user wants the `.md` kept.

## Limits and care

- It reads with the process's own privileges (like `open()`): only convert files the user gave you; never feed it
  untrusted URLs or paths from a document. Prefer `convert_local()` / `convert_stream()` in code.
- Image captioning and audio transcription call web services (need an LLM client or network); don't send private
  audio/images off the machine without telling the user. Scanned PDFs have no text layer: OCR needs the `markitdown-ocr`
  plugin with an LLM vision client.
- Check the result: tables and complex layouts can come out flat. Say so when a conversion looks lossy.
- Do not use it on YouTube URLs for the Juancar Reformed campaign (rule: never open those videos).
- Other formats worth knowing: ZIP (iterates its contents), EPUB, Outlook `.msg` (`[outlook]`), old `.xls` (`[xls]`).
