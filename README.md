# Business Assistant Chat

An AI-powered business consulting assistant built with Streamlit and LangChain. This application provides an interactive chat interface with specialized tools for mathematical calculations, business KPI analysis, currency conversion, and report generation.

## 🚀 Features

- **💬 Multi-Chat Interface**: Create, switch between, and manage multiple chat sessions
- **🧮 Calculator Tool**: Evaluate mathematical expressions including advanced functions
- **📊 KPI Tool**: Calculate business metrics (ROI, Margin, CAGR, CAC, LTV, Payback Period)
- **💱 Currency Converter**: Real-time currency conversion using live exchange rates
- **📝 Report Generator**: Generate consulting-style business report outlines

## 📋 Prerequisites

Before running the application, ensure you have the following installed:

- **Python 3.10+**
- **Ollama** - Local LLM runtime ([Download here](https://ollama.ai))
- **Exchange Rate API Key** - For currency conversion ([Get free API key](https://www.exchangerate-api.com/))

## 🛠️ Installation

### 1. Clone the Repository

```bash
git clone <https://github.com/GuilhermePC09/business-ai-assistant.git>
cd business-ai-assistant
```

### 2. Create Virtual Environment

```bash
python3 -m venv venv
source venv/bin/activate  # On macOS/Linux
# or
.\venv\Scripts\activate  # On Windows
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Install and Configure Ollama

Download and install Ollama from [ollama.ai](https://ollama.ai), then pull the required model:

```bash
ollama pull llama3.1:8b
```

### 5. Configure Environment Variables

Create a `.env` file in the project root:

```bash
touch .env
```

Add the following content:

```env
EXCHANGE_RATE_API_KEY=your_api_key_here
```

> 💡 Get your free API key at [exchangerate-api.com](https://www.exchangerate-api.com/)

## ▶️ Running the Application

### 1. Start Ollama Server

Make sure Ollama is running. You can either:
- Open the Ollama application, or
- Run in terminal:

```bash
ollama serve
```

### 2. Start the Streamlit Application

```bash
streamlit run app.py
```

The application will open in your default browser at `http://localhost:8501`

## 🧪 Testing the Tools

### Calculator Tool

The calculator supports basic arithmetic, advanced functions, and mathematical constants.

**Test Examples:**

| Input | Expected Output |
|-------|-----------------|
| `What is 128 * 46?` | `5888` |
| `Calculate (15 + 3) * 4` | `72` |
| `What is the square root of 144?` | `12` |
| `Calculate 3^4 + 5` | `86` |
| `What is sin(pi/4)?` | `0.7071...` |
| `Calculate sqrt(2) + log(10) * 3` | `8.317...` |

**Supported Operations:**
- Basic: `+`, `-`, `*`, `/`, `%`, `**`
- Functions: `sqrt()`, `log()`, `ln()`, `sin()`, `cos()`, `tan()`, `abs()`, `pow()`
- Constants: `pi`, `e`

---

### KPI Tool

Calculate common business metrics with the following prompts:

**ROI (Return on Investment)**
```
Calculate the ROI with revenue of 150000 and cost of 100000
```
> Expected: `50.0` (50% ROI)

**Profit Margin**
```
What is the margin if revenue is 200000 and cost is 120000?
```
> Expected: `40.0` (40% margin)

**CAGR (Compound Annual Growth Rate)**
```
Calculate CAGR with start value 100000, end value 150000, over 3 years
```
> Expected: `0.1447...` (14.47% annual growth)

**CAC (Customer Acquisition Cost)**
```
What is the CAC if I spent 50000 to acquire 500 customers?
```
> Expected: `100.0` ($100 per customer)

**LTV (Customer Lifetime Value)**
```
Calculate LTV with revenue 1000, cost 400, over 5 years
```
> Expected: `3000.0`

**Payback Period**
```
What is the payback period with revenue 80000 and cost 200000?
```
> Expected: Payback period in years

---

### Currency Converter Tool

Convert between currencies using real-time exchange rates.

**Test Examples:**

| Input | Description |
|-------|-------------|
| `Convert 100 USD to EUR` | Converts US Dollars to Euros |
| `How much is 500 BRL in USD?` | Converts Brazilian Reais to US Dollars |
| `Convert 1000 JPY to GBP` | Converts Japanese Yen to British Pounds |

**Sample Output:**
```
100.00 USD = 92.35 EUR (rate: 0.9235)
```

> ⚠️ **Note:** Requires a valid `EXCHANGE_RATE_API_KEY` in your `.env` file

---

### Report Generator Tool

Generate consulting-style business report outlines.

**Test Examples:**

```
Generate a report about digital transformation strategy
```

```
Create a business report outline for market expansion in Europe
```

```
Generate a report about cost optimization initiatives
```

**Sample Output Structure:**
- Executive Summary
- Business Context
- Current State
- Data & Methodology
- Analysis
- Key Findings / Insights
- Recommendation
- Action Plan
- Metrics & Tracking
- Risks & Limitations
- Next Steps

---

## 📁 Project Structure

```
case-artefact/
├── app.py                 # Main Streamlit application
├── requirements.txt       # Python dependencies
├── .env                   # Environment variables (create this)
├── README.md              # This file
├── nodes/
│   ├── __init__.py
│   ├── llm.py             # LLM agent configuration
│   └── tools.py           # Tool definitions
└── venv/         # Virtual environment
```

## 🔧 Troubleshooting

### Ollama Connection Error

If you see "Ollama server not responding":
1. Ensure Ollama is installed and running
2. Check if the server is accessible: `curl http://localhost:11434/api/tags`
3. Restart Ollama: `ollama serve`

### Currency Conversion Not Working

1. Verify your API key is set in `.env`
2. Check API key validity at [exchangerate-api.com](https://www.exchangerate-api.com/)
3. Ensure you have internet connectivity

### Model Not Found

If the model is not available:
```bash
ollama pull llama3.1:8b
```

### Import Errors

Ensure all dependencies are installed:
```bash
pip install -r requirements.txt
```

## ⚠️ Known Limitations

- **No Conversation Memory**: The assistant does not remember previous messages in the conversation. Each message is processed independently.
- **Single Task Per Message**: The assistant can only handle one task per message. If you need multiple calculations or operations, please send them as separate messages.

## 📄 License

This project is for demonstration and educational purposes.

## 🤝 Contributing

Feel free to submit issues and pull requests to improve the application.
