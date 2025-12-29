import os
import json
from datetime import datetime
from typing import Dict, Any

def create_directory(path: str) -> None:
    """Create directory if it doesn't exist"""
    if not os.path.exists(path):
        os.makedirs(path)
        print(f"✓ Created directory: {path}")

def save_report(content: str, topic: str, reports_dir: str) -> str:
    """Save report to file"""
    create_directory(reports_dir)
    
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"{topic.replace(' ', '_')}_{timestamp}.md"
    filepath = os.path.join(reports_dir, filename)
    
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(content)
    
    print(f"✓ Report saved: {filepath}")
    return filepath

def format_sources(sources: list) -> str:
    """Format sources for report"""
    if not sources:
        return "No sources available"
    
    formatted = "\n## Sources\n\n"
    for i, source in enumerate(sources, 1):
        formatted += f"{i}. [{source.get('title', 'Unknown')}]({source.get('url', '#')})\n"
    
    return formatted

def log_agent_action(agent_name: str, action: str, details: str = "") -> None:
    """Log agent actions for debugging"""
    timestamp = datetime.now().strftime("%H:%M:%S")
    print(f"[{timestamp}] {agent_name}: {action}")
    if details:
        print(f"    → {details}")