import os
from typing import List
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser

from config import AppConfig, PromptTemplates


class MSAAnalyzer:
    """Class to handle MSA analysis using LLM."""
    
    def __init__(self, api_key: str = None, model: str = AppConfig.DEFAULT_MODEL, temperature: float = AppConfig.DEFAULT_TEMPERATURE):
        """Initialize the LLM."""
        if api_key:
            os.environ["OPENAI_API_KEY"] = api_key
        elif not os.getenv("OPENAI_API_KEY"):
            raise ValueError("OpenAI API key is required. Provide it as parameter or set OPENAI_API_KEY environment variable.")
        
        self.llm = ChatOpenAI(
            model=model,
            temperature=temperature,
            openai_api_key=os.getenv("OPENAI_API_KEY")
        )
        self.output_parser = StrOutputParser()
    
    def analyze_contract_terms(self, contract_text: str) -> str:
        """Extract key terms from a contract."""
        prompt = ChatPromptTemplate.from_template(PromptTemplates.CONTRACT_ANALYSIS)
        
        chain = prompt | self.llm | self.output_parser
        return chain.invoke({"contract_text": contract_text})
    
    def compare_contracts(self, master_contract: str, amendment_contract: str, amendment_number: int) -> str:
        """Compare master contract with amendment and identify changes."""
        prompt = ChatPromptTemplate.from_template(PromptTemplates.CONTRACT_COMPARISON)
        
        chain = prompt | self.llm | self.output_parser
        return chain.invoke({
            "master_contract": master_contract,
            "amendment_contract": amendment_contract,
            "amendment_number": amendment_number
        })
    
    def generate_comprehensive_summary(self, master_contract: str, amendments_analysis: List[str]) -> str:
        """Generate a comprehensive summary of all changes across amendments."""
        amendments_text = "\n\n".join([f"Amendment {i+1} Analysis:\n{analysis}" 
                                     for i, analysis in enumerate(amendments_analysis)])
        
        prompt = ChatPromptTemplate.from_template(PromptTemplates.COMPREHENSIVE_SUMMARY)
        
        chain = prompt | self.llm | self.output_parser
        return chain.invoke({"amendments_analysis": amendments_text})
    
    def validate_api_key(self) -> bool:
        """Validate if the OpenAI API key is working."""
        try:
            # Simple test call to validate the API key
            test_prompt = ChatPromptTemplate.from_template("Say 'API key is valid'")
            chain = test_prompt | self.llm | self.output_parser
            response = chain.invoke({})
            return "valid" in response.lower()
        except Exception:
            return False