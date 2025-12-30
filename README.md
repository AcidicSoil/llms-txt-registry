# llms-txt Registry

A centralized registry of generated `llms.txt` documentation artifacts for various libraries and tools.

## Usage

This registry is designed to be consumed via **MCP** (Model Context Protocol) using `gitmcp` as the gateway.

### Gemini CLI Configuration

Add this to your `~/.gemini/settings.json` (or project config):

```json
{
  "mcpServers": {
    "llms-registry": {
      "command": "npx",
      "args": [
        "-y",
        "mcp-remote",
        "gitmcp.io/<org>/<repo>"
      ]
    }
  }
}
```

Replace `<org>/<repo>` with the GitHub path to this repository.

### Codex Configuration

For Codex or other clients supporting `mcp-remote`:

```toml
[mcpServers.llms-registry]
command = "npx"
args = ["-y", "mcp-remote", "gitmcp.io/<org>/<repo>"]
```

## Structure

Artifacts are stored in the `docs/` directory, organized by source ID:

- `docs/<source-id>/<source-id>-llms.txt`
- `docs/<source-id>/metadata.json`

Example:
- `docs/tanstack-router/tanstack-router-llms.txt`

A machine-readable index is available at `docs/index.json`.

## Contributor Guide (Local-First Workflow)

We use a local-first workflow to generate artifacts using your own LM Studio instance. This avoids sending code to remote APIs during CI.

### Prerequisites

- Python 3.10+
- [LM Studio](https://lmstudio.ai/) (with a model loaded and Server started)
- `lmstudio-llmstxt-generator` CLI tool (installed via `pip install lmstudio-llmstxt-generator` or similar)

### Setup

1. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

2. Install Git hooks (Critical):
   ```bash
   ./scripts/setup_hooks.sh
   ```
   This installs a `pre-push` hook that ensures `docs/` are in sync with `sources.json`.

### Adding a Source

1. Edit `sources.json` to add a new entry:
   ```json
   {
     "id": "my-lib",
     "url": "https://github.com/owner/lib",
     "type": "repo",
     "profile": "default"
   }
   ```

2. Run the refresh script locally:
   ```bash
   # Make sure LM Studio server is running at http://localhost:1234
   python scripts/refresh.py --only my-lib
   ```

3. Verify the output in `docs/my-lib/`.

4. Commit and push.

### Refreshing All Sources

To update all artifacts:
```bash
python scripts/refresh.py
```