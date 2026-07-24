# Digital Twin API

Oil & Gas FGRU and Geothermal H₂S Abatement Digital Twin — Hackathon Edition

## What It Does

A FastAPI backend that simulates two co-located energy systems:

- **Oil & Gas FGRU** — Flare Gas Recovery Unit: recovers otherwise-wasted gas,
  calculates compressor power, recovery rate, and CO₂ emissions avoided.
- **Geothermal H₂S Abatement** — models NCG extraction, H₂S outlet
  concentration, regulatory compliance, and power penalty.

Both engines run in a single `POST /simulate` call and return a unified
response with health scores, charts, and engineering recommendations.

---

## Quickstart

```bash
# 1. Clone and enter the project
git clone <your-repo-url>
cd digital-twin-api

# 2. Create a virtual environment
python -m venv .venv
source .venv/bin/activate      # Windows: .venv\Scripts\activate

# 3. Install dependencies
pip install -r requirements.txt

# 4. Run the API
uvicorn app:app --reload
```

Interactive docs: [http://localhost:8000/docs](http://localhost:8000/docs)

---

## API Reference

### `GET /health`
Liveness probe. Returns `{ "status": "ok" }`.

### `POST /simulate`
Run the combined Digital Twin simulation.

**Request body** — see `examples/request.json`

**Response** — see `examples/response.json`

---

## Project Structure

```
├── app.py               # FastAPI application and /simulate endpoint
├── constants.py         # Engineering constants
├── schemas.py           # Pydantic request and response models
├── requirements.txt
├── engine/
│   ├── oil_gas.py       # FGRU simulation engine
│   ├── geothermal.py    # H₂S abatement simulation engine
│   ├── health.py        # Combined health score calculator
│   ├── recommendations.py  # Prioritised recommendations generator
│   ├── charts.py        # Chart data builder
│   └── scenarios.py     # Preset scenario configurations
├── utils/
│   └── helpers.py       # Shared utility functions
├── examples/
│   ├── request.json     # Sample API request
│   └── response.json    # Sample API response
└── tests/
    └── test_api.py      # Integration tests
```

---

## Running Tests

```bash
pytest tests/ -v
```

---

## Preset Scenarios

Four scenarios are defined in `engine/scenarios.py`:

| Name                    | What It Tests                              |
|-------------------------|--------------------------------------------|
| `normal_operation`      | Baseline — healthy plant                   |
| `compressor_trip`       | Reduced uptime, lower recovery rate        |
| `hot_day_abatement_stress` | Thermal degradation of H₂S abatement   |
| `full_upset`            | All stress flags active simultaneously     |

---

## Key Design Decisions

- **Engine independence** — simulation engines return plain dicts, not Pydantic
  models. `app.py` handles schema conversion.
- **No external data dependencies** — all calculations are self-contained proxy
  models, suitable for demo and educational use.
- **Single endpoint** — the frontend sends one request and receives everything:
  results, health score, charts, and recommendations.
