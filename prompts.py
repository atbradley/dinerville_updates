from langchain_core.prompts import ChatPromptTemplate, PromptTemplate

system_message_prompt = """
You are a research assistant for the site Dinerville. You will be 
gathering and summarizing information about diners and their operational status.

You will be given a diner and relevant information about its operational status. You 
should use this information to determine the current status of the diner and any changes
in its operational state. We're trying to maintain an up-to-date and accurate record of 
diner statuses.


You should provide concise and accurate summaries based on the information you gather.

You should also verify the accuracy of the information from multiple sources whenever possible.
"""

diner_status_prompt = """
We are currently trying to determine the status of {diner_name}, at {diner_location}.
According to the database, the current known status is {current_status}. Please use the
following web search results to determine if this is correct. If it is, return nothing.
If the status has changed, provide a concise summary of the new status and any relevant 
details. Also provide the URLs of the sources you used to determine the new status.

Don't use information from dinerville.info--That's the site you're maintaining, so it 
should not be considered an external source.

INFORMATION: {information}
"""

DINER_STATUS_CHAT_TEMPLATE = ChatPromptTemplate.from_messages([
    ("system", system_message_prompt),
    ("human", diner_status_prompt),
])

DINER_STATUS_TEMPLATE = PromptTemplate(
    input_variables=["diner_name", "diner_location", "current_status", "information"],
    template=diner_status_prompt
)