"""
Configuration file for AI Research Assistant
Handles all application settings and environment variables
"""

import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

class Config:
    """
    Configuration class for the AI Research Assistant
    Contains all settings and API keys
    """
    
    # ==================== API KEYS ====================
    # OpenAI API key from environment variable
    OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
    
    # ==================== DEMO MODE ====================
    # Enable demo mode to use offline data (no API calls needed)
    DEMO_MODE = True  # Set to True for demo/testing, False for real API calls
    
    # Automatically fall back to demo mode if API errors occur
    USE_FALLBACK_ON_ERROR = True
    
    # ==================== AGENT SETTINGS ====================
    # Maximum number of search results to retrieve
    MAX_SEARCH_RESULTS = 5
    
    # Maximum iterations for agent workflows
    MAX_ITERATIONS = 3
    
    # Temperature for AI responses (0.0 = deterministic, 1.0 = creative)
    TEMPERATURE = 0.7
    
    # ==================== MODEL SELECTION ====================
    # OpenAI model to use for agents
    # Options: "gpt-3.5-turbo", "gpt-4", "gpt-4-turbo"
    MODEL_NAME = "gpt-3.5-turbo"
    
    # ==================== FILE PATHS ====================
    # Directory to save generated reports
    REPORTS_DIR = "data/reports"
    
    # ==================== SEARCH SETTINGS ====================
    # Number of search queries to generate per topic
    NUM_SEARCH_QUERIES = 3
    
    # Timeout for web requests (in seconds)
    REQUEST_TIMEOUT = 10
    
    # ==================== ANALYSIS SETTINGS ====================
    # Maximum number of key points to extract
    MAX_KEY_POINTS = 5
    
    # Maximum number of keywords to extract
    MAX_KEYWORDS = 10
    
    # ==================== AI SETTINGS ====================
    # Maximum tokens for AI responses
    MAX_TOKENS = 2000
    
    # Token limit for content processing
    CONTENT_TOKEN_LIMIT = 3000
    
    # ==================== LOGGING ====================
    # Enable/disable detailed logging
    VERBOSE_LOGGING = True
    
    # Log file path (optional)
    LOG_FILE = "data/app.log"
    
    # ==================== VALIDATION ====================
    @staticmethod
    def validate():
        """
        Validate that all required configuration is present
        Raises ValueError if configuration is invalid
        """
        # In demo mode, we don't need API key
        if Config.DEMO_MODE:
            print("⚠️  Running in DEMO MODE - Using offline data")
            print("   Set DEMO_MODE = False in config.py to use real APIs")
            os.makedirs(Config.REPORTS_DIR, exist_ok=True)
            print("✅ Configuration validated successfully!")
            return True
        
        # Check if OpenAI API key is set
        if not Config.OPENAI_API_KEY:
            raise ValueError(
                "❌ OPENAI_API_KEY not found in environment variables!\n"
                "Please create a .env file with your API key:\n"
                "OPENAI_API_KEY=your-key-here\n\n"
                "OR enable demo mode in config.py:\n"
                "DEMO_MODE = True"
            )
        
        # Check if API key has correct format
        if not Config.OPENAI_API_KEY.startswith(('sk-', 'sk-proj-')):
            raise ValueError(
                "❌ Invalid OpenAI API key format!\n"
                "API key should start with 'sk-' or 'sk-proj-'"
            )
        
        # Create reports directory if it doesn't exist
        os.makedirs(Config.REPORTS_DIR, exist_ok=True)
        
        print("✅ Configuration validated successfully!")
        return True
    
    # ==================== DISPLAY SETTINGS ====================
    @staticmethod
    def display_config():
        """
        Display current configuration (without showing sensitive data)
        """
        print("\n" + "=" * 60)
        print("⚙️  CURRENT CONFIGURATION")
        print("=" * 60)
        print(f"Demo Mode: {'✅ ENABLED' if Config.DEMO_MODE else '❌ DISABLED'}")
        print(f"Model: {Config.MODEL_NAME}")
        print(f"Max Search Results: {Config.MAX_SEARCH_RESULTS}")
        print(f"Temperature: {Config.TEMPERATURE}")
        print(f"Max Tokens: {Config.MAX_TOKENS}")
        print(f"Reports Directory: {Config.REPORTS_DIR}")
        
        if not Config.DEMO_MODE and Config.OPENAI_API_KEY:
            print(f"API Key: {'*' * 20}{Config.OPENAI_API_KEY[-4:]}")
        elif not Config.DEMO_MODE:
            print(f"API Key: ❌ NOT SET")
        
        print("=" * 60 + "\n")
    
    # ==================== COST ESTIMATION ====================
    @staticmethod
    def estimate_cost(num_researches: int = 1):
        """
        Estimate the cost for running researches
        
        Args:
            num_researches: Number of research reports to generate
            
        Returns:
            Estimated cost in USD
        """
        if Config.DEMO_MODE:
            print(f"\n💰 Cost Estimate: $0.00 (Demo Mode - No API calls)")
            return 0.0
        
        # Average tokens per research
        avg_tokens_per_research = 2000
        
        # GPT-3.5-turbo pricing (per 1K tokens)
        cost_per_1k_tokens = 0.0015
        
        # Calculate total cost
        total_tokens = avg_tokens_per_research * num_researches
        estimated_cost = (total_tokens / 1000) * cost_per_1k_tokens
        
        print(f"\n💰 Cost Estimate:")
        print(f"   Researches: {num_researches}")
        print(f"   Estimated tokens: ~{total_tokens:,}")
        print(f"   Estimated cost: ${estimated_cost:.4f} USD")
        
        return estimated_cost


# ==================== ALTERNATIVE CONFIGURATIONS ====================

class DevelopmentConfig(Config):
    """Configuration for development environment"""
    VERBOSE_LOGGING = True
    MAX_SEARCH_RESULTS = 3  # Fewer results for faster testing
    TEMPERATURE = 0.5
    DEMO_MODE = True  # Use demo mode for development


class ProductionConfig(Config):
    """Configuration for production environment"""
    VERBOSE_LOGGING = False
    MAX_SEARCH_RESULTS = 10  # More comprehensive results
    TEMPERATURE = 0.7
    DEMO_MODE = False  # Use real APIs in production


class TestConfig(Config):
    """Configuration for testing"""
    VERBOSE_LOGGING = True
    MAX_SEARCH_RESULTS = 2
    REPORTS_DIR = "tests/test_reports"
    MODEL_NAME = "gpt-3.5-turbo"
    DEMO_MODE = True  # Always use demo mode for tests


# ==================== ENVIRONMENT SELECTION ====================

def get_config(env: str = "development"):
    """
    Get configuration based on environment
    
    Args:
        env: Environment name ('development', 'production', 'test')
        
    Returns:
        Config class for the specified environment
    """
    configs = {
        'development': DevelopmentConfig,
        'production': ProductionConfig,
        'test': TestConfig
    }
    
    return configs.get(env.lower(), Config)


# ==================== MODULE EXECUTION ====================

if __name__ == "__main__":
    """
    Test configuration when running this file directly
    """
    print("Testing Configuration...")
    
    try:
        # Validate configuration
        Config.validate()
        
        # Display configuration
        Config.display_config()
        
        # Show cost estimate
        Config.estimate_cost(num_researches=10)
        
        print("\n✅ All configuration tests passed!")
        
    except Exception as e:
        print(f"\n❌ Configuration Error: {str(e)}")