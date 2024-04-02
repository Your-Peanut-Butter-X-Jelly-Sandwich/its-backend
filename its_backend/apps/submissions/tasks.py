from celery import shared_task

from .models import Submissiondata
from .serializers import CreateUpdateSubmissionSerializer
from .utils import (
    process_submission_request,
)


@shared_task
def process_submission_request_async(submission_pk):
    its_processed_request = process_submission_request(submission_pk)
    instance = Submissiondata.objects.get(pk=submission_pk)
    serializer = CreateUpdateSubmissionSerializer(
        instance=instance, data=its_processed_request, partial=True
    )
    serializer.is_valid(raise_exception=True)
    serializer.save()
    return
