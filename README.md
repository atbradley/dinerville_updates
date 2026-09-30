# Dinerville Updates

A simple, learning-oriented app using LangChain to identify diners that need to be updated on [Dinerville](https://www.dinerville.info).

Since I was more interested in learning LangChain than anything else here, this is over-engineered--an agent with web access does this just as well. It:

1. Grabs a list of diners, with locations and open/closed status, from Dinerville's database;
2. Creates search queries designed to find out if those diners are still open/closed;
3. Runs those search queries using [Ollama's web search API](https://docs.ollama.com/capabilities/web-search)
4. Sends the resulting page content to an LLM with a prompt ordering it to determine whether the diner is open/closed.
5. Prints the results from the models.

The main entry point to the code is `diner_status_chain.py`.

Some of this code and many of the ideas in it is from the book _[AI Agents and Applications](https://www.manning.com/books/ai-agents-and-applications)_, by Roberto Infante.