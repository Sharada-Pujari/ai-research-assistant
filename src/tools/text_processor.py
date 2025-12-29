from typing import List, Dict
import re

class TextProcessor:
    """Tool for processing and analyzing text"""
    
    @staticmethod
    def extract_key_points(text: str, max_points: int = 5) -> List[str]:
        """
        Extract key points from text using simple sentence analysis
        
        Args:
            text: Input text to analyze
            max_points: Maximum number of points to extract
            
        Returns:
            List of key points
        """
        # Split into sentences
        sentences = re.split(r'[.!?]+', text)
        sentences = [s.strip() for s in sentences if len(s.strip()) > 20]
        
        # Simple scoring based on length and position
        scored_sentences = []
        for i, sentence in enumerate(sentences[:max_points * 2]):
            # Prioritize earlier sentences
            position_score = 1 - (i / len(sentences))
            # Prefer medium-length sentences
            length_score = min(len(sentence) / 100, 1.0)
            score = position_score * 0.6 + length_score * 0.4
            
            scored_sentences.append((sentence, score))
        
        # Sort by score and take top N
        scored_sentences.sort(key=lambda x: x[1], reverse=True)
        return [s[0] for s in scored_sentences[:max_points]]
    
    @staticmethod
    def summarize_snippets(snippets: List[str]) -> str:
        """
        Combine multiple text snippets into a coherent summary
        
        Args:
            snippets: List of text snippets
            
        Returns:
            Combined summary text
        """
        if not snippets:
            return "No content available to summarize."
        
        # Remove duplicates while preserving order
        unique_snippets = []
        seen = set()
        
        for snippet in snippets:
            # Normalize for comparison
            normalized = snippet.lower().strip()
            if normalized not in seen:
                seen.add(normalized)
                unique_snippets.append(snippet)
        
        return " ".join(unique_snippets)
    
    @staticmethod
    def clean_text(text: str) -> str:
        """
        Clean and normalize text
        
        Args:
            text: Input text
            
        Returns:
            Cleaned text
        """
        # Remove extra whitespace
        text = re.sub(r'\s+', ' ', text)
        # Remove special characters but keep punctuation
        text = re.sub(r'[^\w\s.,!?-]', '', text)
        return text.strip()
    
    @staticmethod
    def extract_keywords(text: str, top_n: int = 10) -> List[str]:
        """
        Extract important keywords from text
        
        Args:
            text: Input text
            top_n: Number of keywords to return
            
        Returns:
            List of keywords
        """
        # Convert to lowercase and split into words
        words = re.findall(r'\b[a-z]{4,}\b', text.lower())
        
        # Common words to exclude
        stop_words = {'that', 'this', 'with', 'from', 'have', 'been', 
                     'will', 'their', 'there', 'what', 'when', 'where',
                     'which', 'while', 'who', 'would', 'could', 'should'}
        
        # Count word frequency
        word_freq = {}
        for word in words:
            if word not in stop_words:
                word_freq[word] = word_freq.get(word, 0) + 1
        
        # Sort by frequency
        sorted_words = sorted(word_freq.items(), key=lambda x: x[1], reverse=True)
        return [word for word, freq in sorted_words[:top_n]]