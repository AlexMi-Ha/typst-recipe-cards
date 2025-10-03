# Typst Recipe Cards

A streamlined solution to convert cooking recipes stored in an Obsidian vault (Markdown) into neatly formatted, printable PDF cards for your recipe box.

This project automates parsing, data extraction, and PDF generation using **Python** and **Typst**, making it easy to transform your digital recipes into tangible, organized recipe cards.

## Prerequisites

Before building your recipe collection, ensure the following:
- Recipes Structure: All recipes must be stored in a single parent folder within your Obsidian vault.
- Recipe Format: Each recipe file **MUST** follow the [recipe template](./docs/templates/recipe-template.md)
- Dependencies:
    - [Python 3](https://www.python.org/)
    - [Typst](https://github.com/typst/typst)


## Installation

1. Clone this repository:
```bash
git clone https://github.com/AlexMi-Ha/typst-recipe-cards.git
cd typst-recipe-cards
```
2. Ensure Pyhon and Typst are installed
3. Make the build script executable (if needed):
```bash
chmod +x ./build.sh
```

## Usage

Run the build script with the path to your recipe vault:
```bash
./build.sh <PATH-TO-YOUR-RECIPE-VAULT-FOLDER>
```

The script performs the following steps:

1. **Scan Vault**: Searches your specified folder for recipe files, identified by an invisible marker in the last line.
2. **Parse Recipes**: Converts the Markdown recipes into structured JSON data.
3. **Generate PDF**: Uses Typst to transform the JSON data into a printable PDF with cut-out recipe cards.

## Output

Generated PDF files are saved to `./out/pdf`
