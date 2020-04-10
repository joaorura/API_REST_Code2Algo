from rest_framework.response import Response
from rest_framework import status
from rest_framework_mongoengine import viewsets

from .models import Methods
from .serializer import LogicQuestionSerializer



class LogicQuestionViewSet(viewsets.ModelViewSet):
    lookup_field = "id"
    queryset = LogicQuestion.objects.all()
    serializer_class = LogicQuestionSerializer

    @staticmethod
    def error_message(request):
        print(request.data)
        return Response(status=status.HTTP_400_BAD_REQUEST)

    def create(self, request, *args, **kwargs):
        try:
            if request.data == {}:
                list_of_questions = []
                for i in range(0, 7):
                    question = list(LogicQuestion.objects.filter(level=i))
                    if len(question) == 0:
                        return Response("Problem In Database", status=status.HTTP_404_NOT_FOUND)

                    question = sample(question, k=NQPL)
                    for j in question:
                        logic_question_data = copy(LogicQuestionSerializer(j).data)
                        del logic_question_data["id"]
                        list_of_questions.append(logic_question_data)

                return Response(list_of_questions, status=status.HTTP_201_CREATED)
            elif 'note' in request.data and type(request.data['note']) == int:
                print(f"Nota do Usuario: {request.data['note']}")
                return Response()
            else:
                return super(LogicQuestionViewSet, self).create(request, args, kwargs)
        except Exception:
            return self.error_message(request)