"""Main application entry point."""
import sys
import time
import argparse
from pathlib import Path
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
from config import Config
from screenshot_handler import get_latest_screenshot
from ai_providers import create_provider
from ui_overlay import AnswerModal


# AI prompt for question extraction and answering
QUESTION_PROMPT = """Look at this screenshot carefully. If there is a question visible, identify the question number (if applicable) and provide a clear, concise answer. 

Format your response as:
- "Question [number]: [answer]" if a question number is present
- "[answer]" if no question number is present

Only include the question number and answer. Be brief and direct."""


class ScreenshotHandler(FileSystemEventHandler):
    """File system event handler for detecting new screenshots."""
    
    def __init__(self, app_instance):
        self.app = app_instance
    
    def on_created(self, event):
        """Called when a new file is created."""
        if event.is_directory:
            return
        
        # Check if it's an image file
        image_extensions = {'.png', '.jpg', '.jpeg', '.bmp', '.gif', '.webp'}
        file_path = Path(event.src_path)
        
        if file_path.suffix.lower() in image_extensions:
            # Small delay to ensure file is fully written
            time.sleep(0.5)
            self.app.process_screenshot(file_path)


class ScreenshotQuestionAnswerer:
    """Main application class."""
    
    def __init__(self, provider_name=None, model_name=None):
        self.modal = AnswerModal()
        self.provider = None
        self.last_processed_path = None
        self._initialize_provider(provider_name, model_name)
    
    def _initialize_provider(self, provider_name=None, model_name=None):
        """Initialize the AI provider based on configuration or command-line arguments."""
        # Use command-line argument if provided, otherwise use config default
        provider_name = provider_name or Config.DEFAULT_PROVIDER
        api_key = Config.get_api_key(provider_name)
        
        # Use command-line model if provided, otherwise use config default
        model = model_name or Config.get_model(provider_name)
        
        if not api_key:
            print(f"Error: API key for {provider_name} not found.")
            print("Please set the appropriate environment variable in your .env file:")
            if provider_name == "gemini":
                print("  GEMINI_API_KEY=your_key_here")
            elif provider_name == "openai":
                print("  OPENAI_API_KEY=your_key_here")
            elif provider_name == "anthropic":
                print("  ANTHROPIC_API_KEY=your_key_here")
            sys.exit(1)
        
        try:
            self.provider = create_provider(provider_name, api_key, model)
            print(f"Initialized {provider_name} provider with model: {model}")
        except Exception as e:
            print(f"Error initializing provider: {e}")
            sys.exit(1)
    
    def process_screenshot(self, screenshot_path=None):
        """
        Process a screenshot and display the answer.
        
        Args:
            screenshot_path: Optional path to specific screenshot. If None, gets the latest.
        """
        # If no path provided, get the latest screenshot
        if screenshot_path is None:
            screenshot_path = get_latest_screenshot(Config.SCREENSHOT_DIR)
            if not screenshot_path:
                print("No screenshots found in the directory.")
                return
        else:
            screenshot_path = str(screenshot_path)
        
        # Avoid processing the same screenshot twice
        if screenshot_path == self.last_processed_path:
            return
        
        print(f"Processing screenshot: {screenshot_path}")
        self.last_processed_path = screenshot_path
        
        # Process with AI
        try:
            answer, billing_error = self.provider.process_image(screenshot_path, QUESTION_PROMPT)
            
            # Check for billing/credit issues first
            if billing_error:
                print(f"Billing error: {billing_error}")
                # Display billing warning in modal with longer duration (10 seconds)
                self.modal.show_answer(billing_error, duration=Config.MODAL_ERROR_DURATION, is_warning=True)
                return
            
            if not answer:
                print("No answer received from AI.")
                return
            
            print(f"Answer: {answer}")
            
            # Display in modal
            self.modal.show_answer(answer, Config.MODAL_DISPLAY_DURATION)
        
        except Exception as e:
            print(f"Error processing screenshot: {e}")
    
    def run(self):
        """Start the application and monitor for new screenshots."""
        screenshot_dir = Path(Config.SCREENSHOT_DIR)
        
        if not screenshot_dir.exists():
            print(f"Error: Screenshot directory does not exist: {Config.SCREENSHOT_DIR}")
            sys.exit(1)
        
        print(f"Monitoring screenshots directory: {Config.SCREENSHOT_DIR}")
        print("Take a screenshot using Windows Key + Print Screen to process it automatically.")
        print("Press Ctrl+C to exit.")
        
        # Set up file system watcher
        event_handler = ScreenshotHandler(self)
        observer = Observer()
        observer.schedule(event_handler, str(screenshot_dir), recursive=False)
        observer.start()
        
        try:
            # Keep the application running
            # Tkinter runs in its own thread, so we just need to keep main thread alive
            while True:
                time.sleep(1)
        except KeyboardInterrupt:
            print("\nShutting down...")
            observer.stop()
            observer.join()
            self.modal.destroy()
            sys.exit(0)


def main():
    """Application entry point."""
    parser = argparse.ArgumentParser(
        description="Screenshot Question Answerer - Automatically answer questions from screenshots using AI",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python main.py --provider openai
  python main.py -p anthropic -m claude-3-5-haiku-20241022
  python main.py --provider gemini --model gemini-1.5-pro

Available providers: openai, gemini, anthropic
        """
    )
    
    parser.add_argument(
        "-p", "--provider",
        choices=["openai", "gemini", "anthropic"],
        help="AI provider to use (overrides DEFAULT_PROVIDER in .env)"
    )
    
    parser.add_argument(
        "-m", "--model",
        help="Specific model to use (overrides provider default model)"
    )
    
    args = parser.parse_args()
    
    app = ScreenshotQuestionAnswerer(
        provider_name=args.provider,
        model_name=args.model
    )
    app.run()


if __name__ == "__main__":
    main()

