# Reproducing Manuscript Figure 2

This guide explains how to reproduce all four subplots in **Figure 2** of the *Envismetrics* manuscript using the online tool(http://34.162.1.1:8080/).

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

---
## 🧪 Subplots 3 and 4: Cyclic Voltammetry (CV Module)

**Folder used:**  
[data/test_data/06102024_CV_D_AF](https://github.com/Woffee/Envismetrics/tree/main/data/test_data/06102024_CV_D_AF)

**Files:**  
- GP_0.05gLDMAB_40gLKOH_-1.1to0.7_10mVs_CV.xlsx  
- GP_0.05gLDMAB_40gLKOH_-1.1to0.7_20mVs_CV.xlsx  
- GP_0.05gLDMAB_40gLKOH_-1.1to0.7_30mVs_CV.xlsx  
- GP_0.05gLDMAB_40gLKOH_-1.1to0.7_40mVs_CV.xlsx  
- GP_0.05gLDMAB_40gLKOH_-1.1to0.7_50mVs_CV.xlsx  
- GP_0.05gLDMAB_40gLKOH_-1.1to0.7_60mVs_CV.xlsx  
- GP_0.05gLDMAB_40gLKOH_-1.1to0.7_70mVs_CV.xlsx

Each file contains a cyclic voltammetry (CV) curve of DMAB oxidation recorded at a different scan rate. These are required for **Randles–Ševčík analysis** and **standard rate constant estimation**.

---

### 🔧 Steps to Reproduce

1. Go to the [CV module](http://34.162.1.1:8080/cv) to open the **CV-1** page  
2. Upload **all 7 files** listed above  
3. Keep default settings:  
   - **Gaussian filter sigma**: `10`  
   - **Cycle of representative**: `6` (can be any number base on experiment setting in here is 1-12)  
4. Click **Submit** to proceed to the **CV-2.1** page  
5. In **Function 2: Peak searching**, use the following settings:

| Parameter                    | Value                                               | Explanation                                                                 |
|-----------------------------|-----------------------------------------------------|-----------------------------------------------------------------------------|
| **Peak range (top)**        | `(-1, -0.70), (0, 0.2), (0.25, 0.5)`                | Voltage ranges where oxidation peaks are expected                           |
| **Peak range (bottom)**     | `(-0.925, -0.75), (0.0, 0.125), (0.125, 0.25)`      | Voltage ranges where reduction peaks are expected                           |
| **Discard scan rate from**  | `0, 0, 0`                                           | Discards scan rates at the beginning of the sequence — here, none discarded |
| **Discard scan rate after** | `0, 0, 2`                                           | Discards scan rates at the end — only for the 3rd peak (last 2 scan rates)  |
| **Cycle range**             | `(2, 100)`                                          | Only cycles within this range are used in the peak analysis                  |
| **Scan rate to display**    | `20` mV/s                                           | Highlights the curve at 20 mV/s in the display                               |
| **Cycle number to display** | `9`                                                 | The 9th cycle will be shown in the figure                                    |
| **Which method to use**     | `Max`                                               | Peak current is determined by the maximum value                              |
6. Click **Submit** to proceed to the **CV-2.2** page  
7. The results generated correspond to:
   - **Subplot 3 (Figure 2c):** Peak overlay plot with scan rate info

---

8. Then, click **Function 3: Randles–Ševčík Analysis** to enter the **CV-3.1** page  
9. Use the following parameter settings:

| Parameter                                | Value                         | Explanation                                                                 |
|------------------------------------------|-------------------------------|-----------------------------------------------------------------------------|
| **Number of electron transfer (n)**      | `1`                           | Number of electrons involved in redox reaction                             |
| **Concentration of material (C)**        | `0.000000894454 mol/cm³`      | Bulk concentration of DMAB used in the CV test                             |
| **Temperature (T)**                      | `298.15 K`                    | Standard room temperature in Kelvin                                         |
| **Electrode diameter**                   | `0.30 cm`                     | Diameter of the glassy carbon disk electrode used in this setup            |


10. Click **Submit** to see the results  

---

### 📈 Output

- **Subplot 3 (Figure 2c)**: Peak current vs. scan rate from Function 2  
- **Subplot 4 (Figure 2d)**: Randles–Ševčík plot (Ip vs. √v) and regression line

---

### ❗ Notes

- If using your own CV dataset, ensure it contains **at least 3 scan rates** for Randles–Ševčík to function.
- Click the **"?"** icons in the tool for helpful parameter tips.
- The default settings were chosen to exactly reproduce the manuscript results using this dataset.
- **Subplot 4 (Figure 2d)** includes a new feature in the core code — simulated peak currents based on a given diffusion coefficient (shown as triangles ▲ in the plot).  
  ⚠️ **Note:** This simulation functionality is not yet available in the online tool. To reproduce this feature, use the core Python script in the source code instead. The online version currently only supports diffusion coefficient fitting from experimental data.

