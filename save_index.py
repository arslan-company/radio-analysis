import os

from llama_index import GPTVectorStoreIndex, PromptHelper
from llama_index import SimpleDirectoryReader, ServiceContext, LLMPredictor
from langchain.chat_models import ChatOpenAI

# Uncomment to specify your OpenAI API key here (local testing only, not in production!), or add corresponding environment variable (recommended)
# os.environ['OPENAI_API_KEY'] = "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"

# This example uses gpt-3.5-turbo by default; feel free to change if desired
llm_predictor = LLMPredictor(llm=ChatOpenAI(temperature=0, model_name="gpt-3.5-turbo"))

# Configure prompt parameters and initialise helper
max_input_size = 4096
num_output = 256
max_chunk_overlap = 20

prompt_helper = PromptHelper(max_input_size, num_output, max_chunk_overlap)

# Load documents from the 'data' directory
documents = SimpleDirectoryReader('data', recursive=True).load_data()
service_context = ServiceContext.from_defaults(llm_predictor=llm_predictor, prompt_helper=prompt_helper)

index = GPTVectorStoreIndex.from_documents(
    documents,service_context=service_context
)

index.storage_context.persist()
