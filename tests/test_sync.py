import sys
import unittest
from pathlib import Path
from unittest.mock import patch

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "scripts"))
import sync_apt_repo as sync


class SyncTests(unittest.TestCase):
    def test_source_priority_and_unavailable_package(self):
        first = "https://huayuarc.github.io/"
        second = "https://huayuarc.yourepo.com/"

        def entry(name, digest):
            return {"Package": name, "SHA256": digest * 64}

        indexes = {
            first: [entry("github", "a")],
            second: [entry("duplicate", "a"), entry("missing", "b"), entry("available", "c")],
        }
        downloaded = []

        def download(source, package):
            downloaded.append((source, package["Package"]))
            if package["Package"] == "missing":
                raise FileNotFoundError("HTTP 404")
            return Path(package["Package"] + ".deb")

        with patch.object(sync, "load_upstream_index", side_effect=lambda source: source), \
             patch.object(sync, "parse_packages", side_effect=lambda source: indexes[source]), \
             patch.object(sync, "existing_hashes", return_value=set()), \
             patch.object(sync, "download_package", side_effect=download), \
             patch.object(sync, "write_indexes") as write_indexes, \
             patch.object(sys, "argv", ["sync", "--source", first, "--source", second,
                                        "--max-downloads", "2"]):
            sync.main()

        self.assertEqual(downloaded, [(first, "github"), (second, "missing"),
                                      (second, "available")])
        write_indexes.assert_called_once()


if __name__ == "__main__":
    unittest.main()
