#!/bin/bash
set -e

if [ -z "$1" ]; then
    echo "Usage: $0 <input_path>"
    exit 1
fi

INPUT_PATH="$1"
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
    typst compile --input=jsonPath="$json_file" ./main.typ "$pdf_file"
done
rm -r $TYPST_JSON_PATH
cd ..

echo "All PDFs generated in $PDF_OUTPUT"