#!/bin/bash
set -e

# Default format
FORMAT="cards"

# Parse arguments
while [[ $# -gt 0 ]]; do
    case "$1" in
        -h|--help)
            echo "typst-recipe-cards:"
            echo "Usage: $0 [-f cards|a5] <input_path>"
            exit 1
            ;;
        -f|--format)
            FORMAT="$2"
            shift 2
            ;;
        -*)
            echo "Unknown option: $1"
            echo "Usage: $0 [-f cards|a5] <input_path>"
            exit 1
            ;;
        *)
            INPUT_PATH="$1"
            shift
            ;;
    esac
done

# Check required input path
if [ -z "$INPUT_PATH" ]; then
    echo "Usage: $0 [-f cards|a5] <input_path>"
    exit 1
fi

# Validate format
if [[ "$FORMAT" != "cards" && "$FORMAT" != "a5" ]]; then
    echo "Error: format must be either 'cards' or 'a5'"
    exit 1
fi

JSON_OUTPUT="./out/json"
PDF_OUTPUT="./out/pdf"

TYPST_JSON_PATH="./data"

mkdir -p "$JSON_OUTPUT"
mkdir -p "$PDF_OUTPUT"
mkdir -p "./typst/$TYPST_JSON_PATH"
rm -f $JSON_OUTPUT/*.json
rm -f $PDF_OUTPUT/*.pdf
rm -f ./typst/$TYPST_JSON_PATH/*.json

python3 ./scripts/mapper.py -i "$INPUT_PATH" -o "$JSON_OUTPUT"

cp $JSON_OUTPUT/*.json ./typst/$TYPST_JSON_PATH/

cd ./typst

for json_file in "$TYPST_JSON_PATH"/*.json; do
    filename=$(basename "$json_file" .json)    
    pdf_file="../$PDF_OUTPUT/$filename.pdf"
    echo $json_file
    typst compile \
        --input=jsonPath="$json_file" \
        --input=format="$FORMAT" \
        ./main.typ "$pdf_file"
done
rm -r $TYPST_JSON_PATH
cd ..

echo "All PDFs generated in $PDF_OUTPUT"