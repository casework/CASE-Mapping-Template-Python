import sys

from rdflib import Graph, Literal, Namespace, URIRef
from rdflib.namespace import XSD

from .utilities import is_valid_path


def main():
    # Process the command line arguments to get the output path
    if len(sys.argv) > 1:
        output_path = sys.argv[1]

        # Check if paths are valid
        if is_valid_path(output_path):
            g = Graph()
            g.bind("uco-core", "https://ontology.unifiedcyberontology.org/uco/core/")
            g.bind(
                "uco-identity",
                "https://ontology.unifiedcyberontology.org/uco/identity/",
            )

            ns_core = Namespace("https://ontology.unifiedcyberontology.org/uco/core/")

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
            with open(output_path, "w") as case_file:
                case_file.write(g.serialize(format="turtle"))
                print(f"CASE graph exported to: {output_path}")

            sys.exit(0)
        else:
            print("The output path is not valid")
            sys.exit(1)
    else:
        print(f"Insufficient arguments. Usage is {sys.argv[0]} output_path")
        sys.exit(1)


if __name__ == "__main__":
    main()
