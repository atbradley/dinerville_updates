from typing import List

import ollama

def web_search(web_query: str, num_results: int):
    results = ollama.web_search(web_query, max_results=num_results)
    return [{
        'content': r.content,
        'url': r.url
    } for r in results.results]
