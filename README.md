# Mining Multidomain Cellulases Across Fungi

Comparative genome-mining project focused on discovering secreted fungal CAZymes and multidomain cellulase architectures associated with lignocellulose degradation.

---

# Project Goals

Industrial biomass conversion relies heavily on fungal carbohydrate-active enzymes (CAZymes), particularly secreted cellulases and oxidative accessory enzymes involved in plant cell wall deconstruction.

While many industrial enzymes have already been characterized, genome mining across diverse fungal species remains a powerful strategy for discovering:

- novel cellulases
- unusual multidomain architectures
- improved thermostability
- enhanced substrate binding
- synergistic catalytic combinations
- potentially patentable enzyme candidates

This project aims to build a reproducible comparative fungal secretome-mining pipeline capable of:

1. collecting fungal reference proteomes automatically from UniProt
2. predicting secreted proteins using SignalP 6
3. annotating CAZyme domains using HMMER + dbCAN
4. reconstructing multidomain enzyme architectures
5. identifying rare or industrially interesting cellulase combinations across fungi

The workflow combines classical bioinformatics tools with large-scale comparative analysis and focuses on biologically interpretable results rather than black-box predictions.

---

# Biological Background

Filamentous fungi are among the most efficient degraders of lignocellulosic biomass in nature. Species such as *Trichoderma*, *Aspergillus*, *Penicillium*, and thermophilic fungi secrete large extracellular enzyme repertoires specialized for decomposition of cellulose, hemicellulose, and lignin-rich substrates.

Particularly important enzyme classes include:

- Glycoside Hydrolases (GH)
- Auxiliary Activities (AA)
- Carbohydrate Binding Modules (CBM)
- Polysaccharide Lyases (PL)
- Carbohydrate Esterases (CE)

Many industrially valuable enzymes contain multidomain architectures such as:

- catalytic GH + CBM combinations
- oxidative AA modules
- tandem substrate-binding domains

These architectures may improve:
- substrate accessibility
- catalytic efficiency
- processivity
- thermostability
- enzyme synergy on insoluble biomass

---

# Species Selection

The dataset includes 30 fungal species selected based on:

- known cellulolytic capability
- industrial enzyme production
- ecological diversity
- thermophilic adaptation
- representation of major filamentous fungal groups

The collection includes:

- *Trichoderma*
- *Aspergillus*
- *Penicillium*
- *Fusarium*
- *Neurospora*
- *Pleurotus*
- thermophilic fungi such as:
  - *Chaetomium thermophilum*
  - *Thermothelomyces thermophilus*
  - *Thielavia terrestris*

Both mesophilic and thermophilic fungi were included to increase the likelihood of identifying unusual enzyme architectures and potentially thermostable candidates.

---

# Workflow Overview

## 1. Automatic Proteome Retrieval

Reference fungal proteomes were automatically retrieved from UniProt using the REST API.

Selection logic:
- prioritize reference proteomes
- filter out viral entries
- prefer proteomes with realistic fungal protein counts
- fallback taxonomy-based retrieval when reference proteomes were unavailable

The download pipeline automatically generated:
- FASTA proteomes
- metadata report tables
- reproducible species annotations

---

## 2. Secretome Prediction with SignalP 6

Secreted proteins were predicted using a two-stage workflow:

### Fast Screening
SignalP 6 Fast model was first applied to complete fungal proteomes.

### Slow Validation
Proteins predicted as secreted by the Fast model were re-analyzed using the more computationally expensive `slow-sequential` model.

This approach is meant to:
- dramatically reduced runtime
- preserved high sensitivity
- removed low-confidence predictions

The workflow was benchmarked against full `slow-sequential` SignalP 6 predictions using the *Trichoderma reesei* proteome.

Comparison between Fast and Slow models showed:
- ~0.7% disagreement at the full proteome level
- ~9% disagreement within secretome-related predictions (including both Fast-only and Slow-only classifications)

To balance computational efficiency and prediction confidence, a two-stage Fast → Slow validation workflow was implemented:

1. Fast model screening on complete proteomes
2. Slow-sequential validation of Fast-positive secreted proteins

For *T. reesei*, this approach removed ~3.6% of Fast-predicted secreted proteins, which falls within the expected disagreement range between models.

Across all 30 fungal species:
- average Fast → Slow retention was ~96.5%
- only ~3.5% of Fast-positive proteins were rejected during Slow validation

This demonstrated that:
- SignalP Fast performs extremely well for fungal secretome screening
- Slow validation primarily removes marginal predictions
- the hybrid workflow preserves biological realism while dramatically reducing runtime

Performance benchmarking showed:
- Fast mode is ~6× faster than Slow-sequential
- full Slow-sequential analysis of 30 genomes would require approximately one week of continuous runtime on a typical desktop workstation
- the Fast → Slow strategy reduced total runtime by approximately 4.3× while preserving high-confidence predictions

---

# Secretome Statistics

Across species:

- fungal proteomes ranged from ~6,400 to ~15,500 proteins
- predicted secretomes typically represented:
  - ~5–10% of total proteomes
- Fast → Slow retention rates were extremely high:
  - ~95–98%

This demonstrated that:
- SignalP Fast performs remarkably well for fungal secretome screening
- Slow validation primarily removes marginal predictions
- the two-stage workflow is computationally efficient and biologically robust

---

# Example Secretome Retention

| Species | Proteins | Fast Secretome | Slow Secretome | Retention |
|---|---:|---:|---:|---:|
| *Trichoderma reesei* | 9115 | 666 | 642 | 96.4% |
| *Aspergillus niger* | 14069 | 955 | 913 | 95.6% |
| *Fusarium graminearum* | 14147 | 1298 | 1259 | 97.0% |
| *Pleurotus ostreatus* | 11624 | 1110 | 1084 | 97.7% |

---

## Secretome Fraction Across Fungal Species

The proportion of predicted secreted proteins varied substantially across fungal species, ranging from ~4% to ~10% of total proteomes.

Notable differences were observed between fungal groups:
- *Podospora anserina* and *Pleurotus ostreatus* showed the largest predicted secretomes
- *Rhizopus oryzae* exhibited a comparatively small secretome fraction

These differences likely reflect ecological specialization and distinct strategies of extracellular biomass degradation.

![Secretome fraction across species](results/figures/secretome_fraction_across_species.png)

---

# CAZyme Annotation

Validated secretomes were annotated using:

- HMMER3
- dbCAN HMM database (v14)

The workflow identifies:
- CAZyme families
- catalytic domains
- carbohydrate-binding modules
- multidomain architectures

Additional filtering stages were implemented to:
- remove overlapping domain artifacts
- merge fragmented domain predictions
- reconstruct biologically realistic architectures

---

# Current Status

Completed:
- automated fungal proteome retrieval
- large-scale secretome prediction
- validated SignalP workflow
- dbCAN annotation across 30 fungal secretomes

In progress:
- multidomain architecture reconstruction
- comparative CAZyme analysis
- identification of unusual cellulase combinations
- cross-species enrichment analysis
- candidate enzyme prioritization

---

# Planned Analyses

Upcoming analyses include:

- CAZyme class composition across fungi
- multidomain cellulase architectures
- GH + CBM combinations
- thermophile-specific enzyme repertoires
- comparative enrichment analysis
- candidate prioritization for biomass degradation applications

---

# Tools Used

- Python
- Pandas
- Biopython
- SignalP 6
- HMMER3
- dbCAN v14
- UniProt REST API
- Jupyter Notebook
- WSL / Ubuntu

---

# Repository Structure

```text
data/
  proteomes/

results/
  signalp_fast/
  signalp_fast_slow/
  dbcan_hits/

tools/
  signalp6_fast/
  signalp6_slow_sequential/
  dbcan/

scripts/
```
---

# References

SignalP 6:
Teufel et al., 2022
https://www.nature.com/articles/s41587-021-01156-3

dbCAN:

- dbCAN-HMMdb-V14.txt
https://pro.unl.edu/dbCAN2/browse_download.php

- Zhang et al., 2023
https://academic.oup.com/nar/article/51/D1/D1347/6775304
