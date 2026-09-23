from documents.services.search import semantic_search


class RAGService:
    """ Coordinates semantic search and answer generation """
    def __init__(self, prompt_builder, llm_service):
        self.prompt_builder = prompt_builder
        self.llm_service = llm_service

    def answer_question(self, question: str, user):
        chunks = list(semantic_search(question, user))
        contents = [chunk.content for chunk in chunks]
        prompt = self.prompt_builder.build_rag_prompt(question, contents)
        answer = self.llm_service.generate_answer(prompt)

        response = {
            "answer": answer,
            "sources": [
                {"document": chunk.document.title, "chunk_id": chunk.id}
                for chunk in chunks
            ]
        }

        return response