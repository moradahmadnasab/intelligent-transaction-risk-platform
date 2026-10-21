# Phase 6 — Deployment

## 6.1 Deployment Objective

The objective of this phase is to demonstrate that the selected and evaluated RF-3 fraud-risk model can be executed independently of the modeling notebook.

The deliverable is a local batch-inference prototype, not a production banking system.

## 6.2 Deployment Architecture

The inference workflow consists of five principal stages:

1. **Transaction input:** Read a CSV file containing the required `amount` and `category` features.
2. **Input validation:** Verify that the required features are present and satisfy basic input constraints.
3. **Risk prediction:** Load the fitted RF-3 pipeline from `models/rf3_pipeline.joblib` and generate predicted fraud-risk scores.
4. **Decision policy:** Load the frozen thresholds from `models/rf3_policy.json` and assign Approve, Review, or Escalate.
5. **Output generation:** Write the original input features, predicted risk scores, and recommended actions to a CSV file.

The model and policy are stored separately to distinguish statistical prediction from operational decision-making.

## 6.3 Final Model and Policy

The final model is RF-3, a Random Forest classifier with 200 trees, maximum depth 10, and minimum samples per leaf 20.

The model uses two input features: transaction amount and category.

The frozen policy thresholds are:

- Lower threshold: 0.07635097141364822.
- Upper threshold: 0.5731998416519604.

The decision rules are:

- Approve when the predicted score is below the lower threshold.
- Review when the predicted score is at least the lower threshold but below the upper threshold.
- Escalate when the predicted score is at least the upper threshold.

The thresholds were determined from the chronological validation partition and were not modified following the final test evaluation.

## 6.4 Local Inference Implementation

The standalone program `src/predict.py` loads the saved model and policy, validates input data, calculates predicted fraud-risk scores, and generates operational recommendations.

The program accepts input and output CSV paths as command-line arguments.

A five-transaction example was successfully processed, producing the output file `examples/sample_predictions.csv`.

The predictions were independently compared with the original notebook predictions using strict numerical tolerances. All five operational actions also matched exactly.

This confirms reproducibility for the tested examples.

## 6.5 Monitoring Requirements

A future operational deployment should monitor input-data quality, feature-distribution drift, risk-score distributions, intervention volumes, delayed fraud outcomes, and model calibration.

Monitoring should distinguish between immediate information, such as predicted risk scores and action counts, and delayed information, such as verified fraud labels and intervention effectiveness.

Changes in transaction distributions or operational requirements may require a separately governed model or policy update.

## 6.6 Operational and Ethical Considerations

The prototype uses synthetic transactions and is not validated for real-world financial decision-making.

The system does not execute banking transactions or automatically approve, block, or decline payments.

Review and Escalate represent recommended intervention categories.

Operational deployment would require additional validation, security controls, access management, logging, human oversight, and compliance review.

Unseen transaction categories and changes in data distributions require particular attention.

## 6.7 Limitations

The principal limitations are the synthetic dataset, restricted two-feature model, fixed validation-derived thresholds, absence of observed intervention effectiveness, illustrative cost assumptions, and lack of real-time banking integration.

The existing evaluation does not establish financial savings or fraud-prevention effectiveness.

## 6.8 Deployment Conclusion

The project successfully implements a reproducible local batch-inference prototype using the final RF-3 model and frozen three-action policy.

The standalone component loads the saved artifacts and generates predictions independently of the modeling notebook.

The prototype demonstrates a complete technical path from transaction features to risk estimates and operational recommendations.

It is suitable as an evaluated portfolio prototype, subject to the stated limitations, but is not production-ready.
