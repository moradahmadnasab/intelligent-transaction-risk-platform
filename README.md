# Intelligent Transaction Risk & Fraud Detection Platform

**An end-to-end BankSim case study in supervised fraud-risk modeling, operational decision support, and reproducible local inference.**

## Project overview

This project develops and evaluates a machine-learning prototype for transaction fraud-risk assessment. A supervised classifier estimates a transaction's fraud-risk score, and a **separate, validation-derived decision policy** converts that score into one of three *recommended* actions:

- **Approve:** Lower predicted fraud risk.
- **Review:** Intermediate predicted fraud risk.
- **Escalate:** Higher predicted fraud risk.

The project follows the six phases of **CRISP-DM**: Business Understanding, Data Understanding, Data Preparation, Modeling, Evaluation, and Deployment. It is an **evaluated research and software portfolio prototype**, not a production banking application or automated payment-authorization service.

## Dataset and experimental design

The study uses the **BankSim synthetic transaction dataset**, comprising **594,643 transactions** and **7,200 labeled fraud cases** (approximately **1.21%** fraud overall).

A chronological split based on the simulator's `step` variable reserves later observations for evaluation:

| Partition | Simulation steps | Transactions | Fraud cases |
|---|---|---:|---:|
| Training | 0–125 | 396,332 | 5,040 |
| Validation | 126–152 | 98,194 | 1,080 |
| Test | 153–179 | 100,117 | 1,080 |

These are **synthetic simulation steps**, not verified real-world timestamps. The split proportions refer to steps, not exactly to transaction counts. Model selection and decision-threshold development use training and validation data; the test partition is reserved for final evaluation.

The final predictive features are `amount` (numerical) and `category` (categorical). Data-dependent preprocessing is incorporated in the fitted scikit-learn pipeline.

## Modeling and model selection

A **Logistic Regression** baseline was compared with several **Random Forest** configurations. Evaluation considers **Average Precision (AP)**, **ROC-AUC**, **Brier score**, and **log loss**, reflecting both fraud discrimination and the quality of model-generated probability scores.

The selected **RF-3** Random Forest configuration uses:

| Parameter | Value |
|---|---|
| Number of trees | 200 |
| Maximum tree depth | 10 |
| Minimum samples per leaf | 20 |
| `max_features` | `sqrt` |
| `random_state` | 42 |

RF-3 was selected primarily for its validation **Average Precision** (0.807737), with supporting ROC-AUC (0.992853) and reduced tree complexity. **RF-2** achieved slightly better validation Brier score and log loss, so RF-3 is **not** claimed to be best on every metric.

## Final test results

The frozen RF-3 model achieved the following results on the **100,117-transaction reserved test partition**:

| Metric | Test value |
|---|---:|
| Average Precision | **0.804028** |
| ROC-AUC | **0.992570** |
| Brier score | **0.003996** |
| Log loss | **0.015835** |
| Fraud prevalence | **1.0787%** |

The reported values describe performance on **synthetic BankSim data**; they do not establish performance on real banking transactions or perfect probability calibration.

## Three-action decision policy

The policy thresholds were determined from the chronological validation partition and **frozen before test evaluation**:

- **Approve:** score < `0.07635097141364822`
- **Review:** `0.07635097141364822` ≤ score < `0.5731998416519604`
- **Escalate:** score ≥ `0.5731998416519604`

The final test action-by-outcome table is:

| Recommended action | Non-fraud | Fraud | Total |
|---|---:|---:|---:|
| Approve | 98,191 | 200 | 98,391 |
| Review | 825 | 271 | 1,096 |
| Escalate | 21 | 609 | 630 |
| **Total** | **99,037** | **1,080** | **100,117** |

The policy routed **880 / 1,080 = 81.48%** of observed fraud cases to **Review or Escalate**, while assigning **1,726 / 100,117 = 1.72%** of all test transactions to those intervention categories. Of the 1,726 interventions, **846** concerned non-fraudulent transactions.

**Important:** Fraud *routing* is not proof of fraud *prevention*. Review and Escalate are decision-support recommendations, not evidence that payments were blocked or losses avoided.

## Repository contents

| Path | Purpose |
|---|---|
| `README.md` | Project overview, experimental results, and usage instructions |
| `docs/01_business_understanding.md` | Business problem, objectives, assumptions, and scope |
| `docs/02_data_understanding.md` | BankSim dataset structure, exploration, and data-quality verification |
| `docs/03_data_preparation.md` | Chronological splitting, feature selection, and preprocessing |
| `docs/04_modeling.md` | Model comparisons, selection, and decision-policy development |
| `docs/05_evaluation.md` | Reserved-test metrics, policy outcomes, and illustrative cost scenarios |
| `docs/06_deployment.md` | Standalone batch-inference design and limitations |
| [Mathematical Foundations report (PDF)](docs/mathematical_foundations_consolidated_source/07_mathematical_foundations_consolidated_release.pdf) | Mathematical formulation, evaluation metrics, methodological rationale, and limitations |
| `notebooks/01_data_understanding.ipynb` | Exploratory analysis and dataset understanding |
| `notebooks/02_data_preparation.ipynb` | Data preparation and feature-processing workflow |
| `notebooks/03_modeling.ipynb` | Model training, comparison, and evaluation |
| `src/predict.py` | Standalone CSV batch-inference program |
| `models/rf3_policy.json` | Frozen validation-derived decision-policy thresholds |
| `reports/` | Final test metrics, action table, policy summary, and cost scenarios |
| `examples/sample_transactions.csv` | Example transactions for local inference |
| `examples/sample_predictions.csv` | Example prediction outputs |
| `requirements.txt` | Python dependencies |

**Model artifact availability:** The fitted Random Forest pipeline, `models/rf3_pipeline.joblib`, is maintained locally and is not distributed in the current repository. Reproducing standalone inference requires a compatible locally trained pipeline and the published decision-policy JSON file.

The Mathematical Foundations report provides additional theoretical discussion of the classification problem, model formulation, evaluation metrics, methodological choices, and limitations.

## Reproducibility and local usage

### 1. Set up Python dependencies

From the repository root, create and activate a virtual environment if desired, then install the declared dependencies:

```bash
python -m pip install -r requirements.txt
```

### 2. Obtain the dataset

Obtain the publicly distributed **BankSim** CSV from its original public distribution (described in `docs/02_data_understanding.md`) and place the unmodified file at:

```text
data/raw/bs140513_032310.csv
```

The raw CSV is **not included in the Git repository**. The Data Understanding document records the source, file size, and SHA-256 checksum used for the study.

### 3. Reproduce the analysis

Consult `notebooks/03_modeling.ipynb` and the CRISP-DM documents for the modeling and evaluation workflow. The notebook's actual execution order, expected working directory, and artifact-writing cells should be checked before treating it as a one-command end-to-end training script.

### 4. Run standalone inference with a locally available trained model

The batch-inference program requires **both** of these local files:

```text
models/rf3_pipeline.joblib
models/rf3_policy.json
```

The current `.gitignore` excludes `models/*.joblib`, so **cloning the repository alone will not provide the fitted model**. A compatible trained pipeline must first be generated locally from the modeling workflow or provided separately.

When the model and policy are available, and the example input file exists, run from the project root:

```bash
python src/predict.py --input examples/sample_transactions.csv --output examples/sample_predictions.csv
```

The input CSV must include `amount` and `category`. The program outputs model-generated fraud-risk scores and recommended actions. The local five-transaction inference check reported agreement with the notebook's predictions and policy assignments; it does not establish broader deployment readiness.

## Limitations and future work

- **Synthetic data:** BankSim performance cannot be generalized directly to real payment systems.
- **Restricted predictors:** The final model uses only transaction amount and category.
- **Single reserved test partition:** Results do not measure variability across independent datasets.
- **Probability interpretation:** Model scores should not be assumed perfectly calibrated.
- **Fixed policy thresholds:** Future intervention rates may change under distribution shift.
- **Hypothetical economics:** Three illustrative cost scenarios use assumed normalized costs and intervention effectiveness, not observed financial savings.
- **Local prototype:** There is no live banking integration, automated payment execution, production monitoring, or production security validation.

Potential future work includes richer leakage-safe behavioral features, additional temporal validation, calibration assessment, automated testing, model packaging, and operational monitoring.

## Project status

**Completed for the BankSim case study:** six CRISP-DM phases, candidate-model comparisons, frozen policy development, reserved-test evaluation, saved evaluation artifacts, and a local batch-inference demonstration.

**Not claimed:** production readiness, proven real-world fraud prevention, or measured financial benefits.
