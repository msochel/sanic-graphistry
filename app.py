# external libraries
from sanic import Sanic
from sanic.response import html, redirect, text
from jinja2 import Environment, PackageLoader
import graphistry
import igraph as ig
import os

graphistry.register(
    key='77ab9bcccd62c6bcf10ed37fb759fa849cd9bb1157cff17260da05e9e898d6ba'
    )

env = Environment(
    loader=PackageLoader("app", "templates"),
)

app = Sanic(__name__)
app.static("/static", "./static")


@app.route("/", methods=["POST", "GET"])
async def start(request):
    if request.method == "POST":
        pages = list()
        req_file = request.files.getlist("file")
        for file_ in req_file:
            file_name = file_.name
            print(file_name)
            body = file_.body.decode("unicode_escape")
            with open("files/" + file_name, "w") as file:
                file.write(body)
            file_path = "files/" + file_name
            graph = ig.read(file_path, format="graphml")
            colors = {
                        "#3217A7":10008,
                        "#F0F007": 205005,
                        "White":163001,
                        "#9725A4":135007,
                        "#000000": 164010,
                        "#156911":189010,
                        '#A71717':157000,
                        "#2E2E2E": 164009,
                    }
            for pos, x in enumerate(graph.vs['color']):
                graph.vs[pos]['color'] = colors[x]

            for pos, x in enumerate(graph.es['color']):
                graph.es[pos]['color'] = colors[x]

            url = graphistry.bind(
                        source='src',
                        destination='dst',
                        point_color='color',
                        edge_color='color'
                    ).plot(graph)
            pages.append(url)
            # print(type(url))
            view = env.get_template("home.html")
            html_content = view.render(url=pages)
            # hola.append(html_content)
        return(html_content)
        # view = env.get_template("home.html")
        # html_content = view.render(url="null")
        # return html(html_content)
        # hola.append(view.render(url="null"))
        # return html(hola[0], hola[1], hola[2])
    elif request.method == "GET":
        template = env.get_template("home.html")
        html_content = template.render(url="null")
        return html(html_content)


if __name__ == "__main__":
    heroku = True
    if not heroku:
        port=8000
    else:
        port=int(os.environ['PORT'])
    app.run(
        debug=False,
        host="0.0.0.0",
        port=port
    )
