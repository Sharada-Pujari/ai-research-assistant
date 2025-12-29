from duckduckgo_search import DDGS
from typing import List, Dict, Any
import time
import random
import sys
import os

# Add parent directory to path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from config import Config

# Import demo data if available
try:
    from .demo_data import get_demo_results
    DEMO_AVAILABLE = True
except ImportError:
    DEMO_AVAILABLE = False

class WebSearchTool:
    """Tool for searching the web using DuckDuckGo"""
    
    def __init__(self, max_results: int = 5):
        self.max_results = max_results
        self.ddgs = DDGS()
        self.use_demo = Config.DEMO_MODE
    
    def search(self, query: str) -> List[Dict[str, Any]]:
        """
        Search the web for a given query
        
        Args:
            query: Search query string
            
        Returns:
            List of search results with title, url, and snippet
        """
        # Check if demo mode is enabled
        if self.use_demo and DEMO_AVAILABLE:
            print(f"\n🔍 [DEMO MODE] Searching for: '{query}'")
            time.sleep(1)  # Simulate search delay
            results = get_demo_results(query, self.max_results)
            print(f"✓ Found {len(results)} demo results")
            return results
        
        # Real search with retry logic
        max_retries = 3
        retry_delay = 2
        
        for attempt in range(max_retries):
            try:
                print(f"\n🔍 Searching for: '{query}'")
                time.sleep(random.uniform(2, 4))
                
                results = []
                search_results = self.ddgs.text(
                    query, 
                    max_results=self.max_results,
                    region='wt-wt',
                    safesearch='moderate'
                )
                
                for result in search_results:
                    results.append({
                        'title': result.get('title', 'No title'),
                        'url': result.get('href', ''),
                        'snippet': result.get('body', 'No description available')
                    })
                
                print(f"✓ Found {len(results)} results")
                return results
                
            except Exception as e:
                error_msg = str(e)
                
                if 'Ratelimit' in error_msg:
                    if attempt < max_retries - 1:
                        wait_time = retry_delay * (2 ** attempt)
                        print(f"⚠️  Rate limited. Retrying in {wait_time}s...")
                        time.sleep(wait_time)
                        continue
                    else:
                        # Fall back to demo mode if available
                        if DEMO_AVAILABLE and Config.USE_FALLBACK_ON_ERROR:
                            print("⚠️  Switching to demo mode due to rate limiting")
                            self.use_demo = True
                            return get_demo_results(query, self.max_results)
                        else:
                            print(f"❌ Rate limit exceeded. Try again in a few minutes.")
                            return []
                else:
                    print(f"❌ Search error: {error_msg}")
                    return []
        
        return []