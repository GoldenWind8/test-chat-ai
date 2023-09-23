from langchain.document_loaders import TextLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.vectorstores import Chroma
from langchain.embeddings import HuggingFaceBgeEmbeddings

#splitting the text into
loader = TextLoader('data.txt')
documents = loader.load()
text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
texts = text_splitter.split_documents(documents)
print(len(texts))


def generateEmbeddings():
    model_name = "C:/Users/sashi/PycharmProjects/cai/rag/bge-base-en-v1.5"
    encode_kwargs = {'normalize_embeddings': True}  # set True to compute cosine similarity
    model_norm = HuggingFaceBgeEmbeddings(
        model_name=model_name,
        model_kwargs={'device': 'cpu'},
        encode_kwargs=encode_kwargs
    )
    persist_directory = 'db3'
    ## Here is the nmew embeddings being used
    embedding = model_norm
    vectordb = Chroma.from_documents(documents=texts,
                                     embedding=embedding,
                                     persist_directory=persist_directory)
    return vectordb


vectordb = generateEmbeddings()
retriever = vectordb.as_retriever()
print(retriever.get_relevant_documents("Staff")[0].page_content)