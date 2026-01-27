import math
import numexpr
from langchain_community.utilities.wolfram_alpha import WolframAlphaAPIWrapper
from langchain_core.tools import BaseTool
from pydantic import BaseModel, Field
from typing import Optional

class CalculatorTool(BaseTool):
    name: str = "Calculator"
    description: str = """Calculate expression using Python's numexpr library.
    Expression should be a single line mathematical expression that solves the problem.
    Examples:
        "37593 * 67" for "37593 times 67"
        "37593**(1/5)" for "37593^(1/5)"
    """
    
    def _run(self, expression: str) -> str:
        
        local_dict = {"pi": math.pi, "e": math.e}
        try:  
            return str(
                numexpr.evaluate(
                    expression.strip(),
                    global_dict={},  # restrict access to globals
                    local_dict=local_dict,  # add common mathematical functions
                )
            )
        except KeyboardInterrupt:
            exit(0)
        except:
            return "Error while evaluating expression!"
            
    
    async def _arun(self, expression: str) -> str: 
        local_dict = {"pi": math.pi, "e": math.e}
        return str(
            numexpr.evaluate(
                expression.strip(),
                global_dict={},  # restrict access to globals
                local_dict=local_dict,  # add common mathematical functions
            )
        )

class WolframAlpha(WolframAlphaAPIWrapper):
    """Subclass of WolframAlphaAPIWrapper with modified run method."""

    def run(self, query: str) -> str:
        """Run query through WolframAlpha and parse all results."""
        res = self.wolfram_client.query(query)

        try:
            results_pod = next(
                    pod for pod in res['pod'] if pod["@title"] in ["Result", "Results", "Exact result", "Complex roots"]
                )

            if isinstance(results_pod["subpod"], dict):
                answers = [results_pod["subpod"]["plaintext"]]
            elif isinstance(results_pod["subpod"], list):
                answers = [
                    subpod["plaintext"] for subpod in results_pod["subpod"] if subpod["plaintext"]
                ]
            else:
                raise TypeError("Not supported type")

        except (StopIteration, KeyError):
            return "Wolfram Alpha wasn't able to answer it"

        if not answers:
            return "No good Wolfram Alpha Result was found"
        else:
            # Join answers into a single string
            answers_str = "\n".join(answers)
            return answers_str

    async def arun(self, query: str) -> str:
        """Run query through WolframAlpha and parse all results."""
        res = await self.wolfram_client.aquery(query)
        print(f"res: {res}")  # Debug output

        try:
            results_pod = next(
                    pod for pod in res['pod'] if pod["@title"] in ["Result", "Results", "Exact result", "Complex roots"]
                )

            if isinstance(results_pod["subpod"], dict):
                answers = [results_pod["subpod"]["plaintext"]]
            elif isinstance(results_pod["subpod"], list):
                answers = [
                    subpod["plaintext"] for subpod in results_pod["subpod"] if subpod["plaintext"]
                ]
            else:
                raise TypeError("Not supported type")

        except (StopIteration, KeyError):
            return "Wolfram Alpha wasn't able to answer it"

        if not answers:
            return "No good Wolfram Alpha Result was found"

        answers_str = "\n".join(answers)
        return answers_str

class WolframAlphaTool(BaseTool):
    name: str = "WolframAlpha"
    description: str = """
    WolframAlpha Tool: Solve complex mathematical equations and perform symbolic computations.  

    Input should be a mathematical expression or equation that WolframAlpha can interpret and solve.  

    Examples:  
        - "Solve 2a + 3 = 2 - 5"  
        - "Factor c^2 + 6c - 27"  
        - "Integrate x^2 from 0 to 1"  
        - "What is 2x+5 = -3x + 7?"

    Use this tool exclusively for advanced mathematical problems, including algebra, calculus, and equation solving.
    If Calculator returns error, try to use WolframAlpha tool to solve complex math question.
    """
    api_wrapper: WolframAlpha = WolframAlpha()

    def _run(self, query: str) -> str:
        """Run query through WolframAlpha and parse all results."""
        return self.api_wrapper.run(query)

    async def _arun(self, query: str) -> str:
        return await self.api_wrapper.arun(query)
    
class FinishTool_schema(BaseModel):
    thought: Optional[str] = Field(
        description="Thought of current status and next step based on previous messages."
    )
    answer: str = Field(
        description="""answer should be a value or latex format expression in short without any equations. Do not include any = in your answer. If you can convert the \\frac{{a}}{{b}} into simple values, answer with simplified format.
You must answer with simplified format like as follows:
-12
\\frac{{-6}}{{5}}
(1,2)""",
    )

class FinishTool(BaseTool):
    name: str = "finish"
    description: str = """Finish the question with short answer"""
    # args_schema: Type[BaseModel] = FinishTool_schema
    
    def _run(self, answer: str = "") -> str:
        return f"Answer: {answer}"

    async def _arun(self, answer: str = "") -> str:
        return f"Answer: {answer}"