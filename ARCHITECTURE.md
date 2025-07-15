# MSA Contract Review Assistant - Architecture

This document describes the architecture of the MSA Contract Review Assistant after the separation of business logic and UI components.

## Project Structure

```
├── app.py                          # Main application entry point
├── msa_review_app.py              # Legacy monolithic application (for reference)
├── requirements.txt               # Python dependencies
├── .env                          # Environment variables (create this)
├── config/                       # Configuration package
│   ├── __init__.py
│   └── settings.py               # App settings, messages, and prompt templates
├── core/                         # Business logic package
│   ├── __init__.py
│   ├── document_processor.py     # Document processing and text extraction
│   └── msa_analyzer.py          # Contract analysis using LLM
└── ui/                          # User interface package
    ├── __init__.py
    ├── components.py            # Reusable UI components
    └── pages.py                # Page controllers and state management
```

## Architecture Overview

### Separation of Concerns

The application has been refactored to follow clean architecture principles with clear separation between:

1. **Business Logic** (`core/`): Contains all the domain logic and data processing
2. **User Interface** (`ui/`): Contains all Streamlit-specific UI components and presentation logic
3. **Configuration** (`config/`): Contains all application settings, constants, and templates
4. **Orchestration** (`app.py`): Main entry point that coordinates between layers

### Core Business Logic (`core/`)

#### DocumentProcessor (`core/document_processor.py`)
- **Purpose**: Handle document processing and text extraction
- **Responsibilities**:
  - Extract text from PDF, DOCX, and TXT files
  - Validate file formats
  - Provide supported format information
- **Dependencies**: PyPDF2, python-docx, config
- **Key Methods**:
  - `extract_text()`: Main method to extract text from any supported file
  - `get_supported_formats()`: Returns list of supported file formats
  - `validate_file_format()`: Validates file format compatibility

#### MSAAnalyzer (`core/msa_analyzer.py`)
- **Purpose**: Handle contract analysis using LLM
- **Responsibilities**:
  - Analyze contract terms and extract key information
  - Compare master contracts with amendments
  - Generate comprehensive summaries
  - Validate API connectivity
- **Dependencies**: LangChain, OpenAI, config
- **Key Methods**:
  - `analyze_contract_terms()`: Extract key terms from contracts
  - `compare_contracts()`: Compare master contract with amendments
  - `generate_comprehensive_summary()`: Create executive summary
  - `validate_api_key()`: Test API connectivity

### User Interface (`ui/`)

#### UIComponents (`ui/components.py`)
- **Purpose**: Reusable Streamlit UI components
- **Responsibilities**:
  - Render common UI elements (buttons, messages, file uploaders)
  - Generate report content for downloads
  - Manage page configuration and layout
- **Dependencies**: Streamlit, config
- **Key Methods**:
  - `setup_page_config()`: Configure Streamlit page settings
  - `render_*()`: Various methods to render UI components
  - `generate_report_content()`: Create downloadable report content

#### MSAReviewPages (`ui/pages.py`)
- **Purpose**: Page controllers and state management
- **Responsibilities**:
  - Coordinate between UI components and business logic
  - Manage Streamlit session state
  - Handle page flow and user interactions
- **Dependencies**: Streamlit, core modules, ui.components, config
- **Key Methods**:
  - `render_upload_tab()`: Handle document upload interface
  - `render_analysis_tab()`: Manage analysis execution and display
  - `render_summary_tab()`: Show comprehensive summary and reports

### Configuration (`config/`)

#### AppConfig (`config/settings.py`)
- **Purpose**: Application configuration and constants
- **Contains**:
  - Application metadata (title, icon, layout settings)
  - File processing settings (supported formats, limits)
  - LLM configuration (model, temperature)
  - Session state key definitions

#### UIMessages (`config/settings.py`)
- **Purpose**: Centralized UI message definitions
- **Contains**:
  - Error messages
  - Success messages
  - Info messages
  - Processing messages

#### PromptTemplates (`config/settings.py`)
- **Purpose**: LLM prompt templates
- **Contains**:
  - Contract analysis prompts
  - Contract comparison prompts
  - Comprehensive summary prompts

## Data Flow

1. **User Interaction**: User interacts with Streamlit UI components
2. **Page Controller**: UI pages handle user actions and coordinate responses
3. **Business Logic**: Core modules process documents and analyze contracts
4. **UI Response**: Results are passed back through page controllers to UI components
5. **State Management**: Session state is managed at the page controller level

## Benefits of This Architecture

### Maintainability
- **Single Responsibility**: Each module has a clear, focused purpose
- **Loose Coupling**: UI and business logic are independent
- **Easy Testing**: Business logic can be tested independently of UI

### Scalability
- **Modular Structure**: Easy to add new features or modify existing ones
- **Configuration Management**: Centralized settings make changes easier
- **Component Reusability**: UI components can be reused across different pages

### Code Quality
- **Separation of Concerns**: Clear boundaries between different types of logic
- **DRY Principle**: Eliminates code duplication
- **Clean Interfaces**: Well-defined APIs between modules

## Running the Application

### Using the New Architecture
```bash
streamlit run app.py
```

### Using the Legacy Application (for comparison)
```bash
streamlit run msa_review_app.py
```

## Environment Setup

Create a `.env` file in the project root:
```
OPENAI_API_KEY=your_openai_api_key_here
```

## Development Guidelines

### Adding New Features
1. **Business Logic**: Add new functionality to appropriate core modules
2. **UI Components**: Create reusable UI elements in `ui/components.py`
3. **Page Logic**: Add new page controllers in `ui/pages.py`
4. **Configuration**: Add new settings to `config/settings.py`

### Modifying Existing Features
1. **Identify the Layer**: Determine if changes are to business logic, UI, or configuration
2. **Make Targeted Changes**: Only modify the relevant layer
3. **Test Independently**: Test business logic separately from UI
4. **Update Configuration**: Adjust settings if needed

### Best Practices
- Keep business logic independent of Streamlit
- Use configuration constants instead of hardcoded values
- Handle errors gracefully at appropriate layers
- Maintain clear separation between data processing and presentation