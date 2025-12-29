"""
Streamlit Web Interface for AI Research Assistant
"""

import streamlit as st
import sys
import os
from datetime import datetime

# Add src to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from main import AIResearchAssistant
from config import Config

# Page configuration
st.set_page_config(
    page_title="AI Research Assistant",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS
st.markdown("""
<style>
    .main-header {
        font-size: 3rem;
        font-weight: bold;
        text-align: center;
        color: #1E88E5;
        margin-bottom: 2rem;
    }
    .stButton>button {
        width: 100%;
        background-color: #1E88E5;
        color: white;
        font-size: 1.2rem;
        padding: 0.5rem;
        border-radius: 10px;
    }
    .success-box {
        padding: 1rem;
        border-radius: 10px;
        background-color: #E8F5E9;
        border-left: 5px solid #4CAF50;
    }
</style>
""", unsafe_allow_html=True)

# Initialize session state
if 'assistant' not in st.session_state:
    with st.spinner("Initializing AI Research Assistant..."):
        try:
            st.session_state.assistant = AIResearchAssistant()
            st.session_state.initialized = True
        except Exception as e:
            st.error(f"Failed to initialize: {str(e)}")
            st.session_state.initialized = False

if 'research_history' not in st.session_state:
    st.session_state.research_history = []

# Header
st.markdown('<div class="main-header">🤖 AI Research Assistant</div>', unsafe_allow_html=True)
st.markdown("---")

# Sidebar
with st.sidebar:
    st.header("⚙️ Settings")
    
    # Show current mode
    if Config.DEMO_MODE:
        st.warning("🔴 Demo Mode Active")
        st.caption("Using offline sample data")
    else:
        st.success("🟢 Live Mode Active")
        st.caption("Using real APIs")
    
    st.markdown("---")
    
    # Configuration info
    with st.expander("📊 Configuration"):
        st.write(f"**Model:** {Config.MODEL_NAME}")
        st.write(f"**Max Results:** {Config.MAX_SEARCH_RESULTS}")
        st.write(f"**Temperature:** {Config.TEMPERATURE}")
    
    st.markdown("---")
    
    # Research history
    st.header("📚 History")
    if st.session_state.research_history:
        for i, item in enumerate(reversed(st.session_state.research_history[-5:]), 1):
            with st.expander(f"{i}. {item['topic'][:30]}..."):
                st.caption(f"⏰ {item['timestamp']}")
                if st.button(f"View Report #{i}", key=f"view_{i}"):
                    st.session_state.view_report = item['report_path']
    else:
        st.caption("No research history yet")
    
    st.markdown("---")
    
    # Example topics
    st.header("💡 Example Topics")
    example_topics = [
        "artificial intelligence in healthcare",
        "climate change solutions",
        "quantum computing basics",
        "renewable energy trends",
        "machine learning applications"
    ]
    
    for topic in example_topics:
        if st.button(topic, key=f"example_{topic}"):
            st.session_state.research_topic = topic

# Main content
col1, col2 = st.columns([2, 1])

with col1:
    st.header("🔍 Research Topic")
    
    # Get topic from session state or user input
    default_topic = st.session_state.get('research_topic', '')
    topic = st.text_input(
        "Enter a topic to research:",
        value=default_topic,
        placeholder="e.g., artificial intelligence in healthcare",
        help="Enter any topic you want to research"
    )
    
    # Research button
    research_button = st.button("🚀 Start Research", type="primary", use_container_width=True)

with col2:
    st.header("📊 Stats")
    st.metric("Total Researches", len(st.session_state.research_history))
    st.metric("Reports Generated", len(st.session_state.research_history))
    if Config.DEMO_MODE:
        st.metric("API Cost", "$0.00", "Demo Mode")
    else:
        estimated_cost = len(st.session_state.research_history) * 0.005
        st.metric("Estimated Cost", f"${estimated_cost:.3f}")

# Research execution
if research_button and topic:
    if not st.session_state.initialized:
        st.error("❌ Assistant not initialized. Please refresh the page.")
    else:
        # Progress tracking
        progress_bar = st.progress(0)
        status_text = st.empty()
        
        try:
            # Phase 1: Search
            status_text.text("🔍 Phase 1/3: Gathering information...")
            progress_bar.progress(10)
            
            with st.spinner("Searching the web..."):
                search_data = st.session_state.assistant.search_agent.search_and_gather(topic)
            
            progress_bar.progress(40)
            
            # Phase 2: Analysis
            status_text.text("🧠 Phase 2/3: Analyzing sources...")
            
            with st.spinner("Extracting insights..."):
                analysis_data = st.session_state.assistant.analyzer_agent.analyze_sources(search_data)
            
            progress_bar.progress(70)
            
            # Phase 3: Report
            status_text.text("📄 Phase 3/3: Generating report...")
            
            with st.spinner("Creating report..."):
                report_path = st.session_state.assistant.report_agent.generate_report(
                    analysis_data,
                    Config.REPORTS_DIR
                )
            
            progress_bar.progress(100)
            status_text.text("✅ Research complete!")
            
            # Add to history
            st.session_state.research_history.append({
                'topic': topic,
                'timestamp': datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                'report_path': report_path,
                'sources_count': analysis_data['sources'].__len__()
            })
            
            # Show success
            st.balloons()
            st.success(f"✅ Research completed successfully!")
            
            # Display report
            st.markdown("---")
            st.header("📄 Generated Report")
            
            with open(report_path, 'r', encoding='utf-8') as f:
                report_content = f.read()
            
            st.markdown(report_content)
            
            # Download button
            st.download_button(
                label="📥 Download Report",
                data=report_content,
                file_name=f"{topic.replace(' ', '_')}_report.md",
                mime="text/markdown"
            )
            
        except Exception as e:
            st.error(f"❌ Error during research: {str(e)}")
            import traceback
            with st.expander("Error Details"):
                st.code(traceback.format_exc())

# View historical report
if 'view_report' in st.session_state:
    st.markdown("---")
    st.header("📄 Historical Report")
    
    try:
        with open(st.session_state.view_report, 'r', encoding='utf-8') as f:
            report_content = f.read()
        
        st.markdown(report_content)
        
        st.download_button(
            label="📥 Download This Report",
            data=report_content,
            file_name=os.path.basename(st.session_state.view_report),
            mime="text/markdown"
        )
    except Exception as e:
        st.error(f"Error loading report: {str(e)}")
    
    if st.button("Clear View"):
        del st.session_state.view_report
        st.rerun()

# Footer
st.markdown("---")
st.markdown("""
<div style='text-align: center; color: gray; padding: 2rem;'>
    <p>🤖 AI Research Assistant | Built with Streamlit & OpenAI</p>
    <p>Made for internship project demonstration</p>
</div>
""", unsafe_allow_html=True)