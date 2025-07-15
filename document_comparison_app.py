import streamlit as st
import difflib
import pandas as pd
from io import StringIO
import base64
from typing import Tuple, List
import re
import nltk
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np

# Download required NLTK data
try:
    nltk.data.find('tokenizers/punkt')
except LookupError:
    nltk.download('punkt')

def preprocess_text(text: str) -> str:
    """Clean and preprocess text for comparison."""
    # Remove extra whitespace and normalize line endings
    text = re.sub(r'\s+', ' ', text.strip())
    return text

def calculate_similarity_metrics(text1: str, text2: str) -> dict:
    """Calculate various similarity metrics between two texts."""
    # Text similarity using cosine similarity
    vectorizer = TfidfVectorizer(stop_words='english', ngram_range=(1, 2))
    try:
        tfidf_matrix = vectorizer.fit_transform([text1, text2])
        cosine_sim = cosine_similarity(tfidf_matrix[0:1], tfidf_matrix[1:2])[0][0]
    except:
        cosine_sim = 0.0
    
    # Character-level similarity
    char_similarity = difflib.SequenceMatcher(None, text1, text2).ratio()
    
    # Word-level similarity
    words1 = set(text1.lower().split())
    words2 = set(text2.lower().split())
    word_similarity = len(words1.intersection(words2)) / len(words1.union(words2)) if words1.union(words2) else 0
    
    return {
        "cosine_similarity": cosine_sim,
        "character_similarity": char_similarity,
        "word_similarity": word_similarity
    }

def get_text_diff_html(text1: str, text2: str) -> str:
    """Generate HTML diff between two texts."""
    d = difflib.HtmlDiff()
    diff_html = d.make_table(
        text1.splitlines(keepends=True),
        text2.splitlines(keepends=True),
        fromdesc="Document 1",
        todesc="Document 2",
        context=True,
        numlines=3
    )
    return diff_html

def extract_text_from_file(uploaded_file) -> str:
    """Extract text from uploaded file based on file type."""
    if uploaded_file is None:
        return ""
    
    file_extension = uploaded_file.name.split('.')[-1].lower()
    
    if file_extension == 'txt':
        return str(uploaded_file.read(), "utf-8")
    elif file_extension == 'pdf':
        try:
            import PyPDF2
            from io import BytesIO
            
            pdf_reader = PyPDF2.PdfReader(BytesIO(uploaded_file.read()))
            text = ""
            for page in pdf_reader.pages:
                text += page.extract_text() + "\n"
            return text
        except ImportError:
            st.error("PyPDF2 is required for PDF files. Please install it: pip install PyPDF2")
            return ""
    elif file_extension in ['docx', 'doc']:
        try:
            import docx
            from io import BytesIO
            
            doc = docx.Document(BytesIO(uploaded_file.read()))
            text = ""
            for paragraph in doc.paragraphs:
                text += paragraph.text + "\n"
            return text
        except ImportError:
            st.error("python-docx is required for Word files. Please install it: pip install python-docx")
            return ""
    else:
        st.error(f"Unsupported file type: {file_extension}")
        return ""

def main():
    st.set_page_config(
        page_title="Document Comparison Tool",
        page_icon="📋",
        layout="wide",
        initial_sidebar_state="expanded"
    )
    
    # Custom CSS for better styling
    st.markdown("""
    <style>
    .main {
        padding-top: 2rem;
    }
    .stMetric {
        background-color: #f0f2f6;
        border: 1px solid #e0e2e6;
        padding: 1rem;
        border-radius: 0.5rem;
        margin: 0.5rem 0;
    }
    .comparison-container {
        background-color: #fafafa;
        padding: 1rem;
        border-radius: 0.5rem;
        margin: 1rem 0;
    }
    .diff-stats {
        background: linear-gradient(90deg, #667eea 0%, #764ba2 100%);
        padding: 1rem;
        border-radius: 0.5rem;
        color: white;
        margin: 1rem 0;
    }
    </style>
    """, unsafe_allow_html=True)
    
    st.title("📋 Document Comparison Tool")
    st.markdown("Compare two documents side-by-side with advanced similarity analysis")
    
    # Sidebar for settings
    with st.sidebar:
        st.header("⚙️ Settings")
        comparison_mode = st.selectbox(
            "Comparison Mode",
            ["Side-by-side", "Inline Diff", "Similarity Only"],
            help="Choose how to display the comparison results"
        )
        
        highlight_differences = st.checkbox("Highlight Differences", value=True)
        case_sensitive = st.checkbox("Case Sensitive", value=False)
        ignore_whitespace = st.checkbox("Ignore Extra Whitespace", value=True)
        
        st.header("📊 Export Options")
        if st.button("Generate Report"):
            st.info("Report generation feature coming soon!")
    
    # Main content area
    tab1, tab2, tab3 = st.tabs(["📄 Upload Files", "✏️ Text Input", "📊 Results"])
    
    # Initialize session state
    if 'text1' not in st.session_state:
        st.session_state.text1 = ""
    if 'text2' not in st.session_state:
        st.session_state.text2 = ""
    
    with tab1:
        st.header("Upload Documents")
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.subheader("📄 Document 1")
            file1 = st.file_uploader(
                "Choose first document",
                type=['txt', 'pdf', 'docx'],
                key="file1"
            )
            if file1:
                st.session_state.text1 = extract_text_from_file(file1)
                st.success(f"✅ Loaded: {file1.name}")
                with st.expander("Preview"):
                    st.text_area("Content preview", st.session_state.text1[:500] + "...", height=100, disabled=True)
        
        with col2:
            st.subheader("📄 Document 2")
            file2 = st.file_uploader(
                "Choose second document",
                type=['txt', 'pdf', 'docx'],
                key="file2"
            )
            if file2:
                st.session_state.text2 = extract_text_from_file(file2)
                st.success(f"✅ Loaded: {file2.name}")
                with st.expander("Preview"):
                    st.text_area("Content preview", st.session_state.text2[:500] + "...", height=100, disabled=True)
    
    with tab2:
        st.header("Direct Text Input")
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.subheader("📝 Document 1")
            text1_input = st.text_area(
                "Enter or paste text for document 1",
                value=st.session_state.text1,
                height=300,
                key="text1_input"
            )
            if text1_input != st.session_state.text1:
                st.session_state.text1 = text1_input
        
        with col2:
            st.subheader("📝 Document 2")
            text2_input = st.text_area(
                "Enter or paste text for document 2",
                value=st.session_state.text2,
                height=300,
                key="text2_input"
            )
            if text2_input != st.session_state.text2:
                st.session_state.text2 = text2_input
    
    with tab3:
        st.header("Comparison Results")
        
        if st.session_state.text1 and st.session_state.text2:
            # Preprocess texts based on settings
            text1_processed = st.session_state.text1
            text2_processed = st.session_state.text2
            
            if not case_sensitive:
                text1_processed = text1_processed.lower()
                text2_processed = text2_processed.lower()
            
            if ignore_whitespace:
                text1_processed = preprocess_text(text1_processed)
                text2_processed = preprocess_text(text2_processed)
            
            # Calculate similarity metrics
            metrics = calculate_similarity_metrics(text1_processed, text2_processed)
            
            # Display metrics
            st.markdown('<div class="diff-stats">', unsafe_allow_html=True)
            st.subheader("📈 Similarity Metrics")
            st.markdown('</div>', unsafe_allow_html=True)
            
            col1, col2, col3 = st.columns(3)
            
            with col1:
                st.metric(
                    "Cosine Similarity",
                    f"{metrics['cosine_similarity']:.3f}",
                    help="Semantic similarity based on TF-IDF vectors"
                )
            
            with col2:
                st.metric(
                    "Character Similarity",
                    f"{metrics['character_similarity']:.3f}",
                    help="Character-level similarity ratio"
                )
            
            with col3:
                st.metric(
                    "Word Similarity",
                    f"{metrics['word_similarity']:.3f}",
                    help="Overlap of unique words"
                )
            
            # Overall similarity score
            overall_score = (metrics['cosine_similarity'] + metrics['character_similarity'] + metrics['word_similarity']) / 3
            
            if overall_score >= 0.8:
                st.success(f"🟢 High Similarity: {overall_score:.3f}")
            elif overall_score >= 0.5:
                st.warning(f"🟡 Medium Similarity: {overall_score:.3f}")
            else:
                st.error(f"🔴 Low Similarity: {overall_score:.3f}")
            
            st.divider()
            
            # Display comparison based on mode
            if comparison_mode == "Side-by-side":
                st.subheader("📖 Side-by-Side Comparison")
                
                col1, col2 = st.columns(2)
                
                with col1:
                    st.markdown("**Document 1**")
                    st.text_area("", st.session_state.text1, height=400, disabled=True, key="side1")
                
                with col2:
                    st.markdown("**Document 2**")
                    st.text_area("", st.session_state.text2, height=400, disabled=True, key="side2")
            
            elif comparison_mode == "Inline Diff":
                st.subheader("🔍 Inline Differences")
                
                # Generate unified diff
                diff = list(difflib.unified_diff(
                    text1_processed.splitlines(keepends=True),
                    text2_processed.splitlines(keepends=True),
                    fromfile="Document 1",
                    tofile="Document 2",
                    lineterm=""
                ))
                
                if diff:
                    diff_text = ''.join(diff)
                    st.code(diff_text, language="diff")
                else:
                    st.success("✅ No differences found!")
            
            # Word-level differences
            st.subheader("📝 Word-Level Analysis")
            
            words1 = set(text1_processed.lower().split())
            words2 = set(text2_processed.lower().split())
            
            col1, col2, col3 = st.columns(3)
            
            with col1:
                unique_to_doc1 = words1 - words2
                st.markdown("**Unique to Document 1**")
                if unique_to_doc1:
                    st.write(", ".join(sorted(list(unique_to_doc1)[:10])))
                    if len(unique_to_doc1) > 10:
                        st.caption(f"... and {len(unique_to_doc1) - 10} more")
                else:
                    st.write("None")
            
            with col2:
                unique_to_doc2 = words2 - words1
                st.markdown("**Unique to Document 2**")
                if unique_to_doc2:
                    st.write(", ".join(sorted(list(unique_to_doc2)[:10])))
                    if len(unique_to_doc2) > 10:
                        st.caption(f"... and {len(unique_to_doc2) - 10} more")
                else:
                    st.write("None")
            
            with col3:
                common_words = words1.intersection(words2)
                st.markdown("**Common Words**")
                if common_words:
                    st.write(f"{len(common_words)} words in common")
                    with st.expander("Show common words"):
                        st.write(", ".join(sorted(list(common_words)[:20])))
                else:
                    st.write("None")
        
        else:
            st.info("👆 Please upload or enter documents in the tabs above to see comparison results.")
    
    # Footer
    st.markdown("---")
    st.markdown("Built with ❤️ using Streamlit | Document Comparison Tool v1.0")

if __name__ == "__main__":
    main()