import torch
from transformers import AutoModelForCausalLM, AutoTokenizer
from embeddings import EmbeddingStore

class RAGEngine:
    def __init__(self, model_name="meta-llama/Meta-Llama-3-8B-Instruct"):
        print("Loading LLaMA 3...")
        self.tokenizer = AutoTokenizer.from_pretrained(model_name)
        self.model = AutoModelForCausalLM.from_pretrained(
            model_name,
            torch_dtype=torch.float16,
            device_map="auto"
        )
        self.embedding_store = EmbeddingStore()

    def add_knowledge_base(self, pages, rules):
        """
        pages: list of page dicts {id, url, content, meta}
        rules: dict returned from rules_engine.py
        """
        docs = []

        # Store web pages
        for page in pages:
            docs.append({
                "id": page["id"],
                "text": page["content"],
                "meta": {"url": page["url"], **page.get("meta", {})}
            })

        # Store rules/quick checks
        for rule_name, result in rules.items():
            docs.append({
                "id": f"rule_{rule_name}",
                "text": f"SEO Rule: {rule_name} → {result}",
                "meta": {"type": "rule"}
            })

        self.embedding_store.add_documents(docs)

    def ask(self, query, top_k=5, max_new_tokens=300):
        """
        Retrieve relevant docs and ask LLaMA 3
        """
        results = self.embedding_store.query(query, top_k=top_k)
        context = "\n".join([r["text"] for r in results])

        prompt = f"""You are an SEO assistant.
Use the following context to answer the question:

{context}

Question: {query}
Answer:"""

        inputs = self.tokenizer(prompt, return_tensors="pt").to(self.model.device)
        outputs = self.model.generate(
            **inputs,
            max_new_tokens=max_new_tokens,
            temperature=0.7,
            top_p=0.9
        )

        answer = self.tokenizer.decode(outputs[0], skip_special_tokens=True)
        return {
            "query": query,
            "answer": answer,
            "retrieved": results
        }
