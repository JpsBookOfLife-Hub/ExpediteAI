# PowerShell script to run the application with virtual environment
# Usage: .\run.ps1 [provider] [model]
# Example: .\run.ps1 openai
# Example: .\run.ps1 anthropic claude-3-5-haiku-20241022
param(
    [string]$Provider = "",
    [string]$Model = ""
)

.\venv\Scripts\Activate.ps1

if ($Provider -eq "") {
    python main.py
} elseif ($Model -eq "") {
    python main.py --provider $Provider
} else {
    python main.py --provider $Provider --model $Model
}

