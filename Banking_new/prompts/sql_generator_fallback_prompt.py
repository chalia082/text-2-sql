class SQLGeneratorFallbackPrompt:
    """Fallback prompt used when the user's question doesn't match known tables or columns."""

    def __init__(self):
        self._template = """The user's question could not be directly mapped to known tables or columns.

Try your best to infer what the user might be asking using general SQL knowledge.

Still follow these strict rules:
- Output only one syntactically correct SQL SELECT query.
- Do not return UPDATE, DELETE, INSERT, or DROP queries.
- Prefer using COUNT, AVG, or JOINs based on likely intent.
- If the question is vague or references missing data, generate a best-effort SELECT using available structure.

User Question:
{input}
"""

    @property
    def template(self):
        return self._template

    def get_prompt(self, user_question: str) -> str:
        return self._template.replace("{input}", user_question)
