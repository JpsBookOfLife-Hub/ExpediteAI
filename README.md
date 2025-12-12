# ExpediteAI - Screenshot Question Answerer

A Python desktop application that automatically processes screenshots, uses AI vision APIs to extract and answer questions, and displays results in a minimalistic dark-themed modal overlay.

## Quick Start

```bash
# Clone the repository
git clone https://github.com/JpsBookOfLife-Hub/ExpediteAI.git
cd ExpediteAI

# Install dependencies
pip install -r requirements.txt

# Set up your API key in .env file
# See Setup section below

# Run the application
python main.py --provider openai
```

## Overview

A Python desktop application that processes screenshots, uses AI vision APIs to extract and answer questions, and displays results in a minimalistic dark-themed modal.

## Features

- **Automatic Detection**: Automatically processes screenshots when you take them (Windows Key + Print Screen)
- **Multi-Provider Support**: Works with Gemini, OpenAI GPT-4 Vision, or Anthropic Claude
- **Smart Question Detection**: Automatically identifies questions and provides answers
- **Minimalistic UI**: Dark-themed modal in bottom-left corner
- **Auto-dismiss**: Modal disappears after 5 seconds (10 seconds for errors)
- **Click-through**: Modal doesn't block clicks to windows underneath
- **Billing Alerts**: Notifies you when API credits/billing is low

## Prerequisites

- Python 3.8 or higher
- Windows 10/11
- API key for at least one of the supported providers:
  - Google Gemini API key
  - OpenAI API key
  - Anthropic Claude API key

## Installation

1. Clone or download this repository

2. Create and activate a virtual environment (recommended to avoid conflicts):
```bash
# Create virtual environment
python -m venv venv

# Activate virtual environment
# On Windows PowerShell:
.\venv\Scripts\Activate.ps1
# On Windows CMD:
venv\Scripts\activate.bat
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Set up your API keys and select your model:

### Method 1: .env File (Easiest - Recommended)

Create a file named `.env` in the project directory (same folder as `main.py`) with the following content:

```
# Add your API keys here (you only need one, but can add all three)
GEMINI_API_KEY=your_gemini_api_key_here
OPENAI_API_KEY=your_openai_api_key_here
ANTHROPIC_API_KEY=your_anthropic_api_key_here

# Select which AI provider to use: 'gemini', 'openai', or 'anthropic'
DEFAULT_PROVIDER=openai

# Select specific models (optional - uses defaults if not specified)
# Gemini models: gemini-1.5-flash, gemini-1.5-pro, gemini-pro, gemini-pro-vision
GEMINI_MODEL=gemini-1.5-flash

# OpenAI models: gpt-4o, gpt-4o-mini, gpt-4-turbo, gpt-4-vision-preview
OPENAI_MODEL=gpt-4o

# Anthropic models: claude-3-5-sonnet-20241022, claude-3-5-haiku-20241022, claude-3-opus-20240229, claude-3-sonnet-20240229
ANTHROPIC_MODEL=claude-3-5-sonnet-20241022
```

**To select a provider**, change `DEFAULT_PROVIDER` to one of:
- `gemini` - Uses Google Gemini
- `openai` - Uses OpenAI (default)
- `anthropic` - Uses Anthropic Claude

**To select a specific model**, add the corresponding `*_MODEL` variable. For example:
```
ANTHROPIC_API_KEY=sk-ant-...your_key
DEFAULT_PROVIDER=anthropic
ANTHROPIC_MODEL=claude-3-5-haiku-20241022
```

### Method 2: Environment Variables (PowerShell)

If you prefer using environment variables, run these commands in PowerShell:

**For OpenAI (default):**
```powershell
$env:OPENAI_API_KEY="your_openai_api_key_here"
$env:DEFAULT_PROVIDER="openai"
```

**For Gemini:**
```powershell
$env:GEMINI_API_KEY="your_gemini_api_key_here"
$env:DEFAULT_PROVIDER="gemini"
```

**For Anthropic:**
```powershell
$env:ANTHROPIC_API_KEY="your_anthropic_api_key_here"
$env:DEFAULT_PROVIDER="anthropic"
$env:ANTHROPIC_MODEL="claude-3-5-haiku-20241022"
```

**Note:** Environment variables set this way only last for the current PowerShell session. Use `.env` file for a permanent setup.

## Available Models

### Gemini Models
- `gemini-1.5-flash` (default) - Fast and efficient
- `gemini-1.5-pro` - More capable, slower
- `gemini-pro` - Legacy model
- `gemini-pro-vision` - Legacy vision model

### OpenAI Models
- `gpt-4o` (default) - Latest and most capable, best for complex questions
- `gpt-4o-mini` - Faster, lower cost, good for simple questions
- `gpt-4-turbo` - Previous generation, still very capable
- `gpt-4-turbo-preview` - Preview version of GPT-4 Turbo
- `gpt-4` - Standard GPT-4 model
- `gpt-4-vision-preview` - Legacy vision model

### Anthropic Models
- `claude-3-5-sonnet-20241022` (default) - Latest and most capable
- `claude-3-5-haiku-20241022` - Fastest and most affordable
- `claude-3-opus-20240229` - Most powerful (legacy)
- `claude-3-sonnet-20240229` - Balanced (legacy)

## Usage

1. Make sure the virtual environment is activated:
```bash
# PowerShell:
.\venv\Scripts\Activate.ps1

# Or use the provided run scripts:
# Windows: double-click run-openai.bat, run-gemini.bat, or run-anthropic.bat
```

2. Run the application:

**Option 1: Use convenience batch files (easiest)**
- Double-click `run-openai.bat` to use OpenAI GPT-4o
- Double-click `run-gemini.bat` to use Gemini
- Double-click `run-anthropic.bat` to use Anthropic

**Option 2: Use command-line arguments**
```bash
# Use OpenAI (your default)
python main.py --provider openai

# Use Anthropic with specific model
python main.py --provider anthropic --model claude-3-5-haiku-20241022

# Use Gemini
python main.py -p gemini
```

**Option 3: Use PowerShell script with arguments**
```bash
# Using PowerShell
.\run.ps1 openai
.\run.ps1 anthropic claude-3-5-haiku-20241022
```

**Note:** Command-line arguments override the `DEFAULT_PROVIDER` setting in your `.env` file.

3. The application will start monitoring the screenshots directory automatically.

4. When you see a question on your screen:
   - Take a screenshot using **Windows Key + Print Screen** (saves to `C:\Users\YOUR_PROFILE_NAME\Pictures\Screenshots`)
   - The application will automatically detect the new screenshot
   - The answer will appear in a modal in the bottom-left corner
   - The modal will automatically disappear after 3 seconds

**Note:** The application continuously monitors the screenshots folder, so just take a screenshot and it will be processed automatically!

## Contributing

Contributions are welcome! Feel free to open an issue or submit a pull request.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Configuration

You can customize the following settings via environment variables:

- `DEFAULT_PROVIDER`: AI provider to use (default: `openai`)
- `MODAL_DISPLAY_DURATION`: How long the modal stays visible (default: 3 seconds)

## Troubleshooting

**Screenshots not being detected:**
- Verify that screenshots are being saved to `C:\Users\YOUR_PROFILE_NAME\Pictures\Screenshots`
- Check that the directory exists
- Make sure you're using Windows Key + Print Screen (not just Print Screen)
- The application monitors the folder continuously - wait a moment after taking a screenshot

**Application not processing screenshots:**
- Check the console output for error messages
- Verify your API key is set correctly in the `.env` file

**API errors:**
- Verify your API key is set correctly
- Check your internet connection
- Ensure you have sufficient API credits/quota

## Security Note

Never commit your `.env` file or hardcode API keys in the source code. Always use environment variables for sensitive information.

