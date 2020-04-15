import re
import subprocess

from rest_framework.response import Response
from rest_framework import status
from rest_framework_mongoengine import viewsets

from .models import Methods
from .serializer import MethodsSerializer


INPUT_FILE = "/home/joaorura/PycharmProjects/API_REST_Code2Algo/external_projects/code2vec/Input.java"
COMMAND = [
    "python3",
    "/home/joaorura/PycharmProjects/API_REST_Code2Algo/external_projects/code2vec/code2vec.py",
    "--load", "/home/joaorura/PycharmProjects/API_REST_Code2Algo/external_projects/code2vec/models/theModel",
    "--predict"
]


class MethodsViewSet(viewsets.ModelViewSet):
    lookup_field = "id"
    queryset = Methods.objects.all()
    serializer_class = MethodsSerializer

    @staticmethod
    def error_message(request):
        print(request.data)
        return Response(status=status.HTTP_400_BAD_REQUEST)

    @staticmethod
    def process_out(out):
        value = re.findall("Original name:[^!]*Attention:", out)[0]
        value = value.replace("Original name:", "")
        value = value.replace("Attetion:", "")
        value = value.replace("\t", "")
        print(value.split("\n"))

    def list(self, request, *args, **kwargs):
        if "methods" in request.data:
            methods = request.data["methods"]

            for i in methods:
                with open(INPUT_FILE, 'w') as file:
                    file.write("public class Test {\n" + i + "\n}\n")

                process = subprocess.Popen(COMMAND, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
                out, err = process.communicate()
                out = out.decode("utf-8")
                self.process_out(out)

            return Response()
        else:
            return super(MethodsViewSet, self).list(request, args, kwargs)
