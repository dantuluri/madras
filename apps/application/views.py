from rest_framework import status
from rest_framework import generics, viewsets
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.decorators import api_view

from django.urls import reverse

from .serializers import ApplicationSerializer, QuestionSerializer
from .models import Question, Application


@api_view(['GET'])
def home(request):
    return Response({
        reverse('application:home'): 'Information about application submission endpoints.',
        reverse('application:submit'): 'Submit a new application.',
        reverse('application:list_questions'): 'List questions required for the application.',
        reverse('application:create_question'): 'Create a new application question.',
        reverse('application:question', kwargs={'pk': 1234}): 'Get, modify, and delete questions.'
    })


class ApplicationView(generics.ListCreateAPIView):
    """ Create a new application. Pass in key value pairs in the form 'question_X': ... where X is the ID of the question and ... is the answer. """
    serializer_class = ApplicationSerializer
    permission_classes = (IsAuthenticated,)

    def list(self, request):
        try:
            app = Application.objects.get(user=request.user)
        except Application.DoesNotExist:
            return Response({'error': 'No application has been submitted yet!'}, status=status.HTTP_404_NOT_FOUND)
        return Response(ApplicationSerializer(app).data)


class QuestionView(viewsets.ModelViewSet):
    serializer_class = QuestionSerializer
    permission_classes = (IsAdminUser,)
    queryset = Question.objects.all()


class QuestionListView(generics.ListAPIView):
    serializer_class = QuestionSerializer
    permission_classes = (IsAuthenticated,)
    queryset = Question.objects.all()
