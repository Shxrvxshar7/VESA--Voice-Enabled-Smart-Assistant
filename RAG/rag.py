from langchain_community.document_loaders import JSONLoader
from langchain_ollama import OllamaEmbeddings
from langchain_community.vectorstores import FAISS

class RAG:
    def __init__(self,path,label="label"):
        # load the JSON file
        loader = JSONLoader(
            file_path=path,
            jq_schema=".[]",
            content_key="query",
            metadata_func=lambda record, _: {label: record[label]}  # Add "_" for unused arg
        )

        examples = loader.load()

        # generate embeddings for the documents
        self.embeddings = OllamaEmbeddings(model="nomic-embed-text")
        self.vectorstore = FAISS.from_documents(documents=examples,embedding= self.embeddings)
       
 
    def retrive(self):
         retriever = self.vectorstore.as_retriever(search_kwargs={"k": 1})
         return retriever
        


# rag = RAG()
# retriver = rag.retrive()
# response = retriver.invoke("what is the temperature in newyork?")
# print("Classification Result:", response)
