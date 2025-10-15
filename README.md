# Genus2Genes

## Motivation

This repository hosts the source code and example data for the tool Genus2Genes, developed to automate the retrieval of gene information from the biomedical literature based on microbial genera.
The motivation behind this work is to facilitate the systematic exploration of microbe–gene associations by integrating publicly available resources through programmatic access. Specifically, Genus2Genes queries the EBI/NCBI Taxonomy API to expand each input genus into its corresponding species and then interrogates the PubTator database to identify scientific articles (PMIDs) where those taxa are mentioned. From the resulting corpus, the tool extracts gene symbols and identifiers, producing structured tables that can be easily incorporated into downstream functional or network analyses.

This project aims to enable large-scale, reproducible text mining in microbiome-related research, supporting the identification of microbial taxa linked to particular genes or biological processes described in the literature.

## Code availability

This repository contains the Python code required to perform:

- automated taxonomy expansion via the EBI/NCBI API,

- retrieval of relevant PubMed articles using the PubTator API,

- extraction and tabulation of gene annotations, and

- example notebooks demonstrating basic data handling and visualization steps.

The code is distributed under the GNU General Public License v3.0 (GPLv3) to promote transparency and reproducibility in scientific research.

## Installation

Clone the repository and install the required dependencies:

git clone https://github.com/<your-user>/Genus2Genes.git
cd Genus2Genes
pip install -r requirements.txt

All dependencies will be automatically installed.

## Data availability

The repository includes example input data (input_lista_genus.txt) containing microbial genera (e.g., Eubacterium, Rickettsiella, Lautropia) and a demonstration notebook (pubtator.ipynb) illustrating the full data retrieval and processing pipeline.
All queries rely on publicly accessible APIs from EBI and PubTator, and the resulting output tables can be freely shared or extended. No sensitive or proprietary data are included in this repository.

## Credits

This code was created by Fernando Lucas-Ruiz, Biomedical Research Institute of Murcia, Spain.
For correspondence, please contact fernando.lucas@um.es

## How to cite

If you use this software, please cite:
Lucas-Ruiz, F. (2025). Genus2Genes (v1.0.0) [Software]. Zenodo. https://doi.org/10.5281/zenodo.1234568]
