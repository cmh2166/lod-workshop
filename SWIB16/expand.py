"""Take workshop participant's RDF turtle data, validate, expand, & load."""
import rdflib
import sys
import os


def getExtURIs(newGraph):
    """Get select statements from named graphs of external URIs used."""
    predsWeWant = ["http://dbpedia.org/ontology/country",
                   "http://dbpedia.org/ontology/populationTotal"]
    extURIs = set()
    for stmt in newGraph.objects():
        if type(stmt) is rdflib.term.URIRef and 'etherpad' not in stmt:
            extURIs.add(stmt)

    for extURI in extURIs:
        try:
            for extstmt in rdflib.Graph().parse(extURI):
                if extstmt[1].toPython() in predsWeWant:
                    print(extstmt)
                    newGraph.add(extstmt)
        except:
            sys.stdout.write("Error with " + extURI.toPython())
            pass
    return(newGraph)


def main():
    """Take original graph, expand by graph traversal, write to ttl file."""
    dataDir = sys.argv[1]
    newGraph = rdflib.Graph()
    for origGraph in os.listdir(dataDir):
        try:
            newGraph.parse(dataDir + '/' + origGraph, format="turtle")
        except Exception as e:
            sys.stdout.write("Unexpected error with file: " + origGraph)
            sys.stdout.write(str(e))
            exit()
    newGraph = getExtURIs(newGraph)
    newGraph.serialize('swib_output.ttl', format='turtle')





if __name__ == '__main__':
    main()