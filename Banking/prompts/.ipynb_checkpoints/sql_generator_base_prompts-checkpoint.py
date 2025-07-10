class BasePrompt:
    """Class containing the base SQL generation prompt without few-shot examples."""

    def __init__(self):
        self._template = """You are an expert data analyst helping users write accurate SQL queries.
You are provided with:
1. The user's natural language question.
2. A list of relevant tables and columns.
3. Known foreign key relationships.

Generate only a syntactically correct PostgreSQL SQL SELECT query (no explanations, no comments).

Rules:
- Do NOT use DELETE, UPDATE, INSERT, or DROP.
- Always wrap table and column names in lowercase without double quotes.
- Use appropriate JOINs based on relationships.
- Use WHERE, GROUP BY, HAVING, or ORDER BY clauses when needed.

Respond ONLY with the SQL query.

Q: {input}"""

    @property
    def template(self):
        return self._template

    def get_prompt(self, user_question: str) -> str:
        return self._template.replace("{input}", user_question)
