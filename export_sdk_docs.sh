#!/bin/bash
# Script to generate SDK documentation for the svml Python package using pdoc
# Edit this script to change output format, location, or options

# Set output directory (edit as needed)
OUTPUT_DIR="docs"

# Ensure output directory exists
mkdir -p "$OUTPUT_DIR"

# Generate Markdown documentation using the Python script
python export_sdk_docs.py

# Uncomment below to generate HTML docs instead
# pdoc svml --html --output-dir "$OUTPUT_DIR"

# Print completion message
echo "SDK documentation generated at $OUTPUT_DIR/svml.md" 