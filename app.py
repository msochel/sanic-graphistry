# external libraries
from sanic import Sanic
from sanic.response import html, redirect, text
from jinja2 import Environment, PackageLoader
import graphistry
# import igraph as ig
# from gi.repository import Gtk

graphistry.register(key='77ab9bcccd62c6bcf10ed37fb759fa849cd9bb1157cff17260da05e9e898d6ba')

env = Environment(
    loader=PackageLoader("app", "templates"),
)

app = Sanic(__name__)


@app.route("/")
async def start(request):
    template = env.get_template("home.html")
    html_content = template.render()
    return html(html_content)

@app.route("/query", methods=['POST', 'GET'])
async def query(request):
    if request.method == "POST":
        req_file = request.files.get("file")
        body = req_file.body.decode("unicode_escape")
        graph = ig.read(body, format="graphml")
        colors = {
                    "#3217A7":10008,
                    "#F0F007": 205005,
                    "White":163001,
                    "#9725A4":135007,
                    "#000000": 164010,
                    "#156911":189010,
                    '#A71717':157000
                }
        for pos, x in enumerate(graph.vs['color']):
            graph.vs[pos]['color'] = colors[x]

        for pos, x in enumerate(graph.es['color']):
            graph.es[pos]['color'] = colors[x]

        graphistry.bind(source='src', destination='dst', point_color='color', edge_color='color').plot(graph)


if __name__ == "__main__":
    app.run(
        debug=True,
        host="127.0.0.1",
        port=8000
    )
