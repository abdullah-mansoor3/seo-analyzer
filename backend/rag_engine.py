"""RAG engine – retrieves relevant context via lightweight embeddings, then
sends the enriched prompt to the Groq cloud API for generation.

No local LLM is loaded, so this runs on any machine (i5 + 8 GB RAM is fine).
"""

import os
from groq import Groq
from backend.embeddings import EmbeddingStore

# ---------------------------------------------------------------------------
# Singleton embedding store – created once, reused across requests
# ---------------------------------------------------------------------------
_store = EmbeddingStore()

GROQ_MODEL = os.getenv("GROQ_MODEL", "llama-3.1-8b-instant")


def get_store() -> EmbeddingStore:
    """Return the shared embedding store (for testing / direct access)."""
    return _store


def build_knowledge_base(pages: list[dict], rules: dict) -> None:
    """Index crawled pages and rule-check results into the vector store."""
    _store.reset()

    documents: list[dict] = []

    for page in pages:
        documents.append({
            "source": page.get("url", "unknown"),
            "text": (
                f"URL: {page.get('url', '')}\n"
                f"Title: {page.get('title', '')}\n"
                f"Meta description: {page.get('meta_description', '')}\n"
                f"H1 tags: {', '.join(page.get('h1', []))}\n"
                f"H2 tags: {', '.join(page.get('h2', []))}\n"
                f"Content snippet: {page.get('text_content', '')[:2000]}"
            ),
        })

    # Append rule-based findings so the LLM can reference them too
    for check in rules.get("checks", []):
        if check.get("issues"):
            documents.append({
                "source": f"rules:{check['page']}",
                "text": (
                    f"Rule-based SEO issues for {check['page']}:\n"
                    + "\n".join(f"  • {issue}" for issue in check["issues"])
                ),
            })

    _store.add_documents(documents)


def rag_query(query: str, top_k: int = 8) -> str:
    """Retrieve relevant context from the vector store, then call Groq."""
    retrieved = _store.query(query, top_k=top_k)
    context_block = "\n\n---\n\n".join(
        f"[Source: {r['source']}]\n{r['text']}" for r in retrieved
    )

    system_prompt = (
        "You are an expert SEO consultant. The user has crawled a website and "
        "collected page metadata plus automated rule-based SEO checks. Relevant "
        "excerpts are provided below as context.\n\n"
        "Your job:\n"
        "1. Identify the most impactful SEO issues across the site.\n"
        "2. For EACH issue, cite the specific page URL and the exact problem.\n"
        "3. Provide a concrete, actionable fix (not vague advice).\n"
        "4. Prioritise issues by potential traffic impact (critical → minor).\n"
        "5. End with a short overall score (1-10) and a one-paragraph summary.\n\n"
        "Format your answer in **Markdown** with clear headings and bullet points."
    )

    user_message = (
        f"### Retrieved context\n\n{context_block}\n\n---\n\n"
        f"### User question\n\n{query}"
    )

    client = Groq(api_key=os.getenv("GROQ_API_KEY"))
    chat = client.chat.completions.create(
        model=GROQ_MODEL,
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_message},
        ],
        temperature=0.4,
        max_tokens=2048,
    )

    return chat.choices[0].message.content
