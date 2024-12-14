param (
    [string]$path
)

# Check if the virtual environment directory exists
if (-Not (Test-Path .\venv\Scripts\Activate.ps1)) {
    Write-Host "Creating virtual environment..."
    python -m venv venv
}

# Activate the virtual environment
.\venv\Scripts\Activate.ps1

# Install required packages
pip install -r requirements.txt

# Run the Python script and pass the arguments
if ($path) {
    python clean-genres.py -path "$path"
} else {
    Write-Host "No path provided. Running the script without arguments..."
    python clean-genres.py
}

# No need to explicitly deactivate in PowerShell
Write-Host "Script finished. You can close this session to deactivate the virtual environment."
