# Huayuarc source archive

Upstream sources, in priority order:

1. https://huayuarc.github.io/
2. https://huayuarc.yourepo.com/

This is a private archive for the repository owner. It does not publish a GitHub Pages source.

GitHub Actions checks both sources every six hours and can be run manually. It identifies identical `.deb` files by SHA-256, choosing the GitHub source when the same file appears in both indexes. It preserves previously archived versions even if upstream removes them.

Each run downloads at most 100 new packages by default. A manual run with `max_downloads=0` continues until all indexed packages are archived, committing and pushing every 100 packages. Downloads are checked against upstream SHA-256 and size metadata and validated as DEB files. Requests are at least three seconds apart, with retries for temporary server errors.
