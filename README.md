# MSA Contract Review Assistant 📋

A Streamlit-based application that helps you review Master Service Agreements (MSAs) along with their amendments, providing detailed AI-powered analysis of changes and their implications.

## Features ✨

- **Document Upload**: Support for PDF, DOCX, and TXT file formats
- **Multi-Amendment Analysis**: Upload and analyze multiple amendments/sub-contracts
- **AI-Powered Analysis**: Uses OpenAI's GPT models via LangChain for intelligent contract analysis
- **Comprehensive Comparison**: Identifies new, modified, and deleted terms between master contract and amendments
- **Executive Summary**: Generates professional reports suitable for leadership review
- **Risk Assessment**: Analyzes potential risks and implications of contract changes
- **Downloadable Reports**: Export complete analysis as markdown files

## Setup Instructions 🚀

### 1. Install Dependencies

```bash
pip install -r requirements.txt
```

### 2. Environment Setup

1. Copy the environment template:
   ```bash
   cp .env.template .env
   ```

2. Edit the `.env` file and add your OpenAI API key:
   ```
   OPENAI_API_KEY=your_actual_openai_api_key_here
   ```

   To get an OpenAI API key:
   - Visit [OpenAI API](https://platform.openai.com/api-keys)
   - Create an account or log in
   - Generate a new API key
   - Make sure you have sufficient credits/billing set up

### 3. Run the Application

```bash
streamlit run msa_review_app.py
```

The application will open in your default web browser at `http://localhost:8501`

## How to Use 📖

### Step 1: Configure Upload
- In the sidebar, select the number of amendments/sub-contracts you want to analyze (1-10)

### Step 2: Upload Documents
- **Master Contract**: Upload your original MSA document
- **Amendments**: Upload each amendment document one by one
- Supported formats: PDF, DOCX, TXT

### Step 3: Start Analysis
- Click "🚀 Start Analysis" to begin the AI-powered review process
- The system will:
  - Extract key terms from the master contract
  - Compare each amendment with the master contract
  - Identify changes, additions, and deletions

### Step 4: Review Results
- **Analysis Tab**: View detailed comparisons for each amendment
- **Summary Report Tab**: Get a comprehensive executive summary
- Download the complete report as a markdown file

## Analysis Features 🔍

### Master Contract Analysis
- Payment terms and amounts
- Service scope and deliverables
- Timeline and milestones
- Termination clauses
- Liability and indemnification
- Intellectual property rights
- Confidentiality provisions
- Dispute resolution mechanisms
- Governing law
- Other significant contractual obligations

### Amendment Comparison
For each amendment, the system identifies:
- **NEW Terms**: Clauses added in the amendment
- **MODIFIED Terms**: Changes from the original contract
- **DELETED Terms**: Clauses removed in the amendment
- **Impact Assessment**: Overall impact of changes
- **Risk Analysis**: Potential risks or benefits

### Comprehensive Summary
- Executive overview of all changes
- Chronological timeline of modifications
- Financial impact summary
- Risk assessment across all amendments
- Compliance considerations
- Actionable recommendations

## File Format Support 📄

| Format | Extension | Notes |
|--------|-----------|-------|
| PDF | `.pdf` | Supports text-based PDFs (not scanned images) |
| Word Document | `.docx` | Modern Word format |
| Text File | `.txt` | Plain text documents |

## Technical Requirements 💻

- Python 3.8+
- OpenAI API key with sufficient credits
- Internet connection for API calls
- Modern web browser

## Cost Considerations 💰

- The application uses OpenAI's GPT-3.5-turbo model
- Cost depends on document length and number of amendments
- Typical analysis costs range from $0.10-$2.00 per document set
- Monitor your OpenAI usage at [OpenAI Usage Dashboard](https://platform.openai.com/usage)

## Security & Privacy 🔒

- Documents are processed locally and sent to OpenAI for analysis
- No documents are stored permanently by the application
- Review OpenAI's [data usage policies](https://openai.com/policies/api-data-usage-policies)
- For sensitive documents, consider using local LLMs or ensure compliance with your organization's data policies

## Troubleshooting 🛠️

### Common Issues:

1. **"OpenAI API key not found"**
   - Ensure you've created a `.env` file with your API key
   - Check that the key is correctly formatted

2. **"Error reading PDF"**
   - Ensure the PDF contains selectable text (not scanned images)
   - Try converting scanned PDFs to text-searchable format first

3. **"An error occurred during analysis"**
   - Check your internet connection
   - Verify your OpenAI API key has sufficient credits
   - Try with smaller documents if hitting token limits

4. **Slow performance**
   - Large documents take longer to process
   - Consider breaking very large contracts into sections

### Support

For technical issues:
1. Check the error messages in the application
2. Verify your OpenAI API setup
3. Ensure all dependencies are properly installed

## License 📝

This project is provided as-is for educational and professional use. Please ensure compliance with your organization's policies when using with sensitive documents.

---

**Note**: This application is designed to assist in contract review but should not replace professional legal advice. Always consult with qualified legal professionals for important contract decisions.