# Set HF_HOME environment variable
import os
os.environ["HF_HOME"] = "E:/Cache"  # Set the path to your desired cache directory
os.environ["LANGCHAIN_TRACING_V2"]="true"                       #LangSmith: automatically trace for all codes executed
os.environ["LANGCHAIN_API_KEY"]=os.getenv("LANGCHAIN_API_KEY")  #To store monitoring results of chatbot calls for analisys via LangSmith

import streamlit as st
from dotenv import load_dotenv
from PyPDF2 import PdfReader
from langchain.text_splitter import CharacterTextSplitter
#from langchain_community.embeddings import CohereEmbeddings
from langchain_community.vectorstores import faiss
from langchain_cohere import ChatCohere, CohereEmbeddings
from langchain.memory import ConversationBufferMemory
from langchain.chains.conversational_retrieval.base import ConversationalRetrievalChain
from langchain.chains import retrieval_qa
from htmlTemplates import css, bot_template, user_template

#Using cohere.Reranker to optimize query search
from langchain.retrievers.contextual_compression import ContextualCompressionRetriever
from langchain_cohere import CohereRerank

def get_pdf_text(pdf_docs):
    text = ""
    for pdf in pdf_docs:
        pdf_reader = PdfReader(pdf)
        for page in pdf_reader.pages:
            text += page.extract_text()
    return text


def get_text_chunks(text):
    text_splitter = CharacterTextSplitter(
        separator="\n",
        chunk_size=1000,
        chunk_overlap=200,
        length_function=len
    )
    chunks = text_splitter.split_text(text)
    return chunks


def get_vectorstore(text_chunks):
    embeddings = CohereEmbeddings()
    vectorstore = faiss.FAISS.from_texts(texts=text_chunks, embedding=embeddings)
    return vectorstore

def get_chat_chain(vectorstore):
    llm = ChatCohere()
    memory = ConversationBufferMemory(memory_key='chat_history', return_messages=True)
    retriever = vectorstore.as_retriever()
    #conversation_chain = ConversationalRetrievalChain.from_llm(llm=llm, retriever=retriever, memory=memory)
    
    #Optimized using Cohere.Reranker to comprese all chunks to few relevant chunks
    compressor = CohereRerank(top_n=8)
    compression_retriever = ContextualCompressionRetriever(base_compressor=compressor, base_retriever=retriever)
    conversation_chain = ConversationalRetrievalChain.from_llm(llm=llm, retriever=compression_retriever, memory=memory)
    return conversation_chain

def handle_userinput(user_question):
    response = st.session_state.conversation({'question': user_question})
    st.session_state.chat_history = response['chat_history']

    for i, message in enumerate(st.session_state.chat_history):
        if i % 2 == 0:
            st.write(user_template.replace(
                "{{MSG}}", message.content), unsafe_allow_html=True)
        else:
            st.write(bot_template.replace(
                "{{MSG}}", message.content), unsafe_allow_html=True)


def main():
    load_dotenv()
    st.write(css, unsafe_allow_html=True)

    if "conversation" not in st.session_state:
        st.session_state.conversation = None
    if "chat_history" not in st.session_state:
        st.session_state.chat_history = None

    user_question = st.chat_input("Ask a question about your documents:")
    if user_question:
        handle_userinput(user_question)

    with st.sidebar:
        st.header("Chat with multiple PDFs :books:")
        st.subheader("Developed by Kartikeya Dubey")
        st.link_button(":link: LinkedIn","https://www.linkedin.com/in/kartikeyadubey/")
        st.link_button(":link: GitHub","https://github.com/kartikeya-dubey")
        pdf_docs = st.file_uploader(
            "Upload your PDFs here and click on 'Process'", accept_multiple_files=True)
        if st.button("Process"):
            with st.spinner("Processing"):
                # get pdf text
                raw_text = get_pdf_text(pdf_docs)

                # get the text chunks
                text_chunks = get_text_chunks(raw_text)

                # create vector store
                vectorstore = get_vectorstore(text_chunks)

                # create conversation chain
                st.session_state.conversation = get_chat_chain(
                    vectorstore)


if __name__ == '__main__':
    main()