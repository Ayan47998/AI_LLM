"""
UI modules for MSA Contract Review Assistant.

This package contains the user interface components separated from business logic:
- UIComponents: Reusable Streamlit UI components
- MSAReviewPages: Page controllers and state management
"""

from .components import UIComponents
from .pages import MSAReviewPages

__all__ = ['UIComponents', 'MSAReviewPages']