"""
Configuration settings for MSA Contract Review Assistant.

This module contains all configuration constants and settings used throughout the application.
"""

import os
from typing import List


class AppConfig:
    """Application configuration constants."""
    
    # Application metadata
    APP_TITLE = "MSA Contract Review Assistant"
    APP_ICON = "📋"
    PAGE_LAYOUT = "wide"
    SIDEBAR_STATE = "expanded"
    
    # File processing settings
    SUPPORTED_FILE_FORMATS = ['pdf', 'docx', 'txt']
    MAX_AMENDMENTS = 10
    MIN_AMENDMENTS = 1
    DEFAULT_AMENDMENTS = 1
    
    # LLM settings
    DEFAULT_MODEL = "gpt-3.5-turbo"
    DEFAULT_TEMPERATURE = 0.2
    
    # UI settings
    UPLOAD_HELP_TEXT = {
        'master': "Upload the original Master Service Agreement",
        'amendment': "Upload Amendment {number} document"
    }
    
    # Session state keys
    SESSION_KEYS = {
        'master_contract_text': 'master_contract_text',
        'amendments_data': 'amendments_data',
        'master_analysis': 'master_analysis',
        'amendments_analysis': 'amendments_analysis',
        'comprehensive_summary': 'comprehensive_summary',
        'analysis_complete': 'analysis_complete',
        'run_analysis': 'run_analysis'
    }
    
    @staticmethod
    def get_supported_formats() -> List[str]:
        """Get list of supported file formats."""
        return AppConfig.SUPPORTED_FILE_FORMATS.copy()
    
    @staticmethod
    def get_openai_api_key() -> str:
        """Get OpenAI API key from environment."""
        return os.getenv("OPENAI_API_KEY", "")
    
    @staticmethod
    def validate_environment() -> tuple[bool, str]:
        """Validate environment configuration."""
        api_key = AppConfig.get_openai_api_key()
        if not api_key:
            return False, "OpenAI API key not found in environment variables"
        return True, "Environment configuration is valid"


class UIMessages:
    """UI message constants."""
    
    # Error messages
    ERRORS = {
        'no_api_key': "⚠️ OpenAI API key not found. Please set OPENAI_API_KEY in your environment variables or .env file.",
        'invalid_api_key': "⚠️ Invalid OpenAI API key. Please check your API key and try again.",
        'missing_files': "Please upload the master contract and all amendment documents before starting analysis.",
        'processing_error': "Error processing {file_type}: {error}",
        'analysis_error': "An error occurred during analysis: {error}",
        'api_check_error': "Please check your OpenAI API key and try again."
    }
    
    # Success messages
    SUCCESS = {
        'file_uploaded': "Master contract uploaded: {filename}",
        'amendment_uploaded': "Amendment {number} uploaded: {filename}",
        'analysis_complete': "Analysis completed! Check the Summary Report tab for comprehensive insights."
    }
    
    # Info messages
    INFO = {
        'upload_prompt': "👆 Please upload documents and click 'Start Analysis' in the Document Upload tab.",
        'complete_analysis': "📈 Complete the analysis in the previous tabs to view the comprehensive summary report."
    }
    
    # Processing messages
    PROCESSING = {
        'master_contract': "Processing master contract...",
        'amendment': "Processing Amendment {number}...",
        'analyzing_master': "Analyzing master contract terms...",
        'comparing_amendment': "Comparing Amendment {number} with Master Contract...",
        'generating_summary': "Generating comprehensive summary..."
    }


class PromptTemplates:
    """LLM prompt templates."""
    
    CONTRACT_ANALYSIS = """
    You are a legal contract analyst. Analyze the following contract and extract key terms including:
    
    1. Payment terms and amounts
    2. Service scope and deliverables
    3. Timeline and milestones
    4. Termination clauses
    5. Liability and indemnification
    6. Intellectual property rights
    7. Confidentiality provisions
    8. Dispute resolution mechanisms
    9. Governing law
    10. Any other significant contractual obligations
    
    Present the analysis in a clear, structured format with bullet points for each category.
    
    Contract Text:
    {contract_text}
    
    Key Terms Analysis:
    """
    
    CONTRACT_COMPARISON = """
    You are a legal contract analyst comparing a master contract with its amendment.
    
    Analyze the differences between the Master Contract and Amendment {amendment_number} and identify:
    
    1. NEW terms or clauses added in the amendment
    2. MODIFIED terms or clauses that changed from the master contract
    3. DELETED terms or clauses removed in the amendment
    4. Impact of these changes on the overall agreement
    5. Risk assessment of the changes
    
    Present your analysis in this format:
    
    ## Amendment {amendment_number} Analysis
    
    ### NEW Terms Added:
    - [List new terms with details]
    
    ### MODIFIED Terms:
    - [List modified terms with before/after comparison]
    
    ### DELETED Terms:
    - [List any removed terms]
    
    ### Impact Assessment:
    - [Describe overall impact of changes]
    
    ### Risk Analysis:
    - [Identify potential risks or benefits]
    
    Master Contract:
    {master_contract}
    
    Amendment {amendment_number}:
    {amendment_contract}
    
    Analysis:
    """
    
    COMPREHENSIVE_SUMMARY = """
    You are a senior legal analyst preparing an executive summary of contract amendments.
    
    Based on the master contract and all amendment analyses provided, create a comprehensive summary that includes:
    
    1. **Executive Summary**: High-level overview of all changes
    2. **Key Changes Timeline**: Chronological summary of major modifications
    3. **Financial Impact**: Summary of all financial term changes
    4. **Risk Assessment**: Overall risk profile changes
    5. **Compliance Considerations**: Any regulatory or compliance impacts
    6. **Recommendations**: Suggested actions or considerations
    
    Present this as a professional executive report suitable for leadership review.
    
    Master Contract Summary:
    [Provide a brief overview of the original agreement]
    
    All Amendments Analysis:
    {amendments_analysis}
    
    Comprehensive Summary Report:
    """