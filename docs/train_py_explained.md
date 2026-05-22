# `src/train.py` — Full Teaching Notes (Tanglish)

> MLOps Engineer perspective-la, every line yen iruku, how it works, alternatives enna — ellam cover pannuvom.

---

## File-oda Purpose

```
prepare.py  → Raw data clean panni train/test split save pannudu
train.py    → train.csv load panni model train pannudu
              MLflow-la log pannudu
              GCS-la model upload pannudu
              joblib-la local save pannudu
evaluate.py → test.csv + model load panni metrics calculate pannudu
```

---

## Part 1 — Imports

```python
import os
import joblib
import numpy as np
import pandas as pd
import yaml
import mlflow
import mlflow.sklearn
from sklearn.linear_model import LinearRegression
```

### `import os` — Yen?

```python
# 2 main uses:

# 1. OS-independent file paths
os.path.join("data", "processed", "train.csv")
# Windows → data\processed\train.csv
# Linux   → data/processed/train.csv
# Hardcode panna koodadhu — CI/CD Linux-la run aagum, local Windows-la

# 2. Environment variables read panna
os.environ.get("MLFLOW_TRACKING_URI", "sqlite:///mlflow.db")
# Local-la set illana → default value use pannudu
# CI/CD-la set pannuvom → automatically pick up pannudu
```

### `import joblib` — Yen pickle illa?

```python
# joblib vs pickle:

import pickle
pickle.dump(model, open("model.pkl", "wb"))   # slow for large numpy arrays

import joblib
joblib.dump(model, "model.joblib")            # fast, numpy optimized

# sklearn models internally numpy arrays use pannudu
# joblib → numpy arrays efficiently serialize pannudu
# Production-la always joblib use pannuvom
```

### `import mlflow` vs `import mlflow.sklearn` — Yen separate?

```python
import mlflow
# Core MLflow — experiments, runs, params, metrics log panna

import mlflow.sklearn
# sklearn-specific functions
# mlflow.sklearn.log_model() → sklearn model-a MLflow format-la save panna
# Itha separately import pannanum — mlflow alone import pannina log_model() illa
```

---

## Part 2 — Constants

```python
TRAIN_PATH = os.path.join("data", "processed", "train.csv")
MODEL_PATH = os.path.join("models", "model.joblib")
PARAMS_PATH = "params.yaml"
METRICS_PATH = os.path.join("metrics", "scores.json")

MLFLOW_ARTIFACT_URI = os.environ.get(
    "MLFLOW_ARTIFACT_URI",
    "gs://devmlops-496015-mlops-artifacts/mlflow"
)
MLFLOW_TRACKING_URI = os.environ.get("MLFLOW_TRACKING_URI", "sqlite:///mlflow.db")
```

### Yen top-la constants define pannuvom?

```python
# Bad way — hardcoded inside functions
def train():
    df = pd.read_csv("data/processed/train.csv")   # change panna 3 places touch pannanum
def save():
    joblib.dump(model, "data/processed/train.csv") # typo possible

# Good way — constants top-la
TRAIN_PATH = os.path.join("data", "processed", "train.csv")
def train(path=TRAIN_PATH):   # change panna 1 place matum
    df = pd.read_csv(path)

# Benefits:
# 1. One place change → everywhere reflect
# 2. Test panna easy — different path pass panna mudiyum
# 3. Read panna easy — top-la paathu ellam paths theriyum
```

### `os.environ.get()` — How it works

```python
MLFLOW_TRACKING_URI = os.environ.get("MLFLOW_TRACKING_URI", "sqlite:///mlflow.db")

# Scenario 1: Local development
# MLFLOW_TRACKING_URI not set → "sqlite:///mlflow.db" use pannudu
# mlflow.db → project root-la create aagum

# Scenario 2: GitHub Actions
# env:
#   MLFLOW_TRACKING_URI: http://mlflow-server:5000
# → automatically http://mlflow-server:5000 use pannudu

# Scenario 3: Vertex AI
# env:
#   MLFLOW_TRACKING_URI: https://vertex-ai-experiments-url
# → automatically Vertex AI use pannudu

# Same code, different environments — zero code change!
# This is called "12-factor app" principle
```

### `sqlite:///mlflow.db` — Enna idu?

```
sqlite:///mlflow.db
  sqlite:// → protocol (SQLite database)
  /         → relative path indicator
  mlflow.db → filename

→ Project root-la mlflow.db file create aagum
→ Runs, metrics, params, experiment metadata store aagum
→ Local development-ku perfect
→ Production-la PostgreSQL/MySQL use pannuvom
```

---

## Part 3 — `load_params()` Function

```python
def load_params() -> dict:
    if os.path.exists(PARAMS_PATH):
        with open(PARAMS_PATH) as f:
            return yaml.safe_load(f)
    return {}
```

### Line by line:

```python
def load_params() -> dict:
# -> dict = return type hint
# Function always dict return pannudu nu indicate pannudu
# Python enforce pannadu, but documentation-ku useful
# MLOps-la type hints important — team members understand panna easy

    if os.path.exists(PARAMS_PATH):
# params.yaml file iruka check pannudu
# Illa na → empty dict return pannudu → crash aagadu
# Defensive programming — always check before open

        with open(PARAMS_PATH) as f:
# "with" = context manager
# File open pannudu, block end-la automatically close pannudu
# close() manually call pannanum illa → memory leak prevent

            return yaml.safe_load(f)
# yaml.safe_load() vs yaml.load():
#
# yaml.load(f) → DANGEROUS
#   YAML-la arbitrary Python code embed panna mudiyum
#   !!python/object/apply:os.system ['rm -rf /']  ← possible attack!
#   Execute aagum → server wipe!
#
# yaml.safe_load(f) → SAFE
#   Only basic types: dict, list, str, int, float, bool
#   Arbitrary code execute pannadu
#   Always use safe_load!

    return {}
# params.yaml illa na → empty dict return
# Caller .get() use pannudu → KeyError aagadu
```

### params.yaml → Python dict conversion:

```yaml
# params.yaml
prepare:
  test_size: 0.2
  random_state: 42
train:
  model_type: linear_regression
  random_state: 42
```

```python
# yaml.safe_load() result:
{
    "prepare": {
        "test_size": 0.2,
        "random_state": 42
    },
    "train": {
        "model_type": "linear_regression",
        "random_state": 42
    }
}

# Usage:
params = load_params()
test_size = params.get("prepare", {}).get("test_size", 0.2)
# .get("prepare", {}) → "prepare" key illa na empty dict return
# .get("test_size", 0.2) → "test_size" key illa na 0.2 default
```

---

## Part 4 — `train()` Function

```python
def train(train_path: str = TRAIN_PATH) -> LinearRegression:
    df = pd.read_csv(train_path)
    X = df[["sqft"]].values
    y = df["price"].values
    model = LinearRegression()
    model.fit(X, y)
    print(f"Model trained. Coef: {model.coef_[0]:.2f}, Intercept: {model.intercept_:.2f}")
    return model, X, y
```

### `df[["sqft"]]` vs `df["sqft"]` — Critical difference!

```python
df = pd.read_csv("train.csv")
# df content:
#    sqft    price
#    1500   300000
#    2000   400000

# Single bracket → Series (1D)
df["sqft"]
# 0    1500
# 1    2000
# dtype: int64
# Shape: (16,)  ← 1 dimension

# Double bracket → DataFrame (2D)
df[["sqft"]]
#    sqft
# 0  1500
# 1  2000
# Shape: (16, 1)  ← 2 dimensions

# sklearn LinearRegression expect pannudu:
# X → 2D: (n_samples, n_features) → (16, 1)
# y → 1D: (n_samples,)            → (16,)

# Wrong:
X = df["sqft"].values    # shape (16,) → sklearn error!

# Correct:
X = df[["sqft"]].values  # shape (16, 1) → sklearn happy!
```

### `.values` — Yen?

```python
df[["sqft"]]        # pandas DataFrame object
df[["sqft"]].values # numpy array

# sklearn internally numpy use pannudu
# pandas DataFrame pass pannalum work aagum, but:
# - numpy faster
# - sklearn warnings less
# - MLflow log panna easy
# Always .values use pannuvom
```

### `model.fit(X, y)` — Internally enna pannudu?

```python
model = LinearRegression()
model.fit(X, y)

# Internally:
# 1. X, y numpy arrays-a convert pannudu
# 2. Least squares method use panni best fit line find pannudu
#    Formula: y = mx + b
#    m (coef_)      = 200.0  → 1 sqft increase = $200 increase
#    b (intercept_) = 0.0    → base price
# 3. model.coef_, model.intercept_ set pannudu

print(model.coef_)       # [200.]
print(model.intercept_)  # 0.0

# Predict:
model.predict([[3500]])  # 200 * 3500 + 0 = 700000
```

---

## Part 5 — `save_model()` Function

```python
def save_model(model: LinearRegression, path: str = MODEL_PATH):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    joblib.dump(model, path)
    print(f"Model saved to {path}")
```

### `os.makedirs()` — Yen?

```python
MODEL_PATH = "models/model.joblib"

os.path.dirname("models/model.joblib")  # → "models"

os.makedirs("models", exist_ok=True)
# "models" folder create pannudu
# exist_ok=True → already irundha error throw pannadu, skip pannudu
# exist_ok=False (default) → already irundha FileExistsError!

# Yen vendum?
# Fresh clone → models/ folder illa
# makedirs illana → joblib.dump() → FileNotFoundError crash
```

### `joblib.dump()` — Enna save pannudu?

```python
joblib.dump(model, "models/model.joblib")

# model object-la irukuradhu:
# - model.coef_       = [200.0]
# - model.intercept_  = 0.0
# - model.__class__   = LinearRegression
# - All internal state

# Binary format-la serialize panni file-la write pannudu
# Later load panna:
loaded_model = joblib.load("models/model.joblib")
loaded_model.predict([[3500]])  # → [700000.0]  exact same result
```

---

## Part 6 — MLflow Experiment Setup

```python
mlflow.set_tracking_uri(MLFLOW_TRACKING_URI)

client = MlflowClient()
experiment = client.get_experiment_by_name("house-price-prediction")
if experiment is None:
    client.create_experiment(
        name="house-price-prediction",
        artifact_location=MLFLOW_ARTIFACT_URI,
    )
mlflow.set_experiment("house-price-prediction")
```

### Yen ippadi complex-a pannuvom? Direct `set_experiment()` pannala?

```python
# Simple way (WRONG for GCS):
mlflow.set_experiment("house-price-prediction")
# → Experiment create aagum, but artifact_location = local mlruns/
# → GCS-la upload aagadu!

# Correct way:
# Step 1: Experiment already iruka check
experiment = client.get_experiment_by_name("house-price-prediction")

# Step 2: Illa na → GCS location set panni create
if experiment is None:
    client.create_experiment(
        name="house-price-prediction",
        artifact_location="gs://bucket/mlflow",  # ← GCS point pannudu
    )
# Irundha → existing experiment use pannudu (already GCS set)

# Step 3: Active experiment-a set pannudu
mlflow.set_experiment("house-price-prediction")

# artifact_location = experiment-level setting
# Once set → all runs under this experiment → GCS-la upload
```

### `MlflowClient` vs `mlflow` module — Difference?

```python
# mlflow module → high-level, simple API
mlflow.set_experiment()
mlflow.log_param()
mlflow.log_metric()

# MlflowClient → low-level, full control
client = MlflowClient()
client.create_experiment(artifact_location=...)  # artifact_location set panna
client.get_experiment_by_name(...)               # experiment check panna
client.transition_model_version_stage(...)       # model staging/production move panna

# mlflow module-la artifact_location set panna option illa
# So MlflowClient use pannuvom
```

---

## Part 7 — `mlflow.start_run()` Context Manager

```python
with mlflow.start_run(run_name="linear_regression"):
    mlflow.log_param(...)
    mlflow.log_metric(...)
    mlflow.sklearn.log_model(...)
```

### `with` statement — Yen?

```python
# Without with:
run = mlflow.start_run()
try:
    mlflow.log_param("model_type", "linear_regression")
    # ... more logging
finally:
    mlflow.end_run()  # manually call pannanum, forget pannuvom

# With "with":
with mlflow.start_run():
    mlflow.log_param("model_type", "linear_regression")
    # block end-la automatically end_run() call aagum
    # Exception vandhalum properly close aagum
```

### `mlflow.log_param()` vs `mlflow.log_metric()`

```python
# log_param → hyperparameters, config values
# Single value, doesn't change during run
mlflow.log_param("model_type", "linear_regression")
mlflow.log_param("test_size", 0.2)

# log_metric → performance numbers
# Can log multiple steps (training curves)
mlflow.log_metric("r2_score", 1.0)
mlflow.log_metric("rmse", 0.0)

# UI-la:
# Params → table view, filter panna mudiyum
# Metrics → chart view, runs compare panna mudiyum
```

---

## Part 8 — `mlflow.sklearn.log_model()` — GCS Upload Happens Here!

```python
model_info = mlflow.sklearn.log_model(
    model,
    artifact_path="model",
    registered_model_name="house-price-model",
)
```

### Internally step by step:

```
1. model object receive pannudu

2. Temporary folder create pannudu:
   /tmp/mlflow-xxx/
   ├── model.pkl          ← joblib serialize
   ├── MLmodel            ← metadata YAML
   ├── conda.yaml         ← conda environment
   ├── python_env.yaml    ← virtualenv environment
   └── requirements.txt   ← pip packages

3. artifact_location check pannudu:
   "gs://devmlops-496015-mlops-artifacts/mlflow"

4. google-cloud-storage library use panni upload:
   gs://.../mlflow/<exp-id>/<run-id>/artifacts/model/model.pkl
   gs://.../mlflow/<exp-id>/<run-id>/artifacts/model/MLmodel
   gs://.../mlflow/<exp-id>/<run-id>/artifacts/model/conda.yaml
   gs://.../mlflow/<exp-id>/<run-id>/artifacts/model/python_env.yaml
   gs://.../mlflow/<exp-id>/<run-id>/artifacts/model/requirements.txt

5. registered_model_name irundha:
   Model Registry-la "house-price-model" check pannudu
   Irundha → new version create (v1, v2, v3...)
   Illa na → new model create, v1 add

6. model_info return pannudu:
   model_info.model_uri = "models:/house-price-model/4"
   model_info.run_id    = "abc123..."
```

### GCS Auth epdi work pannudu?

```
gcloud auth application-default login → panninom
→ ~/.config/gcloud/application_default_credentials.json create aagudhu

google-cloud-storage library (dvc-gs install panna vandhadhu):
→ automatically credentials file check pannudu
→ Explicitly pass pannanum illa
→ MLflow → google-cloud-storage → credentials → GCS upload

CI/CD-la:
→ WIF (Workload Identity Federation) → temporary token
→ Same google-cloud-storage library → same flow
→ No hardcoded credentials anywhere!
```

---

## Part 9 — `mlflow.log_artifact()` vs `mlflow.sklearn.log_model()`

```python
# log_artifact → any file upload panna
mlflow.log_artifact(PARAMS_PATH)
# params.yaml → GCS-la upload
# gs://.../artifacts/params.yaml

# log_model → specifically model upload panna
mlflow.sklearn.log_model(model, artifact_path="model")
# model.pkl + MLmodel + conda.yaml + requirements.txt → GCS-la upload
# gs://.../artifacts/model/

# Difference:
# log_artifact → raw file, no metadata, no registry
# log_model    → structured format, MLmodel metadata, registry support
#                load panna mlflow.pyfunc.load_model() use pannalam
#                Vertex AI, SageMaker directly serve panna mudiyum
```

---

## Full Data Flow — Visual

```
train.py start
    │
    ├── load_params()
    │     └── params.yaml read → {test_size: 0.2, model_type: lr}
    │
    ├── mlflow.set_tracking_uri("sqlite:///mlflow.db")
    │     └── SQLite-la connect pannudu
    │
    ├── client.create_experiment(artifact_location="gs://...")
    │     └── SQLite-la experiment entry create
    │         artifact_location = GCS bucket
    │
    ├── mlflow.start_run()
    │     └── SQLite-la run entry create (run_id generate)
    │
    ├── mlflow.log_param() × 5
    │     └── SQLite-la params store
    │
    ├── train()
    │     └── train.csv → X, y → LinearRegression.fit() → model
    │
    ├── mlflow.log_metric() × 3
    │     └── SQLite-la metrics store
    │
    ├── mlflow.sklearn.log_model()
    │     ├── model.pkl generate
    │     ├── MLmodel generate
    │     ├── conda.yaml generate
    │     ├── python_env.yaml generate
    │     ├── requirements.txt generate
    │     └── GCS-la upload ← HERE!
    │         gs://devmlops-496015-mlops-artifacts/mlflow/
    │
    ├── mlflow.log_artifact(params.yaml)
    │     └── GCS-la upload
    │
    └── save_model()
          └── models/model.joblib → local save (DVC track pannudu)
```

---

## Key Takeaways

```
1. os.environ.get()     → Same code, different environments
2. yaml.safe_load()     → Always safe, never yaml.load()
3. df[[col]].values     → 2D numpy array for sklearn
4. joblib > pickle      → numpy arrays faster
5. MlflowClient         → Low-level control (artifact_location set panna)
6. mlflow.start_run()   → Context manager, auto close
7. log_param vs metric  → Config vs Performance numbers
8. log_model            → 5 files generate + GCS upload + Registry
9. GCS auth             → gcloud ADC, no hardcoded credentials
10. exist_ok=True       → makedirs safe, no crash if folder exists
```
