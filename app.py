import os
from dotenv import load_dotenv
from PyPDF2 import PdfReader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_google_genai import GoogleGenerativeAIEmbeddings
import google.generativeai as genai
from langchain.vectorstores import FAISS
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.chains.question_answering import load_qa_chain
from langchain.prompts import PromptTemplate

# Load environment variables from .env file
load_dotenv()
API_KEY = os.getenv("API_KEY")

# Configure the API with the provided key
genai.configure(api_key=API_KEY)

def get_pdf_text(pdf_docs):
    text = ""
    for pdf in pdf_docs:
        pdf_reader = PdfReader(pdf)
        for page in pdf_reader.pages:
            text += page.extract_text()
    return text

def get_text_chunks(text):
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=10000, chunk_overlap=1000)
    chunks = text_splitter.split_text(text)
    return chunks

def get_vector_store(text_chunks):
    embeddings = GoogleGenerativeAIEmbeddings(model="models/embedding-001")
    vector_store = FAISS.from_texts(text_chunks, embedding=embeddings)
    vector_store.save_local("faiss_index")  # This creates the index

def load_vector_store(embeddings):
    try:
        new_db = FAISS.load_local("faiss_index", embeddings, allow_dangerous_deserialization=True)
        return new_db
    except FileNotFoundError:
        print("FAISS index not found. Please create it by processing PDF files first.")
        return None

def get_conversational_chain():
    prompt_template = """
    Answer the question in as detailed manner as possible from the provided context. Make sure to provide all the details. If the answer is not in the provided
    context, then just say, "answer is not available in the context." Don't provide the wrong answer.\n\n
    Context:\n {context}?\n
    Question:\n {question}\n

    Answer:
    """
    model = ChatGoogleGenerativeAI(model="gemini-pro", temperature=0.3)

    prompt = PromptTemplate(template=prompt_template, input_variables=["context", "question"])
    chain = load_qa_chain(model, chain_type="stuff", prompt=prompt)
    return chain

def user_input(user_question):
    embeddings = GoogleGenerativeAIEmbeddings(model="models/embedding-001")

    new_db = load_vector_store(embeddings)
    if new_db is None:  # If the index couldn't be loaded, exit early
        return

    docs = new_db.similarity_search(user_question)

    chain = get_conversational_chain()

    response = chain(
        {"input_documents": docs, "question": user_question}, return_only_outputs=True
    )

    print(response)
    return response["output_text"]

def main():
    # PDF upload section
    pdf_file = input("Enter the path of your PDF file (e.g., /content/myfile.pdf): ")

    # Process the PDF file and create the FAISS index
    try:
        raw_text = get_pdf_text([pdf_file])
        text_chunks = get_text_chunks(raw_text)
        get_vector_store(text_chunks)
        print("Done processing the PDF!")

        # Now, ask the user for questions
        while True:
            user_question = input("Ask a Question from the PDF Files (or type 'exit' to quit): ")
            if user_question.lower() == 'exit':
                break
            answer = user_input(user_question)
            print("Reply:", answer)

    except Exception as e:
        print(f"Error processing the PDF file: {e}")

if __name__ == "__main__":
    main()
