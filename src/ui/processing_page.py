"""
Processing Page - Invoice Processing Interface
"""

import streamlit as st
from pathlib import Path
import time
import sys
from datetime import datetime

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from database.db_manager import DatabaseManager
from src.processors.batch_processor import BatchProcessor
from config.settings import settings

def render_processing_page():
    """Render the processing page"""
    
    st.markdown('<div class="main-header">⚙️ Invoice Processing</div>', unsafe_allow_html=True)
    
    st.markdown("""
    ### 📑 Process Production Invoices
    
    Use this page to process real invoices and extract IBAN information for integration 
    with Dynamics GP. The model should be trained before processing.
    """)
    
    st.markdown("---")
    
    # Check if training was done
    if st.session_state.get('total_trained', 0) == 0:
        st.warning("""
        ⚠️ **Warning:** No training detected. 
        
        For best results, it is recommended to train the model first on the **Training** page.
        
        You can still process invoices, but accuracy may be reduced.
        """)
    
    # Processing configuration
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.markdown("### 📤 Invoice Upload for Processing")
        
        # File uploader
        uploaded_files = st.file_uploader(
            "Select invoices to process (PDF or images)",
            type=['pdf', 'jpg', 'jpeg', 'png', 'tiff', 'tif'],
            accept_multiple_files=True,
            help="Production invoices for IBAN extraction"
        )
        
        if uploaded_files:
            st.success(f"✅ {len(uploaded_files)} file(s) selected")
            
            # Show file list in expander
            with st.expander("📋 View file list"):
                for idx, file in enumerate(uploaded_files, 1):
                    file_size = len(file.getvalue()) / 1024  # KB
                    st.text(f"{idx}. {file.name} ({file_size:.1f} KB)")
            
            # Batch info
            st.info(f"""
            **📊 Batch Information:**
            - Total files: {len(uploaded_files)}
            - Estimated time: ~{len(uploaded_files) * 5} seconds
            - Total size: {sum(len(f.getvalue()) for f in uploaded_files) / (1024*1024):.2f} MB
            """)
    
    with col2:
        st.markdown("### ⚙️ Settings")
        
        # Processing options
        confidence_threshold = st.slider(
            "Confidence Threshold (%)",
            min_value=70,
            max_value=100,
            value=90,
            step=5,
            help="Extractions below this value will be marked for review"
        )
        
        generate_validation_report = st.checkbox(
            "Generate Validation Report",
            value=True,
            help="Creates detailed report with all validations"
        )
        
        export_to_csv = st.checkbox(
            "Export to CSV",
            value=True,
            help="Generate CSV file for Dynamics GP import"
        )
        
        st.markdown("---")
        
        st.markdown("#### 📋 Output Format")
        st.markdown("""
        - **vendor_id**: Vendor ID
        - **iban**: Extracted IBAN number
        - **account_name**: Account name
        - **confidence_score**: Confidence level
        """)
    
    st.markdown("---")
    
    # Processing section
    col_left, col_right = st.columns([3, 2])
    
    with col_left:
        st.markdown("### 🚀 Start Processing")
        
        # Information box
        st.info("""
        **ℹ️ Information:**
        - Processing uses the trained model
        - Results are saved to the database
        - CSV is generated automatically
        - Low confidence requires manual review
        """)
        
        # Start processing button
        if st.button("▶️ Process Invoices", type="primary", use_container_width=True):
            if not uploaded_files:
                st.error("❌ Please upload files first!")
            else:
                run_processing(
                    uploaded_files, 
                    confidence_threshold, 
                    generate_validation_report,
                    export_to_csv
                )
    
    with col_right:
        st.markdown("### 📊 Expected Statistics")
        
        if uploaded_files:
            estimated_time = len(uploaded_files) * 5
            st.metric("Estimated Time", f"{estimated_time}s")
            st.metric("Files", len(uploaded_files))
            st.metric("Success Rate", ">95%")
        else:
            st.metric("Files", "0")
            st.metric("Ready to Process", "No")
        
        st.markdown("---")
        
        st.markdown("#### ⚠️ Important Notes")
        st.markdown("""
        - Keep the window open during processing
        - Do not upload duplicate files
        - Check the image quality
        """)
    
    st.markdown("---")
    
    # Recent processing history
    st.markdown("### 📜 Recent History")
    
    output_dir = Path("data/output")
    if output_dir.exists():
        csv_files = sorted(output_dir.glob("iban_extractions_*.csv"), 
                          key=lambda x: x.stat().st_mtime, 
                          reverse=True)[:5]
        
        if csv_files:
            st.markdown("#### Latest Generated Files:")
            for file in csv_files:
                modified_time = datetime.fromtimestamp(file.stat().st_mtime)
                col_file, col_date, col_action = st.columns([3, 2, 1])
                
                with col_file:
                    st.text(f"📄 {file.name}")
                
                with col_date:
                    st.caption(modified_time.strftime('%m/%d/%Y %H:%M'))
                
                with col_action:
                    with open(file, 'rb') as f:
                        st.download_button(
                            "⬇️",
                            f,
                            file_name=file.name,
                            mime="text/csv",
                            key=f"download_{file.name}"
                        )
        else:
            st.info("📭 No previous processing found")
    else:
        st.warning("⚠️ Output directory not found")


def run_processing(uploaded_files, confidence_threshold, generate_report, export_csv):
    """Execute the processing"""
    
    st.markdown("---")
    st.markdown("### 🔄 Processing in Progress")
    
    # Save uploaded files
    processing_dir = Path("data/invoices/processing")
    processing_dir.mkdir(parents=True, exist_ok=True)
    
    progress_bar = st.progress(0)
    status_text = st.empty()
    
    try:
        # Save files
        status_text.text("💾 Saving files...")
        saved_files = []
        
        for idx, uploaded_file in enumerate(uploaded_files):
            file_path = processing_dir / uploaded_file.name
            with open(file_path, 'wb') as f:
                f.write(uploaded_file.getbuffer())
            saved_files.append(file_path)
            progress_bar.progress((idx + 1) / (len(uploaded_files) * 2))
        
        st.success(f"✅ {len(saved_files)} file(s) saved!")
        
        # Initialize database
        status_text.text("🗄️ Connecting to database...")
        time.sleep(0.5)
        
        try:
            db_manager = DatabaseManager()
            st.success("✅ Database connected!")
        except Exception as e:
            st.error(f"❌ Error connecting to database: {str(e)}")
            return
        
        # Initialize batch processor
        status_text.text("⚙️ Initializing processor...")
        time.sleep(0.5)
        
        try:
            batch_processor = BatchProcessor(db_manager)
            st.success("✅ Processor ready!")
        except Exception as e:
            st.error(f"❌ Error initializing processor: {str(e)}")
            return
        
        # Process production batch
        status_text.text("🤖 Extracting IBANs with AI...")
        progress_bar.progress(0.6)
        
        vendor_mapping = {}
        
        with st.spinner("Processing with Claude API..."):
            try:
                results = batch_processor.process_production_batch(
                    str(processing_dir),
                    vendor_mapping
                )
                progress_bar.progress(1.0)
                
                # Display results
                status_text.empty()
                
                st.markdown("---")
                st.markdown("### ✅ Processing Completed!")
                
                # Results metrics
                col1, col2, col3, col4 = st.columns(4)
                
                with col1:
                    st.metric(
                        "Total Processed",
                        results.get('total', 0)
                    )
                
                with col2:
                    success_rate = (results.get('successful', 0) / results.get('total', 1)) * 100
                    st.metric(
                        "Success Rate",
                        f"{success_rate:.1f}%"
                    )
                
                with col3:
                    st.metric(
                        "IBANs Extracted",
                        results.get('successful', 0)
                    )
                
                with col4:
                    failed = results.get('total', 0) - results.get('successful', 0)
                    st.metric(
                        "Failed",
                        failed
                    )
                
                # Update session state
                st.session_state.total_processed += results.get('total', 0)
                
                # Show output files
                st.markdown("### 📥 Generated Files")
                
                col_csv, col_report = st.columns(2)
                
                with col_csv:
                    if results.get('csv_output'):
                        csv_path = Path(results['csv_output'])
                        if csv_path.exists():
                            st.success(f"✅ CSV: `{csv_path.name}`")
                            with open(csv_path, 'rb') as f:
                                st.download_button(
                                    "⬇️ Download CSV",
                                    f,
                                    file_name=csv_path.name,
                                    mime="text/csv",
                                    use_container_width=True
                                )
                
                with col_report:
                    if results.get('validation_report'):
                        report_path = Path(results['validation_report'])
                        if report_path.exists():
                            st.success(f"✅ Report: `{report_path.name}`")
                            with open(report_path, 'rb') as f:
                                st.download_button(
                                    "⬇️ Download Report",
                                    f,
                                    file_name=report_path.name,
                                    mime="text/csv",
                                    use_container_width=True
                                )
                
                # Success message
                if success_rate >= 95:
                    st.markdown('<div class="success-box">🎉 <strong>Excellent!</strong> Processing completed successfully! Data is ready for Dynamics GP.</div>', unsafe_allow_html=True)
                elif success_rate >= 80:
                    st.markdown('<div class="warning-box">⚠️ <strong>Attention!</strong> Some extractions failed. Manually review problematic cases.</div>', unsafe_allow_html=True)
                else:
                    st.markdown('<div class="error-box">❌ <strong>Problem!</strong> Low success rate. Check invoice quality and consider retraining the model.</div>', unsafe_allow_html=True)
                
                # Next steps
                st.markdown("### 📋 Next Steps")
                st.markdown("""
                1. ✅ Download CSV files and report
                2. 🔍 Review extractions with low confidence
                3. 📊 Check results on **Results** page
                4. 💾 Import CSV into Dynamics GP
                """)
                
            except Exception as e:
                st.error(f"❌ Error during processing: {str(e)}")
                st.exception(e)
                return
        
    except Exception as e:
        st.error(f"❌ Error saving files: {str(e)}")
        st.exception(e)
        return
