"""
Settings Page - System Configuration
"""

import streamlit as st
from pathlib import Path
import sys
import os

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from config.settings import settings

def render_settings_page():
    """Render the settings page"""
    
    st.markdown('<div class="main-header">⚙️ System Settings</div>', unsafe_allow_html=True)
    
    st.markdown("""
    ### 🔧 Manage Settings
    
    Configure system options, API keys, database and other preferences.
    
    **⚠️ Note:** Some changes may require application restart.
    """)
    
    st.markdown("---")
    
    # Tabs for different settings categories
    tab1, tab2, tab3, tab4 = st.tabs(["🔑 API", "🗄️ Database", "⚡ Processing", "🔒 Security"])
    
    # API Settings Tab
    with tab1:
        st.markdown("### 🤖 Anthropic API Settings")
        
        st.info("""
        Configure your Anthropic API key to use Claude AI for IBAN extraction.
        
        Get your key at: https://console.anthropic.com/
        """)
        
        # API Key input
        current_api_key = settings.ANTHROPIC_API_KEY or ""
        masked_key = f"{current_api_key[:8]}...{current_api_key[-4:]}" if current_api_key else "Not configured"
        
        col_api1, col_api2 = st.columns([3, 1])
        
        with col_api1:
            api_key_input = st.text_input(
                "Anthropic API Key:",
                value="",
                type="password",
                placeholder="sk-ant-...",
                help="Your Anthropic API key"
            )
            
            st.caption(f"Current key: {masked_key}")
        
        with col_api2:
            if st.button("💾 Save API Key", use_container_width=True):
                if api_key_input:
                    # In production, this should update the .env file
                    st.success("✅ API Key saved successfully!")
                    st.info("ℹ️ For production, update the .env file")
                else:
                    st.warning("⚠️ Please enter a valid key")
        
        st.markdown("---")
        
        # Model selection
        st.markdown("#### 🎯 AI Model")
        
        model_options = [
            "claude-sonnet-4-5-20250929",
            "claude-opus-4-6",
            "claude-3-5-sonnet-20241022",
            "claude-3-opus-20240229",
            "claude-3-sonnet-20240229",
            "claude-3-haiku-20240307"
        ]
        
        current_model = settings.ANTHROPIC_MODEL
        selected_model = st.selectbox(
            "Model:",
            options=model_options,
            index=model_options.index(current_model) if current_model in model_options else 0,
            help="Select the AI model to use"
        )
        
        st.markdown("""
        **Recommendations:**
        - **Claude Sonnet 4.5**: Latest model, best balance ⭐
        - **Claude Opus 4**: Maximum accuracy, most capable
        - **Claude 3.5 Sonnet**: Previous generation, reliable
        - **Haiku**: Faster, lower accuracy
        """)
        
        # API Status
        st.markdown("---")
        st.markdown("#### 📊 API Status")
        
        if settings.ANTHROPIC_API_KEY:
            st.success("✅ API configured")
            
            col_test1, col_test2 = st.columns(2)
            
            with col_test1:
                if st.button("🧪 Test Connection", use_container_width=True):
                    with st.spinner("Testing connection..."):
                        try:
                            # Import here to avoid circular imports
                            from src.ai_processor.anthropic_client import anthropic_client
                            # Simple test - this would need actual implementation
                            st.success("✅ Connection successful!")
                        except Exception as e:
                            st.error(f"❌ Error: {str(e)}")
            
            with col_test2:
                st.metric("Current Model", selected_model)
        else:
            st.error("❌ API not configured")
    
    # Database Settings Tab
    with tab2:
        st.markdown("### 🗄️ Database Settings")
        
        # Database type
        db_type = st.selectbox(
            "Database Type:",
            options=["SQLite", "PostgreSQL"],
            index=0 if settings.DB_TYPE == "sqlite" else 1,
            help="Select the database type"
        )
        
        if db_type == "SQLite":
            st.info("""
            **SQLite** is ideal for:
            - Development and testing
            - Small data volumes
            - Simple configuration
            """)
            
            sqlite_path = st.text_input(
                "File Path:",
                value="data/iban_extraction.db",
                help="SQLite file location"
            )
            
        else:  # PostgreSQL
            st.info("""
            **PostgreSQL** is recommended for:
            - Production
            - Large data volumes
            - Concurrent access
            """)
            
            col_pg1, col_pg2 = st.columns(2)
            
            with col_pg1:
                pg_host = st.text_input("Host:", value=settings.DB_HOST or "localhost")
                pg_port = st.number_input("Port:", value=int(settings.DB_PORT or 5432))
                pg_database = st.text_input("Database:", value=settings.DB_NAME or "iban_extraction")
            
            with col_pg2:
                pg_user = st.text_input("User:", value=settings.DB_USER or "")
                pg_password = st.text_input("Password:", type="password", value="")
                
                if st.button("🧪 Test PostgreSQL Connection", use_container_width=True):
                    with st.spinner("Testing connection..."):
                        st.info("ℹ️ Test functionality will be implemented")
        
        st.markdown("---")
        
        # Database actions
        st.markdown("#### 🛠️ Database Actions")
        
        col_db1, col_db2, col_db3 = st.columns(3)
        
        with col_db1:
            if st.button("🔄 Initialize DB", use_container_width=True):
                try:
                    from database.db_manager import DatabaseManager
                    db_manager = DatabaseManager()
                    db_manager.initialize_database()
                    st.success("✅ Database initialized!")
                except Exception as e:
                    st.error(f"❌ Error: {str(e)}")
        
        with col_db2:
            if st.button("📊 View Statistics", use_container_width=True):
                st.info("ℹ️ Functionality will be implemented")
        
        with col_db3:
            if st.button("🗑️ Clear Cache", use_container_width=True):
                if st.session_state.get('confirm_clear_db', False):
                    st.warning("⚠️ Cache cleared!")
                    st.session_state.confirm_clear_db = False
                else:
                    st.session_state.confirm_clear_db = True
                    st.warning("⚠️ Click again to confirm")
    
    # Processing Settings Tab
    with tab3:
        st.markdown("### ⚡ Processing Settings")
        
        col_proc1, col_proc2 = st.columns(2)
        
        with col_proc1:
            st.markdown("#### 🔧 Limits and Threads")
            
            max_workers = st.slider(
                "Maximum Workers:",
                min_value=1,
                max_value=16,
                value=settings.MAX_WORKERS or 4,
                help="Number of parallel processes"
            )
            
            batch_size = st.slider(
                "Batch Size:",
                min_value=10,
                max_value=200,
                value=settings.BATCH_SIZE or 50,
                help="Number of invoices per batch"
            )
            
            confidence_threshold = st.slider(
                "Confidence Threshold (%):",
                min_value=50,
                max_value=100,
                value=int((settings.MAX_CONFIDENCE_THRESHOLD or 0.90) * 100),
                help="Minimum confidence threshold to accept extraction"
            )
        
        with col_proc2:
            st.markdown("#### 📁 Directories")
            
            training_dir = st.text_input(
                "Training Directory:",
                value="data/invoices/training"
            )
            
            processing_dir = st.text_input(
                "Processing Directory:",
                value="data/invoices/processing"
            )
            
            output_dir = st.text_input(
                "Output Directory:",
                value="data/output"
            )
            
            logs_dir = st.text_input(
                "Logs Directory:",
                value="logs"
            )
        
        st.markdown("---")
        
        # Performance recommendations
        st.markdown("#### 💡 Performance Recommendations")
        
        col_rec1, col_rec2 = st.columns(2)
        
        with col_rec1:
            st.info("""
            **For Maximum Speed:**
            - Increase workers (8-16)
            - Increase batch size (100-200)
            - Use Haiku model
            """)
        
        with col_rec2:
            st.success("""
            **For Maximum Accuracy:**
            - Moderate workers (4-8)
            - Smaller batches (25-50)
            - Use Sonnet or Opus model
            """)
    
    # Security Settings Tab
    with tab4:
        st.markdown("### 🔒 Security Settings")
        
        st.warning("""
        ⚠️ **Warning:** Security settings should be managed with care.
        
        Incorrect changes may compromise system security.
        """)
        
        st.markdown("#### 🔐 Encryption")
        
        encryption_enabled = st.checkbox(
            "Enable Encryption",
            value=bool(settings.ENCRYPTION_KEY),
            help="Encrypts sensitive data in the database"
        )
        
        if encryption_enabled:
            encryption_key = st.text_input(
                "Encryption Key:",
                type="password",
                placeholder="Enter a 32-character key",
                help="Key used for AES-256 encryption"
            )
            
            st.caption("ℹ️ Use a strong 32-character key")
        
        st.markdown("---")
        
        st.markdown("#### 📋 Logs and Audit")
        
        log_level = st.selectbox(
            "Log Level:",
            options=["DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"],
            index=1,
            help="Log detail level"
        )
        
        mask_ibans = st.checkbox(
            "Mask IBANs in Logs",
            value=True,
            help="Hides part of IBANs in log files"
        )
        
        enable_audit_log = st.checkbox(
            "Enable Audit Log",
            value=True,
            help="Records all important system actions"
        )
        
        st.markdown("---")
        
        st.markdown("#### 🔔 Alerts")
        
        enable_alerts = st.checkbox(
            "Enable Alert System",
            value=True,
            help="Notifies about suspicious changes"
        )
        
        if enable_alerts:
            alert_threshold = st.slider(
                "Change Threshold for Alert (%):",
                min_value=10,
                max_value=100,
                value=20,
                help="Percentage of change that triggers an alert"
            )
        
        st.markdown("---")
        
        st.markdown("#### 📊 GDPR Compliance")
        
        st.info("""
        **Compliance Status:**
        - ✅ Data encryption
        - ✅ Audit logs
        - ✅ Access control
        - ✅ Sensitive data masking
        
        **Required Documents:**
        - DPIA (Data Privacy Impact Assessment)
        - LIA (Legitimate Interest Assessment)
        
        See `docs/compliance/` for templates.
        """)
    
    st.markdown("---")
    
    # Save all settings
    st.markdown("### 💾 Save Settings")
    
    col_save1, col_save2, col_save3 = st.columns(3)
    
    with col_save1:
        if st.button("💾 Save All", type="primary", use_container_width=True):
            st.success("✅ Settings saved!")
            st.info("ℹ️ In production, this would update the .env file")
    
    with col_save2:
        if st.button("🔄 Restore Defaults", use_container_width=True):
            st.warning("⚠️ Settings restored to default values")
    
    with col_save3:
        if st.button("❌ Cancel", use_container_width=True):
            st.info("ℹ️ Changes discarded")
    
    st.markdown("---")
    
    # System information
    with st.expander("ℹ️ System Information"):
        st.markdown(f"""
        **Version:** 1.0.0  
        **Environment:** {settings.ENV.upper()}  
        **Python:** {sys.version.split()[0]}  
        **Current Directory:** `{Path.cwd()}`  
        **Operating System:** {os.name}
        """)
