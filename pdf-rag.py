from langchain_community.document_loaders import UnstructuredPDFLoader
from langchain_community.document_loaders import OnlinePDFLoader
from langchain_ollama import OllamaEmbeddings
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import Chroma
import os.path as osp
import ollama as oll


def load_pdf(doc_path, verbose: int = 0):
    if doc_path:
        loader = UnstructuredPDFLoader(file_path=doc_path)
        data = loader.load()
        print("done loading....")
    else:
        print("Upload a PDF file")

    if verbose:
        content = data[0].page_content
        print(content[:100])
        
    return data


def extract_text(data, verbose: int = 0):
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=1200, chunk_overlap=300)
    chunks = text_splitter.split_documents(data)
    print("done splitting....")

    if verbose:
        print(f"Number of chunks: {len(chunks)}")
        print(f"Example chunk: {chunks[0]}")
    
    return chunks

def make_vector_db(chunks):

    oll.pull("nomic-embed-text")

    vector_db = Chroma.from_documents(
        documents=chunks,
        embedding=OllamaEmbeddings(model="nomic-embed-text"),
        collection_name="simple-rag",
    )
    print("done adding to vector database....")
    
    return vector_db

def main():

    doc_path: str = osp.join('data', 'BOI.pdf')
    MODEL: str = 'llama3.2'


    data = load_pdf(doc_path)
    chunks = extract_text(data)
    vector_db = make_vector_db(chunks)

if __name__ == "__main__":
    main()