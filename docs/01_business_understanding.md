# Business Understanding

## 1.1 Project Context

The **Intelligent Transaction Risk & Fraud Detection Platform** is an independent portfolio and R&D project that investigates how machine learning and software-engineering methods can support fraud-risk assessment for electronic payment transactions.

The project uses a realistic reference scenario rather than requirements obtained from an actual financial institution. Business assumptions and system requirements are therefore treated as design assumptions informed by established fraud-detection and machine-learning practices and are revised as the project develops.

The project is intended to evolve incrementally from an evaluated machine-learning prototype into a reproducible ML engineering system and, subsequently, a production-oriented fraud-risk platform.

---

## 1.2 Business Problem

Electronic payment organizations must identify potentially fraudulent transactions while processing large numbers of legitimate transactions.

Failing to identify fraudulent activity can result in financial loss and operational risk. Conversely, excessive fraud alerts or unnecessary intervention can disrupt legitimate transactions, inconvenience customers, and increase investigation workload.

The problem is therefore not simply to maximize fraud detection. A useful fraud-risk system must balance fraud detection against false positives, operational workload, customer disruption, and system reliability.

---

## 1.3 Business Objective

The primary business objective is:

> Develop a decision-support capability that helps a payment-transaction organization identify potentially fraudulent transactions early enough to reduce fraud-related losses and operational risk, while limiting unnecessary disruption to legitimate transactions and keeping the investigation workload manageable.

The main business-success dimensions are therefore:

- improved identification of fraudulent transactions;
- reduced fraud-related loss and operational exposure;
- controlled false-positive burden;
- limited disruption of legitimate transactions;
- manageable manual-review workload;
- sufficiently timely transaction-risk assessment; and
- reliable and reproducible system behavior.

Because this project does not have access to an actual organization's financial baselines, investigation costs, or fraud-loss data, arbitrary monetary ROI targets are not imposed at this stage.

---

## 1.4 Operational Decision to Be Supported

For each incoming transaction, the proposed system should produce information that can support an operational decision policy.

Conceptually, downstream actions may include:

1. **Approve** — allow a sufficiently low-risk transaction to proceed normally.
2. **Verify / Review** — request additional verification or route the transaction for further investigation.
3. **Escalate** — recommend stronger intervention when the assessed risk is sufficiently high.

These actions are conceptual reference actions rather than policies of a particular financial institution.

The machine-learning model itself will **not directly determine the business action**. Instead, it will generate a fraud-risk score. A separate policy layer will translate that score, together with appropriate thresholds and business rules, into an operational action.

This separation allows decision policies and risk tolerances to change without necessarily retraining the underlying model.

---

## 1.5 Machine-Learning Objective

For a transaction represented by information legitimately available at decision time, estimate a fraud-risk score indicating how strongly the transaction is associated with fraudulent activity.

For observations

\[
D = \{(x_i,y_i)\}_{i=1}^{n},
\]

where \(x_i\) represents the available transaction information and

\[
y_i =
\begin{cases}
1, & \text{fraudulent transaction},\\
0, & \text{legitimate transaction},
\end{cases}
\]

the initial machine-learning task is supervised binary classification.

The principal model output is a **continuous risk score**, rather than merely a hard fraud/non-fraud classification.

A model score will not automatically be interpreted as a calibrated fraud probability. Probability calibration must be evaluated and, where necessary, improved before such an interpretation is used.

---

## 1.6 Machine-Learning Success Criteria

Because transaction fraud is expected to be an imbalanced classification problem, overall accuracy alone is not considered an adequate evaluation criterion.

Evaluation will consider, where appropriate:

- precision;
- recall;
- F1 score;
- confusion matrix;
- precision-recall behavior and Average Precision;
- ROC-AUC;
- probability calibration;
- false-positive burden;
- false-negative consequences;
- threshold-dependent behavior; and
- cost-sensitive or decision-oriented measures.

The relative importance of these measures will be determined by the operational decision problem rather than treating every metric as equally important.

Quantitative performance targets will not be invented before the dataset, baseline performance, and plausible operational trade-offs have been established.

---

## 1.7 Prediction-Time Validity and Leakage Control

Only information that would legitimately be available when the transaction is assessed should be used as predictive input.

Potential features will therefore be examined for:

- availability at prediction time;
- target leakage;
- information derived from future transactions;
- inappropriate use of post-event information; and
- dependencies that could make offline evaluation unrealistically optimistic.

Where meaningful temporal information is available, evaluation should preferentially reflect the operational direction of time—for example, learning from earlier observations and evaluating on later observations—rather than automatically relying only on random train/test splitting.

The exact validation strategy will be determined after Data Understanding.

---

## 1.8 Resources

### Available Resources

The project currently has:

- a public fraud-detection dataset selected during Data Understanding;
- Python;
- pandas and NumPy;
- scikit-learn;
- Jupyter;
- Git and GitHub;
- local computing resources;
- mathematical, statistical, numerical, and machine-learning expertise; and
- previous experience developing a credit-risk classification pipeline.

Additional engineering technologies will be introduced only when required by later project releases.

### Currently Unavailable Resources

The project does not currently have:

- access to a live institutional transaction stream;
- proprietary bank or payment-provider data;
- organization-specific fraud costs;
- organization-specific intervention policies;
- production fraud investigators as formal project stakeholders;
- real production traffic; or
- production infrastructure.

These limitations constrain the conclusions that can legitimately be drawn from the project.

---

## 1.9 Requirements

The initial system requirements are:

**R1 — Transaction-level risk assessment**  
The system should generate a fraud-risk assessment for an individual transaction.

**R2 — Decision-support output**  
The model output should be usable by a downstream operational decision policy.

**R3 — Imbalance-aware evaluation**  
Evaluation must account explicitly for class imbalance; accuracy alone is insufficient.

**R4 — False-positive assessment**  
The effect of incorrectly flagging legitimate transactions must be measured explicitly.

**R5 — Reproducibility**  
Data processing, training, evaluation, and model artifacts should be reproducible.

**R6 — Explainability**  
The project should provide meaningful model and prediction interpretation to the extent permitted by the available data.

**R7 — Prediction-time validity**  
Predictive variables must be checked for availability at transaction-decision time and for potential leakage.

---

## 1.10 Assumptions

The initial working assumptions are:

- a public dataset is sufficient for methodological development but not for establishing real-world production performance;
- the available fraud labels are usable for initial supervised learning, subject to verification during Data Understanding;
- historical transaction patterns contain information useful for fraud-risk estimation;
- the initial system is a decision-support prototype, not an autonomous financial authorization system;
- offline historical evaluation can provide useful initial evidence while remaining an approximation of operational deployment; and
- actual organization-specific fraud and intervention costs are unavailable, so cost analysis will initially use qualitative reasoning and, where useful, scenario or sensitivity analysis.

These assumptions may be revised as evidence is obtained during subsequent CRISP-DM phases.

---

## 1.11 Constraints

Important project constraints include:

- reliance on publicly available data;
- possible anonymization or simulation limitations;
- absence of real production traffic;
- unknown organization-specific business costs;
- limited local computing resources;
- limited project-development time; and
- implementation initially being performed by a single developer.

The project therefore prioritizes a focused, reproducible, and technically defensible implementation over unnecessary infrastructure complexity.

---

## 1.12 Major Risks

Major project risks include:

- dataset behavior that does not adequately represent real-world fraud;
- severe class imbalance;
- target or temporal leakage;
- limited feature interpretability;
- overfitting;
- inappropriate treatment of synthetic or anonymized variables;
- distribution shift over time;
- unrealistic offline evaluation;
- overengineering before establishing a strong ML baseline; and
- drawing production-level conclusions from development data.

These risks will be monitored and addressed progressively through Data Understanding, Data Preparation, Modeling, Evaluation, and later engineering stages.

---

## 1.13 Cost-Benefit Perspective

The operational cost of a fraud-detection system can be conceptualized as involving several components:

\[
C_{\text{total}}
=
C_{\text{FN}}
+
C_{\text{FP}}
+
C_{\text{review}}
+
C_{\text{system}}
+\cdots
\]

where, conceptually:

- \(C_{\text{FN}}\) represents consequences of undetected fraud;
- \(C_{\text{FP}}\) represents consequences of incorrectly flagging legitimate transactions;
- \(C_{\text{review}}\) represents investigation or verification workload; and
- \(C_{\text{system}}\) represents operational system costs.

No arbitrary monetary values are assigned to these components without defensible evidence.

The framework will instead be used later to reason about threshold selection and operational trade-offs.

---

## 1.14 Project Scope and Release Plan

The following release plan records the original development intentions. The implementation status of the current BankSim case study is summarized in Section 1.16.

### V0.1 — Employable ML Core

The first release focuses on:

- Business Understanding;
- dataset selection and Data Understanding;
- Data Preparation;
- simple or heuristic baseline where appropriate;
- statistical ML baseline;
- stronger tree-based or boosting models where justified;
- class-imbalance treatment;
- rigorous evaluation;
- threshold analysis;
- probability calibration where relevant;
- explainability;
- error analysis; and
- reproducible documentation and public repository structure.

The objective is to establish a defensible fraud-risk modeling core before adding production infrastructure.

### V0.2 — ML Engineering System

The second release is expected to introduce:

- professional Python package structure;
- persisted model artifacts;
- inference API;
- input/output validation;
- automated testing;
- structured logging; and
- containerization.

The objective is to transform the ML prototype into a testable software system.

### V1.0 — Production-Oriented ML/MLOps Showcase

The later release is expected to address, where justified:

- CI/CD;
- persistent storage;
- deployment;
- monitoring;
- model and data drift;
- model versioning; and
- production-oriented architecture and documentation.

Advanced infrastructure or modeling techniques such as Kubernetes, streaming platforms, graph neural networks, complex feature stores, automated retraining, and distributed training are intentionally postponed until the core system provides a clear reason to introduce them.

---

## 1.15 Phase-1 Outcome

Business Understanding establishes the project as a **fraud-risk decision-support problem**, rather than merely a binary-classification exercise.

The central design principle is:

**transaction data → fraud-risk score → decision policy → operational action**

This separation will guide subsequent Data Understanding, modeling, evaluation, software architecture, and deployment decisions.

---

## 1.16 Current Implementation Status — BankSim Case Study (October 2026)

The original roadmap in Section 1.14 describes planned capabilities; it should not be read as an inventory of completed deliverables. The current evaluated prototype has progressed through all six CRISP-DM phases for the BankSim case study:

- **Data Understanding and Preparation:** The synthetic BankSim dataset was characterized and divided chronologically into training (steps 0–125), validation (126–152), and test (153–179) partitions. The model uses transaction `amount` and `category`; preprocessing is fitted on training data.
- **Modeling:** Logistic Regression and several Random Forest configurations were compared using validation data. RF-3 was selected primarily for validation Average Precision; RF-2 had slightly better validation Brier score and log loss.
- **Decision policy:** Validation-derived thresholds were frozen at `0.07635097141364822` and `0.5731998416519604`, mapping risk scores to **Approve**, **Review**, or **Escalate** recommendations.
- **Final evaluation:** On the reserved 100,117-transaction synthetic test partition, RF-3 achieved Average Precision **0.804028** and ROC-AUC **0.992570**. The frozen policy routed **880 of 1,080** labeled fraud cases to Review or Escalate, involving **1,726 of 100,117** transactions.
- **Local deployment prototype:** A standalone batch-inference program (`src/predict.py`) loads the saved model and policy and produces risk scores and recommended actions. This is not a production payment-processing service.

**Not established:** Actual fraud prevention, monetary savings, performance on real banking data, production-grade deployment, live monitoring, or automatic payment authorization. The three cost scenarios are hypothetical and expressed in normalized units.

**Reproducibility note:** The local trained model is stored as `models/rf3_pipeline.joblib`; the project's `.gitignore` excludes `.joblib` files from the public repository by default. Users will need to reproduce the model locally or obtain a separately distributed artifact before running saved-model inference.

See Phases 2–6 for detailed evidence, procedures, results, and limitations.
