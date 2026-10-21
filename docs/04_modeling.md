# Phase 4 — Modeling

## 4.1 Objective

The modeling phase develops and compares supervised classification models for estimating fraud risk in the BankSim synthetic transaction dataset.

The objective is to identify a model with strong fraud-discrimination performance, acceptable probability-quality metrics, and practical computational complexity, then establish a validation-derived three-action decision policy.

Model development and selection use the training and validation partitions. The reserved chronological test partition is excluded from model selection and threshold development.

## 4.2 Dataset Partitioning and Features

The chronological partition consists of:

| Partition | Simulation steps | Transactions | Fraud cases |

|---|---|---:|---:|

| Training | 0–125 | 396,332 | 5,040 |

| Validation | 126–152 | 98,194 | 1,080 |

| Test | 153–179 | 100,117 | 1,080 |

The final modeling pipeline uses two predictors:

- `amount`: Transaction amount.

- `category`: Transaction category.

Categorical preprocessing is included within the fitted machine-learning pipeline.

The partitioning strategy preserves the ordering of synthetic simulation steps and avoids using the reserved test partition for model development.

## 4.3 Candidate Models

Two principal classifier families were evaluated:

1. Logistic Regression, serving as an interpretable linear baseline.

2. Random Forest, providing a nonlinear ensemble alternative.

The initial unrestricted Random Forest is designated RF-0.

Additional Random Forest configurations, RF-1 through RF-5, were evaluated with different maximum tree depths and minimum leaf sizes.

## 4.4 Evaluation Metrics

Model performance was assessed using:

- **Average Precision (AP):** Summarizes the precision–recall relationship and is particularly relevant to rare fraud events.

- **ROC-AUC:** Measures discrimination across classification thresholds.

- **Brier score:** Measures mean squared error of predicted probabilities against binary outcomes.

- **Log loss:** Penalizes probabilistic predictions according to their agreement with observed outcomes.

Higher AP and ROC-AUC are preferable; lower Brier score and log loss are preferable.

These metrics measure different properties and should not be interpreted as interchangeable.

## 4.5 Initial Candidate Comparison

The initial validation results were:

| Model | Average Precision | ROC-AUC | Brier score | Log loss |

|---|---:|---:|---:|---:|

| Logistic Regression | 0.783930 | 0.992308 | 0.004312 | 0.016985 |

| Unrestricted Random Forest (RF-0) | 0.708612 | 0.908137 | 0.005720 | 0.084423 |

The unrestricted Random Forest performed worse than Logistic Regression on all four reported validation metrics.

This motivated an investigation of tree-complexity restrictions.

## 4.6 Random Forest Regularization Experiments

Six Random Forest configurations were compared.

| Model | Maximum depth | Minimum leaf size | Average Precision | ROC-AUC | Brier score | Log loss |

|---|---:|---:|---:|---:|---:|---:|

| RF-0 | Unlimited | 1 | 0.708612 | 0.908137 | 0.005720 | 0.084423 |

| RF-1 | 20 | 5 | 0.792198 | 0.991686 | 0.004142 | 0.016680 |

| RF-2 | 15 | 10 | 0.805055 | 0.992544 | 0.004003 | 0.015751 |

| RF-3 | 10 | 20 | 0.807737 | 0.992853 | 0.004038 | 0.015968 |

| RF-4 | 15 | 50 | 0.803650 | 0.992634 | 0.004108 | 0.016025 |

| RF-5 | 10 | 100 | 0.797432 | 0.992811 | 0.004258 | 0.016543 |

Regularized configurations substantially improved validation performance relative to RF-0.

RF-3 achieved the highest Average Precision and ROC-AUC among the tested configurations.

RF-2 achieved slightly better Brier score and log loss than RF-3.

Therefore, RF-3 was not uniformly superior across all evaluation metrics.

## 4.7 Model Complexity and Computation

The unrestricted RF-0 configuration had an average tree depth of approximately 48.845 and an average of 2,245.59 leaves per tree.

RF-3 restricted maximum tree depth to 10 and minimum leaf size to 20, producing an average of approximately 106.605 leaves per tree.

The measured RF-3 fitting time was approximately 16.31 seconds in the experimental environment.

These measurements illustrate a substantial reduction in tree complexity relative to the unrestricted configuration.

Execution times depend on the computing environment and should not be treated as universal benchmarks.

## 4.8 Final Model Selection

RF-3 was selected as the final model based primarily on validation Average Precision, supported by its ROC-AUC and reduced tree complexity.

Relative to Logistic Regression, RF-3 improved validation Average Precision from 0.783930 to 0.807737 and ROC-AUC from 0.992308 to 0.992853.

It also achieved lower Brier score and log loss than the Logistic Regression baseline.

The final RF-3 configuration uses:

- 200 trees.

- Maximum tree depth of 10.

- Minimum samples per leaf of 20.

- `max_features="sqrt"`.

- `random_state=42`.

The model is implemented as a fitted preprocessing-and-classification pipeline.

## 4.9 Three-Action Operational Policy

The selected model produces a numerical fraud-risk score.

A separate decision policy maps this score to one of three operational recommendations:

- Approve.

- Review.

- Escalate.

The frozen validation-derived thresholds are:

- Lower threshold: 0.07635097141364822.

- Upper threshold: 0.5731998416519604.

For predicted score p, the action rules are:

- Approve if p is below the lower threshold.

- Review if p is at least the lower threshold but below the upper threshold.

- Escalate if p is at least the upper threshold.

The resulting validation action counts were:

| Action | Transactions |

|---|---:|

| Approve | 96,398 |

| Review | 1,111 |

| Escalate | 685 |

| Total | 98,194 |

These counts describe the workload induced by the frozen thresholds on the validation partition. They are not guaranteed capacities for future datasets.

## 4.10 Model and Policy Artifacts

The final fitted model and decision policy were serialized separately:

- `models/rf3_pipeline.joblib`

- `models/rf3_policy.json`

The policy file preserves the thresholds at full numerical precision and records the required input-feature schema.

This separation enables the standalone inference program to load both artifacts without retraining the model.

## 4.11 Modeling Limitations

The model was developed using synthetic transaction data and only two input features.

The Random Forest probability estimates are model-generated scores and are not guaranteed to represent perfectly calibrated real-world fraud probabilities.

The reported comparisons are based on the available validation partition and the configurations tested; they do not establish that RF-3 is globally optimal.

Operational outcomes depend on the chosen policy and intervention assumptions, not solely on predictive discrimination.

## 4.12 Modeling Conclusion

The modeling phase identified RF-3 as the preferred discrimination-focused classifier among the evaluated candidates.

The experiments demonstrated that restricting Random Forest complexity substantially improved validation results relative to the unrestricted configuration.

A three-action policy was developed using validation-derived thresholds and frozen before the reserved test evaluation.

The selected model and policy were saved as reproducible artifacts for final evaluation and local deployment.
