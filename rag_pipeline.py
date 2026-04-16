
from langchain_community.vectorstores import FAISS
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_core.prompts import PromptTemplate
from langchain_core.runnables import RunnablePassthrough
from langchain_core.output_parsers import StrOutputParser
from langchain_community.llms import HuggingFacePipeline
from transformers import pipeline


embedding = HuggingFaceEmbeddings(
    model_name="sentence-transformers/all-MiniLM-L6-v2"
)

db = FAISS.load_local("faiss_index", embedding,allow_dangerous_deserialization=True)
retriever = db.as_retriever(search_kwargs={"k": 3})


pipe = pipeline(
    "text2text-generation",
    model="google/flan-t5-large",
    max_new_tokens=200,
    temperature=0.5
)

llm = HuggingFacePipeline(pipeline=pipe)


prompt = PromptTemplate(
    template="""Answer the question clearly using the context.

Context:
{context}

Question:
{question}

Answer in steps:""",
    input_variables=["context", "question"]
)

def format_docs(docs):
    return "\n\n".join(doc.page_content for doc in docs)


qa_chain = (
    {
        "context": retriever | format_docs,
        "question": RunnablePassthrough()
    }
    | prompt
    | llm
    | StrOutputParser()
)


def ask_question(query):
    return qa_chain.invoke(query)


