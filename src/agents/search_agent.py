from openai import OpenAI
from typing import List, Dict, Any
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from tools.web_search import WebSearchTool
from utils.helpers import log_agent_action
from config import Config

class SearchAgent:
    """Agent responsible for searching and gathering information"""
    
    def __init__(self, api_key: str, max_results: int = 5):
        self.max_results = max_results
        self.demo_mode = Config.DEMO_MODE
        
        # Only initialize OpenAI client if not in demo mode
        if not self.demo_mode:
            # Validate API key
            if not api_key:
                raise ValueError(
                    "❌ No API key provided!\n"
                    "Make sure your .env file contains:\n"
                    "OPENAI_API_KEY=your-key-here"
                )
            
            if not api_key.startswith(('sk-', 'sk-proj-')):
                raise ValueError(
                    f"❌ Invalid API key format!\n"
                    f"Key should start with 'sk-' or 'sk-proj-'\n"
                    f"Your key starts with: {api_key[:10]}..."
                )
            
            # Clean the API key (remove any whitespace)
            api_key = api_key.strip()
            
            try:
                self.client = OpenAI(api_key=api_key)
                print("✅ OpenAI client initialized successfully")
            except Exception as e:
                raise ValueError(
                    f"❌ Failed to create OpenAI client: {str(e)}\n"
                    "Check:\n"
                    "1. API key is valid\n"
                    "2. Billing is set up at https://platform.openai.com/account/billing\n"
                    "3. API key hasn't been revoked"
                )
        else:
            self.client = None
            print("✅ Search Agent initialized in demo mode")
        
        self.search_tool = WebSearchTool(max_results=max_results)
        self.name = "SearchAgent"
    
    def generate_search_queries(self, topic: str, num_queries: int = 3) -> List[str]:
        """
        Use AI to generate effective search queries for a topic
        
        Args:
            topic: The research topic
            num_queries: Number of queries to generate
            
        Returns:
            List of search query strings
        """
        log_agent_action(self.name, "Generating search queries", f"Topic: {topic}")
        
        # Demo mode: Generate simple queries without AI
        if self.demo_mode:
            queries = [
                topic,
                f"{topic} latest developments",
                f"{topic} practical applications"
            ]
            log_agent_action(self.name, "Generated demo queries", f"Count: {len(queries)}")
            for i, q in enumerate(queries, 1):
                print(f"  {i}. {q}")
            return queries[:num_queries]
        
        # Real mode: Use AI
        prompt = f"""You are a research assistant. Generate {num_queries} different search queries 
to comprehensively research the topic: "{topic}"

Each query should focus on a different aspect:
1. General overview and definition
2. Recent developments or news
3. Practical applications or use cases

Return ONLY the queries, one per line, without numbering or explanation."""

        try:
            response = self.client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": "You are a research query generator."},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.7,
                max_tokens=200
            )
            
            queries_text = response.choices[0].message.content.strip()
            queries = [q.strip() for q in queries_text.split('\n') if q.strip()]
            
            log_agent_action(self.name, "Generated queries", f"Count: {len(queries)}")
            for i, q in enumerate(queries, 1):
                print(f"  {i}. {q}")
            
            return queries[:num_queries]
            
        except Exception as e:
            log_agent_action(self.name, "ERROR generating queries", str(e))
            print(f"⚠️  Falling back to simple queries due to error: {str(e)}")
            # Fallback to simple queries
            return [topic, f"{topic} latest news", f"{topic} applications"]
    
    def search_and_gather(self, topic: str) -> Dict[str, Any]:
        """
        Main method: Generate queries and search for information
        
        Args:
            topic: Research topic
            
        Returns:
            Dictionary containing all search results and metadata
        """
        log_agent_action(self.name, "Starting research", topic)
        
        # Generate smart search queries
        queries = self.generate_search_queries(topic)
        
        # Search for each query
        all_results = []
        for query in queries:
            results = self.search_tool.search(query)
            all_results.extend(results)
        
        # Remove duplicates based on URL
        unique_results = []
        seen_urls = set()
        for result in all_results:
            if result['url'] not in seen_urls:
                seen_urls.add(result['url'])
                unique_results.append(result)
        
        log_agent_action(self.name, "Research complete", 
                        f"Found {len(unique_results)} unique sources")
        
        return {
            'topic': topic,
            'queries': queries,
            'results': unique_results,
            'total_sources': len(unique_results)
        }