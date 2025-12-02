import os
from langchain_core.prompts import PromptTemplate
from langchain_classic.chains.llm import LLMChain
from langchain_groq import ChatGroq


def get_llm_chain():
        prompt = PromptTemplate.from_template(
            """
            You are a helpful AI assistant.
            Use ONLY the provided context to answer the question.

            Context:
            {context}

            Question: {question}

            If answer is not in the context, say: "I don't know."
            """
        )

        llm = ChatGroq(model="llama-3.3-70b-versatile", api_key=os.getenv("GROQ_API_KEY"))
        return LLMChain(llm=llm, prompt=prompt)

