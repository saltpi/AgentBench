from langchain_core.tools import BaseTool
from src.tools.humaneval_tools.generators import generator_factory
from src.tools.humaneval_tools.executors import executor_factory
from src.tools.humaneval_tools.generators.generator_types import Generator
from src.tools.humaneval_tools.executors.executor_types import Executor
from langchain_openai import ChatOpenAI

from typing import Optional
import re

def evaluate_humaneval(output=None, label=None):
    return "True" in output, None

def parse_first_func(code: str, lang: str = "python") -> Optional[str]:
    assert lang == "python", "Only python is supported for now. TODO: Rust"
    code_lines = code.split("\n")
    def_i = -1
    last_i = 0
    got_return = False
    for i, line in enumerate(code_lines):
        if line.startswith("def "):
            if def_i == -1:
                def_i = i
            else:
                break
        elif "return" in line and def_i != -1:
            got_return = True
        if line == "" and def_i != -1 and got_return:
            last_i = i
            break

    if last_i == 0:
        last_i = len(code_lines) - 1

    if def_i == -1:
        return None

    return "\n".join(code_lines[def_i:last_i+1]).rstrip("[/PYTHON]")

def parse_code_block(string: str, lang: str = "python") -> Optional[str]:
    code_pattern = fr"```{lang}\n(.*?)\n```"
    match = re.search(code_pattern, string, re.DOTALL)

    if match:
        return match.group(1)

    generic_code_pattern = r"```\n(.*?)\n```"
    match = re.search(generic_code_pattern, string, re.DOTALL)

    if match:
        return match.group(1)

    return parse_first_func(string, lang)

class GeneratorTool(BaseTool):
    name: str = "generate"
    description: str = """Generate unit tests for functions given the signature and docstring.
    **IMPORTANT**
    - your unit tests should be like

    assert <func_name>(<arguments>) == <expected_value>
    assert <func_name>(<arguments>) == <expected_value>
    ...

    with appropriate <func_name> from [func signature], <arguments> and <expected_value> as Examples did.
    """
    gen: Generator = generator_factory("python")
    llm: ChatOpenAI
    def _run(self, query) -> str:
        return self.gen.internal_tests(query, self.llm, 1)
    
class ExecutorTool(BaseTool):
    name: str = "execute"
    description: str = """Execute the given code using LeetCode Python executor
    """
    is_leet: bool = False
    exe: Executor = executor_factory("python", is_leet=False)
    tests_i: str = ""
    def _run(self, func_impl) -> str:
        func_impl = parse_code_block(func_impl)
        is_passing, feedback, _ = self.exe.execute(func_impl, self.tests_i)
        if is_passing:
            output = "Passed, use finish('func impl') tool to validate your answer\nFeedback:\n" + feedback 
        else:
            output = "Failed!\nFeedback:\n" + feedback
        return output
    
class FinishTool(BaseTool):
    name: str = "finish"
    description: str = """Finish the question with short answer"""
    exe: Executor = executor_factory("python", is_leet=False)
    entry_point: str = ""
    tests: list[str] = []
    def _run(self, func_impl) -> str:
        if isinstance(func_impl, str) and func_impl.startswith("```"):
            func_impl = parse_code_block(func_impl)
        if func_impl == '':
            return f"Answer: False"
        is_passing = self.exe.evaluate(self.entry_point, func_impl, self.tests, timeout=5)
        return f"Answer: {is_passing}"