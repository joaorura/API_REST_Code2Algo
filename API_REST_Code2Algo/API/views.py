import random
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
    def process_out(list_out):
        count_dict = {}

        for out in list_out:
            value = re.findall("Original name:[^!]*Attention:", out)[0]
            value = value.replace("Original name:", "").replace("Attention:", "").replace("\t", "")
            value = value.replace("[", "").replace("]", "").replace("'", "").replace(", ", "")
            value = value.split("\n")

            original_name = value[0].replace("|", "")
            del value[0]
    
            for i in range(0, len(value)):
                actual = value[i]
                if actual == "":
                    continue
                aux = actual.split(" predicted: ")
                name_code = aux[1]

                if name_code not in count_dict:
                    count_dict[name_code] = 0

                count_dict[name_code] += i

            if original_name in count_dict:
                return tuple([original_name])

        count_list = []
        for i in count_dict:
            count_list.append((count_dict[i], i))

        count_list.sort(key=lambda tup: tup[0])

        answer_list = []
        for i in count_list[0:3]:
            answer_list.append(i[1])

        return tuple(answer_list)

    def create(self, request, *args, **kwargs):
        if "methods" in request.data:
            methods = request.data["methods"]

            list_out = []
            for i in methods:
                with open(INPUT_FILE, 'w') as file:
                    file.write("public class Test {\n" + i + "\n}\n")

                process = subprocess.Popen(COMMAND, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
                out, err = process.communicate()
                list_out.append(out.decode("utf-8"))

            answer = self.process_out(list_out)

            methods_list = []
            for i in answer:
                answer_methods = list(Methods.objects.filter(method_name=i))
                if len(answer_methods) == 0:
                    continue

                sorted_element = random.choice(answer_methods)
                methods_list.append(sorted_element)

            answer_dict = {"methods_list": methods_list}
            return Response(answer_dict)
        else:
            return super(MethodsViewSet, self).create(request, args, kwargs)
