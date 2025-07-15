import streamlit as st
import os
import io
from typing import List, Dict, Any
from datetime import datetime
import PyPDF2
import docx
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Configure Streamlit page
st.set_page_config(
    page_title="MSA Contract Review Assistant",
    page_icon="📋",
    layout="wide",
    initial_sidebar_state="expanded"
)

class DocumentProcessor:
    """Class to handle document processing and text extraction."""
    
    @staticmethod
    def extract_text_from_pdf(uploaded_file) -> str:
        """Extract text from PDF file."""
        try:
            pdf_reader = PyPDF2.PdfReader(uploaded_file)
            text = ""
            for page in pdf_reader.pages:
                text += page.extract_text() + "\n"
            return text
        except Exception as e:
            st.error(f"Error reading PDF: {str(e)}")
            return ""
    
    @staticmethod
    def extract_text_from_docx(uploaded_file) -> str:
        """Extract text from DOCX file."""
        try:
            doc = docx.Document(uploaded_file)
            text = ""
            for paragraph in doc.paragraphs:
                text += paragraph.text + "\n"
            return text
        except Exception as e:
            st.error(f"Error reading DOCX: {str(e)}")
            return ""
    
    @staticmethod
    def extract_text_from_txt(uploaded_file) -> str:
        """Extract text from TXT file."""
        try:
            content = uploaded_file.read()
            if isinstance(content, bytes):
                content = content.decode('utf-8')
            return content
        except Exception as e:
            st.error(f"Error reading TXT: {str(e)}")
            return ""
    
    @classmethod
    def extract_text(cls, uploaded_file) -> str:
        """Extract text from uploaded file based on file type."""
        if uploaded_file is None:
            return ""
        
        file_extension = uploaded_file.name.split('.')[-1].lower()
        
        if file_extension == 'pdf':
            return cls.extract_text_from_pdf(uploaded_file)
        elif file_extension == 'docx':
            return cls.extract_text_from_docx(uploaded_file)
        elif file_extension == 'txt':
            return cls.extract_text_from_txt(uploaded_file)
        else:
            st.error(f"Unsupported file format: {file_extension}")
            return ""

class MSAAnalyzer:
    """Class to handle MSA analysis using LLM."""
    
    def __init__(self):
        """Initialize the LLM."""
        self.llm = ChatOpenAI(
            model="gpt-3.5-turbo",
            temperature=0.2,
            openai_api_key=os.getenv("OPENAI_API_KEY")
        )
        self.output_parser = StrOutputParser()
    
    def analyze_contract_terms(self, contract_text: str) -> str:
        """Extract key terms from a contract."""
        prompt = ChatPromptTemplate.from_template("""
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
        """)
        
        chain = prompt | self.llm | self.output_parser
        return chain.invoke({"contract_text": contract_text})
    
    def compare_contracts(self, master_contract: str, amendment_contract: str, amendment_number: int) -> str:
        """Compare master contract with amendment and identify changes."""
        prompt = ChatPromptTemplate.from_template("""
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
        """)
        
        chain = prompt | self.llm | self.output_parser
        return chain.invoke({
            "master_contract": master_contract,
            "amendment_contract": amendment_contract,
            "amendment_number": amendment_number
        })
    
    def generate_comprehensive_summary(self, master_contract: str, amendments_analysis: List[str]) -> str:
        """Generate a comprehensive summary of all changes across amendments."""
        amendments_text = "\n\n".join([f"Amendment {i+1} Analysis:\n{analysis}" 
                                     for i, analysis in enumerate(amendments_analysis)])
        
        prompt = ChatPromptTemplate.from_template("""
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
        """)
        
        chain = prompt | self.llm | self.output_parser
        return chain.invoke({"amendments_analysis": amendments_text})

def main():
    """Main Streamlit application."""
    
    # Header
    st.title("📋 MSA Contract Review Assistant")
    st.markdown("""
    This application helps you review Master Service Agreements (MSAs) along with their amendments, 
    providing detailed analysis of changes and their implications using AI-powered analysis.
    """)
    
    # Check for OpenAI API key
    if not os.getenv("OPENAI_API_KEY"):
        st.error("⚠️ OpenAI API key not found. Please set OPENAI_API_KEY in your environment variables or .env file.")
        st.stop()
    
    # Initialize components
    doc_processor = DocumentProcessor()
    analyzer = MSAAnalyzer()
    
    # Sidebar for configuration
    with st.sidebar:
        st.header("📁 Upload Configuration")
        
        # Number of amendments
        num_amendments = st.number_input(
            "Number of Amendments/Sub-contracts",
            min_value=1,
            max_value=10,
            value=1,
            help="Select how many amendment documents you want to upload"
        )
        
        st.markdown("---")
        st.markdown("### Supported File Formats")
        st.markdown("• PDF (.pdf)")
        st.markdown("• Word Document (.docx)")
        st.markdown("• Text File (.txt)")
    
    # Main content area
    tab1, tab2, tab3 = st.tabs(["📄 Document Upload", "🔍 Analysis", "📊 Summary Report"])
    
    with tab1:
        st.header("Document Upload")
        
        # Master Contract Upload
        st.subheader("1. Upload Master Service Agreement (MSA)")
        master_contract_file = st.file_uploader(
            "Choose MSA file",
            type=['pdf', 'docx', 'txt'],
            key="master_contract",
            help="Upload the original Master Service Agreement"
        )
        
        if master_contract_file:
            st.success(f"✅ Master contract uploaded: {master_contract_file.name}")
            if 'master_contract_text' not in st.session_state:
                with st.spinner("Processing master contract..."):
                    st.session_state.master_contract_text = doc_processor.extract_text(master_contract_file)
        
        # Amendments Upload
        st.subheader("2. Upload Amendment Documents")
        
        if 'amendments_data' not in st.session_state:
            st.session_state.amendments_data = {}
        
        for i in range(num_amendments):
            amendment_key = f"amendment_{i+1}"
            st.markdown(f"**Amendment {i+1}:**")
            
            amendment_file = st.file_uploader(
                f"Choose Amendment {i+1} file",
                type=['pdf', 'docx', 'txt'],
                key=f"amendment_file_{i+1}",
                help=f"Upload Amendment {i+1} document"
            )
            
            if amendment_file:
                st.success(f"✅ Amendment {i+1} uploaded: {amendment_file.name}")
                if amendment_key not in st.session_state.amendments_data:
                    with st.spinner(f"Processing Amendment {i+1}..."):
                        amendment_text = doc_processor.extract_text(amendment_file)
                        st.session_state.amendments_data[amendment_key] = {
                            'filename': amendment_file.name,
                            'text': amendment_text
                        }
        
        # Process button
        if st.button("🚀 Start Analysis", type="primary"):
            if master_contract_file and len(st.session_state.amendments_data) == num_amendments:
                st.session_state.analysis_complete = False
                st.session_state.run_analysis = True
                st.rerun()
            else:
                st.error("Please upload the master contract and all amendment documents before starting analysis.")
    
    with tab2:
        st.header("Contract Analysis")
        
        if hasattr(st.session_state, 'run_analysis') and st.session_state.run_analysis:
            try:
                # Master Contract Analysis
                st.subheader("📋 Master Contract Analysis")
                with st.spinner("Analyzing master contract terms..."):
                    master_analysis = analyzer.analyze_contract_terms(st.session_state.master_contract_text)
                    st.session_state.master_analysis = master_analysis
                
                with st.expander("View Master Contract Key Terms", expanded=True):
                    st.markdown(master_analysis)
                
                # Amendment Analysis
                st.subheader("🔍 Amendment Analysis")
                amendments_analysis = []
                
                for i, (amendment_key, amendment_data) in enumerate(st.session_state.amendments_data.items()):
                    st.markdown(f"**Analyzing Amendment {i+1}: {amendment_data['filename']}**")
                    
                    with st.spinner(f"Comparing Amendment {i+1} with Master Contract..."):
                        comparison = analyzer.compare_contracts(
                            st.session_state.master_contract_text,
                            amendment_data['text'],
                            i+1
                        )
                        amendments_analysis.append(comparison)
                    
                    with st.expander(f"View Amendment {i+1} Analysis", expanded=False):
                        st.markdown(comparison)
                
                st.session_state.amendments_analysis = amendments_analysis
                st.session_state.analysis_complete = True
                st.success("✅ Analysis completed! Check the Summary Report tab for comprehensive insights.")
                
            except Exception as e:
                st.error(f"An error occurred during analysis: {str(e)}")
                st.error("Please check your OpenAI API key and try again.")
        
        elif not hasattr(st.session_state, 'run_analysis'):
            st.info("👆 Please upload documents and click 'Start Analysis' in the Document Upload tab.")
    
    with tab3:
        st.header("Executive Summary Report")
        
        if hasattr(st.session_state, 'analysis_complete') and st.session_state.analysis_complete:
            st.subheader("📊 Comprehensive Contract Review Summary")
            
            with st.spinner("Generating comprehensive summary..."):
                comprehensive_summary = analyzer.generate_comprehensive_summary(
                    st.session_state.master_contract_text,
                    st.session_state.amendments_analysis
                )
                st.session_state.comprehensive_summary = comprehensive_summary
            
            st.markdown(comprehensive_summary)
            
            # Download option
            st.markdown("---")
            col1, col2 = st.columns(2)
            
            with col1:
                # Generate downloadable report
                report_content = f"""
# MSA Contract Review Report
Generated on: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

## Master Contract Key Terms
{st.session_state.master_analysis}

## Individual Amendment Analyses
{chr(10).join([f'### Amendment {i+1}{chr(10)}{analysis}' for i, analysis in enumerate(st.session_state.amendments_analysis)])}

## Comprehensive Summary
{comprehensive_summary}
"""
                
                st.download_button(
                    label="📥 Download Full Report",
                    data=report_content,
                    file_name=f"msa_review_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.md",
                    mime="text/markdown"
                )
            
            with col2:
                if st.button("🔄 Start New Analysis"):
                    # Clear session state for new analysis
                    for key in list(st.session_state.keys()):
                        del st.session_state[key]
                    st.rerun()
        
        else:
            st.info("📈 Complete the analysis in the previous tabs to view the comprehensive summary report.")

if __name__ == "__main__":
    main()