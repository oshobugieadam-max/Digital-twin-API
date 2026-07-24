"""
tests/test_api.py

Integration tests for the Digital Twin API.
Run with:  pytest tests/
"""

import pytest
from fastapi.testclient import TestClient

from app import app

client = TestClient(app)


# ──────────────────────────────────────────────────────────
# Fixtures
# ──────────────────────────────────────────────────────────

@pytest.fixture
def base_payload():
    return {
        "flare_gas_flow":        1200,
        "suction_pressure":      1.0,
        "discharge_pressure":    6.0,
        "compressor_efficiency": 65,
        "fuel_gas_demand":       900,
        "uptime":                92,
        "steam_flow_proxy":      8000,
        "ncg_fraction":          2.5,
        "h2s_in_ppm":            500,
        "abatement_efficiency":  95,
        "permit_limit_ppm":      50,
        "ambient_temp":          25,
        "upset_event":           False,
        "compressor_trip":       False,
        "hot_day":               False,
        "abatement_drop":        False,
    }


# ──────────────────────────────────────────────────────────
# Health check
# ──────────────────────────────────────────────────────────

def test_health_check():
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "ok"}


# ──────────────────────────────────────────────────────────
# Normal simulation
# ──────────────────────────────────────────────────────────

def test_simulate_returns_200(base_payload):
    response = client.post("/simulate", json=base_payload)
    assert response.status_code == 200


def test_simulate_response_structure(base_payload):
    data = client.post("/simulate", json=base_payload).json()

    for key in ["metadata", "summary", "oil_gas", "geothermal",
                "comparison", "health_score", "recommendations", "charts"]:
        assert key in data, f"Missing key: {key}"


def test_oil_gas_values_are_positive(base_payload):
    data = client.post("/simulate", json=base_payload).json()
    og = data["oil_gas"]
    assert og["gas_recovered"]       >= 0
    assert og["gas_flared"]          >= 0
    assert og["compressor_power_kw"] >= 0
    assert 0 <= og["recovery_rate"]  <= 100
    assert og["co2_avoided"]         >= 0


def test_geothermal_compliance_field(base_payload):
    data = client.post("/simulate", json=base_payload).json()
    assert data["geothermal"]["compliance"] in ("Compliant", "Non-Compliant")


def test_health_score_in_range(base_payload):
    data = client.post("/simulate", json=base_payload).json()
    score = data["health_score"]["score"]
    assert 0 <= score <= 100


def test_charts_not_empty(base_payload):
    data = client.post("/simulate", json=base_payload).json()
    assert len(data["charts"]) > 0


def test_recommendations_not_empty(base_payload):
    data = client.post("/simulate", json=base_payload).json()
    assert len(data["recommendations"]) > 0


# ──────────────────────────────────────────────────────────
# Scenario: compressor trip lowers recovery rate
# ──────────────────────────────────────────────────────────

def test_compressor_trip_reduces_recovery(base_payload):
    normal   = client.post("/simulate", json=base_payload).json()
    tripped  = base_payload.copy()
    tripped["compressor_trip"] = True
    stressed = client.post("/simulate", json=tripped).json()
    assert (
        stressed["oil_gas"]["recovery_rate"]
        < normal["oil_gas"]["recovery_rate"]
    )


# ──────────────────────────────────────────────────────────
# Scenario: abatement drop causes non-compliance
# ──────────────────────────────────────────────────────────

def test_abatement_drop_can_cause_non_compliance(base_payload):
    payload = base_payload.copy()
    payload["h2s_in_ppm"]           = 1500
    payload["abatement_efficiency"]  = 80
    payload["abatement_drop"]        = True
    data = client.post("/simulate", json=payload).json()
    # At 80% - 20% drop = 60% efficiency on 1500 ppm → 600 ppm out >> 50 ppm limit
    assert data["geothermal"]["compliance"] == "Non-Compliant"


# ──────────────────────────────────────────────────────────
# Validation: bad inputs
# ──────────────────────────────────────────────────────────

def test_invalid_payload_returns_422(base_payload):
    bad = base_payload.copy()
    bad["flare_gas_flow"] = 9999999   # exceeds max
    response = client.post("/simulate", json=bad)
    assert response.status_code == 422
