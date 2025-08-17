# backend/report_generator.py
from rag_engine import RAGEngine

class ReportGenerator:
    def __init__(self, rag_engine: RAGEngine):
        self.rag = rag_engine

    def generate_report(self, site_url, pages, rules):
        """
        Combine quick checks + RAG insights into a structured SEO report
        """
        # Step 1: Add documents to knowledge base
        self.rag.add_knowledge_base(pages, rules)

        # Step 2: Ask structured SEO questions
        questions = [
            "What are the biggest SEO issues on this website?",
            "How is the keyword optimization across pages?",
            "Is the site mobile friendly and fast?",
            "What improvements can be made in meta tags and headings?",
            "What are the overall strengths and weaknesses of the site?"
        ]

        insights = []
        for q in questions:
            result = self.rag.ask(q)
            insights.append({"question": q, "answer": result["answer"]})

        # Step 3: Compile final report
        report = {
            "site": site_url,
            "rules_summary": rules,
            "rag_insights": insights
        }
        return report
