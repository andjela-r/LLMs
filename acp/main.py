import asyncio
from acp_sdk.client import Client
from smolagents import InferenceClientModel
from colorama import Fore

model = InferenceClientModel()

leetcode_q = """
Your task is to solve the following Leetcode problem:
Given an array of integers nums and an integer target, return indices of the two numbers such that they add up to target.

You may assume that each input would have exactly one solution, and you may not use the same element twice.

You can return the answer in the function in any order. 

### Important Instructions:
Only return the implementation of the function. 
Do NOT create test cases or print statements.
Do NOT run or return the output of the function.
Do NOT include `if __name__ == "__main__"` or any usage code.

Your final output should be just the definition of the function that solves the problem."""

leetcode_hard_q = """
Your task is to solve the following Leetcode problem:
Given a string s and a dictionary of strings wordDict, add spaces in s to construct a sentence where each word is a valid dictionary word. Return all such possible sentences in any order.

Note that the same word in the dictionary may be reused multiple times in the segmentation.

 

Example 1:

Input: s = "catsanddog", wordDict = ["cat","cats","and","sand","dog"]
Output: ["cats and dog","cat sand dog"]
Example 2:

Input: s = "pineapplepenapple", wordDict = ["apple","pen","applepen","pine","pineapple"]
Output: ["pine apple pen apple","pineapple pen apple","pine applepen apple"]
Explanation: Note that you are allowed to reuse a dictionary word.
Example 3:

Input: s = "catsandog", wordDict = ["cats","dog","sand","and","cat"]
Output: []
 

Constraints:

1 <= s.length <= 20
1 <= wordDict.length <= 1000
1 <= wordDict[i].length <= 10
s and wordDict[i] consist of only lowercase English letters.
All the strings of wordDict are unique.
Input is generated in a way that the length of the answer doesn't exceed 105.

### Important Instructions:
Only return the implementation of the function. 
Do NOT create test cases or print statements.
Do NOT run or return the output of the function.
Do NOT include `if __name__ == "__main__"` or any usage code.

Your final output should be just the definition of the function that solves the problem.
"""

async def leetcode_solver() -> None:
    async with Client(base_url="http://localhost:8000") as coder, Client(base_url="http://localhost:8001") as explainer:
        run1 = await coder.run_sync(
            agent="coder", input = leetcode_hard_q
        )
        content = run1.output[0].parts[0].content

        print(Fore.LIGHTMAGENTA_EX+ content + Fore.RESET)

        run2 = await explainer.run_sync(
            agent="explainer", input=f"Code: {content}\n\n Explain this code line by line, and the whole solution based on the task:\n {leetcode_hard_q}"
        )
        print(Fore.YELLOW + run2.output[0].parts[0].content + Fore.RESET)

if __name__ == "__main__":
    asyncio.run(leetcode_solver())