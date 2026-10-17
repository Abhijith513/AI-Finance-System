"""
Gemini Reporting Service

Gemini is used ONLY for reporting and interpretation.

All numerical metrics are calculated by Python first:
    - anomaly count
    - anomaly percentage
    - precision
    - recall
    - F1 score
    - confusion matrix
    - MAE
    - RMSE
    - MAPE
    - forecast values

Gemini must not calculate or invent these values.
"""

import json
import logging
import re

from django.conf import settings
from google import genai

from .cached_research import get_cached_research_evaluations


# ============================================================
# GEMINI CLIENT
# ============================================================

def get_gemini_client():
    """
    Create the Gemini client using the API key from .env.
    """

    api_key = getattr(
        settings,
        "GEMINI_API_KEY",
        None,
    )

    if not api_key:
        raise ValueError(
            "GEMINI_API_KEY is not configured."
        )

    return genai.Client(
        api_key=api_key
    )


# ============================================================
# VERIFIED RESULTS
# ============================================================

def get_verified_results():
    """
    Run the application's verified evaluation functions.

    Gemini receives the results produced here.
    """

    research = get_cached_research_evaluations()
    fraud_results = research["fraud_evaluation"]
    forecast_results = research["forecast_evaluation"]

    return {
        "fraud_evaluation": fraud_results,
        "forecast_evaluation": forecast_results,
    }


# Every displayed numeric claim is rendered from Python metrics, never
# accepted as free-form model-authored figures.
logger = logging.getLogger(__name__)


def render_verified_numeric_report(verified):
    """A deterministic, traceable metric section and dataset limitation."""
    fraud = verified.get("fraud_evaluation") or {}
    forecast = verified.get("forecast_evaluation") or {}
    baseline = fraud.get("statistical_baseline") or {}
    forest = fraud.get("isolation_forest") or {}

    def pct(value):
        if value is None:
            return "Unavailable"
        return f"{value * 100:.2f}%"

    lines = [
        "# Financial Analytics Management Report",
        "",
        "## Verified Python-computed research metrics",
        "",
        f"- Synthetic transactions: {fraud.get('dataset', 'Unavailable')}",
        f"- Labelled anomalies: {fraud.get('actual_anomalies', 'Unavailable')}",
        f"- Statistical baseline F1: {pct(baseline.get('f1'))}",
        f"- Isolation Forest F1: {pct(forest.get('f1'))}",
        "",
        "| Series | Seasonal-Naive MAPE | SARIMA MAPE | Baseline windows | SARIMA windows |",
        "|---|---:|---:|---:|---:|",
    ]
    for series in ("income", "expense"):
        result = forecast.get(series) or {}
        models = result.get("models") or {}
        validation = result.get("validation") or {}
        naive = (models.get("seasonal_naive") or {}).get("mape")
        sarima = (models.get("sarima") or {}).get("mape")
        lines.append(
            f"| {series.title()} | {naive if naive is not None else 'Unavailable'}% "
            f"| {sarima if sarima is not None else 'Unavailable'}% "
            f"| {validation.get('observations', 'Unavailable')} "
            f"| {validation.get('sarima_observations', 'Unavailable')} |"
        )
    lines.extend([
        "",
        "> **Scope:** These figures are computed by Python on synthetic data. "
        "Isolation Forest's original comparison is in-sample; the month-window "
        "SARIMA and baseline results may not be fully paired. The live "
        "behavioural risk score is uncalibrated and is not a fraud probability.",
    ])
    return "\n".join(lines)


def validate_narrative(text):
    """Reject model-authored numbers; no fabricated or altered numerical claims."""
    if not isinstance(text, str) or not text.strip():
        raise ValueError("Gemini returned an empty narrative.")
    # Digit-bearing narratives are not accepted; all figures live in the
    # deterministic Python section. Models may discuss qualitative patterns.
    if re.search(r"\d", text):
        raise ValueError("Gemini narrative contains unverified numeric claims.")
    forbidden = (
        "guaranteed", "risk-free", "proven real-world", "certified bank",
        "zero risk", "real bank fraud detected",
    )
    if any(phrase in text.lower() for phrase in forbidden):
        raise ValueError("Gemini narrative contains unsupported assurances.")
    if len(text) > 12000:
        raise ValueError("Gemini narrative exceeds the allowed length.")
    return text.strip()


# ============================================================
# BUILD CONTROLLED PROMPT
# ============================================================

def build_report_prompt(verified_results):
    """
    Build a controlled reporting prompt.

    Gemini is explicitly instructed not to calculate or invent
    numerical results.
    """

    results_json = json.dumps(
        verified_results,
        indent=2,
        default=str,
    )

    return f"""
You are a financial analytics interpreter for a SYNTHETIC banking data
research project. Write concise qualitative interpretation only.

RULES:
- Return plain Markdown sections titled Observations, Limitations, Recommendations.
- NEVER write digits, numbers, dates, percentages, currency amounts or newly
  calculated figures. All numbers will be supplied separately by Python.
- Do not claim real fraud detection, bank certification or forecast guarantees.
- Do not assert causal explanations for model failure without independent tests.
- Discuss where an amount-based statistical baseline may outperform a complex
  unsupervised model on amount-heavy synthetic anomalies.
- Explain that incomplete SARIMA validation coverage limits comparisons.
- If the data does not support a conclusion, say so; do not improvise facts.

Verified application evidence (read only; DO NOT reproduce the digits):
{results_json}
"""




# ============================================================
# GENERATE REPORT
# ============================================================

def generate_gemini_report():
    """
    Generate a management report using verified Python results.

    Python calculates the metrics.
    Gemini only interprets the verified results.
    If Gemini is unavailable, return a fallback report.
    """

    verified_results = get_verified_results()
    prompt = build_report_prompt(verified_results)
    numeric_section = render_verified_numeric_report(verified_results)

    try:
        client = get_gemini_client()
        response = client.models.generate_content(
            model=getattr(settings, "GEMINI_MODEL", "gemini-3.8-flash"),
            contents=prompt,
        )
        interpretation = validate_narrative(response.text if response else None)
        return {
            "verified_results": verified_results,
            "report": numeric_section + "\n\n## AI-assisted qualitative interpretation (not independent evidence)\n\n" + interpretation,
            "report_source": "gemini",
            "gemini_available": True,
            "numeric_claims_source": "python_only",
            "narrative_numeric_validation": "passed",
        }
    except Exception as exc:
        logger.warning("Gemini report unavailable or rejected: %s", type(exc).__name__)
        return {
            "verified_results": verified_results,
            "report": numeric_section + "\n\n## AI reporting status\n\nGemini unavailable or its narrative failed validation. This is the deterministic Python-only fallback; no external AI interpretation was accepted.",
            "report_source": "fallback",
            "gemini_available": False,
            "numeric_claims_source": "python_only",
            "narrative_numeric_validation": "not_applicable",
        }
