
from fastapi import FastAPI
from pydantic import BaseModel
from typing import List, Dict
import re
import os
from langchain_groq import ChatGroq

app = FastAPI()

# Use GROQ_API_KEY from environment
llm = ChatGroq(
    model="llama3-8b-8192",
    temperature=0,
    groq_api_key=os.getenv("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")
)

class SkinRequest(BaseModel):
    skin_issues: List[str]
    skin_type: str

@app.post("/get-chemical-combos/")
def get_chemical_combinations(req: SkinRequest):
    results = {}

    for issue in req.skin_issues:
        prompt = (
            f"Give only the most effective chemical combinations used to treat {issue} for {req.skin_type} skin. "
            "Don't include chemicals with heavy side effects like benzoyl peroxide. You can include natural ingredients too like plant or fruit extracts. "
            "Provide the output in a numbered list format only. No introduction, no headings, no extra text."
        )

        try:
            response = llm.invoke(prompt).content
            lines = response.strip().split("\n")

            cleaned_chemicals = [
                re.sub(r"^\d+\.\s*", "", line).strip()
                for line in lines if line.strip() and not line.lower().startswith("here is")
            ]
            results[issue.lower()] = cleaned_chemicals

        except Exception as e:
            results[issue.lower()] = [f"Error fetching data: {e}"]

    return results
