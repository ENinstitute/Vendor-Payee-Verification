"""
Streamlit Web Interface
AI-Powered IBAN Extraction System
Chartered Accountants Ireland
"""

import streamlit as st
import sys
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path(__file__).parent))

from src.ui.main_page import render_main_page
from src.ui.training_page import render_training_page
from src.ui.processing_page import render_processing_page
from src.ui.results_page import render_results_page
from src.ui.settings_page import render_settings_page
from config.settings import settings

# Page configuration
st.set_page_config(
    page_title="IBAN Extraction System",
    page_icon="💳",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS
st.markdown("""
    <style>
    .main-header {
        font-size: 2.5rem;
        font-weight: bold;
        color: #1f77b4;
        text-align: center;
        padding: 1rem;
        background: linear-gradient(90deg, #f0f2f6 0%, #ffffff 100%);
        border-radius: 10px;
        margin-bottom: 2rem;
    }
    .metric-card {
        background-color: #f0f2f6;
        padding: 1rem;
        border-radius: 10px;
        border-left: 5px solid #1f77b4;
    }
    .success-box {
        padding: 1rem;
        border-radius: 5px;
        background-color: #d4edda;
        border: 1px solid #c3e6cb;
        color: #155724;
    }
    .warning-box {
        padding: 1rem;
        border-radius: 5px;
        background-color: #fff3cd;
        border: 1px solid #ffeeba;
        color: #856404;
    }
    .error-box {
        padding: 1rem;
        border-radius: 5px;
        background-color: #f8d7da;
        border: 1px solid #f5c6cb;
        color: #721c24;
    }
    </style>
    """, unsafe_allow_html=True)

def main():
    """Main application entry point"""
    
    # Sidebar navigation
    st.sidebar.image("https://via.placeholder.com/300x100/1f77b4/ffffff?text=CAI+IBAN+System", use_container_width=True)
    st.sidebar.title("🧭 Navigation")
    
    # Navigation menu
    page = st.sidebar.radio(
        "Choose an option:",
        ["🏠 Home", "🎓 Training", "⚙️ Processing", "📊 Results", "⚙️ Settings"],
        label_visibility="collapsed"
    )
    
    # System status in sidebar
    st.sidebar.markdown("---")
    st.sidebar.markdown("### 📊 System Status")
    
    # Check API connection
    api_status = "✅ Connected" if settings.ANTHROPIC_API_KEY else "❌ Not configured"
    db_status = "✅ Connected" if settings.DB_TYPE else "❌ Not configured"
    
    st.sidebar.markdown(f"**Anthropic API:** {api_status}")
    st.sidebar.markdown(f"**Database:** {db_status}")
    st.sidebar.markdown(f"**Environment:** {settings.ENV.upper()}")
    
    # Quick stats
    st.sidebar.markdown("---")
    st.sidebar.markdown("### 📈 Quick Stats")
    
    # Initialize session state for stats if not exists
    if 'total_processed' not in st.session_state:
        st.session_state.total_processed = 0
    if 'total_trained' not in st.session_state:
        st.session_state.total_trained = 0
    if 'avg_confidence' not in st.session_state:
        st.session_state.avg_confidence = 0.0
    
    st.sidebar.metric("Trained Invoices", st.session_state.total_trained)
    st.sidebar.metric("Processed Invoices", st.session_state.total_processed)
    st.sidebar.metric("Average Confidence", f"{st.session_state.avg_confidence:.1%}")
    
    # Footer
    st.sidebar.markdown("---")
    st.sidebar.markdown("""
        <div style='text-align: center; font-size: 0.8rem; color: #666;'>
            <p><strong>IBAN Extraction System v1.0</strong></p>
            <p>Chartered Accountants Ireland</p>
            <p>© 2025 All Rights Reserved</p>
        </div>
    """, unsafe_allow_html=True)
    
    # Main content area
    if page == "🏠 Home":
        render_main_page()
    elif page == "🎓 Training":
        render_training_page()
    elif page == "⚙️ Processing":
        render_processing_page()
    elif page == "📊 Results":
        render_results_page()
    elif page == "⚙️ Settings":
        render_settings_page()

if __name__ == "__main__":
    main()
