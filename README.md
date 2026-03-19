# Browser Agent

Browser automation agent for fetching utility bills and emitting invoices from Brazilian service providers. Built with FastAPI, Playwright, and [browser-use](https://github.com/browser-use/browser-use).

## Supported Providers

| Provider | Actions | Required Params |
|----------|---------|-----------------|
| **Copel** (electricity) | `fetch-bill` | `reference_month` (MM/YYYY) |
| **Claro** (telecom) | `fetch-bill` | `product_type` (`movel` or `residencial`) |
| **Sanepar** (water) | `fetch-bill` | — |
| **Countfly** | `emit-invoice` | `amount`, `description` |

## Requirements

- Python 3.11+
- [uv](https://docs.astral.sh/uv/) package manager
- An OpenAI API key (for the browser-use LLM agent)

## Setup

```bash
# Clone and install
git clone https://github.com/felipemeriga/browser-agent.git
cd browser-agent
uv sync

# Install Playwright browsers
uv run playwright install chromium --with-deps

# Configure environment
cp .env.example .env
# Edit .env with your credentials and API key
```

## Running

```bash
# Start the API server
uv run fastapi run src/browser_agent/main.py --port 8000
```

The API will be available at `http://localhost:8000`. Interactive docs at `http://localhost:8000/docs`.

### Docker

```bash
docker compose up --build
```

## API

### Create a task

```
POST /tasks/{provider}/{action}
```

```json
{
  "params": {
    "reference_month": "03/2026"
  }
}
```

Returns a job with an `id` to poll for status.

### Check job status

```
GET /jobs/{job_id}
```

### List jobs

```
GET /jobs
GET /jobs?status=completed
```

### Download a file

```
GET /downloads/{provider}/{filename}
```

### Health check

```
GET /health
```

## Development

```bash
# Install dev dependencies
uv sync --extra dev

# Run tests
uv run pytest

# Lint and format
uv run ruff check src/ tests/
uv run ruff format src/ tests/
```

## Configuration

| Variable | Default | Description |
|----------|---------|-------------|
| `BROWSER_HEADLESS` | `false` | Run browser in headless mode |
| `OPENAI_API_KEY` | — | OpenAI API key for the LLM agent |
| `LLM_MODEL` | `gpt-4o-mini` | LLM model to use |
| `USE_VISION` | `false` | Enable vision for the browser agent |
| `DOWNLOADS_DIR` | `./downloads` | Directory for downloaded files |
| `API_PORT` | `8000` | API server port |
| `MAX_CONCURRENT_TASKS` | `2` | Max parallel browser tasks |
| `JOB_TIMEOUT_SECONDS` | `300` | Timeout per job |
