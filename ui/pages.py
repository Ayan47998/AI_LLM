import streamlit as st
from datetime import datetime
from typing import Dict, Any, List, Optional

from .components import UIComponents
from core import DocumentProcessor, MSAAnalyzer
from config import AppConfig, UIMessages


class MSAReviewPages:
    """Page controllers for the MSA Contract Review application."""
    
    def __init__(self, doc_processor: DocumentProcessor, analyzer: MSAAnalyzer):
        self.doc_processor = doc_processor
        self.analyzer = analyzer
        self.ui = UIComponents()
    
    def render_upload_tab(self, num_amendments: int) -> bool:
        """Render the document upload tab and return if analysis should start."""
        self.ui.render_subheader("Document Upload")
        
        # Master Contract Upload
        self.ui.render_subheader("1. Upload Master Service Agreement (MSA)")
        master_contract_file = self.ui.render_file_uploader(
            "Choose MSA file",
            "master_contract",
            "Upload the original Master Service Agreement",
            self.doc_processor.get_supported_formats()
        )
        
        if master_contract_file:
            self.ui.render_success_message(f"Master contract uploaded: {master_contract_file.name}")
            if 'master_contract_text' not in st.session_state:
                try:
                    with self.ui.render_spinner("Processing master contract..."):
                        st.session_state.master_contract_text = self.doc_processor.extract_text(master_contract_file)
                except Exception as e:
                    self.ui.render_error_message(f"Error processing master contract: {str(e)}")
                    return False
        
        # Amendments Upload
        self.ui.render_subheader("2. Upload Amendment Documents")
        
        if 'amendments_data' not in st.session_state:
            st.session_state.amendments_data = {}
        
        for i in range(num_amendments):
            amendment_key = f"amendment_{i+1}"
            self.ui.render_markdown(f"**Amendment {i+1}:**")
            
            amendment_file = self.ui.render_file_uploader(
                f"Choose Amendment {i+1} file",
                f"amendment_file_{i+1}",
                f"Upload Amendment {i+1} document",
                self.doc_processor.get_supported_formats()
            )
            
            if amendment_file:
                self.ui.render_success_message(f"Amendment {i+1} uploaded: {amendment_file.name}")
                if amendment_key not in st.session_state.amendments_data:
                    try:
                        with self.ui.render_spinner(f"Processing Amendment {i+1}..."):
                            amendment_text = self.doc_processor.extract_text(amendment_file)
                            st.session_state.amendments_data[amendment_key] = {
                                'filename': amendment_file.name,
                                'text': amendment_text
                            }
                    except Exception as e:
                        self.ui.render_error_message(f"Error processing Amendment {i+1}: {str(e)}")
                        return False
        
        # Process button
        if self.ui.render_button("🚀 Start Analysis", "primary"):
            if master_contract_file and len(st.session_state.amendments_data) == num_amendments:
                st.session_state.analysis_complete = False
                st.session_state.run_analysis = True
                st.rerun()
                return True
            else:
                self.ui.render_error_message("Please upload the master contract and all amendment documents before starting analysis.")
                return False
        
        return False
    
    def render_analysis_tab(self) -> bool:
        """Render the analysis tab and perform analysis if requested."""
        self.ui.render_subheader("Contract Analysis")
        
        if hasattr(st.session_state, 'run_analysis') and st.session_state.run_analysis:
            try:
                # Master Contract Analysis
                self.ui.render_subheader("📋 Master Contract Analysis")
                with self.ui.render_spinner("Analyzing master contract terms..."):
                    master_analysis = self.analyzer.analyze_contract_terms(st.session_state.master_contract_text)
                    st.session_state.master_analysis = master_analysis
                
                self.ui.render_analysis_section("View Master Contract Key Terms", master_analysis, expanded=True)
                
                # Amendment Analysis
                self.ui.render_subheader("🔍 Amendment Analysis")
                amendments_analysis = []
                
                for i, (amendment_key, amendment_data) in enumerate(st.session_state.amendments_data.items()):
                    self.ui.render_markdown(f"**Analyzing Amendment {i+1}: {amendment_data['filename']}**")
                    
                    with self.ui.render_spinner(f"Comparing Amendment {i+1} with Master Contract..."):
                        comparison = self.analyzer.compare_contracts(
                            st.session_state.master_contract_text,
                            amendment_data['text'],
                            i+1
                        )
                        amendments_analysis.append(comparison)
                    
                    self.ui.render_analysis_section(f"View Amendment {i+1} Analysis", comparison, expanded=False)
                
                st.session_state.amendments_analysis = amendments_analysis
                st.session_state.analysis_complete = True
                self.ui.render_success_message("Analysis completed! Check the Summary Report tab for comprehensive insights.")
                return True
                
            except Exception as e:
                self.ui.render_error_message(f"An error occurred during analysis: {str(e)}")
                self.ui.render_error_message("Please check your OpenAI API key and try again.")
                return False
        
        elif not hasattr(st.session_state, 'run_analysis'):
            self.ui.render_info_message("👆 Please upload documents and click 'Start Analysis' in the Document Upload tab.")
        
        return False
    
    def render_summary_tab(self):
        """Render the summary report tab."""
        self.ui.render_subheader("Executive Summary Report")
        
        if hasattr(st.session_state, 'analysis_complete') and st.session_state.analysis_complete:
            self.ui.render_subheader("📊 Comprehensive Contract Review Summary")
            
            # Generate comprehensive summary if not already done
            if 'comprehensive_summary' not in st.session_state:
                with self.ui.render_spinner("Generating comprehensive summary..."):
                    comprehensive_summary = self.analyzer.generate_comprehensive_summary(
                        st.session_state.master_contract_text,
                        st.session_state.amendments_analysis
                    )
                    st.session_state.comprehensive_summary = comprehensive_summary
            
            self.ui.render_markdown(st.session_state.comprehensive_summary)
            
            # Download and reset options
            self.ui.render_markdown("---")
            col1, col2 = self.ui.render_columns(2)
            
            with col1:
                # Generate downloadable report
                report_content = self.ui.generate_report_content(
                    st.session_state.master_analysis,
                    st.session_state.amendments_analysis,
                    st.session_state.comprehensive_summary
                )
                
                filename = f"msa_review_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.md"
                self.ui.render_download_button(report_content, filename)
            
            with col2:
                if self.ui.render_button("🔄 Start New Analysis"):
                    self._clear_session_state()
                    st.rerun()
        
        else:
            self.ui.render_info_message("📈 Complete the analysis in the previous tabs to view the comprehensive summary report.")
    
    def _clear_session_state(self):
        """Clear session state for new analysis."""
        keys_to_clear = [
            'master_contract_text', 'amendments_data', 'master_analysis',
            'amendments_analysis', 'comprehensive_summary', 'analysis_complete', 'run_analysis'
        ]
        for key in keys_to_clear:
            if key in st.session_state:
                del st.session_state[key]