import json
import sys


def main() -> None:
    """
    The main entrypoint for the script that takes a directory path and lists
    the contained files into a CASE JSON-LD file.
    """

    # Initialize the basic CASE graph that will have the files appended
    case: dict = {
        "@context": {
            "case-investigation": "https://ontology.caseontology.org/case/investigation/",
            "kb": "http://example.org/kb/",
            "drafting": "http://example.org/ontology/drafting/",
            "rdf": "http://www.w3.org/1999/02/22-rdf-syntax-ns#",
            "rdfs": "http://www.w3.org/2000/01/rdf-schema#",
            "uco-action": "https://ontology.unifiedcyberontology.org/uco/action/",
            "uco-core": "https://ontology.unifiedcyberontology.org/uco/core/",
            "uco-identity": "https://ontology.unifiedcyberontology.org/uco/identity/",
            "uco-location": "https://ontology.unifiedcyberontology.org/uco/location/",
            "uco-observable": "https://ontology.unifiedcyberontology.org/uco/observable/",
            "uco-tool": "https://ontology.unifiedcyberontology.org/uco/tool/",
            "uco-types": "https://ontology.unifiedcyberontology.org/uco/types/",
            "uco-vocabulary": "https://ontology.unifiedcyberontology.org/uco/vocabulary/",
            "xsd": "http://www.w3.org/2001/XMLSchema#",
        },
        "@graph": [],
    }

    # Process the command line arguments to get the output path
    if len(sys.argv) == 1:
        print(f"Insufficient arguments. Usage is {sys.argv[0]} output_path")
        sys.exit(1)
    output_path: str = sys.argv[1]

    # Add a uco-identity:Organization to the graph
    case["@graph"].append(
        {
            "@id": "kb:organization-2b3b98e2-aea2-4270-876a-7f9917623cb6",
            "@type": "uco-identity:Organization",
            "uco-core:name": "Cyber Domain Ontology",
        }
    )

    # Write the CASE graph to a file
    try:
        with open(output_path, "w") as case_file:
            json.dump(case, case_file, ensure_ascii=False, indent=4)
            print(f"CASE graph exported to: {output_path}")
    except IOError:
        print(f"Error writing to path: {output_path}")
        sys.exit(1)

    sys.exit(0)


if __name__ == "__main__":
    main()
