from langchain.vectorstores import Chroma
from langchain.embeddings import HuggingFaceBgeEmbeddings

def loadEmbeddings(dir):
    model_name = "C:/Users/sashi/PycharmProjects/cai/rag/bge-base-en-v1.5"
    encode_kwargs = {'normalize_embeddings': True}  # set True to compute cosine similarity
    model_norm = HuggingFaceBgeEmbeddings(
        model_name=model_name,
        model_kwargs={'device': 'cpu'},
        encode_kwargs=encode_kwargs
    )
    # load from disk
    return Chroma(persist_directory=dir, embedding_function=model_norm)


db3 = loadEmbeddings("db3")
query = ""

docs = db3.similarity_search(query)
#print(docs[0].page_content)


retriever = db3.as_retriever()
print(retriever.get_relevant_documents(query))
