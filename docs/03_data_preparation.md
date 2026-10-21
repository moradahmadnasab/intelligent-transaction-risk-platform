# Data Preparation

**Project:** Intelligent Transaction Risk & Fraud Detection Platform  
**Dataset:** BankSim (`bs140513_032310.csv`)  
**CRISP-DM phase:** Phase 3 — Data Preparation  
**Implementation notebook:** `notebooks/02_data_preparation.ipynb`  
**Status:** Baseline preparation completed and verified; its two-feature design was retained in the final evaluated model. Extended feature engineering remains deferred.

## 3.1 Preparation Strategy and Modeling Assumptions

The purpose of this phase is to establish a reproducible, leakage-aware data preparation workflow for transaction-level fraud prediction. The intended prediction task is to estimate whether a submitted transaction is fraudulent using information assumed to be available when the transaction is assessed, before the true fraud outcome is known.

BankSim is a synthetic dataset and does not provide a complete operational banking workflow or actual transaction timestamps. Prediction-time feature availability is therefore treated as an explicit modeling assumption, not an independently verified operational fact.

The initial workflow preserves the original raw dataset, selects a small baseline feature set, creates chronological partitions using complete simulation steps, fits preprocessing only on the training partition, and verifies the prepared outputs. Customer- and merchant-history features, demographic predictors, and other extensions are deferred until their information-availability and evaluation requirements can be addressed.

## 3.2 Candidate Feature Selection and Prediction-Time Availability

The initial baseline uses two predictors:

- `amount`: transaction amount, assumed to be available at transaction submission.
- `category`: transaction category, assumed to be available at transaction submission.

The target is `fraud`, which is excluded from all predictors.

| Original variable | Baseline decision | Rationale |
|---|---|---|
| `amount` | Include | Numerical transaction attribute assumed available at assessment time. |
| `category` | Include | Categorical transaction attribute assumed available at assessment time. |
| `step` | Retain for partitioning; defer as predictor | Simulation ordering, not an actual timestamp; direct predictive use may exploit synthetic regularities. |
| `customer` | Defer | Potential source of customer-history features; raw identifier is excluded from the baseline. |
| `merchant` | Defer | Potential source of merchant-history features; raw identifier is excluded from the baseline. |
| `age` | Defer | Encoded demographic attribute requiring interpretation, relevance, and fairness assessment. |
| `gender` | Defer | Encoded demographic/customer-type attribute requiring governance and relevance assessment. |
| `zipcodeOri` | Exclude | Constant throughout the dataset. |
| `zipMerchant` | Exclude | Constant throughout the dataset. |
| `fraud` | Target only | Outcome to be predicted; never a predictor. |

These are baseline design choices, not permanent exclusions from all future experiments. The original attributes remain in the working partition DataFrames for controlled extensions.

## 3.3 Chronological Data Partitioning

The original dataset contains **594,643 transactions** across **180 consecutive simulation steps (0–179)**. The initial partition was constructed using complete steps, without random reshuffling or stratification:

| Partition | Steps | Steps count | Transactions | Share of transactions | Fraud cases | Fraud prevalence |
|---|---|---:|---:|---:|---:|---:|
| Training | 0–125 | 126 | 396,332 | 66.650410% | 5,040 | 1.271661% |
| Validation | 126–152 | 27 | 98,194 | 16.513101% | 1,080 | 1.099864% |
| Test | 153–179 | 27 | 100,117 | 16.836488% | 1,080 | 1.078738% |
| **Total** | **0–179** | **180** | **594,643** | **100%** | **7,200** | **approximately 1.21%** |

The proposed 70%/15%/15% allocation applies to **simulation steps**, not transaction counts. The actual transaction shares differ because transaction volume varies by step.

Verification confirmed that the partitions cover the full dataset, have disjoint original row indices, and preserve chronological step ordering. Each partition contains both target classes. The fixed count of **40 fraudulent transactions per step** is a known synthetic characteristic; differences in fraud prevalence are retained rather than artificially corrected in the validation or test data.

The validation partition is designated for model development and selection; the test partition is reserved for final evaluation. A step-based split does not, by itself, prevent all forms of preprocessing or feature-engineering leakage.

## 3.4 Baseline Data Preparation and Preprocessing

The initial preprocessing uses scikit-learn's `ColumnTransformer` with two branches:

| Input | Transformation | Configuration |
|---|---|---|
| `amount` | `StandardScaler` | Fit on training data only; apply unchanged to validation and test. |
| `category` | `OneHotEncoder` | `handle_unknown="ignore"`; learn categories from training data only. |

The preprocessing object was fitted using `X_train` and then applied, without refitting, to `X_valid` and `X_test`. Predictor matrices and target vectors were separated for each chronological partition.

The resulting matrices contain **16 features**: one standardized `amount` column and 15 one-hot category indicators. The encoder's feature names correspond to the 15 transaction categories documented during Data Understanding.

Standardization changes the scale of transaction amounts but does not remove their skewness or extreme values. No resampling, outlier deletion, target-based feature selection, or model fitting was performed. The raw CSV was not modified.

For subsequent model training and hyperparameter tuning, preprocessing should be incorporated into a **fresh estimator pipeline** and fitted within each permitted training split or fold. The standalone fitted preprocessing object used here verifies the baseline preparation; it should not be reused indiscriminately in later cross-validation experiments.

## 3.5 Prepared Data Verification

The prepared matrices were checked for row preservation, equal feature dimensions, finite numerical values, expected scaling behavior, valid one-hot representation, and unseen validation/test categories.

| Check | Training | Validation | Test |
|---|---:|---:|---:|
| Matrix shape | 396,332 × 16 | 98,194 × 16 | 100,117 × 16 |
| All values finite | Yes | Yes | Yes |
| Standardized `amount` mean | Approximately 0 | −0.007082 | −0.012404 |
| Standardized `amount` standard deviation | Approximately 1 | 0.888619 | 0.868031 |
| Rows with exactly one active category indicator | 396,332 (100%) | 98,194 (100%) | 100,117 (100%) |
| Categories unseen during training | Not applicable | None | None |

The categorical encoder learned **15 categories** from the training partition. All rows in all three partitions have exactly one active category indicator. No missing or non-finite values were introduced by the transformations.

The training-set standardized amount has a mean effectively equal to zero and standard deviation effectively equal to one, as expected. Validation and test means and standard deviations differ because they were transformed using training-fitted parameters rather than refitted separately.

**Verification decision:** The baseline prepared matrices passed the planned integrity and representation checks and are suitable for initial model-development experiments. This does not establish predictive performance or real-world operational validity.

## 3.6 Limitations, Deferred Activities, and Phase Status

### Completed for the initial baseline

- Defined a transaction-time baseline using `amount` and `category`.
- Separated the binary target `fraud` from predictors.
- Established and verified disjoint chronological training, validation, and test partitions using complete simulation steps.
- Fitted scaling and one-hot encoding on the training partition only.
- Applied the fitted transformations consistently to validation and test partitions.
- Verified matrix dimensions, finite values, training scaling behavior, categorical coverage, and one-hot consistency.
- Preserved the original raw dataset without modification.

### Deferred or requiring later verification

- Customer- and merchant-history features, including the treatment of within-step ordering and the timing of confirmed fraud labels.
- Any inclusion of `age`, `gender`, raw identifiers, or `step` as predictors, subject to relevance, fairness, and generalization considerations.
- Alternative numerical transformations, categorical representations, and other feature-engineering experiments.
- Evaluation of class imbalance through appropriate modeling objectives and metrics; no balancing was applied to validation or test partitions.
- Verification of leakage controls in the final estimator pipeline and in any cross-validation or hyperparameter-tuning procedure.
- Model training, threshold selection, performance evaluation, and operational decision analysis (deferred at the time of this preparation phase; subsequently completed and documented in Phases 4–5).

### Phase status and subsequent implementation

**The initial baseline Data Preparation workflow is complete and verified.** The two-feature design (`amount` and `category`) was retained in the final evaluated Logistic Regression and Random Forest pipelines. The later modeling phase used preprocessing within fitted estimator pipelines; the standalone prepared matrices described here were an initial verification step, not an independently fitted preprocessing artifact reused for test-time model selection.

The subsequent Modeling, Evaluation, and Deployment phases are documented in `04_modeling.md`, `05_evaluation.md`, and `06_deployment.md`. Additional feature engineering remains a possible future extension.
