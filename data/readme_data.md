# Data Directory

This folder contains reference files and datasets for using and testing the Envismetrics toolbox.

## 📁 `example_files/`

This folder includes example input files for the three supported electrochemical techniques:

- **CV** – Cyclic Voltammetry
- **HDV** – Hydrodynamic Voltammetry (Rotating Disk Electrode)
- **CA** – Chronoamperometry

These example files demonstrate the expected format and column structure for user-uploaded datasets.

> ⚠️ Uploading files with missing or mismatched columns may cause parsing errors in Envismetrics. Use these examples as templates.

---

## 📁 `test_data/`

This folder contains real experimental data collected during electrochemical studies involving DMAB, PFOS, PFOA, and related compounds.

- Used for **internal testing**, **algorithm validation**, and **performance benchmarking**
- Includes a variety of conditions and instrument outputs
- Suitable for full-feature module testing

> Users do not need these files for normal operation, but developers may use them for verification and QA.

---
