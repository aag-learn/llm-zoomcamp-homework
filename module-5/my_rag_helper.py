INSTRUCTIONS = """
Your task is to answer questions from the course participants
based on the provided context.

Use the context to find relevant information and provide accurate
answers. If the answer is not found in the context,
respond with "I don't know."
"""

PROMPT_TEMPLATE = """
QUESTION: {question}

CONTEXT:
{context}
""".strip()


class RAGBase:
    def __init__(
        self,
        index,
        llm_client,
        instructions=INSTRUCTIONS,
        prompt_template=PROMPT_TEMPLATE,
        model="gpt-5.4-mini",
    ):
        self.index = index
        self.llm_client = llm_client
        self.instructions = instructions
        self.prompt_template = prompt_template
        self.model = model

    def search(self, query, num_results=5):
        return self.index.search(query, num_results=num_results)

    def build_context(self, search_results):
        lines = []

        for doc in search_results:
            lines.append(doc["filename"])
            lines.append(doc["content"])
            lines.append("")

        return "\n".join(lines).strip()

    def build_prompt(self, query, search_results):
        context = self.build_context(search_results)
        return self.prompt_template.format(question=query, context=context)

    def llm(self, prompt):
        input_messages = [
            {"role": "developer", "content": self.instructions},
            {"role": "user", "content": prompt},
        ]

        response = self.llm_client.responses.create(
            model=self.model, input=input_messages
        )

        return response

    def rag(self, query):
        search_results = self.search(query)
        prompt = self.build_prompt(query, search_results)
        response = self.llm(prompt)
        return response.output_text


class RAGTraced(RAGBase):
    def __init__(
        self,
        index,
        llm_client,
        tracer,
        instructions=INSTRUCTIONS,
        prompt_template=PROMPT_TEMPLATE,
        model="gpt-5.4-mini",
    ):
        super().__init__(index, llm_client, instructions, prompt_template, model)
        self.tracer = tracer

    def rag(self, query):
        result = None
        with self.tracer.start_as_current_span("rag") as span:
            result = super().rag(query)
            # your code here
            span.set_attribute("query", query)
            span.set_attribute("result", result)
            return result

    def search(self, query, num_results=5):
        with self.tracer.start_as_current_span("search") as span:
            span.set_attribute("query", query)
            results = super().search(query, num_results)
            span.set_attribute("num_results", num_results)
            return results

    def llm(self, prompt):
        with self.tracer.start_as_current_span("llm") as span:
            input_messages = [
                {"role": "developer", "content": self.instructions},
                {"role": "user", "content": prompt},
            ]

            response = self.llm_client.responses.create(
                model=self.model, input=input_messages
            )

            span.set_attribute(
                "input_messages.role.developer.content",
                input_messages[0]["content"],
            )

            span.set_attribute(
                "input_messages.role.user.content",
                input_messages[1]["content"],
            )
            # span.set_attribute("answer", response.output_text)
            span.set_attribute("input_tokens", response.usage.input_tokens)
            span.set_attribute("output_tokens", response.usage.output_tokens)
            return response
