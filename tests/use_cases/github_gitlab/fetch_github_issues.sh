#!/bin/sh

# Get the directory where the script is located
SCRIPT_DIR=$(dirname "$0")

# Load environment variables from .env file
ENV_FILE="$SCRIPT_DIR/.env"

if [ ! -f "$ENV_FILE" ]; then
    echo "Error: .env file not found at $ENV_FILE"
    exit 1
fi

# Load .env file
. "$ENV_FILE"

# Verify required variables are set
if [ -z "$GITHUB_TOKEN" ]; then
    echo "Error: GITHUB_TOKEN is not set in .env file"
    exit 1
fi

if [ -z "$GITHUB_REPO" ]; then
    echo "Error: GITHUB_REPO is not set in .env file (format: owner/repo)"
    exit 1
fi

# Create data directory if it doesn't exist
DATA_DIR="$SCRIPT_DIR/data"
mkdir -p "$DATA_DIR"

# Output file
OUTPUT_FILE="$DATA_DIR/github_issues.json"
STDERR_FILE="$DATA_DIR/error.log"

# Make the API request
echo "Fetching GitHub issues from $GITHUB_REPO..."
echo "Output file: $OUTPUT_FILE"

# Fetch the data
RESPONSE=$(curl -s -L \
    -H "Accept: application/vnd.github+json" \
    -H "Authorization: Bearer $GITHUB_TOKEN" \
    -H "X-GitHub-Api-Version: 2022-11-28" \
    https://api.github.com/repos/$GITHUB_REPO/issues 2>"$STDERR_FILE")

# Save the response
echo "$RESPONSE" > "$OUTPUT_FILE"

# Check if the request was successful
if [ $? -eq 0 ]; then
    echo "✓ GitHub issues saved successfully to $OUTPUT_FILE"
else
    echo "✗ Error fetching GitHub issues. Check $STDERR_FILE for details."
    exit 1
fi
