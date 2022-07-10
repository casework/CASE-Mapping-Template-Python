import hashlib
import json
import sys
import uuid
from datetime import datetime
from os import path

from .utilities import get_files_in_dir, hash_file, is_valid_path


def main():
    """
    The main entrypoint for the script that takes a directory path and lists
    the contained files into a CASE JSON-LD file.
    """

    # Initialize the basic CASE graph that will have the files appended
    case = {
        "@context": {
            "case-investigation": "https://ontology.caseontology.org/case/investigation/",
            "kb": "http://example.org/kb/",
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

    # Process the command line arguments to get the input and output paths
    if len(sys.argv) > 2:
        input_path = sys.argv[1]
        output_path = sys.argv[2]

        # TODO check if paths are valid
        if is_valid_path(input_path) and is_valid_path(output_path):
            try:
                files = get_files_in_dir(input_path)

                for file in files:
                    # For each file, add it to the CASE graph
                    case["@graph"].append(
                        get_observable_file(path.join(input_path, file))
                    )

                # Write the CASE graph to a file
                with open(output_path, "w") as case_file:
                    json.dump(case, case_file, ensure_ascii=False, indent=4)

                # TODO print output path
                sys.exit(0)
            except FileNotFoundError as ex:
                print(f"The file path is not valid: {ex}")
                sys.exit(1)
        else:
            print("The input or output path is not valid")
            sys.exit(1)
    else:
        print(f"Insufficient arguments. Usage is {sys.argv[0]} input_path output_path")
        sys.exit(1)


def get_observable_file(filepath: str) -> dict:
    """
    Returns the file specified in the provided filepath as an ObservableObject in the CASE export. This method handles
    calculation of filesize, extension, MD5 hash, SHA1 hash, and other metadata expected in the Observable TTL spec.

    Ontology source: https://github.com/ucoProject/UCO/blob/master/uco-observable/observable.ttl.
    """
    if path.exists(filepath) and path.isfile(filepath):
        # Get the full path we need for reference
        filepath = path.abspath(filepath)

        # Since the extension may take some additional logic checks, compute it out of the main JSON block
        extension = path.splitext(filepath)[1]
        if len(extension) > 0:
            extension = extension[1:]

        # Parse the file and get the attributes we need
        return {
            "@id": ("kb:" + str(uuid.uuid4())),
            "@type": "uco-observable:File",
            "uco-observable:hasChanged": False,
            "uco-core:hasFacet": [
                {
                    "@type": "uco-observable:FileFacet",
                    "uco-observable:observableCreatedTime": {
                        "@type": "xsd:dateTime",
                        "@value": datetime.fromtimestamp(
                            path.getctime(filepath)
                        ).strftime("%Y-%m-%dT%H:%M:%S.%fZ"),
                    },
                    "uco-observable:modifiedTime": {
                        "@type": "xsd:dateTime",
                        "@value": datetime.fromtimestamp(
                            path.getmtime(filepath)
                        ).strftime("%Y-%m-%dT%H:%M:%S.%fZ"),
                    },
                    "uco-observable:accessedTime": {
                        "@type": "xsd:dateTime",
                        "@value": datetime.fromtimestamp(
                            path.getatime(filepath)
                        ).strftime("%Y-%m-%dT%H:%M:%S.%fZ"),
                    },
                    "uco-observable:extension": extension,
                    "uco-observable:fileName": path.basename(filepath),
                    "uco-observable:filePath": filepath,
                    "uco-observable:isDirectory": False,
                    "uco-observable:sizeInBytes": path.getsize(filepath),
                },
                {
                    "@type": "uco-observable:ContentDataFacet",
                    "uco-observable:hash": [
                        {
                            "@type": "uco-types:Hash",
                            "uco-types:hashMethod": {
                                "@type": "uco-vocabulary:HashNameVocab",
                                "@value": "MD5",
                            },
                            "uco-types:hashValue": {
                                "@type": "xsd:hexBinary",
                                "@value": hash_file(filepath, hashlib.md5()),
                            },
                        },
                        {
                            "@type": "uco-types:Hash",
                            "uco-types:hashMethod": {
                                "@type": "uco-vocabulary:HashNameVocab",
                                "@value": "SHA1",
                            },
                            "uco-types:hashValue": {
                                "@type": "xsd:hexBinary",
                                "@value": hash_file(filepath, hashlib.sha1()),
                            },
                        },
                        {
                            "@type": "uco-types:Hash",
                            "uco-types:hashMethod": {
                                "@type": "uco-vocabulary:HashNameVocab",
                                "@value": "SHA256",
                            },
                            "uco-types:hashValue": {
                                "@type": "xsd:hexBinary",
                                "@value": hash_file(filepath, hashlib.sha256()),
                            },
                        },
                        {
                            "@type": "uco-types:Hash",
                            "uco-types:hashMethod": {
                                "@type": "uco-vocabulary:HashNameVocab",
                                "@value": "SHA512",
                            },
                            "uco-types:hashValue": {
                                "@type": "xsd:hexBinary",
                                "@value": hash_file(filepath, hashlib.sha512()),
                            },
                        },
                    ],
                },
            ],
        }
    else:
        raise FileNotFoundError(f"File not found {filepath}")


if __name__ == "__main__":
    main()
