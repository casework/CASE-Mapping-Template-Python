import json
import sys
from io import TextIOWrapper

from rdflib import Graph, Literal, Namespace, URIRef
from rdflib.namespace import RDF, XSD

from case_example_mapping import JSON

STR_XSD_STRING = str(XSD.string)


def compact_xsd_strings(json_object: JSON) -> JSON:
    """
    Some JSON-LD serializers export all literals with datatype
    annotations.  A string-literal without a datatype can be optionally
    exported with a datatype annotation of ``xsd:string``, or left to be
    interpreted as a ``xsd:string`` by default.  This function compacts
    string-literals that are ``xsd:string``-typed into a JSON String
    instead of a JSON Object.

    >>> from rdflib import XSD
    >>> x = {
    ...     "@id": "http://example.org/s",
    ...     "http://example.org/p": [
    ...         {
    ...             "@type": str(XSD.string),
    ...             "@value": "o"
    ...         }
    ...     ]
    ... }
    >>> x
    {'@id': 'http://example.org/s', 'http://example.org/p': [{'@type': 'http://www.w3.org/2001/XMLSchema#string', '@value': 'o'}]}
    >>> compact_xsd_strings(x)
    {'@id': 'http://example.org/s', 'http://example.org/p': ['o']}
    """
    if json_object is None:
        return json_object
    elif isinstance(json_object, (bool, float, int, str)):
        return json_object
    elif isinstance(json_object, dict):
        if "@value" in json_object:
            # Reviewing Literal.
            if json_object.get("@type") == STR_XSD_STRING:
                assert isinstance(json_object["@value"], str)
                return json_object["@value"]
            else:
                return json_object
        else:
            return {k: compact_xsd_strings(json_object[k]) for k in json_object.keys()}
    elif isinstance(json_object, list):
        return [compact_xsd_strings(x) for x in json_object]
    else:
        raise TypeError("Unexpected type of object: %s." % type(json_object))


def serialize_jsonld(graph: Graph, fh: TextIOWrapper) -> None:
    """
    This function serializes the graph with a step taken to compact
    ``xsd:string`` Literals that became JSON Objects.
    """
    json_string = graph.serialize(format="json-ld")
    json_object = json.loads(json_string)
    json_object = compact_xsd_strings(json_object)
    json.dump(json_object, fh, indent=4)


def main() -> None:
    # Process the command line arguments to get the output path
    if len(sys.argv) == 1:
        print(f"Insufficient arguments. Usage is {sys.argv[0]} output_path")
        sys.exit(1)
    output_path: str = sys.argv[1]

    g: Graph = Graph()
    g.bind("uco-core", "https://ontology.unifiedcyberontology.org/uco/core/")
    g.bind(
        "uco-identity",
        "https://ontology.unifiedcyberontology.org/uco/identity/",
    )

    ns_core: Namespace = Namespace(
        "https://ontology.unifiedcyberontology.org/uco/core/"
    )

    ns_kb: Namespace = Namespace("http://example.org/kb/")

    # Define an individual.
    # RDFLib Namespace provides two ways to create a URIRef of the
    # namespace as a string-prefix concatenated with an argument:
    # * The . operator.
    # * The [] operator.
    iri_my_organization = ns_kb["organization-b1534f63-b1c3-4b5c-a937-cbe7077571f2"]

    g.add(
        (
            iri_my_organization,
            RDF.type,
            URIRef(
                "https://ontology.unifiedcyberontology.org/uco/identity/Organization"
            ),
        )
    )

    g.add(
        (
            iri_my_organization,
            ns_core.name,
            Literal("Cyber Domain Ontology", datatype=XSD.string),
        )
    )

    # Write the CASE graph to a file
    try:
        with open(output_path, "w") as case_file:
            serialize_jsonld(g, case_file)
            print(f"CASE graph exported to: {output_path}")
    except IOError:
        print(f"Error writing to path: {output_path}")
        sys.exit(1)

    sys.exit(0)


if __name__ == "__main__":
    main()
