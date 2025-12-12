# Quick Setup Guide

## Step 1: Install Dependencies

```bash
pip install -r requirements.txt
```

## Step 2: Create .env File

Create a file named `.env` in this directory with your API keys:

```
OPENAI_API_KEY=sk-your_key_here
DEFAULT_PROVIDER=openai
```

## Step 3: Select Your Provider and Model

Change `DEFAULT_PROVIDER` in your `.env` file to one of:
- `openai` - Uses OpenAI (default model: gpt-4o)
- `gemini` - Uses Google Gemini (default model: gemini-1.5-flash)
- `anthropic` - Uses Anthropic Claude (default model: claude-3-5-sonnet-20241022)

You can also specify a specific model by adding the corresponding model variable:
- `OPENAI_MODEL=gpt-4o-mini` (for faster/cheaper)
- `GEMINI_MODEL=gemini-1.5-pro` (for more capable)
- `ANTHROPIC_MODEL=claude-3-5-haiku-20241022` (for faster/cheaper)

## Step 4: Run the Application

```bash
python main.py
```

## Example .env Files

**For OpenAI:**
```
OPENAI_API_KEY=sk-proj-abc123...
DEFAULT_PROVIDER=openai
```

**For Gemini:**
```
GEMINI_API_KEY=AIzaSyC...
DEFAULT_PROVIDER=gemini
```

**For Anthropic:**
```
ANTHROPIC_API_KEY=sk-ant-...
DEFAULT_PROVIDER=anthropic
ANTHROPIC_MODEL=claude-3-5-haiku-20241022
```

## Getting API Keys

- **OpenAI**: https://platform.openai.com/api-keys
- **Gemini**: https://makersuite.google.com/app/apikey
- **Anthropic**: https://console.anthropic.com/

