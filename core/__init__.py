"""
Core business logic modules for MSA Contract Review Assistant.

This package contains the business logic separated from the UI:
- DocumentProcessor: Handles document processing and text extraction
- MSAAnalyzer: Handles contract analysis using LLM
"""

from .document_processor import DocumentProcessor
from .msa_analyzer import MSAAnalyzer

__all__ = ['DocumentProcessor', 'MSAAnalyzer']