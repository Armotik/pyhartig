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
if [ -z "$GITLAB_TOKEN" ]; then
    echo "Error: GITLAB_TOKEN is not set in .env file"
    exit 1
fi

if [ -z "$GITLAB_PROJECT_ID" ]; then
    echo "Error: GITLAB_PROJECT_ID is not set in .env file"
    exit 1
fi

if [ -z "$GITLAB_URL" ]; then
    echo "Error: GITLAB_URL is not set in .env file"
    exit 1
fi

# Create data directory if it doesn't exist
DATA_DIR="$SCRIPT_DIR/data"
mkdir -p "$DATA_DIR"

# Output file
OUTPUT_FILE="$DATA_DIR/gitlab_issues.json"
STDERR_FILE="$DATA_DIR/error.log"

# Make the API request
echo "Fetching GitLab issues from project $GITLAB_PROJECT_ID..."
echo "Output file: $OUTPUT_FILE"

# Fetch the data
RESPONSE=$(curl -s -L \
    -H "PRIVATE-TOKEN: $GITLAB_TOKEN" \
    "$GITLAB_URL/api/v4/projects/$GITLAB_PROJECT_ID/issues" 2>"$STDERR_FILE")

# Save the response
echo "$RESPONSE" > "$OUTPUT_FILE"

# Check if the request was successful
if [ $? -eq 0 ]; then
    echo "✓ GitLab issues saved successfully to $OUTPUT_FILE"
else
    echo "✗ Error fetching GitLab issues. Check $STDERR_FILE for details."
    exit 1
fi
