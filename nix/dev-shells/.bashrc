SOURCE_DATE_EPOCH=$(date +%s)
if [ -d ".venv" ]; then
    echo "Skipping venv creation, '.venv' already exists"
else
    echo "Creating new venv environment in path: '.venv'"
    uv venv
fi
source ".venv/bin/activate"
uv sync
