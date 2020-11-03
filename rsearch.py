import os, yaml, argparse

reclass_dir = "/srv/salt/reclass/classes/"

def search_class(path, data, key, lev = 0):
    if lev < len(key):
        if isinstance(data, dict):
            for k, v in data.items():
                if k == key[lev]:
                    search_class(path, v, key, lev + 1)
    else:
        print path
        print yaml.dump(data, default_flow_style=False)


def search_node(classes, search):
    print "SEARCH NODE:", search
    print ""
    for el in classes:
        path = reclass_dir + el.replace(".","/")
        if os.path.isdir(path):
            path = path + "/init.yml"
        else:
            path = path + ".yml"
        with open(path, 'r') as stream:
            try:
                data = yaml.load(stream)
                search_class(path, data, search.split("."))
            except yaml.YAMLError as exc:
                print(exc)


def search_all(search):
    print "SEARCH ALL:", search
    print ""
    for dirnam, subdirs, files in os.walk(reclass_dir):
        for el in files:
            path = dirnam + "/" + el
            with open(path, 'r') as stream:
                try:
                    data = yaml.load(stream)
                    search_class(path, data, search.split("."))
                except:
                    pass

def graph(classes):
    print "digraph MCP {"
    print "ratio = fill;"
    print "node [style=filled];"
    for el in classes:
        path = reclass_dir + el.replace(".","/")
        if os.path.isdir(path):
            path = path + "/init.yml"
        else:
            path = path + ".yml"
        with open(path, 'r') as stream:
            try:
                data = yaml.load(stream)
            except yaml.YAMLError as exc:
                print(exc)
            typ = el.split(".")[0]
            path = path[len(reclass_dir):]
            if typ == "cluster":
                print "\"%s\" [href=\"./%s\", color=\"0.355 0.563 1.000\"];" % (el, path)
            elif typ == "system":
                print "\"%s\" [href=\"./%s\", color=\"0.603 0.258 1.000\"];" % (el, path)
            elif typ == "service":
                print "\"%s\" [href=\"./%s\", color=\"gray\"];" % (el, path)
            if "classes" in data:
                for ela in data["classes"]:
                    print "\"%s\" -> \"%s\"" % (el, ela)
    print "}"
    print "http://www.webgraphviz.com/"


parser = argparse.ArgumentParser()
parser.add_argument("-n", "--node", help="provide node file")
parser.add_argument("-a", "--all", help="search all classes", action="store_true")
parser.add_argument("-s", "--search", help="provide search key in dot notation ")
parser.add_argument("-g", "--graph", help="produce node graph", action="store_true")
args = parser.parse_args()

if args.search:
    search = "parameters." + args.search

if args.node:
    with open(args.node, 'r') as stream:
        try:
            data = yaml.load(stream)
            classes = data[next(iter(data))]["__reclass__"]["classes"]
            if args.search:
                search_node(classes, search)
            if args.graph:
                graph(classes)
        except yaml.YAMLError as exc:
            print(exc)

if args.all and args.search:
    search_all(search)

