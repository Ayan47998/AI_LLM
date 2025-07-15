"""
MSA Contract Review Assistant - Main Application

This is the main entry point that orchestrates the business logic and UI components.
The application architecture is separated into:
- core/: Business logic (DocumentProcessor, MSAAnalyzer)
- ui/: User interface components and pages
- app.py: Main application orchestration
"""

import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Import core business logic
from core import DocumentProcessor, MSAAnalyzer

# Import UI components
from ui import UIComponents, MSAReviewPages

# Import configuration
from config import AppConfig, UIMessages


def main():
    """Main Streamlit application entry point."""
    
    # Initialize UI components
    ui = UIComponents()
    
    # Setup page configuration
    ui.setup_page_config()
    
    # Render header
    ui.render_header()
    
    # Check for OpenAI API key
    if not AppConfig.get_openai_api_key():
        ui.render_api_key_error()
        return
    
    try:
        # Initialize core components
        doc_processor = DocumentProcessor()
        analyzer = MSAAnalyzer()
        
        # Validate API key
        if not analyzer.validate_api_key():
            ui.render_error_message(UIMessages.ERRORS['invalid_api_key'])
            return
        
    except Exception as e:
        ui.render_error_message(f"⚠️ Error initializing application: {str(e)}")
        return
    
    # Initialize page controller
    pages = MSAReviewPages(doc_processor, analyzer)
    
    # Render sidebar
    num_amendments = ui.render_sidebar(doc_processor.get_supported_formats())
    
    # Render main application tabs
    tab1, tab2, tab3 = ui.render_tabs()
    
    # Document Upload Tab
    with tab1:
        pages.render_upload_tab(num_amendments)
    
    # Analysis Tab
    with tab2:
        pages.render_analysis_tab()
    
    # Summary Report Tab
    with tab3:
        pages.render_summary_tab()


if __name__ == "__main__":
    main()