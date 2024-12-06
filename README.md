# muse

- currently just a script to run demucs

### How to Use

### Prereqs

- Install `uv`
- `uv venv`
- `source .venv/bin/activate`
- `uv sync`

#### Usage

```bash
python process_project.py project_name
```

- This uses the default `projects` folder as the input base and `output` as the output base.

#### CLI Args
- `project_name`: The name of the project (required positional argument).
- `--input-base`: The base directory containing all projects (optional, default is `projects`).
- `--output-base`: The base directory for output (optional, default is `output`).
