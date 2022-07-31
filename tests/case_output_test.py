import os
import unittest

from rdflib import Graph


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
