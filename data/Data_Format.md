# 📁 Data Format Instructions for Envismetrics

This document describes the required data format and structure for each electrochemical module used in Envismetrics. Please ensure your input files follow the specifications below to avoid upload or parsing issues.

---

## 🌪️ HDV Module (Hydrodynamic Voltammetry / RDE)

### ✅ Required Columns

Each uploaded `.xlsx` file must contain the following **case-sensitive** columns:

- `WE(1).Current (A)` – Measured working electrode current  
- `WE(1).Potential (V)` – Applied potential during the scan  

> ⚠️ **Note:** The rotation speed (`rpm`) is not in the file content itself — it **must be specified in the filename** and will be automatically extracted.

### 📁 File Format

- Files must be in `.xlsx` format, exported from Autolab/NOVA or equivalent software;
- Each file should contain data for **one rotation rate only** (e.g., `800 rpm`);
- The script will extract `rpm` from the filename using patterns like `800rpm`, `1200rpm`, etc.

**Recommended naming pattern:**  
`SampleID_(rpm)rpm_HDV.xlsx`  
*Example:* `Ni_P_1200rpm_HDV.xlsx`

### 🧪 Example Table

| WE(1).Current (A) | WE(1).Potential (V) |
|-------------------|---------------------|
| -3.78845E-05      | -1.096496582        |
| -3.79333E-05      | -1.094360352        |
| -3.74634E-05      | -1.091918945        |

### ⚠️ Common Issues

- Column names must match **exactly**, including capitalization and spacing;
- No metadata, extra headers, or merged cells should appear in the sheet;
- `rpm` must be included in the **filename** — it will not be read from the file;
- All files in a set should span the same potential range to ensure consistent regression.

---

## 🔁 CV Module (Cyclic Voltammetry)

### ✅ Required Columns

Each uploaded `.xlsx` or `.csv` file must contain the following **case-sensitive** column headers:

- `WE(1).Potential (V)` – Applied potential in volts  
- `WE(1).Current (A)` – Measured current in amperes  
- `Scan` – Cycle number (integer values indicating the scan number)

### 📁 File Format

- Files should be in `.xlsx` or `.csv` format, exported from electrochemical workstation software such as NOVA, EC-Lab, or Gamry.
- Data should contain at least one complete CV cycle. Multiple cycles can be distinguished by the `Scan` column.
- The script will attempt to automatically extract the scan rate from the filename using patterns like `10mVs`, `200mVs`, etc. (if not found, analysis may be skipped or mislabelled).

**Recommended naming pattern:**  
`SampleID_(scanrate)mVs_CV.xlsx`  
*Example:* `GC_K3FeCN6_200mVs_CV.xlsx`

### 🧪 Example Table

| WE(1).Current (A) | WE(1).Potential (V) | Scan |
|-------------------|----------------------|------|
| -9.75647E-06      | 0.002682495          | 1    |
| -9.54285E-06      | 0.005136108          | 1    |
| ...               | ...                  | ...  |

### ⚠️ Common Issues

- Column names must match **exactly**, including capitalization and units.
- Files must include the `Scan` column to distinguish between forward and reverse sweeps or multiple cycles.
- If scan rate is not present in the filename, automated categorization or comparison may not work correctly.

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
---

*More modules will be added to this document as needed.*
