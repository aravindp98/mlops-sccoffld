# MLOps Project - Full Explanation (Tanglish)

> **Project Name:** `mlops-sccoffld` — House Price Prediction ML App, GCP-la deploy pannrom.

---

## 1. Ippo Paru - Big Picture Enna?

Namma project simple-a sonna:

```
GitHub-la code push pannuvom
        ↓
GitHub Actions automatically kick off aagum
        ↓
Test → Docker Image Build → GCP Artifact Registry-la push
        ↓
Cloud Run-la deploy → Public URL ready!
```

Basically namma ML model-a internet-la anyone access panna koodiya API-a maathrom. Ellame automated — namma manually onnume pannanum illa.

---

## 2. Folder Structure - Enna Enga Iruku?

```
mlops-sccoffld/
├── main.py                      ← Namma ML app (Flask API)
├── Dockerfile                   ← Container build instructions
├── requirement.txt              ← Python packages list
├── Makefile                     ← Shortcut commands
├── test_main.py                 ← Unit tests
├── new_test.py                  ← Old experiments (all commented out, ignore it)
│
├── .github/workflows/
│   └── main.yaml                ← CI/CD pipeline - heart of automation
│
├── environments/
│   └── dev/                     ← Dev environment terraform config
│       ├── main.tf              ← GCP resources create pannuvom
│       ├── variables.tf         ← Input variables define pannuvom
│       ├── outputs.tf           ← Output values (URLs, emails, etc.)
│       └── terraform.tfvars.example
│
└── modules/
    ├── gcp_wif/                 ← Workload Identity Federation (SUPER IMPORTANT)
    ├── cloud_run/               ← Cloud Run service module
    ├── artifact_registry/       ← Docker image storage module
    ├── ecr/                     ← AWS ECR (currently not used)
    ├── app_runner/              ← AWS App Runner (currently not used)
    └── iam_github/              ← AWS IAM (currently not used)
```

> `ecr/`, `app_runner/`, `iam_github/` — ivanga AWS modules. Project initially AWS-la irunduchu, ippo GCP-ku migrate aagiduchi. So these are just sitting there unused.

---

## 3. ML Application - `main.py`

### Enna pannudu?

Square footage input-a kuduttha house price predict pannudu. Simple Linear Regression use pannrom.

### Endpoints:

| Endpoint | Method | Enna pannudu |
|----------|--------|--------------|
| `/` | GET | Service alive-a nu check pannudu |
| `/health` | GET | Health check (Cloud Run use pannudu internally) |
| `/predict` | POST | Price prediction return pannudu |

### Example call:
```bash
POST /predict
{"sqft": 3500}

# Response:
{"price": 700000.0}
```

### Model logic enna?

```python
# Training data - perfectly linear-a iruku
sqft  = [1500, 2000, 2500, 3000]
price = [300000, 400000, 500000, 600000]

# Pattern: 500 sqft increase = $100,000 increase
# So 3500 sqft → $700,000 — makes sense!
```

App start aagum pothu model train aagum (in-memory). Production-la usually `.joblib` file-la save panni load pannuvanga — ippo namma simple-a keep pannrom.

---

## 4. Dockerfile

```dockerfile
FROM python:3.13-slim      # Lightweight Python base image

WORKDIR /app               # Container-la working directory set pannrom

COPY . /app                # Namma code ellam container-ku copy

RUN pip install -r requirement.txt   # Dependencies install

CMD ["python", "main.py"]  # App start pannudu
```

**Port 8080** — Cloud Run default-a 8080 expect pannudu, so namma app also 8080-la run pannudu.

---

## 5. GCP Setup - Enna Enna Vendum?

GCP-la 3 main things setup pannanum:

```
GCP Project (devmlops-496015)
├── Artifact Registry       ← Docker images store pannra warehouse
├── Cloud Run Service       ← Namma app run pannra serverless platform
└── WIF + Service Account   ← GitHub Actions-ku GCP access kudukkiradu
```

Ellame Terraform use panni code-a define pannrom — manually GCP console-la click pannala.

---

## 6. Terraform - Infrastructure as Code

Terraform = GCP resources-a code-a write pannuvom, apply pannuvom, done. No manual clicking.

### `environments/dev/main.tf` - Enna Pannudu?

#### Step 1: Required APIs Enable Pannudu
```hcl
resource "google_project_service" "required_apis" {
  for_each = toset([
    "artifactregistry.googleapis.com",   # Docker image storage API
    "iam.googleapis.com",                # Identity & Access Management
    "iamcredentials.googleapis.com",     # Token generation
    "run.googleapis.com",                # Cloud Run
    "sts.googleapis.com",                # Security Token Service (WIF needs this)
  ])
}
```
GCP-la any service use pannanum-na first API enable pannanum. Illana "API not enabled" error varum. Terraform ithai automatically pannudu.

#### Step 2: WIF Module Call Pannudu
```hcl
module "gcp_wif" {
  source            = "../../modules/gcp_wif"
  gcp_project_id    = var.gcp_project_id
  github_repository = var.github_repository
}
```
GitHub Actions-ku GCP access kudukka WIF setup pannudu — details section 7-la iruku.

#### Step 3: Artifact Registry Permission
```hcl
resource "google_artifact_registry_repository_iam_member" "github_actions_writer" {
  role   = "roles/artifactregistry.writer"
  member = "serviceAccount:${module.gcp_wif.service_account_email}"
}
```
GitHub Actions service account-ku Docker images push panna permission kudukkirom.

#### Step 4: Cloud Run Service Create
```hcl
module "cloud_run" {
  source    = "../../modules/cloud_run"
  image_uri = var.cloud_run_bootstrap_image_uri  # Google's hello image initially
}
```
First time-la Google's default "hello" image use pannrom. CI/CD run aana piragu namma image replace aagum.

> **Note:** Artifact Registry module commented out — already manually create pannanga, so Terraform recreate pannama skip pannudu.

---

## 7. GCP WIF Module - `modules/gcp_wif/` (MOST IMPORTANT!)

### WIF Enna? Yen Vendum?

**Pazhaya method (Bad way):**
```
GCP Service Account JSON key download pannuvom
→ GitHub Secrets-la store pannuvom
→ Key leak aana → BIG problem
→ Key expire aana → manually renew pannanum
→ Security nightmare!
```

**Pudhusu - WIF (Good way):**
```
GitHub Actions → OIDC Token generate pannudu (temporary, auto-expire)
→ GCP verify pannudu: "Idu namma trusted GitHub repo-va?"
→ Yes-na → temporary GCP credentials kudukudu
→ No secrets store pannanum illa!
→ Fully secure + automatic!
```

### WIF Epdi Work Pannudu? (Step by Step)

```
1. GitHub Actions workflow run aagum
2. GitHub oru OIDC token issue pannudu (JWT format)
   Token-la irukum: repo name, branch, actor, commit SHA, etc.
3. GCP-la Workload Identity Pool antha token verify pannudu
4. "assertion.repository == 'aravindp98/mlops-sccoffld'" condition check pannudu
5. Match aana → Service Account permissions kidaikum
6. GitHub Actions GCP resources access panna mudiyum — no keys needed!
```

### Resources Enna Enna Pannudu?

#### 1. Service Account
```hcl
resource "google_service_account" "github_actions" {
  account_id   = "github-actions-cicd"
  display_name = "GitHub Actions CI/CD"
}
```
GCP-la oru "robot user" create pannrom. GitHub Actions antha account-oda permissions use panni run aagum.

#### 2. Workload Identity Pool
```hcl
resource "google_iam_workload_identity_pool" "github" {
  workload_identity_pool_id = "github-actions-pool"
}
```
External identity providers (like GitHub) trust panna oru container. "Yaara nambalaam" nu define pannudu.

#### 3. Workload Identity Pool Provider
```hcl
resource "google_iam_workload_identity_pool_provider" "github" {
  oidc {
    issuer_uri = "https://token.actions.githubusercontent.com"
  }

  attribute_mapping = {
    "google.subject"       = "assertion.sub"
    "attribute.repository" = "assertion.repository"
  }

  # SECURITY GATE — only this specific repo allowed!
  attribute_condition = "assertion.repository == '${var.github_repository}'"
}
```
GitHub-a specifically trust pannrom. `attribute_condition` = security gate — only `aravindp98/mlops-sccoffld` repo-ku access. Vera repo try pannalum block aagum.

#### 4. IAM Bindings
```hcl
# GitHub Actions → Service Account impersonate panna
resource "google_service_account_iam_member" "github_workload_identity_user" {
  role   = "roles/iam.workloadIdentityUser"
}

# Token create panna
resource "google_service_account_iam_member" "github_token_creator" {
  role   = "roles/iam.serviceAccountTokenCreator"
}

# Project-level permissions
resource "google_project_iam_member" "github_actions_roles" {
  for_each = toset([
    "roles/artifactregistry.writer",   # Docker images push panna
    "roles/iam.serviceAccountUser",    # SA use panna
    "roles/run.admin",                 # Cloud Run deploy panna
  ])
}
```

---

## 8. Cloud Run Module - `modules/cloud_run/`

### Enna Pannudu?

Serverless container hosting. Namma Docker image run panni public URL kudukudu. Namma server manage pannanum illa — Google manage pannudu.

```hcl
resource "google_cloud_run_v2_service" "service" {
  name     = "mlops-house-prices-service"
  location = "us-central1"

  template {
    containers {
      image = var.image_uri
      ports { container_port = 8080 }
      resources {
        limits = { cpu = "1", memory = "512Mi" }
      }
    }
  }

  lifecycle {
    ignore_changes = all   # Terraform itha update pannadu
                           # CI/CD matum update pannum
  }
}

# Public access allow pannudu
resource "google_cloud_run_v2_service_iam_member" "public_invoker" {
  role   = "roles/run.invoker"
  member = "allUsers"
}
```

**`ignore_changes = all` yen?**
Terraform initial setup matum pannudu. Aprom GitHub Actions CI/CD-than image update pannudu. Terraform interference pannama irukka itha use pannrom.

---

## 9. Artifact Registry Module - `modules/artifact_registry/`

Docker images store pannra GCP-oda private registry. Docker Hub mathiri, but private and GCP-la iruku.

```hcl
resource "google_artifact_registry_repository" "docker" {
  repository_id = "mlops-house-prices"
  format        = "DOCKER"
  location      = "us-central1"
}
```

Image URL format:
```
us-central1-docker.pkg.dev/devmlops-496015/mlops-house-prices/mlops-app:latest
```

---

## 10. GitHub Actions CI/CD - `.github/workflows/main.yaml`

### Trigger Eppudi?
- `main` branch-ku push aana automatically
- Manual trigger (workflow_dispatch button)

### 3 Jobs:

```
Job 1: test           → Python tests run pannudu
Job 2: build_push     → Docker build + Artifact Registry push  (needs: test)
Job 3: deploy_cloud_run → Cloud Run deploy                     (needs: build_push)
```

Oru job fail aana next job run aagadu — safety net!

### Job 1: Test
```yaml
- Checkout code
- Python 3.13 setup (pip cache enabled — faster builds)
- pip install -r requirement.txt
- pylint main.py          # Code quality check
- pytest test_main.py     # Unit tests run
```

### Job 2: Build & Push
```yaml
# WIF Authentication — No secrets needed!
- uses: google-github-actions/auth@v2
  with:
    workload_identity_provider: projects/913344865801/.../github-actions-provider
    service_account: github-actions-cicd@devmlops-496015.iam.gserviceaccount.com

# Artifact Registry-la Docker login
- uses: docker/login-action@v3
  with:
    registry: us-central1-docker.pkg.dev
    username: oauth2accesstoken
    password: ${{ steps.auth.outputs.access_token }}   # Temporary token!

# 2 tags-a build pannudu
- docker build \
    -t .../mlops-app:latest \
    -t .../mlops-app:${GITHUB_SHA} \    # Commit SHA tag
    .

# Both push pannudu
- docker push .../mlops-app:latest
- docker push .../mlops-app:${GITHUB_SHA}
```

**Yen 2 tags?**
- `latest` → always latest version point pannudu
- `${GITHUB_SHA}` → exact commit trace panna mudiyum, rollback-ku useful

### Job 3: Deploy to Cloud Run
```yaml
- GCP authenticate (WIF again)
- gcloud run deploy mlops-house-prices-service \
    --image .../mlops-app:${GITHUB_SHA} \   # Specific commit deploy pannudu
    --platform managed \
    --allow-unauthenticated \               # Public access
    --port 8080
```

---

## 11. Variables & Outputs

### Key Variables (`environments/dev/variables.tf`):

| Variable | Value | Yen? |
|----------|-------|------|
| `gcp_project_id` | `devmlops-496015` | GCP project identify panna |
| `gcp_region` | `us-central1` | Resources enga create pannanum |
| `github_repository` | `aravindp98/mlops-sccoffld` | WIF security filter |
| `cloud_run_bootstrap_image_uri` | `us-docker.pkg.dev/cloudrun/container/hello` | First time placeholder image |
| `cloud_run_allow_unauthenticated` | `true` | Public access allow |

### Outputs (`environments/dev/outputs.tf`):

| Output | Enna kudukudu |
|--------|---------------|
| `artifact_registry_repository_url` | Docker repo base URL |
| `artifact_registry_image_uri` | Full image URI |
| `gcp_workload_identity_provider` | WIF provider name — GitHub Actions-la use pannanum |
| `gcp_service_account` | SA email — GitHub Actions-la use pannanum |
| `cloud_run_service_url` | App public URL — itha share pannalam! |

---

## 12. Tests - `test_main.py`

```python
test_data_loading()       # Data keys "sqft" and "price" iruka nu check
test_model_accuracy()     # R² score == 1.0 (data perfectly linear, so perfect score)
test_index_endpoint()     # GET / → {"status": "ok"} varutha nu check
test_predict_endpoint()   # POST /predict {sqft:3500} → price: 700000 varutha nu check
```

CI/CD-la oru test fail aana build stop aagum — safety!

---

## 13. Fresh Setup Epdi Pannuvom? (Step by Step)

### Prerequisites:
- GCP Account + Project ready-a irukanum
- Terraform installed (`terraform -v` check pannunga)
- `gcloud` CLI installed
- GitHub repo ready

### Step 1: GCP Authenticate
```bash
gcloud auth application-default login
gcloud config set project devmlops-496015
```

### Step 2: Terraform Setup
```bash
cd environments/dev

cp terraform.tfvars.example terraform.tfvars
# terraform.tfvars-la gcp_project_id update pannunga

terraform init     # Providers download pannudu
terraform plan     # Enna create aagum nu preview
terraform apply    # Actually create pannudu
```

### Step 3: Terraform Outputs Note Pannunga
```bash
terraform output gcp_workload_identity_provider
# → projects/913344865801/locations/global/workloadIdentityPools/github-actions-pool/providers/github-actions-provider

terraform output gcp_service_account
# → github-actions-cicd@devmlops-496015.iam.gserviceaccount.com
```

### Step 4: GitHub Actions Workflow Update Pannunga
`.github/workflows/main.yaml`-la:
```yaml
GCP_WORKLOAD_IDENTITY_PROVIDER: <terraform output value paste pannunga>
GCP_SERVICE_ACCOUNT: <terraform output value paste pannunga>
```

### Step 5: Push to Main
```bash
git add .
git commit -m "Initial MLOps setup"
git push origin main
```
GitHub Actions automatically trigger aagum → Test → Build → Deploy → Done!

---

## 14. Full Flow - Visual

```
Developer pushes to main branch
            ↓
  GitHub Actions triggers
            ↓
  ┌─────────────────────┐
  │   Job 1: TEST       │
  │  - pylint check     │
  │  - pytest run       │
  └──────────┬──────────┘
             │ pass aana matum
  ┌──────────▼──────────┐
  │  Job 2: BUILD+PUSH  │
  │  - WIF Auth (OIDC)  │  ← No secrets! Token-based
  │  - Docker build     │
  │  - Push to AR       │
  └──────────┬──────────┘
             │ success aana matum
  ┌──────────▼──────────┐
  │  Job 3: DEPLOY      │
  │  - WIF Auth again   │
  │  - gcloud run deploy│
  └──────────┬──────────┘
             ↓
  ┌─────────────────────┐
  │  Cloud Run          │
  │  Public URL live!   │
  │  Anyone can call    │
  │  /predict endpoint  │
  └─────────────────────┘
```

---

## 15. Security - Enna Enna Pannrom?

| Practice | Enga Implement Pannrom |
|----------|------------------------|
| No long-lived credentials | WIF use pannrom — OIDC tokens auto-expire |
| Least privilege | Only needed roles assign pannrom |
| Repo-specific access | `attribute_condition` filter — only our repo allowed |
| Image traceability | SHA-based tags — exact commit trace panna mudiyum |
| API gating | Only required APIs enable pannrom |

---

## 16. Quick Reference - Important Values

```
GCP Project ID  :  devmlops-496015
GCP Region      :  us-central1
AR Repository   :  mlops-house-prices
Cloud Run Svc   :  mlops-house-prices-service
Docker Image    :  mlops-app
SA Email        :  github-actions-cicd@devmlops-496015.iam.gserviceaccount.com
WIF Pool        :  github-actions-pool
WIF Provider    :  github-actions-provider
GitHub Repo     :  aravindp98/mlops-sccoffld
App Port        :  8080
```

---

*Itha padichitu enna doubt-um iruna ask pannunga. GCP WIF part-a first time pakkum-pothu confusing-a irukum, but once understand aana it's the cleanest way to do CI/CD without any secrets!*
