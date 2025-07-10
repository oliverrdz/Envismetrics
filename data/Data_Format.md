# 📁 Data Format Instructions for Envismetrics

This document describes the required data format and structure for each electrochemical module used in Envismetrics. Please ensure your input files follow the specifications below to avoid upload or parsing issues.

---

## ⚗️ CA Module (Chronoamperometry)

### ✅ Required Columns

Each uploaded `.xlsx` or `.csv` file should contain the following **case-sensitive** column headers:

- `Time (s)` – Time of the experiment (in seconds)  
- `WE(1).Current (A)` – Working electrode current (in amperes)  
- `WE(1).Potential (V)` – Applied potential (in volts)  

### 📁 File Format

- Files should be in `.xlsx` format, typically exported from NOVA or Autolab software.
- File names are expected to contain numeric prefixes for ordering (e.g., `1_DMAB_120s_CA.xlsx`, `2_DMAB_120s_CA.xlsx`, etc.).
- The numeric portion of the filename is used for indexing and analysis.

**Recommended naming pattern:**  
`X_description_duration_CA.xlsx`  
*Example:* `2_DMAB_120s_CA.xlsx`

### 🧪 Example Table

| Time (s) | WE(1).Current (A) | WE(1).Potential (V) |
|----------|-------------------|----------------------|
| 0.000    | -1.23E-07         | -0.300               |
| 0.001    | -1.22E-07         | -0.300               |
| 0.002    | -1.25E-07         | -0.300               |

### ⚠️ Common Issues

- Column names must **match exactly**, including units and capitalization.
- Files should not contain metadata or comments in the first rows; only structured data.
- Any missing columns or empty rows may lead to analysis failure or file skipping.
- Ensure the folder contains only the relevant `.xlsx` files to avoid misreading.

---

*More modules will be added to this document as needed.*
