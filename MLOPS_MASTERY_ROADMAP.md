# MLOps Mastery Roadmap - Tanglish Edition
> Senior MLOps Architect perspective-la, namma existing house price project-a base-a vachitu master pannuvom.

---

## WHO IS THIS FOR?
Nee already basic MLOps teriyum — Docker, GitHub Actions, GCP deploy pannirukka.
Ippo next level — DVC, MLflow, Kubeflow, Vertex AI, SageMaker, EKS, GKE — ellame master pannanum.
Lets go one by one, no rush, hands-on with our own project.

---

## PHASE 0 — Foundation Concepts (Understand First, Then Code)

### Enna difference between these 3?

```
Model Training     →  Data vachitu model create pannuvom
Model Deployment   →  Antha model-a server-la run pannuvom
Model Serving      →  Request vandha prediction return pannuvom
Model Inference    →  Actual prediction happen aagura moment
```

### Real world analogy:
```
Training    =  Chef recipe practice pannudu (kitchen-la)
Deployment  =  Restaurant open pannudu (public-ku)
Serving     =  Customer order vandha food kudukudu
Inference   =  Exact moment food plate-la podudu
```

### Ippo namma project enga iruku?
```
main.py       → Training + Inference (both same file, bad practice)
Dockerfile    → Deployment packaging
Cloud Run     → Serving platform
```

Problem: Namma ippo training and serving same-a iruku. Production-la separate pannanum. Itha fix pannuvom step by step.

---

## PHASE 1 — Data Version Control with DVC

### Enna problem solve pannudu DVC?

```
Without DVC:
  - Data enga iruku? S3-la? Local-a? No idea.
  - Model train panna use panna data which version? No tracking.
  - 6 months later reproduce pannanum — impossible.

With DVC:
  - Data versioned like code (Git mathiri)
  - Exact data + exact code = exact model, always reproducible
  - Data S3/GCS-la store, only pointer Git-la
```

### DVC Core Concepts:

```
.dvc files     →  Data pointers (Git-la commit pannuvom)
dvc.yaml       →  Pipeline stages define pannuvom
dvc.lock       →  Exact versions lock pannuvom
Remote storage →  Actual data enga iruku (S3, GCS, Azure Blob)
```

### Namma Project-la DVC Setup Plan:

```
Stage 1: data/raw/        → Raw house price data (DVC track pannudu)
Stage 2: data/processed/  → Cleaned data
Stage 3: models/          → Trained model artifacts
Stage 4: metrics/         → Accuracy scores
```

### DVC Pipeline (dvc.yaml) — How it looks:

```yaml
stages:
  prepare:
    cmd: python src/prepare.py
    deps:
      - data/raw/housing.csv
      - src/prepare.py
    outs:
      - data/processed/train.csv
      - data/processed/test.csv

  train:
    cmd: python src/train.py
    deps:
      - data/processed/train.csv
      - src/train.py
    outs:
      - models/model.joblib
    metrics:
      - metrics/scores.json

  evaluate:
    cmd: python src/evaluate.py
    deps:
      - models/model.joblib
      - data/processed/test.csv
    metrics:
      - metrics/eval.json
```

### Key DVC Commands:
```bash
dvc init                          # Initialize DVC in project
dvc remote add -d myremote gs://bucket/path   # GCS remote set pannudu
dvc add data/raw/housing.csv      # Data track pannudu
dvc push                          # Data remote-ku upload
dvc pull                          # Data download
dvc repro                         # Full pipeline run
dvc params diff                   # Parameter changes show
dvc metrics show                  # Metrics display
```

---

## PHASE 2 — Experiment Tracking with MLflow

### Enna problem solve pannudu MLflow?

```
Without MLflow:
  - 50 experiments run pannuvom — which one best? No idea.
  - Parameters enga note pannuvom? Excel-la? Notebook-la?
  - Best model artifact enga save pannuvom? Local folder-la?
  - Team member different results get pannudu — why? No tracking.

With MLflow:
  - Every experiment automatically logged
  - Parameters, metrics, artifacts — all tracked
  - UI-la compare pannalam
  - Best model register pannalam
  - Anyone reproduce pannalam
```

### MLflow 4 Components:

```
1. MLflow Tracking    →  Experiments log pannudu (params, metrics, artifacts)
2. MLflow Projects    →  Code packaging for reproducibility
3. MLflow Models      →  Model packaging standard format
4. MLflow Registry    →  Model versioning and lifecycle management
```

### MLflow Tracking — How it looks in code:

```python
import mlflow
import mlflow.sklearn

with mlflow.start_run(run_name="linear_regression_v1"):

    # Log parameters
    mlflow.log_param("model_type", "LinearRegression")
    mlflow.log_param("train_size", 0.8)

    # Train model
    model = LinearRegression()
    model.fit(X_train, y_train)

    # Log metrics
    score = model.score(X_test, y_test)
    mlflow.log_metric("r2_score", score)
    mlflow.log_metric("rmse", rmse_value)

    # Log model artifact
    mlflow.sklearn.log_model(model, "model")

    # Log any file
    mlflow.log_artifact("metrics/scores.json")
```

### MLflow Model Registry — Lifecycle:

```
Experiment Run → Staging → Production → Archived

None      →  Just logged, not registered
Staging   →  Testing pannrom, not production ready
Production → Live model, serving pannrom
Archived  →  Old model, retired
```

### MLflow + DVC Together:

```
DVC     →  Data version control + Pipeline orchestration
MLflow  →  Experiment tracking + Model registry

These two complement each other:
DVC tracks WHAT DATA was used
MLflow tracks WHAT RESULTS came out
```

---

## PHASE 3 — Model Deployment, Serving, Inference (Deep Dive)

### Model Deployment Enna?

```
Training complete → model.joblib file ready
Deployment = antha file-a production server-la run panna ready pannudu

Steps:
1. Model serialize pannudu (joblib/pickle/ONNX)
2. Serving code write pannudu (Flask/FastAPI/TorchServe)
3. Container-la pack pannudu (Docker)
4. Cloud-la deploy pannudu (Cloud Run/EKS/GKE/Vertex AI)
```

### Model Serving Patterns:

#### Pattern 1: Online Serving (Real-time)
```
Client → HTTP Request → Model Server → Prediction → Response
Latency: < 100ms
Use case: House price prediction, fraud detection, recommendation
```

#### Pattern 2: Batch Serving (Offline)
```
Scheduler → Trigger → Load 1M records → Predict all → Store results
Latency: Hours acceptable
Use case: Daily report generation, bulk scoring
```

#### Pattern 3: Streaming Serving
```
Kafka/Pub-Sub → Event → Model → Prediction → Another topic
Latency: Seconds
Use case: Real-time fraud, IoT sensor data
```

### Model Inference Enna?

```
Inference = Actual prediction computation happening

Pre-processing  →  Input data clean + transform
Model Forward   →  Actual prediction compute
Post-processing →  Output format, threshold apply
Response        →  Return to client
```

### Inference Optimization Techniques:

```
1. Model Quantization   →  Float32 → Int8 (smaller, faster)
2. Model Pruning        →  Remove unnecessary weights
3. ONNX Runtime         →  Framework-agnostic fast inference
4. TensorRT             →  NVIDIA GPU optimized inference
5. Batching             →  Multiple requests group panni process
6. Caching              →  Same input → cached output return
```

---

## PHASE 4 — Kubeflow (ML Pipelines on Kubernetes)

### Enna pannudu Kubeflow?

```
Kubeflow = Kubernetes-la ML workflows run pannra platform

Without Kubeflow:
  - Training script local-a run pannuvom
  - Scale up pannanum-na manually manage pannanum
  - Pipeline steps manually trigger pannanum

With Kubeflow:
  - Each pipeline step = separate container
  - Auto-scaling built-in
  - Experiment tracking UI
  - Hyperparameter tuning (Katib)
  - Model serving (KServe)
```

### Kubeflow Pipeline — How it looks:

```python
import kfp
from kfp import dsl

@dsl.component
def prepare_data(output_path: str):
    # Data preparation logic
    pass

@dsl.component
def train_model(data_path: str, model_path: str):
    # Training logic
    pass

@dsl.component
def evaluate_model(model_path: str, metrics_path: str):
    # Evaluation logic
    pass

@dsl.pipeline(name="house-price-pipeline")
def house_price_pipeline():
    prepare = prepare_data(output_path="/data/processed")
    train = train_model(
        data_path=prepare.output,
        model_path="/models/model.joblib"
    )
    evaluate = evaluate_model(
        model_path=train.output,
        metrics_path="/metrics/eval.json"
    )
```

### Kubeflow Components:

```
Pipelines      →  ML workflow orchestration
Notebooks      →  Jupyter on Kubernetes
Katib          →  Hyperparameter tuning (AutoML)
KServe         →  Model serving (replaces KFServing)
Training Op    →  Distributed training (TF, PyTorch, XGBoost)
```

---

## PHASE 5 — Vertex AI (GCP Managed MLOps)

### Enna pannudu Vertex AI?

```
Vertex AI = GCP-oda fully managed ML platform
Kubeflow manually manage pannanum illa
Google everything manage pannudu — namma ML logic matum focus pannuvom
```

### Vertex AI Components:

```
Vertex AI Pipelines    →  Kubeflow Pipelines managed version
Vertex AI Training     →  Custom training jobs
Vertex AI Prediction   →  Model serving endpoints
Vertex AI Feature Store → Feature management
Vertex AI Model Registry → Model versioning
Vertex AI Experiments  →  MLflow mathiri experiment tracking
Vertex AI Metadata     →  Lineage tracking
```

### Vertex AI Pipeline — Namma Project-ku:

```python
from google.cloud import aiplatform
from kfp.v2 import dsl, compiler

@dsl.component(base_image="python:3.13-slim")
def train_house_price_model(
    data_path: str,
    model_output: dsl.Output[dsl.Model]
):
    import joblib
    from sklearn.linear_model import LinearRegression
    import numpy as np

    # Train
    model = LinearRegression()
    model.fit(X_train, y_train)

    # Save
    joblib.dump(model, model_output.path)

@dsl.pipeline(name="house-price-vertex-pipeline")
def pipeline():
    train_task = train_house_price_model(
        data_path="gs://my-bucket/data/housing.csv"
    )

# Compile and run
compiler.Compiler().compile(pipeline, "pipeline.json")

aiplatform.init(project="devmlops-496015", location="us-central1")
job = aiplatform.PipelineJob(
    display_name="house-price-training",
    template_path="pipeline.json"
)
job.run()
```

### Vertex AI Endpoint Deployment:

```python
# Model register pannudu
model = aiplatform.Model.upload(
    display_name="house-price-model",
    artifact_uri="gs://my-bucket/models/",
    serving_container_image_uri="us-docker.pkg.dev/vertex-ai/prediction/sklearn-cpu.1-0:latest"
)

# Endpoint create pannudu
endpoint = aiplatform.Endpoint.create(display_name="house-price-endpoint")

# Deploy pannudu
model.deploy(
    endpoint=endpoint,
    machine_type="n1-standard-2",
    min_replica_count=1,
    max_replica_count=5,   # Auto-scaling!
    traffic_percentage=100
)

# Predict pannudu
prediction = endpoint.predict(instances=[{"sqft": 3500}])
```

---

## PHASE 6 — AWS SageMaker (AWS Managed MLOps)

### Enna pannudu SageMaker?

```
SageMaker = AWS-oda fully managed ML platform
Vertex AI = GCP version
SageMaker = AWS version
Concept same, implementation different
```

### SageMaker Components:

```
SageMaker Studio        →  IDE for ML (Jupyter-based)
SageMaker Training      →  Managed training jobs
SageMaker Pipelines     →  ML workflow orchestration
SageMaker Model Registry → Model versioning
SageMaker Endpoints     →  Real-time serving
SageMaker Batch Transform → Batch inference
SageMaker Feature Store →  Feature management
SageMaker Clarify       →  Bias detection + Explainability
SageMaker Model Monitor →  Data drift detection
```

### SageMaker Training Job:

```python
import sagemaker
from sagemaker.sklearn import SKLearn

sklearn_estimator = SKLearn(
    entry_point="train.py",
    role="arn:aws:iam::123456789:role/SageMakerRole",
    instance_type="ml.m5.large",
    framework_version="1.0-1",
    hyperparameters={
        "model-type": "linear-regression",
        "train-size": 0.8
    }
)

sklearn_estimator.fit({
    "train": "s3://my-bucket/data/train.csv",
    "test": "s3://my-bucket/data/test.csv"
})
```

### SageMaker Endpoint Deploy:

```python
predictor = sklearn_estimator.deploy(
    initial_instance_count=1,
    instance_type="ml.t2.medium",
    endpoint_name="house-price-endpoint"
)

# Predict
result = predictor.predict([[3500]])
print(result)  # [700000.0]
```

### SageMaker Pipelines:

```python
from sagemaker.workflow.pipeline import Pipeline
from sagemaker.workflow.steps import TrainingStep, ProcessingStep

# Processing step
processing_step = ProcessingStep(
    name="PrepareData",
    processor=processor,
    inputs=[...],
    outputs=[...]
)

# Training step
training_step = TrainingStep(
    name="TrainModel",
    estimator=sklearn_estimator,
    inputs={"train": training_input}
)

# Pipeline
pipeline = Pipeline(
    name="HousePricePipeline",
    steps=[processing_step, training_step]
)

pipeline.upsert(role_arn="arn:aws:iam::...")
pipeline.start()
```

---

## PHASE 7 — Kubernetes Deployments (EKS + GKE)

### EKS vs GKE Enna Difference?

```
EKS  =  AWS Elastic Kubernetes Service  (AWS-la Kubernetes)
GKE  =  Google Kubernetes Engine        (GCP-la Kubernetes)

Concept same — Kubernetes
Provider different — AWS vs GCP
```

### Namma ML App Kubernetes-la Deploy Pannuvom:

#### Deployment YAML:
```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: house-price-model
spec:
  replicas: 3                    # 3 instances run pannudu
  selector:
    matchLabels:
      app: house-price-model
  template:
    metadata:
      labels:
        app: house-price-model
    spec:
      containers:
      - name: model-server
        image: us-central1-docker.pkg.dev/devmlops-496015/mlops-house-prices/mlops-app:latest
        ports:
        - containerPort: 8080
        resources:
          requests:
            memory: "256Mi"
            cpu: "250m"
          limits:
            memory: "512Mi"
            cpu: "500m"
        readinessProbe:
          httpGet:
            path: /health
            port: 8080
        livenessProbe:
          httpGet:
            path: /health
            port: 8080
```

#### Service YAML:
```yaml
apiVersion: v1
kind: Service
metadata:
  name: house-price-service
spec:
  selector:
    app: house-price-model
  ports:
  - port: 80
    targetPort: 8080
  type: LoadBalancer
```

#### HorizontalPodAutoscaler:
```yaml
apiVersion: autoscaling/v2
kind: HorizontalPodAutoscaler
metadata:
  name: house-price-hpa
spec:
  scaleTargetRef:
    apiVersion: apps/v1
    kind: Deployment
    name: house-price-model
  minReplicas: 2
  maxReplicas: 10
  metrics:
  - type: Resource
    resource:
      name: cpu
      target:
        type: Utilization
        averageUtilization: 70    # CPU 70% aana scale up
```

### GKE Setup:
```bash
# Cluster create
gcloud container clusters create mlops-cluster \
  --zone us-central1-a \
  --num-nodes 3 \
  --machine-type n1-standard-2

# Deploy
kubectl apply -f deployment.yaml
kubectl apply -f service.yaml
kubectl apply -f hpa.yaml

# Status check
kubectl get pods
kubectl get services
kubectl get hpa
```

### EKS Setup:
```bash
# Cluster create
eksctl create cluster \
  --name mlops-cluster \
  --region us-east-1 \
  --nodegroup-name standard-workers \
  --node-type t3.medium \
  --nodes 3

# Deploy (same kubectl commands!)
kubectl apply -f deployment.yaml
kubectl apply -f service.yaml
```

---

## PHASE 8 — Advanced MLOps Concepts

### 1. Feature Store

```
Problem: Same features multiple models use pannudu — duplicate computation
Solution: Feature Store — compute once, use everywhere

Tools:
  - Vertex AI Feature Store (GCP)
  - SageMaker Feature Store (AWS)
  - Feast (Open source)
  - Tecton (Enterprise)

Namma project-ku:
  - sqft_normalized   →  Feature
  - price_per_sqft    →  Derived feature
  - location_score    →  Computed feature
```

### 2. Model Monitoring

```
Problem: Model accuracy production-la degrade aagum — nobody knows
Solution: Continuous monitoring

What to monitor:
  - Data Drift      →  Input distribution change aagiduchi-ya?
  - Concept Drift   →  Relationship between features and target changed-a?
  - Model Drift     →  Prediction distribution shifted-a?
  - Infrastructure  →  Latency, throughput, error rate

Tools:
  - Evidently AI    (open source)
  - WhyLogs
  - Vertex AI Model Monitoring
  - SageMaker Model Monitor
  - Prometheus + Grafana (metrics)
```

### 3. A/B Testing for Models

```
Problem: New model better-a? How to know without full rollout?
Solution: A/B Testing — traffic split pannuvom

Traffic Split:
  Model v1  →  90% traffic
  Model v2  →  10% traffic

Measure:
  - Prediction accuracy
  - Business metrics (conversion, revenue)
  - Latency

If v2 better → gradually increase traffic → 100%
If v2 worse  → rollback → 0%

Kubernetes-la:
  - Istio use pannuvom (service mesh)
  - Traffic weight define pannuvom
```

### 4. Shadow Mode Deployment

```
Production traffic → Model v1 (actual response)
                  ↘ Model v2 (shadow, no response to user)

Compare v1 vs v2 predictions offline
Zero risk to users
Validate new model before real traffic
```

### 5. Canary Deployment

```
Stage 1: 5% traffic → new model
Stage 2: 20% traffic → new model (if ok)
Stage 3: 50% traffic → new model (if ok)
Stage 4: 100% traffic → new model

Automated rollback if error rate spikes
```

### 6. Model Lineage Tracking

```
Which data → Which code → Which model → Which endpoint

Full traceability:
  data/v2.csv + train.py@commit-abc → model-v3.joblib → endpoint-prod

Tools:
  - MLflow (lineage tracking)
  - Vertex AI Metadata
  - Neptune.ai
```

### 7. CI/CD for ML (CT - Continuous Training)

```
Traditional CI/CD:
  Code change → Test → Deploy

ML CI/CD adds:
  Code change → Test → Train → Evaluate → Deploy model
  Data change → Retrain → Evaluate → Deploy model
  Schedule    → Retrain → Evaluate → Deploy model

This is called CT — Continuous Training
```

### 8. Model Compression for Edge Deployment

```
Cloud model: 500MB, needs GPU
Edge model: 5MB, runs on phone/IoT device

Techniques:
  Quantization  →  Float32 → Int8 (4x smaller)
  Pruning       →  Remove 90% weights (sparse model)
  Distillation  →  Big model teach small model
  ONNX Export   →  Framework agnostic deployment
```

---

## PHASE 9 — Complete MLOps Stack Comparison

### When to use What?

```
┌─────────────────┬──────────────────┬──────────────────┐
│   Tool          │   Best For       │   Avoid When     │
├─────────────────┼──────────────────┼──────────────────┤
│ Cloud Run       │ Simple serving   │ Complex scaling  │
│ Vertex AI       │ GCP-first teams  │ Multi-cloud      │
│ SageMaker       │ AWS-first teams  │ Multi-cloud      │
│ GKE/EKS         │ Full control     │ Small teams      │
│ Kubeflow        │ K8s-native ML    │ Managed preferred│
│ MLflow          │ Experiment track │ Enterprise scale │
│ DVC             │ Data versioning  │ Large binary data│
└─────────────────┴──────────────────┴──────────────────┘
```

### Namma Project Evolution Path:

```
Phase 0 (NOW):
  Flask + Cloud Run + GitHub Actions
  Simple, works, no tracking

Phase 1 (NEXT):
  + DVC for data versioning
  + MLflow for experiment tracking
  + Structured src/ folder

Phase 2 (INTERMEDIATE):
  + Kubeflow Pipelines
  + Model Registry
  + Basic monitoring

Phase 3 (ADVANCED):
  + Vertex AI / SageMaker
  + Feature Store
  + Model Monitoring
  + A/B Testing

Phase 4 (EXPERT):
  + GKE/EKS deployment
  + KServe for serving
  + Full observability stack
  + Continuous Training
```

---

## PHASE 10 — Hands-on Order (What We Will Build)

```
Step 1:  Restructure project (src/ layout)              ← START HERE
Step 2:  DVC setup + GCS remote                         ← Data versioning
Step 3:  MLflow tracking + local UI                     ← Experiment tracking
Step 4:  MLflow Model Registry                          ← Model lifecycle
Step 5:  DVC + MLflow pipeline integration              ← Full pipeline
Step 6:  Kubeflow pipeline on local kind cluster        ← K8s pipelines
Step 7:  Vertex AI Pipeline deployment                  ← GCP managed
Step 8:  GKE deployment with KServe                     ← K8s serving
Step 9:  SageMaker training + endpoint                  ← AWS side
Step 10: EKS deployment                                 ← AWS K8s
Step 11: Model monitoring setup                         ← Observability
Step 12: A/B testing + canary deployment                ← Advanced serving
```

---

## QUICK REFERENCE — Tools Summary

```
Data Versioning        →  DVC
Experiment Tracking    →  MLflow
Pipeline Orchestration →  Kubeflow / Vertex AI Pipelines / SageMaker Pipelines
Model Registry         →  MLflow Registry / Vertex AI / SageMaker
Model Serving          →  KServe / Vertex AI Endpoint / SageMaker Endpoint
Container Orchestration → GKE (GCP) / EKS (AWS)
Feature Store          →  Vertex AI Feature Store / SageMaker Feature Store / Feast
Model Monitoring       →  Evidently AI / Vertex AI Monitor / SageMaker Monitor
CI/CD                  →  GitHub Actions (already have this!)
Infrastructure         →  Terraform (already have this!)
```

---

## NEXT STEP

Ippo namma **Step 1** start pannuvom:
- Project restructure pannuvom (`src/` layout)
- DVC install + init pannuvom
- GCS remote configure pannuvom
- First pipeline run pannuvom

Ready-a? Sonna Step 1 hands-on start pannuvom!

---

*This roadmap covers everything from junior to senior MLOps architect level. One step at a time, namma existing project-a upgrade pannuvom. No shortcuts — understand panni build pannuvom.*
