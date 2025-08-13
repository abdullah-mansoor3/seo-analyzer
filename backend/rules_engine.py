# backend/rules_engine.py

def run_rules_checks(pages: list) -> dict:
    """
    Run quick SEO checks on crawled site data.

    Args:
        pages (list): List of page dictionaries from the scraper.
                      Each page contains keys like:
                      {
                          "url": "...",
                          "title": "...",
                          "meta_description": "...",
                          "h1": [...],
                          "h2": [...],
                          "text_content": "...",
                          "internal_links": [...],
                          "external_links": [...],
                          ...
                      }

    Returns:
        dict: { "checks": [ { "page": url, "issues": [...] }, ... ] }
    """

    checks_results = []

    for page in pages:
        issues = []

        # --- Title Checks ---
        title = page.get("title", "").strip()
        if not title:
            issues.append("Missing <title> tag.")
        elif len(title) > 60:
            issues.append(f"Title too long ({len(title)} chars) — keep under 60.")

        # --- Meta Description Checks ---
        meta_desc = page.get("meta_description", "").strip()
        if not meta_desc:
            issues.append("Missing meta description.")
        elif len(meta_desc) > 160:
            issues.append(f"Meta description too long ({len(meta_desc)} chars) — keep under 160.")

        # --- H1 Checks ---
        h1_tags = page.get("h1", [])
        if not h1_tags:
            issues.append("Missing H1 heading.")
        elif len(h1_tags) > 1:
            issues.append("Multiple H1 headings — use only one per page.")

        # --- Content Length Check ---
        content = page.get("text_content", "").strip()
        word_count = len(content.split())
        if word_count < 300:
            issues.append(f"Content too short ({word_count} words) — aim for 300+.")

        # --- Internal Linking Check ---
        internal_links = page.get("internal_links", [])
        if not internal_links:
            issues.append("No internal links found.")

        checks_results.append({
            "page": page.get("url", ""),
            "issues": issues
        })

    return {"checks": checks_results}


# Example usage
if __name__ == "__main__":
    import json
    from pprint import pprint

    with open("../data/sites/groovypakistan.com/crawl.json") as f:
        pages_data = json.load(f)

    results = run_rules_checks(pages_data)
    pprint(results)
