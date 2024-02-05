import os
import streamlit as st

from llama_index import StorageContext, load_index_from_storage

# Uncomment to specify your OpenAI API key here (local testing only, not in production!), or add corresponding environment variable (recommended)
# os.environ['OPENAI_API_KEY'] = "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"

# rebuild storage context
storage_context = StorageContext.from_defaults(persist_dir="./storage")
# load index
index = load_index_from_storage(storage_context)

# Define a simple Streamlit app
st.title("Akıllı bıdığa sor")
query = st.text_area("Bana bu gün ne sormak istersin?", "")
query_engine = index.as_query_engine()

if st.button("Submit"):
    if not query.strip():
        st.error(f"Please provide the search query.")
    else:
        try:
            response = query_engine.query(query)
            st.write("Sorgu: ", query)
            st.write("Cevap: ", response)
        except Exception as e:
            st.error(f"An error occurred: {e}")

