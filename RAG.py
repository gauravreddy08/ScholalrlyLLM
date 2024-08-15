from langchain.docstore.document import Document
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import FAISS
from langchain_openai import OpenAIEmbeddings

class RAG():
    def __init__(self, filename='DATA.txt'):
        
        with open(filename, 'r') as file:
            raw_data = file.read()

        raw_data = raw_data.split("\n\n")

        self.embeddings = OpenAIEmbeddings()
        
        self.build(raw_data)
        
    def build(self, raw_data, split_text=False):
        docs = [Document(page_content=data) for data in raw_data]

        if split_text:
            text_splitter = RecursiveCharacterTextSplitter(chunk_size=3000, chunk_overlap=300)
            docs = text_splitter.split_documents(docs)

        self.db = FAISS.from_documents(documents=docs, embedding=self.embeddings)

    def retrieve(self, query, k=10):
        docs = self.db.similarity_search(query=query, k=10)
        
        if docs:
            return "\n".join(doc.page_content for doc in docs)
        else: 
            return ""

if __name__=='__main__':
    rag = RAG()
    print(rag.retrieve('Publication Date: 2023'))