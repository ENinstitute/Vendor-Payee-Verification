"""
Main Page - Dashboard Overview
"""

import streamlit as st
from pathlib import Path
from datetime import datetime
import pandas as pd

def render_main_page():
    """Render the main dashboard page"""
    
    # Header
    st.markdown('<div class="main-header">💳 AI-Powered IBAN Extraction System</div>', unsafe_allow_html=True)
    
    # Welcome message
    st.markdown("""
    ### 👋 Welcome to the IBAN Extraction System
    
    This system uses Artificial Intelligence (Anthropic's Claude API) to automatically extract 
    IBAN and bank account information from vendor invoices.
    """)
    
    # System overview
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.markdown('<div class="metric-card">', unsafe_allow_html=True)
        st.metric(
            label="🎯 Accuracy Target",
            value=">95%",
            help="Target accuracy rate for extractions"
        )
        st.markdown('</div>', unsafe_allow_html=True)
    
    with col2:
        st.markdown('<div class="metric-card">', unsafe_allow_html=True)
        st.metric(
            label="⚡ Average Time",
            value="<30s",
            help="Processing time per invoice"
        )
        st.markdown('</div>', unsafe_allow_html=True)
    
    with col3:
        st.markdown('<div class="metric-card">', unsafe_allow_html=True)
        st.metric(
            label="📊 Min. Confidence",
            value="90%",
            help="Minimum confidence threshold"
        )
        st.markdown('</div>', unsafe_allow_html=True)
    
    with col4:
        st.markdown('<div class="metric-card">', unsafe_allow_html=True)
        st.metric(
            label="🔒 Security",
            value="GDPR",
            help="GDPR and regulations compliant"
        )
        st.markdown('</div>', unsafe_allow_html=True)
    
    st.markdown("---")
    
    # Quick Start Guide
    col_left, col_right = st.columns([1, 1])
    
    with col_left:
        st.markdown("### 🚀 Quick Start Guide")
        
        with st.expander("**1️⃣ Training**", expanded=True):
            st.markdown("""
            - Go to the **Training** page
            - Upload 100 sample invoices
            - Click **Start Training**
            - Wait for processing (approx. 5-10 min)
            """)
        
        with st.expander("**2️⃣ Processing**"):
            st.markdown("""
            - Go to the **Processing** page
            - Upload invoices to process
            - Click **Process Invoices**
            - Download the generated CSV file
            """)
        
        with st.expander("**3️⃣ Results**"):
            st.markdown("""
            - View detailed statistics
            - Analyze validation reports
            - Export data to Dynamics GP
            - Check processing logs
            """)
    
    with col_right:
        st.markdown("### 📋 System Features")
        
        st.markdown("""
        #### ✅ Main Features
        
        - **AI Extraction**: Uses Anthropic's Claude API
        - **IBAN Validation**: Checksum verification
        - **Batch Processing**: Multiple invoices simultaneously
        - **CSV Export**: Ready for Dynamics GP
        - **Detailed Logs**: Complete audit trail
        - **Alerts**: Notifications for suspicious changes
        
        #### 📄 Supported Formats
        
        - PDF (`.pdf`)
        - JPEG Images (`.jpg`, `.jpeg`)
        - PNG Images (`.png`)
        - TIFF Images (`.tiff`, `.tif`)
        """)
    
    st.markdown("---")
    
    # System Status
    st.markdown("### 🔍 System Status")
    
    status_col1, status_col2, status_col3 = st.columns(3)
    
    with status_col1:
        st.markdown("#### 🗂️ Directories")
        training_dir = Path("data/invoices/training")
        processing_dir = Path("data/invoices/processing")
        output_dir = Path("data/output")
        
        training_count = len(list(training_dir.glob("*.*"))) if training_dir.exists() else 0
        processing_count = len(list(processing_dir.glob("*.*"))) if processing_dir.exists() else 0
        
        st.info(f"📁 Training: **{training_count}** files")
        st.info(f"📁 Processing: **{processing_count}** files")
        st.info(f"📁 Output: {'✅ Configured' if output_dir.exists() else '⚠️ Not found'}")
    
    with status_col2:
        st.markdown("#### ⚙️ Configuration")
        from config.settings import settings
        
        api_configured = bool(settings.ANTHROPIC_API_KEY)
        db_configured = bool(settings.DB_TYPE)
        
        if api_configured:
            st.success("✅ Anthropic API configured")
        else:
            st.error("❌ Anthropic API not configured")
        
        if db_configured:
            st.success(f"✅ Database: {settings.DB_TYPE}")
        else:
            st.warning("⚠️ Database not configured")
        
        st.info(f"🌍 Environment: **{settings.ENV.upper()}**")
    
    with status_col3:
        st.markdown("#### 📈 Recent Activity")
        
        # Check for recent outputs
        if output_dir.exists():
            recent_files = sorted(output_dir.glob("*.csv"), key=lambda x: x.stat().st_mtime, reverse=True)[:3]
            
            if recent_files:
                for file in recent_files:
                    modified_time = datetime.fromtimestamp(file.stat().st_mtime)
                    st.text(f"📄 {file.name}")
                    st.caption(f"   {modified_time.strftime('%m/%d/%Y %H:%M')}")
            else:
                st.info("No recent files")
        else:
            st.warning("Output directory not found")
    
    st.markdown("---")
    
    # Help section
    with st.expander("❓ Need Help?"):
        st.markdown("""
        ### 📚 Available Resources
        
        - **Complete Documentation**: See `README.md` in the repository
        - **Quick Start Guide**: Check `docs/QUICKSTART.md`
        - **Architecture**: Details in `docs/architecture.md`
        
        ### 👥 Support Team
        
        - **Kieran Daly** - Data Architect
        - **Eduardo Nascimento** - Solutions Architect
        - **Altamash Naik** - ERP Architect
        
        ### 🐛 Report Issues
        
        Use GitHub Issues or contact the team directly.
        """)
    
    # Footer
    st.markdown("---")
    st.markdown("""
    <div style='text-align: center; color: #666; font-size: 0.9rem;'>
        <p>💼 <strong>Chartered Accountants Ireland</strong> | Built with ❤️ by IT Team</p>
        <p>Version 1.0.0 | © 2025 All Rights Reserved</p>
    </div>
    """, unsafe_allow_html=True)
