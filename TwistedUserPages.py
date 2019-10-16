from twisted.internet import reactor
from twisted.web.resource import Resource, NoResource
from twisted.web.server import Site

import json

class User:

    id = 0

    def __init__(self, name, last_name):
        self.id = User.id
        self.name = name
        self.last_name = last_name

        User.id += 1

    def as_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "last_name": self.last_name
        }

users = [
    User("Natalia", "Tomczak"),
    User("Bartek", "Wilczak"),
    User("Shaquille", "O'Neal"),
    User("Eren", "Jaeger"),
    User("David", "Beckham"),
    User("Wojciech", "Fortuna"),
    User("Anna", "Reszka")
]

projects = [
    "Rybki i inne stworzenia",
    "Taki tam  stworek",
    "Film jako medium kraju",
    "Sport to zdrowie",
    "Muzyka wschodu",
    "Super projekt"
]


class PageOfUsers(Resource):
    def __init__(self):
        Resource.__init__(self)

    def render_GET(self, request):
        response = json.dumps(
            [user.as_dict() for user in users]
        )
        request.setHeader("Content-Type", "application/json")
        return response.encode()


class PageOfProjects(Resource):
    def __init__(self):
        Resource.__init__(self)

    def render_GET(self, request):
        response = '<html><body>{}</body></html>'
        ul = "<ul>{}</ul>"
        li = "<li>{}</li>"
        elements = []
        for proj in projects:
            elements.append(
                li.format(proj)
            )

        elements = "\n".join(elements)

        ul = ul.format(elements)
        response = response.format(ul)

        return response.encode()


class HomePage(Resource):
    def getChild(self, name, request):
        name = name.decode()
        if name == '':
            return self
        if name == "users":
            return PageOfUsers()
        if name == "projects":
            return PageOfProjects()
        else:
            return NoResource()

    def render_GET(self, request):
        response = '<html><body>Say hello to the home page!</body></html>'
        return response.encode()


root = HomePage()
factory = Site(root)
reactor.listenTCP(8080, factory)
reactor.run()
