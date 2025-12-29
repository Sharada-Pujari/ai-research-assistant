import sys
import os

# Add parent directory to Python path
# This allows importing from the root directory
current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(current_dir)
sys.path.insert(0, parent_dir)

# Now import from parent directory
from config import Config
from agents import SearchAgent, AnalyzerAgent, ReportAgent
from utils.helpers import log_agent_action

class AIResearchAssistant:
    """Main orchestrator for the agentic AI research system"""
    
    def __init__(self):
        # Validate configuration
        Config.validate()
        
        # Initialize all agents
        self.search_agent = SearchAgent(
            api_key=Config.OPENAI_API_KEY,
            max_results=Config.MAX_SEARCH_RESULTS
        )
        
        self.analyzer_agent = AnalyzerAgent(
            api_key=Config.OPENAI_API_KEY
        )
        
        self.report_agent = ReportAgent(
            api_key=Config.OPENAI_API_KEY
        )
        
        print("=" * 60)
        print("🤖 AI Research Assistant Initialized")
        print("=" * 60)
    
    def research(self, topic: str) -> str:
        """
        Main research workflow
        
        Args:
            topic: Research topic
            
        Returns:
            Path to generated report
        """
        print(f"\n📚 Starting research on: '{topic}'\n")
        
        try:
            # Step 1: Search and gather information
            print("\n" + "=" * 60)
            print("PHASE 1: Information Gathering")
            print("=" * 60)
            search_data = self.search_agent.search_and_gather(topic)
            
            # Step 2: Analyze the information
            print("\n" + "=" * 60)
            print("PHASE 2: Analysis")
            print("=" * 60)
            analysis_data = self.analyzer_agent.analyze_sources(search_data)
            
            # Step 3: Generate report
            print("\n" + "=" * 60)
            print("PHASE 3: Report Generation")
            print("=" * 60)
            report_path = self.report_agent.generate_report(
                analysis_data, 
                Config.REPORTS_DIR
            )
            
            print("\n" + "=" * 60)
            print("✅ RESEARCH COMPLETE!")
            print("=" * 60)
            print(f"📄 Report saved at: {report_path}\n")
            
            return report_path
            
        except Exception as e:
            print(f"\n❌ ERROR during research: {str(e)}")
            import traceback
            traceback.print_exc()
            raise

def main():
    """Main entry point"""
    
    # Create the assistant
    assistant = AIResearchAssistant()
    
    # Interactive mode
    print("\n💡 Enter a research topic (or 'quit' to exit)")
    
    while True:
        topic = input("\n🔍 Research Topic: ").strip()
        
        if topic.lower() in ['quit', 'exit', 'q']:
            print("\n👋 Goodbye!")
            break
        
        if not topic:
            print("⚠️  Please enter a valid topic")
            continue
        
        try:
            report_path = assistant.research(topic)
            
            # Ask if user wants to see the report
            show = input("\n📖 Would you like to display the report? (y/n): ").strip().lower()
            if show == 'y':
                with open(report_path, 'r', encoding='utf-8') as f:
                    print("\n" + "=" * 60)
                    print(f.read())
                    print("=" * 60)
        
        except KeyboardInterrupt:
            print("\n\n⚠️  Research interrupted by user")
        except Exception as e:
            print(f"\n❌ An error occurred: {str(e)}")

if __name__ == "__main__":
    main()
