---
title: 'Envismetrics: A Python-based software for electrochemical kinetic analysis'
tags:
  - Python
  - electrochemistry
  - kinetic analysis
  - online software
  - data analysis
authors:
  - name: Huize Xue
    orcid: 0000-0001-7537-2173
    affiliation: "1"
  - name: Wenbo Wang
    orcid: 0000-0002-0784-7509
    affiliation: "2"
  - name: Xinxin Zhou
    orcid: 0009-0001-0960-6688
    affiliation: "3"
  - name: Fuqin Zhou
    orcid: 0009-0000-0342-0033
    affiliation: "2"
  - name: Omowunmi Sadik
    orcid: 0000-0001-8514-0608
    corresponding: true
    affiliation: "4"
affiliations:
 - name: New Jersey Institute of Technology, Department of Physics
   index: 1
 - name: New Jersey Institute of Technology, Department of Informatics
   index: 2
 - name: Independent Researcher
   index: 3
 - name: New Jersey Institute of Technology, Chemistry and Environmental Science
   index: 4
date: "2024-08-30"
bibliography: bibliography.bib
---

# Abstract
Envismetrics is an open-source, cross-platform Python application designed to assist researchers in the automated analysis of electrochemical data. It provides a modular toolbox that enables the processing, visualization, and parameter extraction of data from techniques such as cyclic voltammetry, chronoamperometry, and hydrodynamic voltammetry. The software supports data input from a variety of potentiostat platforms and automates routine analytical steps, including peak identification, Randles–Ševčík plots, diffusion coefficient estimation, rate constant calculations, and Tafel analysis. Envismetrics features a graphical web interface that minimizes the need for coding and enhances accessibility for researchers across disciplines.
By focusing on automation and reproducibility, Envismetrics reduces the manual workload associated with electrochemical data interpretation and promotes transparent research workflows. The source code is openly available at [https://github.com/Woffee/Envismetrics](https://github.com/Woffee/Envismetrics).

# Summary

Accurate determination of kinetic parameters and thermodynamic properties from electrochemical data is fundamental for understanding redox reactions used in diverse applications [@SANECKI2003109, @wang2020redox, @XU20106366]. These values — including diffusion coefficients, standard rate constants, transfer coefficients, and formal potentials — provide mechanistic insight and are commonly used to validate reaction pathways and simulate electrochemical behavior under various conditions [@C9CP05527D].

Although literature values exist for some well-studied redox systems, the evaluation of new analytes or experimental conditions typically requires experimental determination. Techniques such as cyclic voltammetry (CV), linear sweep voltammetry using a rotating disk electrode (LSV at RDE, under laminar flow and planar diffusion conditions), and step methods like chronoamperometry (CA) offer quantitative frameworks for extracting these parameters [@bard2022electrochemical].

Each technique supports specific analyses:

- **LSV at RDE**: Levich and Koutecký–Levich analysis [@doi:10.1021/ar50110a004; @treimer2002koutecky],
- **CV**: Randles–Ševčík plots, rate constant estimation, and transfer coefficient analysis [@doi:10.1002/adts.202500346; @LEFTHERIOTIS2007259],
- **CA**: Cottrell-based diffusion coefficient estimation [@HERATH20084324; @GOMEZ2023143400; @RODRIGUEZLUCAS2025145648].

While these methods are widely accepted, manual analysis can be labor-intensive and prone to inconsistency. To address this, **Envismetrics** is introduced as an open-source, browser-based Python application that automates data processing and analysis workflows for CV, LSV (RDE), and CA. It provides modules for filtering, peak detection, Levich regression, Randles–Ševčík analysis, and chronoamperometric fitting—offering visual outputs and tabulated results. By focusing on automation and reproducibility, Envismetrics lowers the barrier for electrochemical researchers—especially those dealing with large datasets or requiring rapid feedback—while preserving methodological rigor and transparency.

# Statement of Need

Electrochemical researchers commonly analyze data using a combination of proprietary instrument software (e.g., NOVA for Autolab), manual spreadsheet tools (e.g., Excel), and general-purpose plotting software (e.g., Origin, SigmaPlot). While proprietary software facilitates data collection and basic visualization, it is often platform-specific, instrument-dependent, and limited in automation and cross-experiment reproducibility. Tools like Origin provide flexible plotting, but require manual preprocessing, repeated formatting, and domain expertise for kinetic modeling.

Envismetrics fills this gap by offering a powerful modular, web-based platform focused on automated analysis of electrochemical data, particularly from cyclic voltammetry (CV), linear sweep voltammetry at rotating disk electrodes (LSV at RDE), and chronoamperometry (CA). By supporting common data formats like .xlsx, .csv, and .txt, Envismetrics works independently of instrument brands—allowing researchers to export plaintext data from proprietary systems and continue their analysis seamlessly.

Unlike tools that prioritize device control, Envismetrics emphasizes data processing, reproducibility, and accessibility. It features automated peak detection, Levich and Randles–Ševčík analysis, rate constant fitting, and stepwise modules, making it ideal for both routine analysis and instructional purposes. It also runs on Windows, macOS, and Linux with no installation needed.

Table 1. Comparison of Electrochemical Data Processing Tools

| **Aspect**             | **Proprietary (NOVA)**              | **Envismetrics**                                                            | **Homegrown (FuelCell)**               |
|------------------------|-------------------------------------|-----------------------------------------------------------------------------|----------------------------------------|
| **Installation**       | Windows-only installation           | Web-based, no installation needed                                           | Standalone executable                  |
| **Platform Support**   | Windows only                        | Windows, macOS, Linux                                                       | Windows, macOS, Linux                  |
| **Data Collection**    | built-in                            | requires exported files from instruments                                  | requires exported files from instruments |
| **Data Format Support**| Autolab-specific, requires export   | `.xlsx`, `.csv`, `.txt` (plaintext from any system)                         | Multiple formats                       |
| **Analysis Features**  | Basic plotting, smoothing, baseline | Automated Levich/Randles–Ševčík, peak search, rate fitting                  | Tafel slope, HFR extraction            |
| **Customization**      | Limited                             | Modular architecture, easily extensible                                     | Requires code edits                    |
| **Learning Curve**     | Steep, documentation-heavy          | Intuitive GUI with helper prompts                                           | Depends on script complexity           |
| **Publication Output** | Basic figures                       | Clean plots with export                                                     | Requires post-processing               |
| **Educational Use**    | Limited                             | Interface guides + interactive outputs                                      | Not beginner-friendly                  |
| **Hardware Dependency**| Metrohm Autolab only                | Hardware-agnostic                                                           | Hardware-agnostic                      |

[Comparison of Electrochemical Data Analysis Software]\label{table:1}

# Current Functions of Envismetrics Toolbox

To aid in interpreting the equations below, Table 2 summarizes commonly used electrochemical parameters along with their meanings and corresponding units.

> **Note**:  
> • The symbol $\nu$ appears twice in the table with different meanings:  
> &nbsp;&nbsp;&nbsp;&nbsp;– In **CV**, it denotes the *scan rate*, with units of $\mathrm{V/s}$.  
> &nbsp;&nbsp;&nbsp;&nbsp;– In **HDV (RDE)**, it denotes the *kinematic viscosity*, with units of $\mathrm{cm^2/s}$.  
> • Both the *diffusion coefficient* $D$ and *kinematic viscosity* $\nu$ share the unit $\mathrm{cm^2/s}$, but represent distinct physical phenomena—molecular diffusion and fluid flow, respectively.

| **Symbol**          | **Meaning**                                       | **Unit**               | **Context**       |
| ------------------- | ------------------------------------------------- | ---------------------- | ----------------- |
| $n$                 | Number of electrons transferred in redox reaction | —                      | All methods       |
| $n'$                | Number of electrons in preceding equilibrium      | —                      | CV (irreversible) |
| $F$                 | Faraday constant                                  | $\text{C/mol}$         | All methods       |
| $R$                 | Ideal gas constant                                | $\text{J/mol·K}$       | All methods       |
| $T$                 | Temperature                                       | $\text{K}$             | All methods       |
| $\nu$               | Scan rate (CV)                                    | $\text{V/s}$           | CV                |
| $\nu$               | Kinematic viscosity (HDV)                         | $\text{cm}^2/\text{s}$ | HDV (RDE)         |
| $D$                 | Diffusion coefficient                             | $\text{cm}^2/\text{s}$ | All methods       |
| $A$                 | Electrode area                                    | $\text{cm}^2$          | All methods       |
| $C$, $C_0$          | Concentration of electroactive species            | $\text{mol/cm}^3$      | All methods       |
| $I_{\text{peak}}$   | Peak current                                      | $\text{A}$             | CV                |
| $j$                 | Current density                                   | $\text{A/cm}^2$        | CV                |
| $\theta$            | Dimensionless overpotential                       | —                      | CV                |
| $\alpha$, $\alpha'$ | (Apparent) transfer coefficient                   | —                      | CV                |
| $k_0$               | Standard rate constant                            | $\text{cm/s}$          | CV                |
| $\Psi$              | Dimensionless kinetic parameter                   | —                      | CV                |

[Summary of parameters used in electrochemical equations]\label{table:2}

## Data Processing

Envismetrics supports a wide range of data formats from various potentiostats, including EC-Lab, Autolab, Metrohm, and more. The software can handle document types such as XLSX, TXT, and CSV. Users simply need to export their data and drag the files into the software, making data import and processing straightforward and user-friendly. We are continuously adding support for more commonly used commercial potentiostats. If you do not find support for your specific potentiostat, rest assured that updates will be released shortly to include additional data formats.

![Data Import Window: Users can easily drag and drop or select their experimental data for quick and straightforward import.](Image_Set/1.png){ width=80% }

## Hydrodynamic Voltammetry (HDV) Module

### Function 1: Plotting and Gaussian Filtering

This function plots the experimental data sorted by RPM (rotations per minute) values and allows users to apply a Gaussian filter to obtain a smoothed figure. Users can add the optional Gaussian filter by entering the sigma value, enhancing the clarity of the plotted data.

### Function 2: Levich and Koutecky-Levich Analysis

Levich and Koutecky-Levich analyses are essential for calculating the diffusion coefficient [@masa2014koutecky]. Traditionally, this involves selecting several potential values, plotting the function of RPM versus the function of current, performing linear regression, and calculating the diffusion coefficient from the slope.

Envismetrics simplifies this process by providing an automated Levich and Koutecky-Levich plot function. Users can generate these plots directly from their data. Additionally, the software offers an advanced analysis feature that dynamically calculates and records the slope and diffusion coefficient for every applied potential. This allows users to observe the changes in the slope with varying potentials, helping them decide which range of data to select for their analysis.

## Cyclic Voltammetry (CV) Module

### Function 1: Plotting and Gaussian Filtering

This function plots cyclic voltammetry data sorted based on the rate constant value and allows users to apply a Gaussian filter for smoothing. Users can input the sigma value to adjust the degree of smoothing. Both the original figure and the smoothed data will be displayed, allowing users to compare the raw and processed results.

### Function 2: Peak Searching

Peak searching is essential for calculating formal potential, peak separation, and performing Randles-Ševčík analysis. The software provides multiple searching methods, such as max/min and knee/elbow detection within specific ranges, allowing the analysis of multiple peaks and complex reactions. The software will record all the peak points for use in future analyses, and the results will be displayed in a plot.

### Function 3: Randles–Ševčík Analysis

The Randles–Ševčík analysis utilizes equations that incorporate the transfer coefficient and calculate the diffusion coefficient from the peak current and scan rate. This function supports both reversible and irreversible versions of the Randles–Ševčík equation [@zanello2019inorganic]. The peak information data used in this analysis is obtained from Function 2 (Peak Searching):

$$
I_{\text{peak}} = 0.4463 \ n \ F \ C \ A \sqrt{\frac{n F \nu D}{R T}}
$$

$$
I_{\text{peak}} = 0.4463 \sqrt{n^{\prime} + \beta} \ n \ F \ C \ A \sqrt{\frac{n F \nu D}{R T}}
$$

### Function 4: Rate Constant Calculation

The rate constant is calculated using a dimensionless kinetic parameter, \(\Psi\). This parameter is a normalized value that represents the rate constant (\(k_0\)) in relation to various factors such as the diffusion coefficient and the number of electrons transferred. This method was originally proposed by Nicholson [@nicholson1965theory] and later extended by Lavagnini et al. [@lavagnini2004extended].

### Function 5: Tafel Analysis Module

Tafel analysis is used to determine the anodic and cathodic transfer coefficients. The International Union of Pure and Applied Chemistry (IUPAC) formally defines these coefficients as experimentally determined values, given by [@guidelli2014defining]:

$$
\alpha_a = \frac{RT}{F} \left( \frac{d \ln j_{a, \text{corr}}}{dE} \right)
$$

$$
\alpha_c = -\frac{RT}{F} \left( \frac{d \ln |j_{c, \text{corr}}|}{dE} \right)
$$

Additionally, the mass-transport corrected version proposed by Danlei Li et al. [@LI2018117] is implemented in this module. This method has also been applied in other research, including the study of dopamine oxidation at gold electrodes conducted by Bacil and co-workers [@zanello2019inorganic]. The transfer coefficient is calculated by:

$$
-\frac{d\ln \left( \frac{1}{I_a} - \frac{1}{I_{\text{peak}}} \right)}{d\theta} = \alpha_a'
$$

## Step Techniques Structure: CA Module

### Function 1: Plotting and Gaussian Filtering

This function generates plots of applied potential vs. time and corresponding current vs. time. Users have the option to input a sigma value to apply a Gaussian filter, which smooths the data for clearer visualization. Both the original and smoothed figures are displayed, allowing for easy comparison and analysis.

### Function 2: Cottrell Equation Plot

This function utilizes the Cottrell equation to calculate the diffusion coefficient. The Cottrell equation describes the current response of an electrochemical cell as a function of time, providing a means to determine the diffusion coefficient from chronoamperometric data. The software plots the Cottrell equation, allowing users to input parameters such as interval, \( n \), \( A \), and \( C_0 \), and calculates the diffusion coefficient. The outputs include a figure of the Cottrell equation plot and a table of diffusion coefficients.

![(a) Levich plot module](Image_Set/L_DMAB.png){ width=45% }
![(b) Levich analysis module](Image_Set/LA_D.png){ width=45% }
![(c) Peak Searching module](Image_Set/CVPS_D.png){ width=45% }
![(d) Randles–Ševčík Analysis Module](Image_Set/RC_DMAB.png){ width=45% }

![Example of figures in Envismetrics: (a) Levich plot module, (b) Levich analysis module, (c) Peak Searching module, (d) Randles–Ševčík Analysis Module.]

## Applications in Research

Envismetrics has been employed in various research projects, demonstrating its versatility in the analysis of electrochemical systems. For instance, the software was utilized in the investigation of photocatalytic degradation of perfluorooctanoic acid (PFOA), published in *Chemosphere* [@OSONGA2024143057], where it facilitated the precise analysis of kinetic parameters essential to understanding the degradation mechanisms. Additionally, Envismetrics played a key role in mechanistic studies on the electrochemical oxidation of dimethylamine borane (DMAB), as documented in recent works [@sadik2024dimethylamine,@Xue_2023,@TORABFAM2025107950]. In these studies, Envismetrics enabled the accurate processing of electrochemical data, which was crucial for validating the proposed mechanisms and deriving key kinetic parameters.

## Author Contributions (CRediT Taxonomy)

- **Huize Xue**: Conceptualization, Methodology, Software, Formal Analysis, Visualization, Data Curation, Writing – Original Draft.  
  Led the design and development of the electrochemical analysis pipeline, including Python-based processing tools and experimental method validation. Also responsible for manuscript writing and figure preparation.
- **Wenbo Wang**: Software, Writing – Review & Editing, Data Curation, Project Administration.  
  Contributed to the front-end interface, online platform development, and GitHub repository maintenance. Assisted in server deployment and manuscript refinement.
- **Xinxin Zhou**: Validation, Testing, Documentation.  
  Performed internal testing of the software and contributed to documentation and usability feedback.
- **Fuqin Zhou**: Investigation, Data Curation.  
  Supported data formatting and assisted with exploratory testing of selected modules.
- **Omowunmi Sadik**: Supervision, Project Administration, Funding Acquisition.  
  Provided scientific oversight and strategic guidance throughout the project. Contributed to the refinement of analysis direction and manuscript review.

# Technology Stack

The online platform is primarily built with Python, leveraging the Flask framework. JQuery is employed for real-time features and asynchronous tasks. More details can be found on our GitHub repo.

# Acknowledgments
The authors acknowledge the NJIT Start-ups (172803) and the Bill Melinda Gates Foundation for funding.


# Conflict of Interest
The authors confirm that we have read the JOSS conflict of interest policy, that we have no COIs related to reviewing this work, and that JOSS has waived any perceived COIs for the purpose of this review.

# Code of Conduct
The authors confirm that we read and will adhere to the JOSS code of conduct.

# References
