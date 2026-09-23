from django.shortcuts import render

from rest_framework.viewsets import GenericViewSet, ModelViewSet
from rest_framework.mixins import CreateModelMixin
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status

from .models import Document
from .serializers import SearchQuerySerializer, DocumentSerializer
from .services.search import semantic_search
from .tasks import process_documents

class DocumentViewSet(ModelViewSet):
    queryset = Document.objects.all()
    permission_classes = [IsAuthenticated]
    serializer_class = DocumentSerializer
    
    def get_queryset(self):
        return Document.objects.filter(user=self.request.user)
    
    def perform_create(self, serializer):
        document = serializer.save(user=self.request.user)
        process_documents.delay(document.id)
        
class SearchViewSet(CreateModelMixin, GenericViewSet):
    permission_classes = [IsAuthenticated]
    serializer_class = SearchQuerySerializer

    def perform_create(self, serializer):
        question = serializer.validated_data["question"]
        self.chunks = semantic_search(question, self.request.user)

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)

        data = [
            {"chunk_index": chunk.chunk_index, "content": chunk.content}
            for chunk in self.chunks
        ]
        return Response(data, status=status.HTTP_200_OK)