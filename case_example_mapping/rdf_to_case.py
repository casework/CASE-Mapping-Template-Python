import sys

from rdflib import Graph, Literal, Namespace, URIRef
from rdflib.namespace import RDF, XSD


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
            case_file.write(g.serialize(format="json-ld", indent=4))
            print(f"CASE graph exported to: {output_path}")
    except IOError:
        print(f"Error writing to path: {output_path}")
        sys.exit(1)

    sys.exit(0)


if __name__ == "__main__":
    main()
