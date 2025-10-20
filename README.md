# 🎯 Lock-In App

A comprehensive productivity and study management application built with Streamlit, featuring AI-powered document analysis, focus timers, and study tracking.

## 🌟 Features

### 📈 Dashboard
- **Study Timer**: Pomodoro and custom timers with visual progress
- **Alarms**: Set study reminders and notifications
- **Quick Stats**: Daily progress, documents uploaded, analysis completed
- **Preset Sessions**: Quick-start templates (Pomodoro, Deep Work, etc.)

### 📁 Document Management
- **File Upload**: Support for PDF, DOCX, and TXT files
- **Text Extraction**: Automatic content extraction with PyMuPDF/pdfplumber
- **File Organization**: Search, filter, preview, and manage documents
- **Bulk Operations**: Analyze multiple documents simultaneously

### 🤖 AI-Powered Analysis
- **DeepSeek Integration**: Document analysis for key topics and weightage
- **Ollama Local LLM**: Chat assistant for study questions
- **Visual Analytics**: Interactive charts showing topic distribution
- **Study Insights**: Question format predictions and revision summaries

### 🎯 Focus Mode
- **Distraction-Free Interface**: Fullscreen timer with minimal UI
- **Progress Visualization**: Circular progress indicators and session tracking
- **Session Statistics**: Track focus sessions, streaks, and productivity
- **Breathing Animations**: Calming visual effects to maintain focus

### ⚙️ Settings & Customization
- **Timer Presets**: Customizable session lengths and break intervals
- **AI Configuration**: DeepSeek API and Ollama endpoint settings
- **Theme Customization**: Dark mode with customizable accent colors
- **Study Goals**: Daily and weekly target setting with progress tracking

## 🚀 Installation

### Prerequisites
- Python 3.8 or higher
- pip package manager

### Setup Instructions

1. **Clone or download the application:**
   ```bash
   git clone <repository-url>
   cd lock_in_app
   ```

2. **Create a virtual environment:**
   ```bash
   python -m venv venv
   
   # On Windows
   venv\Scripts\activate
   
   # On macOS/Linux  
   source venv/bin/activate
   ```

3. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

4. **Run the application:**
   ```bash
   streamlit run app.py
   ```

5. **Access the app:**
   Open your browser and go to `http://localhost:8501`

## 📋 Dependencies

### Core Requirements
```
streamlit>=1.28.0          # Web framework
plotly>=5.15.0             # Interactive charts
pandas>=2.0.0              # Data manipulation
numpy>=1.24.0              # Numerical computations
```

### File Processing
```
python-docx>=0.8.11        # DOCX file processing
PyMuPDF>=1.23.0            # PDF text extraction (primary)
pdfplumber>=0.10.0         # PDF text extraction (fallback)
```

### AI Integration
```
requests>=2.31.0           # HTTP requests for APIs
python-dotenv>=1.0.0       # Environment variables
```

### Optional Enhancements
```
streamlit-audio>=0.0.7     # Audio notifications
```

## 🔧 Configuration

### AI Integration Setup

#### DeepSeek Configuration
1. Get API key from [deepseek.com](https://deepseek.com)
2. Go to Settings → AI Integration
3. Enter your API key in the DeepSeek settings
4. Test the connection

#### Ollama Setup (Local LLM)
1. Install Ollama from [ollama.ai](https://ollama.ai)
2. Pull a model: `ollama pull llama2`
3. Ensure Ollama is running on `http://localhost:11434`
4. Test connection in Settings → AI Integration

### Theme Customization
- Navigate to Settings → Appearance
- Choose from preset themes or use custom colors
- Adjust layout density and font sizes
- Enable/disable animations and effects

## 📱 Usage Guide

### Getting Started
1. **Set Study Goals**: Configure daily/weekly targets in Settings
2. **Upload Documents**: Add your study materials in Documents page
3. **Start Focus Session**: Use Dashboard timer or Focus Mode
4. **Analyze Content**: Get AI insights on uploaded documents
5. **Track Progress**: Monitor stats and maintain study streaks

### Best Practices
- **Pomodoro Technique**: Use 25-minute focus sessions with 5-minute breaks
- **Document Organization**: Upload materials before study sessions for AI analysis
- **Goal Setting**: Start with realistic daily targets (60-120 minutes)
- **Focus Mode**: Use for deep work sessions without distractions
- **Regular Reviews**: Check AI analysis insights for study optimization

## 🏧 Architecture

### Project Structure
```
lock_in_app/
├── app.py                 # Main application entry point
├── pages/
│   ├── documents.py       # Document management
│   ├── ai_analysis.py     # AI-powered analysis
│   ├── focus_mode.py      # Distraction-free timer
│   └── settings.py        # Configuration management
├── utils/
│   ├── ai_integration.py  # DeepSeek/Ollama clients
│   ├── file_processing.py # Text extraction utilities
│   └── database.py        # SQLite data persistence
├── data/                  # User data storage
├── .streamlit/
│   └── config.toml        # Streamlit configuration
└── requirements.txt       # Python dependencies
```

### Key Components

#### Session State Management
- Persistent timer states across page navigation
- Document storage and analysis results
- User preferences and settings
- Study progress and statistics

#### File Processing Pipeline
1. **Upload Validation**: Check file types and sizes
2. **Text Extraction**: Use PyMuPDF/pdfplumber for PDFs, python-docx for Word
3. **Content Analysis**: Calculate word counts, complexity metrics
4. **Storage**: Save metadata and content to session state

#### AI Integration Layer
- **DeepSeek Client**: Document analysis and summarization
- **Ollama Client**: Local LLM for conversational assistance
- **Mock Responses**: Fallback system for testing without API keys
- **Error Handling**: Graceful degradation when services unavailable

## 🎨 Theming

The app features a modern dark theme with customizable accents:

### Default Color Palette
- **Background**: #1E1E1E (Dark grey)
- **Secondary**: #2D2D2D (Lighter grey) 
- **Primary**: #4A90E2 (Blue)
- **Text**: #FFFFFF (White)
- **Success**: #00CC66 (Green)
- **Error**: #CC0066 (Red)

### Custom CSS Features
- Gradient backgrounds in Focus Mode
- Glassmorphism effects with backdrop blur
- Smooth transitions and hover effects
- Responsive layout for different screen sizes
- Custom scrollbars and component styling

## 🔐 Data & Privacy

### Local Storage
- All data stored locally in browser session state
- No external data transmission (except AI API calls)
- SQLite database for persistent storage (optional)
- User controls over data retention and backup

### AI Data Handling
- Document content sent to AI services only on explicit user request
- API keys stored locally and never transmitted in plaintext
- Users can disable AI features entirely
- Mock responses available for offline usage

## 🛠 Development

### Adding New Features
1. Create new page in `pages/` directory
2. Add navigation in main `app.py` sidebar
3. Follow existing styling patterns
4. Update requirements if new dependencies needed

### Customizing AI Integration
- Implement new AI clients in `utils/ai_integration.py`
- Add configuration options in Settings page
- Create mock responses for testing
- Handle API errors gracefully

### Extending File Support
- Add new file type handlers in `utils/file_processing.py`
- Update upload validation in Documents page
- Test text extraction with various file formats

## 📞 Support & Contributing

### Common Issues
- **PDF extraction fails**: Install PyMuPDF (`pip install PyMuPDF`)
- **Timer not updating**: Refresh the page or check browser console
- **AI features not working**: Verify API keys in Settings
- **File upload errors**: Check file size limits and formats

### Feature Requests
- Audio notifications for timer completion
- Export study statistics to CSV/PDF
- Integration with calendar applications
- Mobile app version
- Collaborative study sessions

## 📄 License

This project is open source and available under the MIT License.

## 🙏 Acknowledgments

- **Streamlit**: Excellent web framework for Python apps
- **DeepSeek**: Powerful AI models for document analysis
- **Ollama**: Local LLM inference server
- **Plotly**: Interactive visualization library
- **PyMuPDF & pdfplumber**: PDF text extraction libraries

---

Built with ❤️ for focused learning and productivity enhancement.
