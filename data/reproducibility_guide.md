# Reproducing Manuscript Figure 2

This guide explains how to reproduce all four subplots in **Figure 2** of the *Envismetrics* manuscript using the [online tool](https://envismetrics.streamlit.app/).

All required input files are included in this GitHub folder:  
🔗 [`/data/test_data/`](https://github.com/Woffee/Envismetrics/tree/main/data/test_data)

---
## 🧪 Subplots 1 & 2: Hydrodynamic Voltammetry (HDV Module)

**Folder used:**  
[`data/test_data/05202024_HDV_D40_A1`](https://github.com/Woffee/Envismetrics/tree/main/data/test_data/05202024_HDV_D40_A1)

**Files:**  
- `HDV_G_DMAB0.05gL_10mVs_200rpm.xlsx`  
- `HDV_G_DMAB0.05gL_10mVs_400rpm.xlsx`  
- `HDV_G_DMAB0.05gL_10mVs_600rpm.xlsx`  
- `HDV_G_DMAB0.05gL_10mVs_800rpm.xlsx`  
- `HDV_G_DMAB0.05gL_10mVs_1000rpm.xlsx`  
- `HDV_G_DMAB0.05gL_10mVs_1200rpm.xlsx`  
- `HDV_G_DMAB0.05gL_10mVs_1400rpm.xlsx`  
- `HDV_G_DMAB0.05gL_10mVs_1600rpm.xlsx`  
- `HDV_G_DMAB0.05gL_10mVs_1800rpm.xlsx`  
- `HDV_G_DMAB0.05gL_10mVs_2000rpm.xlsx`

Each file contains a linear sweep voltammetry (LSV) curve measured under a specific rotation speed. These are ideal for **Levich plot** and **diffusion coefficient analysis**.

---

### 🔧 Steps to Reproduce

1. Go to the [Envismetrics HDV module](http://34.162.1.1:8080/hyd_elec) to open the **HDV-1** page  
2. Upload **all 10 files** listed above  
3. Set **Smoothed / Smoothing Level (sigma):** `10`  
4. Click **Submit** to proceed to the **HDV-2** page  
5. Use the following parameter settings:

| Parameter                           | Default Value                     | Explanation                                                                              |
|-------------------------------------|-----------------------------------|------------------------------------------------------------------------------------------|
| **Concentration of solute (C)**     | `0.000000894454 mol/cm³`          | Bulk concentration of DMAB in the electrolyte                                            |
| **Electrode surface area (A)**      | `0.15 cm²`                         | Area of the working electrode                                                            |
| **Kinematic viscosity (ν)**         | `0.01 cm²/s`                       | Default value for aqueous media at ~25°C                                                 |
| **Number of electron transfer (n)** | `1`                                | Typical for DMAB oxidation                                                               |
| **Method**                          | `Levich plot and Levich analysis` | Performs Levich linear fit and diffusion coefficient extraction                          |
| **Applied potential range (V)**     | `(-1, 1)`                          | Voltage range to extract limiting current                                                |
| **Number of potentials to display** | `9`                                | Determines the number of lines in Subplot 1                                              |
| **Potential step interval (mV)**    | `50`                               | Determines dot density in Subplot 2                                                      |

6. Click **Next** to enter **HDV-3.1**  
7. The results generated correspond to:
   - **Subplot 1 (Figure 2a):** Levich plot – limiting current vs. √ω  
   - **Subplot 2 (Figure 2b):** Calculated **slope** and **diffusion coefficient** at selected potentials (based on limiting current fitting)
---

## 📌 Notes

- These files are calibrated to match the tool's default behavior — **no manual adjustment needed**
- When using your own HDV data:
  - Ensure at least **5 rotation speeds** are provided
  - Click the `?` icon next to each field for tips
- If the page gets stuck or you navigate back:
  - Refresh the browser and **re-enter settings**

Next: [CV Module for Figure 2 subplots 3 & 4 ➡️](#)

## 🧪 Subplots 3 and 4: Cyclic Voltammetry (CV Module)

**Files used:**  
`data/figure2_repro/CV/CV_10mV.xlsx`, `CV_20mV.xlsx`, ..., `CV_100mV.xlsx`  
Each file contains a CV curve at a specific scan rate.

**Steps to reproduce:**

1. Go to the [CV module](https://envismetrics.streamlit.app/)
2. Upload **all files** from `CV/` folder
3. Keep all **default parameter settings**
4. Click **Submit** and proceed through steps:
   - Step 1: Data preview
   - Step 2: Current-Voltage assignment
   - Step 3: **Peak Detection**
   - Step 4: **Randles–Ševčík Analysis**
   - Step 5: **Standard Rate Constant Analysis**
5. If some steps are blocked, try refreshing after step 2 (common workaround)

**Output:**
- **Figure 2c**: CV overlay plot with multiple scan rates
- **Figure 2d**: RS analysis — peak current vs. v^½ plot with regression

---

## ❗ Notes

- If using your own data: hover over the **"?"** icons to understand how to choose parameters
- The default values are optimized for the example datasets
- Files here are intended for **validation, testing, and reproducibility checks**

---

## 📁 File Structure

