class PromptBuilder:
    """ Responsible for creating prompts for LLMs"""
    def build_rag_prompt(self, question: str, chunks: list[str]) -> str:
        SYSTEM_PROMPT = """
        You are a helpful AI assistant.

        Use ONLY the provided context.

        If the answer is not in the context,
        say you don't know.

        Do not make up information.
        """
        if not chunks:
            context = "No relevant context found."
        else:
            context = "\n\n".join(
                f"chunk{index}\n---------\n{chunk}" for index, chunk in enumerate(chunks, start=1)
            )
        
        return (
            f"{SYSTEM_PROMPT}\n\n"
            f"Context:\n{context}\n\n"
            f"Question: {question}\n"
            f"Answer:"
        )