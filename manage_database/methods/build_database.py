import json
from requests import post


class BuildDatabase:
    def __init__(self, url):
        self.baseUrl = url

    def post_object(self, element):
        return post(self.baseUrl, data=element)

    def post_list_of_json(self, path_json):
        with open(path_json, encoding="utf-8") as json_file:
            data = json.load(json_file)
            for element in data:
                print(element)
                response = self.post_object(element)
                print(response.json())


def main():
    build_database = BuildDatabase("http://127.0.0.1:8000/methods/")
    build_database.post_list_of_json("./files/methods.json")


if __name__ == '__main__':
    main()
