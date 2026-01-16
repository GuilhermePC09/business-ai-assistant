import math
import os
from dotenv import load_dotenv
from langchain.tools import tool
import requests
import logging

load_dotenv()

logger = logging.getLogger(__name__)
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)

_ALLOWED_NAMES = {
    "sqrt": math.sqrt,
    "log": math.log,
    "ln": math.log,
    "sin": math.sin,
    "cos": math.cos,
    "tan": math.tan,
    "abs": abs,
    "pow": pow,
    "pi": math.pi,
    "e": math.e,
}

API_KEY = os.getenv("EXCHANGE_RATE_API_KEY")
BASE_URL = "https://v6.exchangerate-api.com/v6"

@tool
def calculator_tool(expression: str) -> str:
    """
    Purpose:
    Perform all mathematical evaluation of numeric expressions, including simple and complex formulas. 
    This tool is use to give the result of any mathematical expression provided by the user.

    Supported operations:
    - Basic arithmetic: +, -, *, /, %, **
    - Parentheses for precedence: ( )
    - Power operator: ^ or **
    - Mathematical functions:
        sqrt(x), log(x), ln(x), sin(x), cos(x), tan(x), abs(x), pow(x, y)
    - Mathematical constants:
        pi, e

    Capabilities:
    - Evaluate single operations:
        "128 * 46"
    - Evaluate combined / multi-step expressions:
        "(15 + 3) * 4"
        "3^4 + 5"
        "sqrt(2) + log(10) * 3"
        "sin(pi/4) + cos(pi/2)"
        "pow(2, 3) + sqrt(16) - 5"

    IMPORTANT RULES:
    - ALWAYS use this tool for ANY mathematical or numeric calculation.
    - NEVER compute results manually.
    - This tool supports expressions mixing multiple operators and functions.
    - Input must be a valid mathematical expression as a string.

    Examples:
    - "128 * 46"
    - "(15 + 3) * 4"
    - "sqrt(2)"
    - "3^4 + 5"
    - "sin(pi/4)"
    - "cos(pi/2)"
    - "sqrt(2) + log(10) * 3"
    """

    logger.info(f"Calculator tool called with expression: {expression}")
    try:
        normalized = expression.replace("^", "**").strip()
        result = eval(normalized, {"__builtins__": {}}, _ALLOWED_NAMES)
        logger.info(f"Calculator result: {result}")
        return str(result)
    except Exception as e:
        logger.error(f"Calculator error: {e}")
        return f"Error evaluating expression: {e}"
    

@tool
def kpi_tool(metric: str, customers: float = None, revenue: float = None, cost: float = None, start: float = None, end: float = None, years: int = None) -> str:
    """
    Calculate business KPIs:
    - ROI: metric="roi", revenue, cost
    - Margin: metric="margin", revenue, cost
    - CAGR: metric="cagr", start, end, years
    - CAC: metric="cac", cost, customers
    - LTV: metric="ltv", revenue, cost, years
    - Payback Period: metric="payback", revenue, cost
    """
    metric = metric.lower()
    logger.info(f"KPI tool called with metric: {metric}")
    try:
        if metric == "roi":
            roi = (revenue - cost) / cost * 100
            
            return str(roi)
        elif metric == "cagr":
            cagr = (end / start) ** (1 / years) - 1
            return str(cagr)
        elif metric == "margin":
            margin = (revenue - cost) / revenue * 100
            return str(margin)
        elif metric == "ltv":
            margin = (revenue - cost) / revenue
            ltv = revenue * margin * years
            return str(ltv)
        elif metric == "cac":
            cac = cost / customers
            return str(cac)
        elif metric == "payback":
            profit = revenue - cost
            payback = cost / profit
            return str(payback)
        else:
            logger.warning(f"Unsupported KPI metric: {metric}")
            return "Unsupported metric"
    except Exception as e:
        logger.error(f"KPI calculation error: {e}")
        return f"Error evaluating expression: {e}"
    
@tool(return_direct=True)
def currency_converter_tool(amount: float, source_currency_code: str, target_currency_code: str) -> str:
    """
    Convert an amount from one currency to another using real-time exchange rates.

    Args:
        amount: The amount to convert
        source_currency_code: The source currency code (e.g., "USD", "EUR")
        target_currency_code: The target currency code (e.g., "BRL", "GBP")

    Examples:
        - "Convert 500 EUR to USD"
        - "How much is 100 USD in BRL?"
        - "Convert 1000 JPY to EUR"

    Rules:
        - Always use this tool for ANY currency conversion question.
        - Do not estimate or calculate exchange rates manually.
    """
    logger.info(f"Currency converter called: {amount} {source_currency_code} -> {target_currency_code}")
    
    if not API_KEY:
        logger.error("Currency API key not configured")
        return "Currency service error: API key not configured."
    
    source_currency_code = source_currency_code.upper()
    target_currency_code = target_currency_code.upper()

    try:
        url = f"{BASE_URL}/{API_KEY}/pair/{source_currency_code}/{target_currency_code}/{amount}"

        response = requests.get(url, timeout=10)
        response.raise_for_status()

        data = response.json()

        if data.get("result") != "success":
            return f"Currency API error: {data.get('error-type', 'unknown')}"

        converted = data["conversion_result"]
        rate = data["conversion_rate"]

        logger.info(f"Currency conversion successful: {amount} {source_currency_code} = {converted} {target_currency_code}")
        return f"{amount:.2f} {source_currency_code} = {converted:.2f} {target_currency_code} (rate: {rate:.4f})"

    except requests.exceptions.Timeout:
        logger.error("Currency API request timed out")
        return "Currency service error: request timed out."

    except Exception as e:
        logger.error(f"Currency service error: {e}")
        return f"Currency service error: {e}"

    
@tool
def generate_report_tool(topic: str) -> str:
    """Generate a consulting-style report outline for a given business topic."""
    logger.info(f"Generate report tool called with topic: {topic}")
    outline = f"""
        Executive Summary
        - Objective: Summarize the goal for {topic}.
        - Key takeaways: 3-5 bullets on expected impact.

        Business Context
        - Company background
        - Market overview
        - Strategic objectives

        Current State
        - Context and baseline metrics.
        - Pain points and risks.

        Data & Methodology
        - Data sources
        - Analytical approach
        - Assumptions

        Analysis
        - Drivers and root causes.
        - Benchmark/market signals.

        Key Findings / Insights
        - Main analytical results
        - Supporting evidence
        - Key metrics

        Recommendation
        - Chosen option and rationale.
        - Dependencies and assumptions.

        Action Plan
        - 30/60/90 milestones and owners.

        Metrics & Tracking
        - KPIs, targets, cadence, owners.

        Risks & Limitations
        - Potential risks
        - Data limitations
        - External dependencies

        Next Steps
        - Short-term actions
        - Long-term roadmap

        """

    return outline.strip()