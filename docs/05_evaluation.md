# Phase 5 — Final Evaluation

## 5.1 Evaluation Objective

The objective of this phase is to assess the selected RF-3 model and its frozen three-action decision policy on the reserved chronological test partition.

The evaluation examines predictive discrimination, probability-quality metrics, operational action distributions, fraud routing, intervention workload, and illustrative economic consequences.

The test partition was not used to select the model or determine the policy thresholds.

## 5.2 Evaluation Dataset

The final test partition contains 100,117 transactions from BankSim simulation steps 153–179.

Of these transactions:

- 1,080 are labeled fraudulent.

- 99,037 are labeled non-fraudulent.

- Fraud prevalence is approximately 1.0787%.

The dataset is synthetic, and its simulation steps should not be interpreted as verified real-world timestamps.

## 5.3 Frozen Model and Policy

The selected model is RF-3, a Random Forest classifier with 200 trees, maximum depth 10, and minimum samples per leaf 20.

It uses transaction `amount` and `category` as input features.

The decision thresholds were established using the validation partition and frozen before final test evaluation:

- Lower threshold: 0.07635097141364822.

- Upper threshold: 0.5731998416519604.

For predicted fraud-risk score p:

- **Approve:** p is below the lower threshold.

- **Review:** p is at least the lower threshold but below the upper threshold.

- **Escalate:** p is at least the upper threshold.

The model and thresholds were not modified based on test results.

## 5.4 Final Test Predictive Performance

| Metric | RF-3 Test |

|---|---:|

| Average Precision | 0.804028 |

| ROC-AUC | 0.992570 |

| Brier score | 0.003996 |

| Log loss | 0.015835 |

| Fraud prevalence | 0.010787 |

Average Precision summarizes performance across the precision–recall curve and is particularly informative for the imbalanced fraud-detection problem.

ROC-AUC summarizes the model's ability to rank fraudulent transactions above non-fraudulent transactions.

Brier score and log loss assess the quality of predicted probabilities, although neither establishes perfect calibration.

The results demonstrate strong discrimination on the reserved synthetic test partition.

## 5.5 Final Test Action-by-Outcome Analysis

The frozen policy produced the following results:

| Action | Non-fraud | Fraud | Total | Fraud concentration (%) | Transactions (%) |

|---|---:|---:|---:|---:|---:|

| Approve | 98,191 | 200 | 98,391 | 0.203 | 98.276 |

| Review | 825 | 271 | 1,096 | 24.726 | 1.095 |

| Escalate | 21 | 609 | 630 | 96.667 | 0.629 |

| **Total** | **99,037** | **1,080** | **100,117** | | **100.000** |

The Approve group contains most transactions and has a relatively low observed fraud concentration.

The Review group contains a substantially higher fraud concentration than the overall test prevalence.

The Escalate group has the highest observed fraud concentration, at approximately 96.67%.

These findings indicate that the frozen policy concentrates many labeled fraudulent transactions into a small intervention workload.

## 5.6 Operational Policy Metrics

| Metric | Test result |

|---|---:|

| Fraud approved | 200 |

| Fraud reviewed | 271 |

| Fraud escalated | 609 |

| Fraud routed to intervention | 880 |

| Fraud coverage | 81.481% |

| Escalation precision | 96.667% |

| Intervention precision | 50.985% |

| Intervention rate | 1.724% |

| Legitimate interventions | 846 |

Here, intervention refers to either Review or Escalate.

Fraud coverage is the proportion of observed fraud cases assigned to Review or Escalate:

880 / 1,080 ≈ 81.481%.

The intervention rate is the proportion of all test transactions assigned to Review or Escalate:

1,726 / 100,117 ≈ 1.724%.

Intervention precision is the proportion of intervened transactions that were labeled fraudulent:

880 / 1,726 ≈ 50.985%.

Escalation precision is the proportion of escalated transactions that were labeled fraudulent:

609 / 630 ≈ 96.667%.

The policy also assigned 846 legitimate transactions to Review or Escalate.

These quantities describe the observed classification and routing outcomes. They do not establish that fraudulent transactions were actually prevented.

## 5.7 Validation and Test Workload Comparison

The frozen thresholds generated the following action counts:

| Action | Validation | Test |

|---|---:|---:|

| Approve | 96,398 | 98,391 |

| Review | 1,111 | 1,096 |

| Escalate | 685 | 630 |

| Total | 98,194 | 100,117 |

The thresholds were applied unchanged to the test partition.

The resulting action volumes differed between validation and test, demonstrating that fixed score thresholds do not guarantee fixed transaction counts or intervention capacities.

## 5.8 Hypothetical Economic Evaluation

Three illustrative cost scenarios were evaluated:

| Scenario | Hypothetical total cost |

|---|---:|

| A — Review effective | 26,956 |

| B — Review less effective | 38,892 |

| C — Escalation costly | 31,287 |

These values are expressed in hypothetical normalized cost units.

They depend on the cost and intervention-effectiveness assumptions used in the evaluation notebook.

The scenario results illustrate that operational cost is sensitive to the effectiveness and expense of different interventions.

They are not observed financial losses, measured savings, or verified economic benefits.

Without real intervention outcomes and empirically established costs, the results cannot support claims of actual financial savings.

## 5.9 Consistency and Reproducibility

All final evaluation consistency checks passed.

The action-level counts sum to the total number of test transactions.

The fraud and non-fraud counts agree with the test-label totals.

The operational summary is consistent with the action-by-outcome table.

The final evaluation artifacts were saved as:

- `reports/final_test_metrics.json`

- `reports/final_test_action_table.csv`

- `reports/final_test_policy_summary.json`

- `reports/final_test_costs.csv`

The fitted model and frozen policy were also saved separately for standalone inference.

A subsequent five-transaction standalone inference test confirmed numerical agreement with the original notebook predictions and exact agreement in action assignments.

## 5.10 Evaluation Limitations

The final evaluation has several important limitations:

1. **Synthetic data:** Performance on BankSim does not establish generalization to real financial transactions.

2. **Limited features:** Only amount and category were used as predictors.

3. **Single reserved test partition:** The reported results do not quantify performance variability across multiple independent datasets.

4. **Fixed thresholds:** Future intervention rates may differ when transaction distributions change.

5. **Unobserved intervention effectiveness:** Routing a fraudulent transaction to Review or Escalate does not prove that fraud would be prevented.

6. **Hypothetical costs:** Economic scenarios use assumed rather than empirically measured operational costs.

7. **No production validation:** The model has not been tested in a live banking environment.

The final test partition was used for evaluation, not additional model or threshold selection.

## 5.11 Final Evaluation Conclusion

The selected RF-3 model achieved an Average Precision of 0.804028 and ROC-AUC of 0.992570 on the reserved chronological test partition.

The frozen three-action policy routed approximately 81.48% of observed fraud cases to Review or Escalate while assigning approximately 1.72% of all test transactions to intervention.

The Escalate group exhibited an observed fraud concentration of approximately 96.67%.

These results demonstrate promising fraud-risk discrimination and prioritization within the synthetic evaluation setting.

They do not establish real-world fraud prevention, production readiness, or actual economic savings.

The evaluated model and frozen policy were preserved as reproducible artifacts and subsequently used in the standalone local inference prototype.
