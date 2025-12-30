# mProcess

<a href="https://doi.org/10.5281/zenodo.18093335"><img src="https://zenodo.org/badge/1125146883.svg" alt="DOI"></a>

**mProcess** is a specialized Python toolkit designed for the high-throughput analysis of microplate reader data. It provides an automated workflow for processing both single-channel intensity data and dual-channel ratiometric biosensor data.

## Key Features

### 🟢 Single Channel Mode
- Processes standard intensity-based kinetics data.
- Automatically calculates dynamic range (DR) and area under the curve (AU).
- Generates heatmaps for rapid hit identification.

### 🔵 Dual Channel Mode (Ratio)
- Designed for ratiometric sensors (e.g., 485nm/420nm).
- Automated ratio calculation and background correction.
- Extracts kinetics parameters (T1-T6) and generates ratio heatmaps.

### 🌍 Bi-lingual Support
- One-click switching between **English** and **Chinese** interfaces suitable for international lab environments.

## Installation

1. Install dependencies:
   ```bash
   pip install -r requirements.txt