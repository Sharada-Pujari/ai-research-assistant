from openai import OpenAI
from typing import List, Dict, Any
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from tools.text_processor import TextProcessor
from utils.helpers import log_agent_action
from config import Config

class AnalyzerAgent:
    """Agent responsible for analyzing and synthesizing information"""
    
    def __init__(self, api_key: str):
        self.demo_mode = Config.DEMO_MODE
        
        # Only initialize OpenAI client if not in demo mode
        if not self.demo_mode:
            self.client = OpenAI(api_key=api_key)
        else:
            self.client = None
            print("✅ Analyzer Agent initialized in demo mode")
        
        self.text_processor = TextProcessor()
        self.name = "AnalyzerAgent"
    
    def analyze_sources(self, search_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Analyze search results and extract insights
        
        Args:
            search_data: Data from SearchAgent
            
        Returns:
            Analysis results with key insights
        """
        log_agent_action(self.name, "Starting analysis", 
                        f"{search_data['total_sources']} sources")
        
        results = search_data['results']
        
        # Combine all snippets
        all_text = " ".join([r['snippet'] for r in results])
        
        # Extract keywords
        keywords = self.text_processor.extract_keywords(all_text, top_n=10)
        log_agent_action(self.name, "Extracted keywords", f"{len(keywords)} keywords")
        
        # Extract key points from snippets
        key_points = []
        for result in results[:5]:  # Top 5 results
            points = self.text_processor.extract_key_points(result['snippet'], max_points=2)
            key_points.extend(points)
        
        # Use AI to synthesize insights (or demo mode)
        insights = self._synthesize_insights(search_data['topic'], all_text, results)
        
        log_agent_action(self.name, "Analysis complete", "Generated insights")
        
        return {
            'topic': search_data['topic'],
            'keywords': keywords,
            'key_points': key_points,
            'insights': insights,
            'sources': results
        }
    
    def _synthesize_insights(self, topic: str, content: str, results: list) -> Dict[str, str]:
        """
        Use AI to generate insights from content
        
        Args:
            topic: Research topic
            content: Combined text content
            results: Search results
            
        Returns:
            Dictionary of insights
        """
        # Demo mode: Create insights from the content directly
        if self.demo_mode:
            log_agent_action(self.name, "Generating demo insights")
            
            # Create a summary from the first few snippets
            overview_parts = []
            for result in results[:3]:
                snippet = result['snippet']
                # Take first sentence
                first_sentence = snippet.split('.')[0] + '.'
                overview_parts.append(first_sentence)
            
            overview = " ".join(overview_parts)
            
            # Extract key findings from snippets
            key_findings = []
            for result in results[:4]:
                snippet = result['snippet']
                sentences = [s.strip() + '.' for s in snippet.split('.') if len(s.strip()) > 30]
                if sentences:
                    key_findings.append(f"• {sentences[0]}")
            
            key_findings_text = "\n".join(key_findings)
            
            # Create implications
            implications = f"The research on {topic} shows significant developments and practical applications. "
            implications += "Organizations are increasingly adopting these technologies to improve efficiency and outcomes. "
            implications += "Continued innovation in this field is expected to drive further advancements."
            
            return {
                'overview': overview if overview else f"Research on {topic} reveals multiple important aspects and developments.",
                'key_findings': key_findings_text if key_findings_text else "Various perspectives and applications identified in the research.",
                'implications': implications
            }
        
        # Real mode: Use AI
        log_agent_action(self.name, "Synthesizing insights with AI")
        
        # Truncate content if too long
        max_content_length = 3000
        if len(content) > max_content_length:
            content = content[:max_content_length] + "..."
        
        prompt = f"""Analyze the following information about "{topic}" and provide:

1. A brief overview (2-3 sentences)
2. Key findings (3-4 bullet points)
3. Important implications or applications

Content:
{content}

Format your response as:
OVERVIEW: [your overview]
KEY_FINDINGS: [bullet points]
IMPLICATIONS: [implications]"""

        try:
            response = self.client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": "You are an expert research analyst."},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.5,
                max_tokens=500
            )
            
            analysis = response.choices[0].message.content.strip()
            
            # Parse the response
            insights = {
                'overview': '',
                'key_findings': '',
                'implications': ''
            }
            
            sections = analysis.split('\n')
            current_section = None
            
            for line in sections:
                if 'OVERVIEW:' in line:
                    current_section = 'overview'
                    insights['overview'] = line.replace('OVERVIEW:', '').strip()
                elif 'KEY_FINDINGS:' in line:
                    current_section = 'key_findings'
                    insights['key_findings'] = line.replace('KEY_FINDINGS:', '').strip()
                elif 'IMPLICATIONS:' in line:
                    current_section = 'implications'
                    insights['implications'] = line.replace('IMPLICATIONS:', '').strip()
                elif current_section and line.strip():
                    insights[current_section] += '\n' + line.strip()
            
            return insights
            
        except Exception as e:
            log_agent_action(self.name, "ERROR in synthesis", str(e))
            # Fallback to demo mode logic
            return self._synthesize_insights(topic, content, results) if not self.demo_mode else {
                'overview': f"Analysis of {topic} based on gathered sources.",
                'key_findings': "Multiple perspectives found in research.",
                'implications': "Further research recommended."
            }