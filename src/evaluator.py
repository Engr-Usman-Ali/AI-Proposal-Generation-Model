# src/evaluator.py

from textblob import TextBlob
import json
import os

def evaluate_proposal(proposal: dict):
    """
    Evaluate a proposal based on structure, tone, and text quality.
    Returns a score dictionary.
    """

    formatted_text = proposal.get("formatted_text", "")
    tone = proposal.get("tone", "Unknown")

    # Sentiment analysis
    sentiment = TextBlob(formatted_text).sentiment.polarity

    # Structure check
    structure_score = 0
    required_fields = ["service_type", "project_overview", "objectives", "timeline", "estimated_budget"]
    structure_score = sum(1 for key in required_fields if proposal.get(key) not in ["N/A", "", None])

    # Calculate tone score
    tone_score = 1 if tone.lower() in ["professional", "formal", "neutral"] else 0.5

    # Weighted total
    total_score = round((structure_score / len(required_fields)) * 0.6 + tone_score * 0.2 + (sentiment + 1) / 2 * 0.2, 2)

    return {
        "structure_score": round(structure_score / len(required_fields), 2),
        "tone_score": tone_score,
        "sentiment_score": round(sentiment, 2),
        "total_score": total_score
    }


def evaluate_all(proposals, output_path="output/evaluation_report.json"):
    """Evaluate all proposals and save summary."""
    results = []
    for i, proposal in enumerate(proposals, 1):
        eval_result = evaluate_proposal(proposal)
        eval_result["id"] = i
        results.append(eval_result)

    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(results, f, indent=4)

    print(f"📊 Evaluation report saved to: {output_path}")
