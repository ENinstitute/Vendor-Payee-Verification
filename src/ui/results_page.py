"""
Results Page - Results Analysis and Visualization
"""

import streamlit as st
from pathlib import Path
import pandas as pd
from datetime import datetime
import sys

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent.parent))

def render_results_page():
    """Render the results page"""
    
    st.markdown('<div class="main-header">📊 Results and Analysis</div>', unsafe_allow_html=True)
    
    st.markdown("""
    ### 📈 View and Analyze Results
    
    Analyze IBAN extraction results, view detailed statistics and 
    identify cases that require manual review.
    """)
    
    st.markdown("---")
    
    # Load recent results
    output_dir = Path("data/output")
    
    if not output_dir.exists():
        st.warning("⚠️ Output directory not found. Run a processing first.")
        return
    
    # Get all CSV files
    csv_files = sorted(output_dir.glob("iban_extractions_*.csv"), 
                      key=lambda x: x.stat().st_mtime, 
                      reverse=True)
    
    if not csv_files:
        st.info("""
        📭 **No results available yet.**
        
        Run a processing on the **Processing** page to see results here.
        """)
        return
    
    # File selector
    st.markdown("### 📁 Select Results File")
    
    col_select, col_info = st.columns([2, 1])
    
    with col_select:
        # Create friendly names for files
        file_options = {}
        for f in csv_files[:10]:  # Show last 10 files
            modified_time = datetime.fromtimestamp(f.stat().st_mtime)
            friendly_name = f"{f.name} ({modified_time.strftime('%m/%d/%Y %H:%M')})"
            file_options[friendly_name] = f
        
        selected_file_name = st.selectbox(
            "Choose a file:",
            options=list(file_options.keys()),
            help="Select a results file to view"
        )
        
        selected_file = file_options[selected_file_name]
    
    with col_info:
        file_size = selected_file.stat().st_size / 1024  # KB
        st.metric("File Size", f"{file_size:.1f} KB")
        
        # Download button
        with open(selected_file, 'rb') as f:
            st.download_button(
                "⬇️ Download File",
                f,
                file_name=selected_file.name,
                mime="text/csv",
                use_container_width=True
            )
    
    st.markdown("---")
    
    # Load and display data
    try:
        df = pd.read_csv(selected_file)
        
        if df.empty:
            st.warning("⚠️ Empty file or no data.")
            return
        
        # Summary statistics
        st.markdown("### 📊 General Statistics")
        
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.metric(
                "Total Extractions",
                len(df),
                help="Total number of IBANs extracted"
            )
        
        with col2:
            if 'confidence_score' in df.columns:
                avg_confidence = df['confidence_score'].mean()
                st.metric(
                    "Average Confidence",
                    f"{avg_confidence:.1%}",
                    help="Average confidence level"
                )
            else:
                st.metric("Average Confidence", "N/A")
        
        with col3:
            if 'confidence_score' in df.columns:
                high_conf = len(df[df['confidence_score'] >= 0.90])
                st.metric(
                    "High Confidence (≥90%)",
                    high_conf,
                    help="Extractions with confidence ≥90%"
                )
            else:
                st.metric("High Confidence", "N/A")
        
        with col4:
            if 'confidence_score' in df.columns:
                low_conf = len(df[df['confidence_score'] < 0.70])
                st.metric(
                    "Low Confidence (<70%)",
                    low_conf,
                    delta=f"-{low_conf}" if low_conf > 0 else None,
                    delta_color="inverse",
                    help="Extractions that need review"
                )
            else:
                st.metric("Low Confidence", "N/A")
        
        st.markdown("---")
        
        # Confidence distribution
        if 'confidence_score' in df.columns:
            st.markdown("### 📈 Confidence Distribution")
            
            # Create confidence bins
            bins = [0, 0.7, 0.8, 0.9, 1.0]
            labels = ['<70% (Low)', '70-80% (Medium)', '80-90% (Good)', '≥90% (High)']
            df['confidence_category'] = pd.cut(df['confidence_score'], bins=bins, labels=labels)
            
            confidence_dist = df['confidence_category'].value_counts().sort_index()
            
            col_chart, col_table = st.columns([2, 1])
            
            with col_chart:
                st.bar_chart(confidence_dist)
            
            with col_table:
                st.dataframe(
                    pd.DataFrame({
                        'Category': confidence_dist.index,
                        'Quantity': confidence_dist.values,
                        'Percentage': [f"{(v/len(df)*100):.1f}%" for v in confidence_dist.values]
                    }),
                    hide_index=True,
                    use_container_width=True
                )
        
        st.markdown("---")
        
        # Data preview
        st.markdown("### 🔍 Data Visualization")
        
        # Filter options
        col_filter1, col_filter2, col_filter3 = st.columns(3)
        
        with col_filter1:
            if 'confidence_score' in df.columns:
                show_filter = st.selectbox(
                    "Filter by:",
                    ["All", "High Confidence (≥90%)", "Medium Confidence (70-90%)", "Low Confidence (<70%)"]
                )
            else:
                show_filter = "All"
        
        with col_filter2:
            search_term = st.text_input(
                "Search:",
                placeholder="Type IBAN, vendor_id, etc."
            )
        
        with col_filter3:
            rows_to_show = st.selectbox(
                "Rows per page:",
                [10, 25, 50, 100, "All"],
                index=1
            )
        
        # Apply filters
        filtered_df = df.copy()
        
        if show_filter != "All" and 'confidence_score' in df.columns:
            if show_filter == "High Confidence (≥90%)":
                filtered_df = filtered_df[filtered_df['confidence_score'] >= 0.90]
            elif show_filter == "Medium Confidence (70-90%)":
                filtered_df = filtered_df[(filtered_df['confidence_score'] >= 0.70) & 
                                         (filtered_df['confidence_score'] < 0.90)]
            elif show_filter == "Low Confidence (<70%)":
                filtered_df = filtered_df[filtered_df['confidence_score'] < 0.70]
        
        if search_term:
            mask = filtered_df.astype(str).apply(
                lambda row: row.str.contains(search_term, case=False).any(), 
                axis=1
            )
            filtered_df = filtered_df[mask]
        
        # Show results count
        st.info(f"📋 Showing {len(filtered_df)} of {len(df)} records")
        
        # Display dataframe
        if rows_to_show == "All":
            st.dataframe(filtered_df, use_container_width=True, height=600)
        else:
            st.dataframe(filtered_df.head(rows_to_show), use_container_width=True)
        
        st.markdown("---")
        
        # Action buttons
        st.markdown("### 🛠️ Actions")
        
        col_action1, col_action2, col_action3 = st.columns(3)
        
        with col_action1:
            if st.button("📊 Export Filtered", use_container_width=True):
                csv = filtered_df.to_csv(index=False).encode('utf-8')
                st.download_button(
                    "⬇️ Download Filtered CSV",
                    csv,
                    file_name=f"filtered_{selected_file.name}",
                    mime="text/csv",
                    use_container_width=True
                )
        
        with col_action2:
            if st.button("📋 Copy to Clipboard", use_container_width=True):
                st.info("💡 Use Ctrl+C to copy the table above")
        
        with col_action3:
            if st.button("🔄 Refresh Data", use_container_width=True):
                st.rerun()
        
        # Low confidence alerts
        if 'confidence_score' in df.columns:
            low_conf_df = df[df['confidence_score'] < 0.70]
            
            if not low_conf_df.empty:
                st.markdown("---")
                st.markdown("### ⚠️ Alerts - Low Confidence")
                
                st.warning(f"""
                **{len(low_conf_df)} extraction(s) with confidence below 70%**
                
                These extractions should be manually reviewed before importing into Dynamics GP.
                """)
                
                with st.expander("View low confidence extraction details"):
                    st.dataframe(low_conf_df, use_container_width=True)
        
    except Exception as e:
        st.error(f"❌ Error loading file: {str(e)}")
        st.exception(e)
    
    st.markdown("---")
    
    # System logs section
    st.markdown("### 📜 System Logs")
    
    logs_dir = Path("logs")
    if logs_dir.exists():
        log_files = sorted(logs_dir.glob("iban_extraction_*.log"), 
                          key=lambda x: x.stat().st_mtime, 
                          reverse=True)[:5]
        
        if log_files:
            selected_log = st.selectbox(
                "Select a log file:",
                [f.name for f in log_files]
            )
            
            selected_log_path = logs_dir / selected_log
            
            if st.button("📖 View Log"):
                try:
                    with open(selected_log_path, 'r', encoding='utf-8') as f:
                        log_content = f.read()
                    
                    st.text_area(
                        "Log Content:",
                        log_content,
                        height=300,
                        help="Last lines of log file"
                    )
                except Exception as e:
                    st.error(f"❌ Error reading log: {str(e)}")
        else:
            st.info("📭 No log files found")
    else:
        st.warning("⚠️ Log directory not found")
