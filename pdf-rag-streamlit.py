from langchain_community.document_loaders import UnstructuredPDFLoader
from langchain_community.document_loaders import OnlinePDFLoader
from langchain_ollama import OllamaEmbeddings
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import Chroma
from langchain.prompts import ChatPromptTemplate, PromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_ollama import ChatOllama
from langchain_core.runnables import RunnablePassthrough
from langchain.retrievers.multi_query import MultiQueryRetriever
import os.path as osp
import ollama as oll
from time import time
import logging
import streamlit as st

logging.basicConfig(level=logging.INFO)

def load_pdf(doc_path, verbose: int = 0):
    start = time()
    if doc_path:
        loader = UnstructuredPDFLoader(file_path=doc_path)
        data = loader.load()
        print("done loading....")
    else:
        print("Upload a PDF file")

    if verbose:
        content = data[0].page_content
        print(content[:100])
    print(round(((time() - start) / 60), 2))
    return data


def extract_text(data, verbose: int = 0):
    start = time()
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=1200, chunk_overlap=300)
    chunks = text_splitter.split_documents(data)
    print("done splitting....")

    if verbose:
        print(f"Number of chunks: {len(chunks)}")
        print(f"Example chunk: {chunks[0]}")
    print(round(((time() - start) / 60), 2))
    return chunks

def make_vector_db(chunks):
    start = time()
    oll.pull("nomic-embed-text")

    vector_db = Chroma.from_documents(
        documents=chunks,
        embedding=OllamaEmbeddings(model="nomic-embed-text"),
        collection_name="simple-rag",
    )
    print("done adding to vector database....")
    print(round(((time() - start) / 60), 2))
    return vector_db

def retrieval(model, vector_db):
    start = time()
    llm = ChatOllama(model=model)

    QUERY_PROMPT = PromptTemplate(
        input_variables=["question"],
        template="""You are an AI language model assistant. Your task is to generate five
        different versions of the given user question to retrieve relevant documents from
        a vector database. By generating multiple perspectives on the user question, your
        goal is to help the user overcome some of the limitations of the distance-based
        similarity search. Provide these alternative questions separated by newlines.
        Original question: {question}""",
    )

    retriever = MultiQueryRetriever.from_llm(
        vector_db.as_retriever(), llm, prompt=QUERY_PROMPT
    )

    template = """Answer the question based ONLY on the following context:
    {context}
    Question: {question}
    """

    prompt = ChatPromptTemplate.from_template(template)

    chain = (
        {"context": retriever, "question": RunnablePassthrough()}
        | prompt
        | llm
        | StrOutputParser()
    )
    print(round(((time() - start) / 60), 2))
    return chain

def main():

    doc_path: str = osp.join('data', 'BOI.pdf')
    MODEL: str = 'llama3.2'

    data = load_pdf(doc_path)
    chunks = extract_text(data)
    vector_db = make_vector_db(chunks)
    chain = retrieval(MODEL, vector_db)

    st.title("Document Assistant")

    # User input
    user_input = st.text_input("Enter your question:", "")

    if user_input:
        with st.spinner("Generating response..."):
            try:

                response = chain.invoke(input=user_input)

                st.markdown("**Assistant:**")
                st.write(response)
            except Exception as e:
                st.error(f"An error occurred: {str(e)}")
    else:
        st.info("Please enter a question to get started.")


if __name__ == "__main__":
    main()