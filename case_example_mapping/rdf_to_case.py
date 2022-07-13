import sys

from rdflib import Graph, Literal, Namespace, URIRef
from rdflib.namespace import XSD


def main():
    # Process the command line arguments to get the output path
    if len(sys.argv) > 1:
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

        g.add(
            (
                URIRef(
                    "https://ontology.unifiedcyberontology.org/uco/identity/Organization"
                ),
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
    else:
        print(f"Insufficient arguments. Usage is {sys.argv[0]} output_path")
        sys.exit(1)


if __name__ == "__main__":
    main()
