from dinerville_utils import random_diners
from web_utils import web_search
from langchain_core.runnables import RunnableLambda

NUM_SEARCH_RESULTS_PER_QUERY = 5
RESULT_TEXT_MAX_CHARACTERS = 10000

get_web_searches_chain = (
    RunnableLambda(lambda _: random_diners())
    | RunnableLambda(
        lambda diners: [
            {
                'search_query': (
                    f"{diner['name']}, {diner['city']}, {diner['state']} open"
                    if diner['status'] == 'Open for business'
                    else f"{diner['name']}, {diner['city']}, {diner['state']} reopening"
                ),
                'diner': diner,
            }
            for diner in diners
        ]
    )
)

web_search_chain = (
    RunnableLambda(lambda diner:
            {
                'search_query': diner['search_query'],
                'diner': diner['diner'],
                'results': web_search(
                    web_query=diner['search_query'],
                    num_results=NUM_SEARCH_RESULTS_PER_QUERY,
                ),
            }
    )
)

do_searches_chain = get_web_searches_chain | web_search_chain.map()