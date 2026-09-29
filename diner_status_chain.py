from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnableLambda

from web_search_chain import do_searches_chain, RESULT_TEXT_MAX_CHARACTERS
from prompts import DINER_STATUS_CHAT_TEMPLATE
from llm_model import get_llm


web_results_chain = do_searches_chain | (
     RunnableLambda(
        lambda search_results: [{
            'diner_name': search_result['diner']['name'],
            'diner_location': f"{search_result['diner']['address']}, {search_result['diner']['city']}, {search_result['diner']['state']}",
            'current_status': search_result['diner']['status'],
            'result_texts': [
                f"SOURCE: {r['url']}\n{r['content'][:RESULT_TEXT_MAX_CHARACTERS]}"
                for r in search_result['results']
            ]} for search_result in search_results
        ]
    )
)

diner_status_chain = (
    RunnableLambda(
        lambda web_result:
            {
                'diner_name': web_result['diner_name'],
                'diner_location': web_result['diner_location'],
                'current_status': web_result['current_status'],
                'information': "\n\n".join(web_result['result_texts']),
            }
    )
    | DINER_STATUS_CHAT_TEMPLATE | get_llm() | StrOutputParser()
)

diner_results_chain = web_results_chain\
      | diner_status_chain.map()\
      | RunnableLambda(lambda x: "\n\n".join(x))

if __name__ == '__main__':
    print(diner_results_chain.invoke(None))