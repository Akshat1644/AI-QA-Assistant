# 🧪 AI QA Assistant

An **AI-powered QA productivity tool** built with **Python, Streamlit, and Google Gemini AI** to assist QA engineers across the software testing lifecycle.

The application analyzes software requirements and uses Generative AI to generate testing artifacts, identify risks and gaps, predict potential defects, assess automation feasibility, and improve requirement-to-test traceability.

---

## 🚀 Key Features

| Feature                          | Purpose                                                                          |
| -------------------------------- | -------------------------------------------------------------------------------- |
| 🧪 **Test Case Generation**      | Generates functional, negative, boundary, and edge test cases                    |
| 📊 **Requirement Quality Score** | Evaluates completeness, clarity, testability, and ambiguity                      |
| 📋 **Requirement Completeness**  | Identifies complete, partial, and missing requirement information                |
| 🔍 **Gap Analysis**              | Identifies missing requirements, ambiguities, risks, and clarification questions |
| 📈 **Coverage Analysis**         | Identifies covered, partial, and missing testing scenarios                       |
| 🧪 **Test Data Generation**      | Generates valid, invalid, and boundary test data                                 |
| 🌐 **API Test Cases**            | Generates API-focused testing scenarios                                          |
| 🐞 **Bug Prediction**            | Predicts defect-prone modules with risk and probability                          |
| 🐛 **Defect Prediction**         | Identifies potential defect areas and production issues                          |
| 📝 **Defect Report**             | Generates structured defect reports with severity, priority, and root cause      |
| 🔄 **Regression Analysis**       | Identifies affected modules and required regression testing                      |
| ⚠️ **Risk Analysis**             | Identifies and prioritizes requirement-level risks                               |
| 🤖 **Automation Feasibility**    | Evaluates automation suitability, framework, effort, and maintenance             |
| 🔗 **Smart RTM**                 | Generates AI-assisted Requirement Traceability information                       |
| 🎭 **Playwright Support**        | Supports AI-assisted automation-oriented testing workflows                       |

---

## 🧠 AI Integration

The application uses **Google Gemini AI** with feature-specific prompt templates.

```text
Software Requirement
        ↓
Streamlit UI
        ↓
Feature Selection
        ↓
Feature-specific Prompt
        ↓
Gemini AI
        ↓
Response Parsing & Validation
        ↓
Structured QA Result
        ↓
Streamlit Dashboard
        ↓
Excel / Text Export
```

For structured features, AI responses are parsed into **Pandas DataFrames** before being displayed or exported.

---

## 🔄 Gemini Reliability

The application supports **multiple Gemini API keys and model fallback**.

If a configured model or API key fails, the application attempts another available key/model combination.

This helps handle failures such as:

* API quota exhaustion
* Unavailable models
* API errors
* Invalid AI responses

> Multiple API keys do not provide unlimited quota; each Gemini project remains subject to Google's applicable usage limits.

---

## 📥 Export

Generated QA artifacts can be exported for further documentation and review.

Supported output includes:

* 📊 Excel
* 📄 Text reports

Excel processing uses **Pandas and OpenPyXL**.

---

## 🛠️ Tech Stack

* **Python**
* **Streamlit**
* **Google Gemini AI**
* **Google GenAI SDK**
* **Pandas**
* **OpenPyXL**
* **python-dotenv**
* **JSON**
* **Git & GitHub**

---

## 📂 Project Structure

```text
AI-QA-Assistant/
│
├── app/
│   ├── gemini_service.py
│   ├── prompts.py
│   ├── test_case_generation.py
│   ├── gap_analysis.py
│   ├── coverage_analysis.py
│   ├── bug_prediction.py
│   ├── regression_analysis.py
│   ├── risk_analysis.py
│   ├── automation_feasibility.py
│   ├── smart_rtm.py
│   └── ...
│
├── utils/
│   ├── formatting.py
│   ├── session_manager.py
│   └── downloads.py
│
├── streamlit_app.py
├── requirements.txt
├── .gitignore
└── README.md
```

---

## ⚙️ Installation

### 1. Clone the repository

```bash
git clone https://github.com/Akshat1644/AI-QA-Assistant.git
cd AI-QA-Assistant
```

### 2. Create virtual environment

```bash
python -m venv venv
venv\Scripts\activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Configure Gemini API

Create a `.env` file:

```env
GEMINI_API_KEY_1=your_api_key
GEMINI_API_KEY_2=your_api_key
GEMINI_API_KEY_3=your_api_key
```

Make sure `.env` is included in `.gitignore`.

### 5. Run the application

```bash
streamlit run streamlit_app.py
```

---

## 📸 Screenshots

### 🏠 Dashboard

*Add screenshot here*

### 🧪 Test Case Generation

*Add screenshot here*

### 📊 AI Analysis

*Add screenshot here*

### 🔗 Smart RTM

*Add screenshot here*

---

## 🎯 Project Objective

The goal of **AI QA Assistant** is to reduce repetitive QA effort by combining **Generative AI with traditional software testing practices**.

The application assists QA engineers with:

* Requirement analysis
* Test design
* Test-data preparation
* Risk-based testing
* Defect prevention
* Regression planning
* Automation planning
* QA documentation
* Requirement traceability

AI-generated results are intended to **assist QA engineers**, while final validation and testing decisions remain with the QA team.

---

## 🔮 Future Enhancements

* Jira integration
* CI/CD integration
* Persistent project history
* Additional AI model providers
* Advanced Playwright automation generation
* Automated defect-management integration

---

## 👨‍💻 Author

**Akshat Dahalwar**

**AI QA Assistant — AI-powered QA productivity and testing platform**
