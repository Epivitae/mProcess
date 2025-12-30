# mProcess

<a href="https://doi.org/10.5281/zenodo.18093335"><img src="https://zenodo.org/badge/1125146883.svg" alt="DOI"></a>
<a href="https://github.com/Epivitae/mProcess/releases"><img src="https://img.shields.io/github/v/release/Epivitae/mProcess?include_prereleases&style=flat-square&color=blue" alt="GitHub release"></a>
<a href="https://github.com/Epivitae/mProcess/blob/main/LICENSE"><img src="https://img.shields.io/github/license/Epivitae/mProcess?style=flat-square&color=green" alt="License"></a>
<img src="https://img.shields.io/badge/python-3.8%2B-blue?style=flat-square&logo=python&logoColor=white" alt="Python Version">
<a href="http://www.cns.ac.cn"><img src="https://img.shields.io/badge/Homepage-www.cns.ac.cn-005BAC?style=flat-square" alt="Homepage"></a>
<img src="https://img.shields.io/github/repo-size/Epivitae/mProcess?style=flat-square&color=orange" alt="Repo Size">
<a href="https://github.com/Epivitae/mProcess"><img src="https://hits.seeyoufarm.com/api/count/incr/badge.svg?url=https%3A%2F%2Fgithub.com%2FEpivitae%2FmProcess&count_bg=%2379C83D&title_bg=%23555555&icon=&icon_color=%23E7E7E7&title=hits&edge_flat=true"/></a>

---

**mProcess** is a specialized Python toolkit designed for the high-throughput analysis of microplate reader data. It provides an automated workflow for processing both single-channel intensity data and dual-channel ratiometric biosensor data.

## Interface Preview
<p align="center">
  <img src="assets/screenshot.png" alt="mProcess GUI Interface" width="600">
</p>

## Key Features

### 🟢 Single Channel Mode
- Processes standard intensity-based kinetics data.
- Automatically calculates dynamic range (DR) and area under the curve (AU).
- Generates heatmaps for rapid hit identification.

### 🔵 Dual Channel Mode (Ratio)
- Designed for ratiometric sensors (e.g., 485nm/420nm).
- Automated ratio calculation and background correction.
- Extracts kinetics parameters (T1-T6) and generates ratio heatmaps.

## Installation

1. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
2. Run the GUI:
   ```bash
   python app.py
   ```

## Advanced Usage (Notebook)
For developers or advanced users who prefer Jupyter Notebooks:

<a href="https://colab.research.google.com/github/Epivitae/mProcess/blob/main/notebooks/pre-process.ipynb">
  <img src="https://colab.research.google.com/assets/colab-badge.svg" alt="Open In Colab"/>
</a>

## Citation
If you use mProcess in your research, please cite it as follows:

### Text format:
   Wang, Kui. (2025). mProcess: Automated Processing Tool for Microplate Reader Data (v4.1.0). Zenodo. https://doi.org/10.5281/zenodo.18093335

### BibTeX format:
```bash
{@software{mProcess_2025,
  author       = {Wang, Kui},
  title        = {mProcess: Automated Processing Tool for Microplate Reader Data},
  month        = dec,
  year         = 2025,
  publisher    = {Zenodo},
  version      = {v4.1.0},
  doi          = {10.5281/zenodo.18093335},
  url          = {[https://doi.org/10.5281/zenodo.18093335](https://doi.org/10.5281/zenodo.18093335)}
}
```