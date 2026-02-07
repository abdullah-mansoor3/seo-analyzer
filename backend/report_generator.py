"""Compile rule-based checks + RAG insights into a structured SEO report."""

from backend.rag_engine import build_knowledge_base, rag_query


def generate_report(pages: list[dict], rules: dict, user_query: str) -> dict:
    """Build the knowledge base and ask the LLM for a full analysis."""

    # 1. Index everything into the vector store
    build_knowledge_base(pages, rules)

    # 2. Ask the Groq-backed RAG engine
    analysis = rag_query(user_query)

    return {
        "rules_summary": rules,
        "ai_analysis": analysis,
        "pages_analyzed": len(pages),
    }
