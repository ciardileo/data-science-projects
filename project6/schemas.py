"""
O pydantic ajuda a criar modelos de estados para estruturar o output das LLMs
"""

# imports
from pydantic import BaseModel
from typing import List  # type hints

# models
# estrutura de uma single query de pesquisa
class QueryResult(BaseModel):
    title: str = None
    url: str = None
    resume: str = None

# estrutura da pesquisa geral
class ReportState(BaseModel):
    user_input: str = None
    final_response: str = None
    queries: List[str] = []