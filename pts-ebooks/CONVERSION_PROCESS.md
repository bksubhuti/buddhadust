# Buddhist Sutta Epub Conversion Process (v2.0 to v1.x Style)

This document outlines the workflow for updating Buddhist sutta epub content from the latest website versions (v2.0) while preserving legacy epub styling and Table of Contents (TOC) compatibility.

## Overview

The goal is to take raw HTML files from [buddhadust.net](https://buddhadust.net), which are optimized for web browsing, and transform them into XHTML files suitable for Sigil-based epub generation. Crucially, we must preserve specific `id` attributes (`sigil_toc_id_X`) used by existing `TOC.xhtml` files to prevent breaking links in the ebook.

## Workflow Steps

### 1. Data Acquisition
Download the content using `wget`. Ensure you exclude navigation-heavy directories like `frontmatter`, `backmatter`, and `abhi`.

```bash
mkdir -p [nikaya]/src/v2.0
cd [nikaya]/src/v2.0
wget -m -np -R "index.html*" -nH --cut-dirs=4 https://buddhadust.net/dhamma-vinaya/pts/[nikaya]/ \
--exclude-directories="/dhamma-vinaya/pts/[nikaya]/abhi,/dhamma-vinaya/pts/[nikaya]/backmatter,/dhamma-vinaya/pts/[nikaya]/frontmatter"
```

Flatten the directory structure immediately after download:

```bash
find . -mindepth 2 -type f -exec mv {} . \;
find . -mindepth 1 -type d -delete
```

### 2. ID Harvesting
Legacy epubs (v1.x) contain `sigil_toc_id_X` attributes in their headers. Since filenames usually match between versions, we harvest these IDs from the old source.

- **Source**: `[nikaya]/src/v1.x/`
- **Output**: A JSON mapping of `filename -> list of {tag, id, title, text}`.
- **Script**: Use a specialized script (e.g., `sn/harvest_sn_ids.py`) that captures `h1-h4` tags and their associated `id` and `title` attributes.

### 3. Transformation & Refactoring
Run a custom Python script (e.g., `sn/match_sn_v1x_style.py`) to process the v2.0 files.

#### Key Refactoring Rules:
- **Normalization**:
    - Convert Pali characters: `ɱ` -> `ṁ`, `ŋ` -> `ṅ`.
    - Standardize tags: `<br />` -> `<br/>`.
    - Enforce XHTML 1.1 Doctype and Namespace.
- **Cleanup**:
    - Strip web navigation, search boxes, and masthead images.
    - Remove copyright paragraphs and translation cross-links (often found in `f3` or `f4` spans).
    - Remove brackets from footnote numbers: `<sup>[1]</sup>` -> `<sup>1</sup>`.
- **Header Logic**:
    - **Pali Headers**: Usually kept as `h4` with `class="sigil_not_in_toc"`.
    - **Hierarchy Splitting**: v2.0 often bundles "Book > Chapter > Vagga" into one `h4`. These must be split into separate `h1`, `h2`, and `h3` tags.
    - **ID Injection**: Match the text of the new headers against the harvested JSON data to inject the correct `id="sigil_toc_id_X"` and `title="..."` attributes.
    - **Sutta Titles**: Demote `h1` Sutta titles to `h2 class="sigil_not_in_toc"`.
- **Styling**:
    - Convert `f1` spans to `f3` (standardized note style).
    - Normalize "Thus Have I Heard": Use the specific casing and bolding found in the legacy version (e.g., `T<span class="f2"><b>HUS</b></span>` -> `<span class="f2"><b>THUS</b></span>`).

### 4. Verification
- Compare a processed file against its v1.x counterpart to ensure the header IDs match exactly.
- Verify that generic text links are removed but footnote links (`#n1`, `#fn1`) are preserved.
- Use `detailed_diff.py` (if available) to check content similarity and ensure no actual sutta text was lost.

## Nikaya-Specific Notes

- **MN**: Standard hierarchy is `h1` (Number. English) and `h2` (Pali).
- **AN**: Book titles are promoted to `h1`, Chapters to `h2`, and Sutta ranges to `h3`.
- **SN**: Follows a complex hierarchy; often requires splitting a multi-line English header block into `h1/h2/h3`.

## Directory Structure Convention
- `src/v1.x`: Reference files with legacy IDs and styles.
- `src/v2.0`: Raw content downloaded from the website.
- `src/epub_v2_styled_[nikaya]`: Final processed files ready for epub creation.
