from django.conf import settings
from openai import OpenAI
from .services.rag import RAGService
from .services.prompt import PromptBuilder
from .services.llm import LLMService
from .serializers import AIQuerySerializer
from rest_framework.viewsets import GenericViewSet
from rest_framework.mixins import CreateModelMixin
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework import status


class AIViewset(CreateModelMixin, GenericViewSet):
    serializer_class = AIQuerySerializer
    permission_classes = [IsAuthenticated]

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        question = serializer.validated_data["question"]
        rag_service = RAGService(
            prompt_builder=PromptBuilder(),
            llm_service=LLMService(client=OpenAI(api_key=settings.OPENAI_API_KEY)),
        )
        response = rag_service.answer_question(question, self.request.user)

        return Response(response, status=status.HTTP_200_OK)
