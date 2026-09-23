
from .models import Document, Documentchunk
from .services import create_chunks, extract_pdf_text, generate_embedding
from celery import shared_task
import time


@shared_task
def process_documents(document_id):
    document = Document.objects.get(id=document_id)
    document.status = Document.ProcessingStatus.PROCESSING
    document.save()
    
    text = extract_pdf_text(document.files.path)
    document.extracted_text = text
    document.status = document.ProcessingStatus.COMPLETED
    document.save()
    
    chunks = create_chunks(text)
        
    Documentchunk.objects.bulk_create(
        [ Documentchunk(
            document=document,
            content=chunk,
            chunk_index=index,
            embedding=generate_embedding(chunk),
        )
         for index, chunk in enumerate(chunks)
        ]
    )
    
    print(f"Processing document {document_id}")
    return document_id