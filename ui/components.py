import streamlit as st
from datetime import datetime
from typing import Dict, Any, List

from config import AppConfig, UIMessages


class UIComponents:
    """Reusable UI components for the MSA Contract Review application."""
    
    @staticmethod
    def setup_page_config():
        """Configure Streamlit page settings."""
        st.set_page_config(
            page_title=AppConfig.APP_TITLE,
            page_icon=AppConfig.APP_ICON,
            layout=AppConfig.PAGE_LAYOUT,
            initial_sidebar_state=AppConfig.SIDEBAR_STATE
        )
    
    @staticmethod
    def render_header():
        """Render the application header."""
        st.title(f"{AppConfig.APP_ICON} {AppConfig.APP_TITLE}")
        st.markdown("""
        This application helps you review Master Service Agreements (MSAs) along with their amendments, 
        providing detailed analysis of changes and their implications using AI-powered analysis.
        """)
    
    @staticmethod
    def render_sidebar(supported_formats: List[str]) -> int:
        """Render the sidebar configuration and return number of amendments."""
        with st.sidebar:
            st.header("📁 Upload Configuration")
            
            # Number of amendments
            num_amendments = st.number_input(
                "Number of Amendments/Sub-contracts",
                min_value=AppConfig.MIN_AMENDMENTS,
                max_value=AppConfig.MAX_AMENDMENTS,
                value=AppConfig.DEFAULT_AMENDMENTS,
                help="Select how many amendment documents you want to upload"
            )
            
            st.markdown("---")
            st.markdown("### Supported File Formats")
            for fmt in supported_formats:
                st.markdown(f"• {fmt.upper()} (.{fmt})")
        
        return num_amendments
    
    @staticmethod
    def render_api_key_error():
        """Render API key error message."""
        st.error(UIMessages.ERRORS['no_api_key'])
        st.stop()
    
    @staticmethod
    def render_file_uploader(label: str, key: str, help_text: str, supported_formats: List[str]):
        """Render a file uploader component."""
        return st.file_uploader(
            label,
            type=supported_formats,
            key=key,
            help=help_text
        )
    
    @staticmethod
    def render_success_message(message: str):
        """Render a success message."""
        st.success(f"✅ {message}")
    
    @staticmethod
    def render_error_message(message: str):
        """Render an error message."""
        st.error(message)
    
    @staticmethod
    def render_info_message(message: str):
        """Render an info message."""
        st.info(message)
    
    @staticmethod
    def render_analysis_section(title: str, content: str, expanded: bool = True):
        """Render an expandable analysis section."""
        with st.expander(title, expanded=expanded):
            st.markdown(content)
    
    @staticmethod
    def render_download_button(content: str, filename: str, label: str = "📥 Download Full Report"):
        """Render a download button for reports."""
        return st.download_button(
            label=label,
            data=content,
            file_name=filename,
            mime="text/markdown"
        )
    
    @staticmethod
    def generate_report_content(master_analysis: str, amendments_analysis: List[str], comprehensive_summary: str) -> str:
        """Generate downloadable report content."""
        return f"""
# MSA Contract Review Report
Generated on: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

## Master Contract Key Terms
{master_analysis}

## Individual Amendment Analyses
{chr(10).join([f'### Amendment {i+1}{chr(10)}{analysis}' for i, analysis in enumerate(amendments_analysis)])}

## Comprehensive Summary
{comprehensive_summary}
"""
    
    @staticmethod
    def render_tabs() -> tuple:
        """Render the main application tabs."""
        return st.tabs(["📄 Document Upload", "🔍 Analysis", "📊 Summary Report"])
    
    @staticmethod
    def render_spinner(message: str):
        """Render a spinner with message."""
        return st.spinner(message)
    
    @staticmethod
    def render_columns(num_columns: int) -> tuple:
        """Render columns layout."""
        return st.columns(num_columns)
    
    @staticmethod
    def render_button(label: str, button_type: str = "secondary", key: str = None) -> bool:
        """Render a button and return if it was clicked."""
        if button_type == "primary":
            return st.button(label, type="primary", key=key)
        else:
            return st.button(label, key=key)
    
    @staticmethod
    def render_subheader(text: str):
        """Render a subheader."""
        st.subheader(text)
    
    @staticmethod
    def render_markdown(text: str):
        """Render markdown text."""
        st.markdown(text)