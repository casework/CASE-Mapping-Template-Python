import os
import unittest
from typing import Set

from rdflib import Graph, URIRef


class CASEOutputTests(unittest.TestCase):
    def test_graphs_exist(self) -> None:
        """
        Identifies all CASE graph files within the ./output directory and ensures there
        are at least two.
        """
        files: list = []
        source_directory: str = "./output"
        for file in os.listdir(source_directory):
            if file.endswith(".json") or file.endswith(".jsonld"):
                files.append(os.path.join(source_directory, file))

        # Ensure there were two graph files as expected
        self.assertEqual(2, len(files))

    def test_triples_exist(self) -> None:
        """
        Identifies all CASE graph files within the ./output directory and ensures they
        contain at least one triple.
        """
        source_directory: str = "./output"
        for file in os.listdir(source_directory):
            if file.endswith(".json") or file.endswith(".jsonld"):
                # Parse the graph to count the number of triples and make sure they
                # both contain at least one triple
                g: Graph = Graph()
                g.parse(os.path.join(source_directory, file))
                self.assertGreaterEqual(
                    len(g), 1, f"There were no triples found in file: {file}"
                )

    def test_organization_iri_found(self) -> None:
        """
        Identifies all CASE graph files within the ./output directory and ensures they contain a graph individual that:

        * Is, by RDF class-membership, a UCO organization; and
        * Has the UCO name "Cyber Domain Ontology".

        When adapting this template repository, this test should be replaced.
        """
        files_tested: int = 0
        source_directory: str = "./output"
        query = """\
PREFIX uco-core: <https://ontology.unifiedcyberontology.org/uco/core/>
PREFIX uco-identity: <https://ontology.unifiedcyberontology.org/uco/identity/>
SELECT ?nOrganization
WHERE {
  ?nOrganization
    a uco-identity:Organization ;
    uco-core:name "Cyber Domain Ontology" ;
    .
}
"""
        for file in os.listdir(source_directory):
            if not (file.endswith(".json") or file.endswith(".jsonld")):
                continue
            files_tested += 1

            computed: Set[URIRef] = set()

            g: Graph = Graph()
            g.parse(os.path.join(source_directory, file))
            for result in g.query(query):
                # Graph.query for a SELECT query returns a tuple, with
                # member count as long as the number of bound variables.
                computed.add(result[0])
            self.assertEqual(
                1, len(computed), f"Organization was not found in file: {file}"
            )
        self.assertGreaterEqual(files_tested, 0, "No output files were tested.")
