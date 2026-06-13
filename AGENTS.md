## Agent Guidance 

* Prefer documented `make` targets for linting, testing, building, and local workflows.
* Always use `uv` as the Python package manager.
  * Use `uv add` or `uv add --dev` for adding dependencies.
* Ask before adding new runtime or developer dependencies unless explicitly requested. Clearly justify why a new one is needed.
* Never run the `prfiesta` tool without any command line arguments
* Always use the `uv run prfiesta --help` installed locally from this project to ensure you have the latest updates.


# Restricted Operations

* Never commit to the repository.
* Never push to the repository.
* Never make external cloud, production, S3, or third-party service changes without explicit approval.
* Never scan the `data`, `.uv-cache`, `node_modules` or any vendor folder.
* Do not directly read the `.env*` file.
* Do not read secrets files, credentials, private keys, or local config containing tokens unless explicitly approved.
* Do not revert or overwrite user changes unless explicitly asked.