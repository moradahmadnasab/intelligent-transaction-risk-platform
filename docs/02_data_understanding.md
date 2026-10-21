# Data Understanding

This document records the Data Understanding phase of the **Intelligent Transaction Risk & Fraud Detection Platform** following the CRISP-DM workflow.

The phase is organized into:

1. Initial Data Collection
2. Data Description
3. Data Exploration
4. Data Quality Verification

All four activities have been completed for the current BankSim case-study scope. Sections 2.1–2.2 record the initial data description; Sections 2.3–2.4 record the subsequent exploration and quality verification.

---

## 2.1 Initial Data Collection

### 2.1.1 Dataset Selection

Several public fraud-detection datasets were considered for the initial development of the project.

The primary dataset selected for the first implementation is **BankSim**.

BankSim was selected because its structure provides several characteristics useful for the objectives of this project:

- transaction-level fraud labels;
- interpretable transaction-related variables;
- repeated customers and merchants;
- transaction categories;
- transaction amounts;
- temporal ordering through simulation steps;
- meaningful class imbalance;
- manageable size for local development; and
- potential for later behavioral, temporal, and relational feature engineering.

The dataset therefore provides a suitable environment for developing the initial fraud-risk methodology and subsequently connecting the ML model to the software-engineering components of the platform.

BankSim is a **simulation-based dataset**. Consequently, performance obtained using BankSim will not be interpreted as evidence of production performance on real financial transactions.

Its role in this project is primarily methodological and developmental.

---

### 2.1.2 Source and Acquisition

The dataset was obtained from the publicly available BankSim distribution on Kaggle.

The downloaded dataset was provided as a compressed archive. The archive was extracted locally, and the original CSV file was placed in:

```text
data/raw/bs140513_032310.csv
```

The raw CSV is treated as immutable project input.

No cleaning, transformation, feature engineering, column removal, row removal, or other intentional modification has been applied to the raw CSV.

Detailed source and integrity information is recorded separately in:

```text
data/raw/README.md
```

**Acquisition date:** 2026-09-29

---

### 2.1.3 Raw-File Integrity Verification

Before loading the dataset into Python, the local file was verified at the filesystem level.

The verified properties are:

| Property | Value |
|---|---|
| Filename | `bs140513_032310.csv` |
| File format | CSV |
| File size | 48,986,035 bytes |
| SHA-256 | `E37006F76D993BFAEC3A02D717B4F0BDC1EBFA5D36449E91FB7C07E225278377` |
| Intentional modifications | None |

The SHA-256 checksum provides a reproducible fingerprint of the exact raw file used in this project.

The raw dataset should not be overwritten by subsequent processing. Derived versions will be stored separately under locations such as:

```text
data/interim/
data/processed/
```

---

## 2.2 Data Description

### 2.2.1 Initial Python Load

The raw dataset was loaded directly into Python using pandas without applying cleaning or transformation.

The file was first verified from Python to exist at the expected location and to have the expected size of:

```text
48,986,035 bytes
```

The CSV was then loaded into a pandas DataFrame.

The resulting dataset shape is:

```text
(594643, 10)
```

Therefore, the dataset contains:

- **594,643 transaction records**
- **10 variables**

The observed columns are:

```text
step
customer
age
gender
zipcodeOri
merchant
zipMerchant
category
amount
fraud
```

---

### 2.2.2 Data Types and Non-Null Counts

The initial pandas representation is:

| Variable | pandas dtype | Non-null observations |
|---|---|---:|
| `step` | `int64` | 594,643 |
| `customer` | `object` | 594,643 |
| `age` | `object` | 594,643 |
| `gender` | `object` | 594,643 |
| `zipcodeOri` | `object` | 594,643 |
| `merchant` | `object` | 594,643 |
| `zipMerchant` | `object` | 594,643 |
| `category` | `object` | 594,643 |
| `amount` | `float64` | 594,643 |
| `fraud` | `int64` | 594,643 |

Pandas therefore detects no standard null (`NaN`) values during the initial load.

This observation does **not** yet establish that all values are semantically known or valid. Object-valued variables may contain encoded values representing unknown or special categories. These cases will be examined during Data Quality Verification.

---

### 2.2.3 Initial Data Dictionary

The following table summarizes the variables based on the current observations.

| Variable | Unique values | Provisional role |
|---|---:|---|
| `step` | 180 | Temporal/simulation-step variable |
| `customer` | 4,112 | Customer identifier |
| `age` | 8 | Encoded age-group/category |
| `gender` | 4 | Encoded categorical variable |
| `zipcodeOri` | 1 | Origin ZIP-code field; constant in this dataset |
| `merchant` | 50 | Merchant identifier |
| `zipMerchant` | 1 | Merchant ZIP-code field; constant in this dataset |
| `category` | 15 | Transaction/merchant category |
| `amount` | 23,767 | Transaction amount |
| `fraud` | 2 | Binary fraud target |

Some interpretations remain provisional until the corresponding BankSim variable definitions and encoded values are verified against dataset documentation.

No preprocessing decision is made solely from this table.

---

### 2.2.4 Temporal Coverage

The `step` variable contains **180 distinct values**.

The observed range is:

```text
Minimum step: 0
Maximum step: 179
```

Transactions occur throughout this range, providing an explicit ordering of observations.

This temporal structure may later support an evaluation strategy in which earlier observations are used for model development and later observations for validation or testing.

No train/validation/test strategy is imposed at this stage. The suitability of temporal splitting will be evaluated after further data exploration.

---

### 2.2.5 Customer and Merchant Structure

The dataset contains:

```text
Unique customers: 4,112
Unique merchants:    50
```

Customer identifiers follow representations such as:

```text
'C1093826151'
'C352968107'
```

and merchant identifiers include representations such as:

```text
'M348934600'
'M1823072687'
```

The same customers and merchants can therefore occur across multiple transaction records.

This repeated-entity structure may later support behavioral features based on customer or merchant transaction histories and, potentially, relational analysis.

Such features are not constructed during Data Description.

---

### 2.2.6 Encoded Age Variable

The `age` variable contains eight observed values:

| Code | Documented meaning | Observed count |
|---|---|---:|
| `'0'` | ≤ 18 years | 2,452 |
| `'1'` | 19–25 years | 58,131 |
| `'2'` | 26–35 years | 187,310 |
| `'3'` | 36–45 years | 147,131 |
| `'4'` | 46–55 years | 109,025 |
| `'5'` | 56–65 years | 62,642 |
| `'6'` | > 65 years | 26,774 |
| `'U'` | Unknown | 1,178 |

The age-group definitions are documented in the original BankSim publication.

Thus, `age` should be interpreted as an **encoded age-group variable**, not as a continuous numerical age measurement. Although codes `0` through `6` have an ordinal age interpretation, preprocessing and encoding decisions are deferred to Data Preparation.

The value `'U'` represents unknown age and therefore constitutes semantically missing or unavailable information even though pandas does not represent it as `NaN`.

---

### 2.2.7 Gender / Customer-Type Variable

The `gender` variable contains four observed values:

| Code | Documented meaning | Observed count |
|---|---|---:|
| `'E'` | Enterprise | 1,178 |
| `'F'` | Female | 324,565 |
| `'M'` | Male | 268,385 |
| `'U'` | Unknown | 515 |

These meanings are defined in the original BankSim publication.

An important consequence is that `gender` is not exclusively a conventional human-gender variable: the code `'E'` identifies enterprise customers. It is therefore more accurately treated as an encoded customer gender/type attribute in this project.

The value `'U'` represents unknown information and should be distinguished from standard pandas null values.

A direct cross-tabulation of `gender` and `age` in the local dataset verifies that all 1,178 observations with `gender == 'E'` also have `age == 'U'`, and all 1,178 observations with `age == 'U'` have `gender == 'E'`. Thus, within this dataset, these two conditions coincide exactly.

The 515 observations with `gender == 'U'` are different: they have known encoded age groups, occurring only in age groups `'1'`, `'2'`, and `'3'` in the observed data.

This distinction is important for later data preparation. In particular, `age == 'U'` should not automatically be treated as ordinary missingness independent of customer type, because in this dataset it is structurally associated with enterprise customers. Any encoding or treatment of these variables will therefore preserve this documented and empirically verified relationship rather than applying automatic missing-value imputation.

---

### 2.2.8 ZIP-Code Variables

Both ZIP-code variables are constant in the observed dataset:

```text
zipcodeOri   : '28007'
zipMerchant  : '28007'
```

Each value occurs in all:

```text
594,643
```

records.

Therefore, these two variables contain no observed transaction-level variation in the current dataset.

Whether they should be excluded from modeling is a Data Preparation decision and is not performed during Data Description.

---

### 2.2.9 Transaction Categories

The dataset contains **15 transaction categories**.

Their observed frequencies are:

| Category | Count |
|---|---:|
| `es_barsandrestaurants` | 6,373 |
| `es_contents` | 885 |
| `es_fashion` | 6,454 |
| `es_food` | 26,254 |
| `es_health` | 16,133 |
| `es_home` | 1,986 |
| `es_hotelservices` | 1,744 |
| `es_hyper` | 6,098 |
| `es_leisure` | 499 |
| `es_otherservices` | 912 |
| `es_sportsandtoys` | 4,002 |
| `es_tech` | 2,370 |
| `es_transportation` | 505,119 |
| `es_travel` | 728 |
| `es_wellnessandbeauty` | 15,086 |

The category distribution is strongly uneven, with `es_transportation` accounting for a large majority of transactions.

The relationship between transaction category and fraud will be investigated during Data Exploration.

---

### 2.2.10 Transaction Amount

`amount` is represented as a continuous numerical variable (`float64`).

The initial descriptive statistics are:

| Statistic | Amount |
|---|---:|
| Count | 594,643 |
| Mean | 37.890135 |
| Standard deviation | 111.402831 |
| Minimum | 0.00 |
| 25th percentile | 13.74 |
| Median | 26.90 |
| 75th percentile | 42.54 |
| Maximum | 8,329.96 |

The mean is greater than the median, while the observed maximum is substantially larger than the upper quartile.

This suggests that the amount distribution may be strongly right-skewed and may contain unusually large transactions.

These observations do not by themselves establish that large values are erroneous or should be removed. In fraud detection, unusual transaction values may contain useful predictive information. Their distribution and relationship with fraud will therefore be examined during Data Exploration and Data Quality Verification.

---

### 2.2.11 Fraud Target

The binary target `fraud` contains two values:

| Fraud label | Count |
|---|---:|
| `0` | 587,443 |
| `1` | 7,200 |

The observed fraud rate is:

```text
0.012108
```

or approximately:

```text
1.211%
```

Thus, fraudulent transactions represent only a small fraction of all observations.

This confirms that the project involves a substantially imbalanced classification problem and supports the Business Understanding decision not to rely on overall accuracy as the primary evaluation criterion.

Detailed analysis of fraud prevalence across amount, category, time, customer, merchant, and other variables belongs to Data Exploration.

---

### 2.2.12 Duplicate Records

The number of exact duplicate rows across all ten variables is:

```text
0
```

Therefore, no completely identical transaction records were detected during this check.

This result should not be interpreted as evidence that the dataset is free of all forms of duplication or data-quality issues. It establishes only that no two rows are identical across the complete observed schema.

---

### 2.2.13 Initial Structural Findings

The initial description establishes several characteristics relevant to subsequent project stages:

- the dataset contains 594,643 transactions and 10 variables;
- the fraud target is strongly imbalanced, with a 1.211% observed fraud rate;
- transactions span 180 ordered simulation steps;
- customers and merchants occur repeatedly across transactions;
- transaction categories are highly uneven in frequency;
- `zipcodeOri` and `zipMerchant` are constant;
- `age` and `gender` contain encoded categorical values requiring semantic verification;
- `amount` has a wide and apparently right-skewed distribution;
- pandas detects no standard null values;
- encoded or semantic missingness still requires investigation; and
- no exact duplicate rows were detected.

These findings provide the basis for Data Exploration and Data Quality Verification.

---

## 2.3 Data Exploration

Data exploration investigates relationships among variables that are relevant to the fraud-risk problem. The analysis remains descriptive at this stage; feature engineering, encoding, resampling, and model-specific transformations are deferred to Data Preparation.

### 2.3.1 Fraud by Transaction Category

Fraud prevalence varies substantially across transaction categories. The overall fraud rate of approximately 1.211% conceals strong category-specific differences.

The highest observed within-category fraud rates occur in `es_leisure` (approximately 95.0%), `es_travel` (79.4%), and `es_sportsandtoys` (49.5%). In contrast, no fraudulent transactions are observed in `es_contents`, `es_food`, or `es_transportation`.

Fraud rate and fraud volume provide different perspectives. For example, `es_leisure` has the highest fraud rate but contains 474 fraud cases, whereas `es_sportsandtoys` contains 1,982 fraud cases despite its lower fraud rate.

Transaction volumes also differ substantially across categories. In particular, `es_transportation` accounts for 505,119 transactions and dominates the dataset by volume while containing no observed fraud cases.

These results indicate a strong association between transaction category and the fraud label in BankSim. Because BankSim is simulation-based, however, the strength of these relationships may partly reflect the simulator's data-generating mechanism and should not be assumed to represent equivalent category-specific fraud behavior in real payment systems.

### 2.3.2 Distribution of Fraud Cases Across Categories

The distribution of the 7,200 fraud cases differs from the ranking based on within-category fraud rates.

`es_sportsandtoys` contributes approximately 27.53% of all observed fraud cases and `es_health` approximately 23.56%. Together, these two categories account for approximately 51.08% of all fraudulent transactions.

This illustrates the distinction between fraud prevalence and fraud volume. For example, `es_leisure` has an observed within-category fraud rate of approximately 95.0% but contributes only approximately 6.58% of all fraud cases because of its relatively small transaction volume. Conversely, `es_health` has a substantially lower fraud rate of approximately 10.51% but contributes approximately 23.56% of all fraud cases.

Category-level fraud behavior should therefore be considered using both within-category fraud prevalence and contribution to the total observed fraud volume.

### 2.3.3 Transaction Amount and Fraud

Transaction amounts differ substantially between fraudulent and non-fraudulent transactions.

The median fraudulent transaction amount is approximately 319.18, compared with 26.61 for non-fraudulent transactions. The corresponding means are approximately 530.93 and 31.85, respectively. The considerably larger means relative to medians, particularly for fraudulent transactions, indicate substantial right-skewness.

The upper tails also differ markedly. The 95th percentile is approximately 1,889.59 for fraudulent transactions compared with 72.81 for non-fraudulent transactions, while the respective 99th percentiles are approximately 4,774.79 and 153.76.

Although fraudulent transactions constitute only approximately 1.211% of all transactions, they account for approximately 16.97% of the total transaction amount observed in the dataset.

Exploration of the log-transformed amount distributions, using `log(1 + amount)` for visualization, shows substantial separation between fraudulent and non-fraudulent transactions while retaining meaningful overlap. Transaction amount therefore contains substantial discriminatory information in BankSim, but it does not by itself perfectly separate the two classes.

Large transaction amounts are not treated as erroneous observations solely because they are extreme. Their relationship with fraud must be considered before any treatment of extreme values is decided during Data Preparation.

### 2.3.4 Temporal Fraud Structure

All 180 simulation steps contain exactly 40 fraudulent transactions. Let

\[
N_t = \text{number of transactions at simulation step } t,
\]

\[
F_t = \text{number of fraudulent transactions at step } t,
\]

and define the step-level fraud rate as

\[
r_t = \frac{F_t}{N_t}.
\]

The observed data satisfy

\[
F_t = 40, \qquad t = 0,\ldots,179,
\]

and consequently

\[
r_t = \frac{40}{N_t}.
\]

Transaction volume generally increases across the simulation period, from approximately 2,400 transactions per step near the beginning to approximately 3,700 toward the end. Correspondingly, the observed fraud rate declines from approximately 1.65% to approximately 1.07%.

Because the fraud count remains fixed at 40 per step, variation in the step-level fraud rate is mathematically determined by variation in the transaction-volume denominator. The strong negative correlation between transaction volume and fraud rate (approximately -0.9934) should therefore not be interpreted causally as evidence that increasing transaction volume reduces fraud occurrence.

A descriptive comparison of three equal 60-step periods shows relatively stable median fraudulent transaction amounts: approximately 325.28, 316.13, and 314.64 for the early, middle, and late periods, respectively. Means and upper-tail values vary more substantially, so this comparison does not establish equality of the complete amount distributions across time.

The observed temporal structure should be considered when designing and interpreting later validation experiments. In particular, chronological validation should be evaluated during model development rather than assuming that a purely random split adequately represents temporal generalization.

### 2.3.5 Customer-Level Fraud Structure

The dataset contains 4,112 distinct customers with substantial variation in transaction activity and observed fraud behavior. Customer transaction counts range from 5 to 265, with a median of 165 transactions.

Of the 4,112 customers, 1,483 (36.07%) have at least one observed fraudulent transaction, while 2,629 (63.93%) have no observed fraud. Consequently, both the median customer-level fraud count and median customer-level fraud rate are zero.

Fraud cases are nevertheless materially concentrated among a smaller subset of customers. The 10 customers with the largest fraud counts account for approximately 15.15% of all 7,200 fraud cases, while the top 100 account for approximately 44.35%. These 100 customers represent only approximately 2.43% of all customers.

Several customers with high fraud counts also exhibit high observed fraud percentages across substantial transaction histories. Thus, the customer-level heterogeneity is not explained solely by unstable rates calculated from very small numbers of transactions.

The mean customer-level fraud percentage (approximately 2.35%) differs from the overall transaction-level fraud rate (approximately 1.21%) because the former gives equal weight to each customer, whereas the latter is weighted by customer transaction volume.

These results indicate that fraud is neither confined to only a handful of customers nor distributed uniformly across customers. Customer identity and any historical customer-level features should therefore be handled carefully during later feature and validation design, particularly when distinguishing prediction for previously observed customers from generalization to unseen customers.

---

### 2.3.6 Merchant-Level Fraud Structure

The dataset contains 50 distinct merchants with highly heterogeneous transaction volumes and observed fraud behavior. Merchant transaction counts range from 3 to 299,693, while observed merchant-level fraud percentages range from 0% to approximately 96.34%.

Of the 50 merchants, 30 (60%) have at least one observed fraudulent transaction, while 20 (40%) have no observed fraud. Fraud cases are strongly concentrated among the highest-fraud merchants: the merchant with the largest fraud count accounts for approximately 22.69% of all fraud cases, the top five account for approximately 59.33%, and the top ten account for approximately 74.89%.

Each merchant is associated with exactly one transaction category in the observed dataset. Thus, if \(M\) denotes merchant identity and \(C\) transaction category,

\[
C = f(M),
\]

so merchant identity deterministically identifies transaction category. The reverse relationship does not generally hold because multiple merchants may belong to the same category.

Merchants belonging to the same category can nevertheless exhibit substantially different observed fraud rates, indicating that merchant identity contains finer-grained information than the category label alone.

This structure has important implications for subsequent modeling and validation. Merchant identity may provide strong discriminatory information when the same merchants appear in both training and evaluation data, but such performance would not by itself demonstrate generalization to previously unseen merchants. Historical merchant-level features must also be constructed using only information available prior to the transaction being scored.

---

### 2.3.7 Encoded Demographic Variables and Fraud

Observed fraud prevalence varies across BankSim's encoded age and gender/customer-type groups. Most human age groups have fraud rates relatively close to the overall transaction-level rate of approximately 1.21%, with no simple monotonic relationship between encoded age group and fraud prevalence.

The `gender` variable requires special interpretation because it contains human gender categories (`'F'` and `'M'`) as well as enterprise (`'E'`) and unknown (`'U'`) categories. All 1,178 enterprise observations correspond to `age='U'`, so this age value should not be interpreted as ordinary missing human age.

Among human observations, the overall observed fraud percentage is approximately 1.47% for `'F'` and 0.91% for `'M'`. The `'F'` group also has a higher observed fraud percentage than the `'M'` group within every encoded human age group. This indicates that the marginal difference is not solely attributable to different age-group compositions.

These relationships are descriptive properties of the BankSim simulation and should not be interpreted causally or generalized directly to real populations. Any later use of demographic variables as model features requires consideration of operational relevance, fairness, governance, and applicable constraints.
---

### 2.3.8 Remaining Exploratory Considerations

The principal exploratory analyses required for the current project stage have been completed. Remaining issues concerning unusual values, encoded missingness, identifier formatting, temporal structure, feature availability, and potential leakage are addressed systematically during Data Quality Verification.

---

## 2.4 Data Quality Verification

Data quality was systematically assessed using the original BankSim dataset containing 594,643 transactions and ten variables. The verification covered structural integrity, missing and specially encoded values, categorical consistency, numerical validity, identifier integrity, target consistency, temporal structure, duplicate records, and potential information leakage.

The objective was to identify data-quality issues and establish requirements for subsequent Data Preparation and Modeling. No cleaning, transformation, or record removal was performed during this stage.

### 2.4.1 Structural Integrity and Missing Values

The dataset contains the expected ten columns with consistent data types and no duplicate column names.

No conventional missing values, empty strings, or whitespace-only values were detected. However, the encoded demographic variables contain special categories, including unknown or nonstandard age and gender/customer-type values. These require explicit interpretation rather than automatic treatment as missing observations.

### 2.4.2 Categorical and Identifier Consistency

No leading or trailing whitespace inconsistencies were detected in the categorical variables, and the expected literal quotation-mark formatting was consistent.

The dataset contains 4,112 distinct customer identifiers and 50 distinct merchant identifiers. All examined identifiers follow their expected formats.

Each merchant is associated with exactly one transaction category.

Both `zipcodeOri` and `zipMerchant` are constant throughout the dataset and therefore provide no observed predictive variation.

Transaction activity is highly concentrated among merchants, with the most frequent merchant accounting for approximately 50.4% of all transactions.

### 2.4.3 Numerical Validity and Transaction Amounts

The numerical variables contain no non-finite values, and no negative transaction amounts were detected.

Transaction amounts range from 0 to 8,329.96 and exhibit a strongly right-skewed distribution.

A total of 52 zero-amount transactions were identified, all labeled non-fraudulent. High-value observations were also identified, but their magnitude alone does not establish that they are erroneous.

Consequently, no observations were removed or modified on the basis of transaction amount.

### 2.4.4 Fraud Target and Class Distribution

The `fraud` variable contains only the valid binary labels 0 and 1.

Of the 594,643 transactions, 587,443 are labeled non-fraudulent and 7,200 are labeled fraudulent, corresponding to a fraud prevalence of approximately 1.21%.

This substantial class imbalance must be considered during model training and evaluation. Classification accuracy alone will not provide an adequate assessment of fraud-detection performance.

### 2.4.5 Temporal Consistency

The dataset contains all 180 consecutive simulation steps, numbered from 0 to 179, without missing steps.

Transaction volume varies between 2,424 and 3,774 observations per step. However, every step contains exactly 40 fraudulent transactions.

This fixed fraud count is an important synthetic characteristic that may affect model behavior and evaluation.

The `step` variable supports temporal ordering but does not provide an actual transaction timestamp or establish the ordering of transactions within the same step.

### 2.4.6 Duplicate Records

No exact duplicate rows were detected. All 594,643 records have distinct complete-row values.

No repeated combinations of the nine recorded transaction attributes were detected when the `fraud` label was excluded.

No deduplication is indicated by the available evidence. Nevertheless, the absence of unique transaction IDs and exact timestamps limits independent verification of transaction-event uniqueness.

### 2.4.7 Prediction-Time Availability and Leakage Risks

The intended prediction scenario is the assessment of transaction fraud risk using information available when a transaction is submitted, before its true fraud outcome is known.

The dataset does not independently establish the operational availability time of every variable.

The principal methodological requirements are:

- Exclude `fraud` from predictor variables.
- Use chronologically ordered partitions for model development and evaluation.
- Construct historical customer and merchant features without using future transactions or unavailable fraud outcomes.
- Fit data-dependent preprocessing operations using the appropriate training partitions.
- Avoid exploiting the artificial regularity of exactly 40 fraudulent transactions per simulation step.
- Assess the operational relevance and fairness implications of demographic predictors.

These are requirements for subsequent phases, not evidence that a leakage-free modeling pipeline has already been implemented.

### 2.4.8 Overall Data Quality Assessment

The verification identified no structural inconsistencies, conventional missing values, malformed identifiers, invalid fraud labels, missing simulation steps, or duplicate recorded transactions.

The principal considerations for subsequent phases are the interpretation of specially encoded values, constant postal-code variables, skewed transaction amounts, merchant concentration, class imbalance, synthetic temporal regularities, and prediction-time information availability.

The dataset is sufficiently consistent and complete to proceed to Data Preparation. However, the suitability of individual features and the reliability of predictive evaluation must be established through carefully designed preparation and modeling procedures.

The raw dataset remains unchanged.


-------

## 2.5 Current Phase Status

The CRISP-DM Data Understanding phase has been completed for the current project scope.

**Completed activities:**

- 2.1 Initial Data Collection
- 2.2 Data Description
- 2.3 Data Exploration
- 2.4 Data Quality Verification

The analysis established the dataset's structure, transaction and fraud characteristics, major data-quality considerations, and methodological requirements for subsequent modeling.

**Next phase: CRISP-DM Phase 3 — Data Preparation**

The next phase will define and implement a reproducible data preparation workflow, including:

- Selection of modeling variables and treatment of encoded categorical values.
- Establishment of chronological training, validation, and test partitions.
- Leakage-safe preprocessing and feature engineering.
- Preparation of suitable modeling datasets while preserving the original raw data.

The raw BankSim dataset has remained unchanged throughout Data Understanding.

Any transformations performed during Data Preparation will be documented and implemented separately from the original data.

----
