import os
import json
from dotenv import load_dotenv
from langchain_groq import ChatGroq
from langchain_openai import ChatOpenAI
from langchain_community.document_loaders import PyPDFLoader
from langchain import hub
from langchain_core.output_parsers import JsonOutputParser
# from langchin_core.runnables import Runnable

class HireMind:
    def __init__(self):
        load_dotenv()
        self.read_prompt = hub.pull("aicraft/resume_details_extractor")
        self.analyse_prompt = hub.pull("aicraft/hiremind_json_score")
        self.jsonparser=JsonOutputParser()
        os.environ["LANGCHAIN_TRACING_V2"]="true"
        os.environ["LANGSMITH_API_KEY"] = os.getenv("LANGSMITH_API_KEY")
        os.environ["LANGSMITH_ENDPOINT"] = os.getenv("LANGSMITH_ENDPOINT")
        os.environ["LANGSMITH_PROJECT"] = os.getenv("LANGSMITH_PROJECT")
    
    def load_model(self, model_name: str, api_key: str, openai=True):
        self.model_name = model_name
        if openai:
            self.__model = ChatOpenAI(temperature=0, model=self.model_name, 
                                      max_completion_tokens=500, api_key=api_key)
        else:
            self.__model = ChatGroq(temperature=0.7, model=self.model_name, 
                                    model_kwargs={"max_completion_tokens": 500}, api_key=api_key, verbose=True)
    
    def test_model(self):
        if self.__model:
            try:
                test_output = self.__model.invoke("", max_completion_tokens=1)
            except Exception as e:
                raise ValueError(f"Failed to load model {self.model_name} with error: {e}")    
    
    def read_resume(self, resume_path: str):
        resume = PyPDFLoader("data/resume_sanjay.pdf")
        documents=resume.load()
        resume_text = "\n".join([doc.page_content for doc in documents])
        self.__chain = self.read_prompt | self.__model | self.jsonparser
        out=self.__chain.invoke({"resume_text": resume_text})
        return out
    
    def analyse_resume(self, resume_content, jd_content):
        self.__chain = self.analyse_prompt | self.__model | self.jsonparser
        out=self.__chain.invoke({"JD_TEXT_HERE":jd_content,
              "RESUME_TEXT_HERE":resume_content})
        return out

#a=HireMind()
# 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
# a.load_model(model_name='llama-3.3-70b-versatile', api_key='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', openai=False)
# resume = a.read_resume(resume_path="data/resume_sanjay.pdf")
# JD_TEXT_HERE = """
# Develop and maintain high-performance applications using Python and related frameworks (Django, Flask, FastAPI).
# Build and integrate RESTful APIs with third-party systems to ensure seamless data exchange.
# Work with large datasets, utilizing Pandas, NumPy, and other data processing tools.
# Automate tasks using Python scripting, Selenium, Airflow, and other automation frameworks.
# Ensure code quality through test-driven development (TDD/BDD) and debugging best practices.
# Collaborate with Agile teams, participate in code reviews, and follow CI/CD and DevOps best practices.
# Optimize system performance, scalability, and reliability.
# Good understanding of database management (SQL, NoSQL, MongoDB, Cassandra, Elasticsearch)
# Exposure to Gen AI, AI/ML concepts, and visualization tools like QlikSense/Tableau is desirable.
# Strong knowledge of OOPs, data structures, and algorithms.
# """

# out = a.analyse_resume(resume_content=resume, jd_content=JD_TEXT_HERE)
# print(out)
# print(type(out))