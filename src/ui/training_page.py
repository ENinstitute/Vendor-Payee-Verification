"""
Training Page - Model Training Interface
"""

import streamlit as st
from pathlib import Path
import time
import sys

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from database.db_manager import DatabaseManager
from src.processors.batch_processor import BatchProcessor
from config.settings import settings

def render_training_page():
    """Render the training page"""
    
    st.markdown('<div class="main-header">🎓 Model Training</div>', unsafe_allow_html=True)
    
    st.markdown("""
    ### 📚 Train the AI Model
    
    Training teaches the system to recognize patterns in invoices and extract IBAN information 
    with high accuracy. Use approximately **100 sample invoices** for best results.
    """)
    
    st.markdown("---")
    
    # Training configuration
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.markdown("### 📤 Training Invoice Upload")
        
        # File uploader
        uploaded_files = st.file_uploader(
            "Select invoices for training (PDF or images)",
            type=['pdf', 'jpg', 'jpeg', 'png', 'tiff', 'tif'],
            accept_multiple_files=True,
            help="Recommended: 100 diverse invoices from different vendors"
        )
        
        if uploaded_files:
            st.success(f"✅ {len(uploaded_files)} file(s) selected")
            
            # Show file list in expander
            with st.expander("📋 View file list"):
                for idx, file in enumerate(uploaded_files, 1):
                    file_size = len(file.getvalue()) / 1024  # KB
                    st.text(f"{idx}. {file.name} ({file_size:.1f} KB)")
    
    with col2:
        st.markdown("### ⚙️ Settings")
        
        # Training options
        confidence_threshold = st.slider(
            "Confidence Threshold (%)",
            min_value=70,
            max_value=100,
            value=90,
            step=5,
            help="Extractions below this value will be marked for manual review"
        )
        
        use_parallel = st.checkbox(
            "Parallel Processing",
            value=True,
            help="Process multiple invoices simultaneously"
        )
        
        max_workers = st.number_input(
            "Max Workers",
            min_value=1,
            max_value=8,
            value=4,
            help="Number of parallel processes"
        ) if use_parallel else 1
    
    st.markdown("---")
    
    # Training progress section
    col_left, col_right = st.columns([3, 2])
    
    with col_left:
        st.markdown("### 🚀 Start Training")
        
        # Information box
        st.info("""
        **ℹ️ Information:**
        - Estimated time: ~5-10 minutes for 100 invoices
        - The process can be interrupted at any time
        - Results are automatically saved to the database
        - Learned patterns improve processing accuracy
        """)
        
        # Start training button
        if st.button("▶️ Start Training", type="primary", use_container_width=True):
            if not uploaded_files:
                st.error("❌ Please upload files first!")
            else:
                run_training(uploaded_files, confidence_threshold, max_workers)
    
    with col_right:
        st.markdown("### 📊 Expected Statistics")
        
        st.metric("Success Target", "95%", help="Expected success rate")
        st.metric("Average Confidence", ">90%", help="Average confidence level")
        st.metric("Tempo/Fatura", "<5s", help="Average time per invoice")
        
        st.markdown("---")
        
        st.markdown("#### 💡 Tips")
        st.markdown("""
        - Use invoices de **different vendors**
        - Include **varied layouts**
        - Prefer **high quality** image
        - Avoid **duplicates**
        """)
    
    st.markdown("---")
    
    # Training history
    st.markdown("### 📜 Training History")
    
    training_dir = Path("data/invoices/training")
    if training_dir.exists():
        file_count = len(list(training_dir.glob("*.*")))
        if file_count > 0:
            st.info(f"📁 {file_count} file(s) in training directory")
            
            if st.button("🗑️ Clear Training Directory"):
                if st.session_state.get('confirm_clear', False):
                    # Clear directory logic here
                    st.warning("⚠️ Cleanup functionality will be implemented")
                    st.session_state.confirm_clear = False
                else:
                    st.session_state.confirm_clear = True
                    st.warning("⚠️ Click again to confirm deletion")
        else:
            st.info("📭 No files in training directory")
    else:
        st.warning("⚠️ Training directory not found")


def run_training(uploaded_files, confidence_threshold, max_workers):
    """Execute the training process"""
    
    st.markdown("---")
    st.markdown("### 🔄 Processing in Progress")
    
    # Save uploaded files temporarily
    training_dir = Path("data/invoices/training")
    training_dir.mkdir(parents=True, exist_ok=True)
    
    progress_bar = st.progress(0)
    status_text = st.empty()
    
    try:
        # Save files
        status_text.text("💾 Saving files...")
        saved_files = []
        
        for idx, uploaded_file in enumerate(uploaded_files):
            file_path = training_dir / uploaded_file.name
            with open(file_path, 'wb') as f:
                f.write(uploaded_file.getbuffer())
            saved_files.append(file_path)
            progress_bar.progress((idx + 1) / (len(uploaded_files) * 2))
        
        st.success(f"✅ {len(saved_files)} file(s) saved successfully!")
        
        # Initialize database
        status_text.text("🗄️ Initializing database...")
        time.sleep(0.5)
        
        try:
            db_manager = DatabaseManager()
            db_manager.initialize_database()
            st.success("✅ Database initialized!")
        except Exception as e:
            st.error(f"❌ Error initializing database: {str(e)}")
            return
        
        # Initialize batch processor
        status_text.text("⚙️ Preparing processor...")
        time.sleep(0.5)
        
        try:
            batch_processor = BatchProcessor(db_manager)
            st.success("✅ Processor initialized!")
        except Exception as e:
            st.error(f"❌ Error initializing processor: {str(e)}")
            return
        
        # Process training batch
        status_text.text("🤖 Processando invoices com IA...")
        progress_bar.progress(0.6)
        
        # Vendor mapping (empty for now)
        vendor_mapping = {}
        
        # Create placeholder for live updates
        results_placeholder = st.empty()
        
        with st.spinner("Processing with Claude API..."):
            try:
                results = batch_processor.process_training_batch(
                    str(training_dir),
                    vendor_mapping
                )
                progress_bar.progress(1.0)
                
                # Display results
                status_text.empty()
                
                st.markdown("---")
                st.markdown("### ✅ Training Completed!")
                
                # Results metrics
                col1, col2, col3, col4 = st.columns(4)
                
                with col1:
                    st.metric(
                        "Total Processed",
                        results.get('total', 0),
                        help="Total invoices processadas"
                    )
                
                with col2:
                    total_count = results.get('total', 0) or 1
                    success_rate = (results.get('successful', 0) / total_count) * 100
                    st.metric(
                        "Success Rate",
                        f"{success_rate:.1f}%",
                        help="Percentage of successful extractions"
                    )
                
                with col3:
                    st.metric(
                        "Average Confidence",
                        f"{results.get('average_confidence', 0):.1%}",
                        help="Average confidence level"
                    )
                
                with col4:
                    failed = results.get('total', 0) - results.get('successful', 0)
                    st.metric(
                        "Failed",
                        failed,
                        help="Invoices that failed processing"
                    )
                
                # Update session state
                st.session_state.total_trained = results.get('total', 0)
                st.session_state.avg_confidence = results.get('average_confidence', 0)
                
                # Success message
                if success_rate >= 95:
                    st.markdown('<div class="success-box">🎉 <strong>Excellent!</strong> The model was successfully trained and is ready to use!</div>', unsafe_allow_html=True)
                elif success_rate >= 80:
                    st.markdown('<div class="warning-box">⚠️ <strong>Attention!</strong> Success rate below expected. Considere adicionar mais invoices de treinamento.</div>', unsafe_allow_html=True)
                else:
                    st.markdown('<div class="error-box">❌ <strong>Problem!</strong> Success rate too low. Verifique as invoices e tente novamente.</div>', unsafe_allow_html=True)
                
                # Next steps
                st.markdown("### 📋 Next Steps")
                st.markdown("""
                1. ✅ Model successfully trained
                2. ➡️ Go to **Processing** para processar invoices reais
                3. 📊 Check the **Results** after processing
                """)
                
            except Exception as e:
                st.error(f"❌ Error during training: {str(e)}")
                st.exception(e)
                return
        
    except Exception as e:
        st.error(f"❌ Error saving files: {str(e)}")
        st.exception(e)
        return
