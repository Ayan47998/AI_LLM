# 📋 Document Comparison Tool

A powerful Streamlit web application for comparing two documents with advanced similarity analysis and multiple viewing modes.

## ✨ Features

### 📄 Multiple Input Methods
- **File Upload**: Support for TXT, PDF, and DOCX files
- **Direct Text Input**: Copy and paste text directly into the interface

### 🔍 Comparison Modes
- **Side-by-Side**: View documents alongside each other
- **Inline Diff**: Traditional diff view with line-by-line changes
- **Similarity Only**: Focus on similarity metrics without full text display

### 📊 Advanced Analytics
- **Cosine Similarity**: Semantic similarity using TF-IDF vectors
- **Character Similarity**: Character-level comparison ratio
- **Word Similarity**: Overlap analysis of unique words
- **Word-Level Analysis**: Shows unique and common words between documents

### ⚙️ Customizable Settings
- Case sensitive/insensitive comparison
- Whitespace normalization options
- Difference highlighting
- Multiple comparison algorithms

### 🎨 Modern UI/UX
- Clean, responsive design
- Intuitive tabbed interface
- Real-time similarity scoring
- Color-coded similarity levels
- Expandable sections for detailed analysis

## 🚀 Getting Started

### Prerequisites
- Python 3.7 or higher
- pip package manager

### Installation

1. **Clone or download the project files**

2. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

3. **Run the application**:
   ```bash
   streamlit run document_comparison_app.py
   ```

4. **Open your browser** and navigate to the displayed URL (typically `http://localhost:8501`)

## 💡 How to Use

### Method 1: File Upload
1. Go to the **"📄 Upload Files"** tab
2. Upload your first document using the "Document 1" uploader
3. Upload your second document using the "Document 2" uploader
4. Switch to the **"📊 Results"** tab to see the comparison

### Method 2: Direct Text Input
1. Go to the **"✏️ Text Input"** tab
2. Paste or type your first document's text in the left text area
3. Paste or type your second document's text in the right text area
4. Switch to the **"📊 Results"** tab to see the comparison

### Customizing Comparison
- Use the **sidebar settings** to adjust comparison parameters:
  - Choose between Side-by-side, Inline Diff, or Similarity Only modes
  - Toggle case sensitivity
  - Enable/disable whitespace normalization
  - Turn on/off difference highlighting

## 📈 Understanding the Results

### Similarity Metrics
- **Cosine Similarity** (0-1): Measures semantic similarity using TF-IDF vectors
- **Character Similarity** (0-1): Character-level similarity ratio
- **Word Similarity** (0-1): Ratio of common words to total unique words

### Similarity Levels
- 🟢 **High Similarity**: Score ≥ 0.8 (Documents are very similar)
- 🟡 **Medium Similarity**: Score 0.5-0.8 (Documents have moderate similarity)
- 🔴 **Low Similarity**: Score < 0.5 (Documents are quite different)

### Word-Level Analysis
- **Unique to Document 1**: Words that appear only in the first document
- **Unique to Document 2**: Words that appear only in the second document
- **Common Words**: Words that appear in both documents

## 🔧 Supported File Formats

| Format | Extension | Notes |
|--------|-----------|-------|
| Plain Text | `.txt` | Direct text processing |
| PDF | `.pdf` | Requires PyPDF2 (auto-installed) |
| Word Documents | `.docx` | Requires python-docx (auto-installed) |

## 🛠️ Technical Details

### Dependencies
- **Streamlit**: Web application framework
- **scikit-learn**: TF-IDF vectorization and cosine similarity
- **NLTK**: Natural language processing utilities
- **PyPDF2**: PDF text extraction
- **python-docx**: Word document processing
- **difflib**: Built-in Python library for text differences

### Performance
- Optimized for documents up to several hundred pages
- Real-time processing for text input
- Efficient similarity calculations using vectorized operations

## 🤝 Contributing

Feel free to contribute improvements, bug fixes, or new features! The code is designed to be modular and extensible.

## 📝 License

This project is open source and available under the MIT License.

## 🆘 Troubleshooting

### Common Issues

**File upload not working**: 
- Ensure your file is in a supported format (TXT, PDF, DOCX)
- Check that the file size is reasonable (< 200MB)

**PDF text extraction issues**:
- Some PDFs may have text as images - these require OCR (not currently supported)
- Complex formatting may affect text extraction quality

**Slow performance**:
- Very large documents may take longer to process
- Consider using the "Similarity Only" mode for faster results

### Getting Help
If you encounter issues, please check:
1. All dependencies are properly installed
2. Your file formats are supported
3. Python version is 3.7 or higher

---

**Built with ❤️ using Streamlit | Document Comparison Tool v1.0**