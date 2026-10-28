# Cybersecurity Vulnerability Severity Prediction Using Graph Machine Learning

Data science class project using CVE data from the Unified Cybersecurity Knowledge Graph (UCKG). So far, we've extracted and cleaned the data and done some exploratory analysis. Model training is the next step.

## Files

- `code/exploration.ipynb` — data exploration notebook
- `dataset/cve_clean.parquet` — cleaned sample of 909 CVEs
- `src/extract.py` — pulls CVE data from Neo4j
- `src/preprocess.py` — cleans the extracted data
- `req.txt` — Python packages needed to run the project

## Getting started

Clone the repo:

```bash
git clone https://github.com/Abdullahi023/Data-Science-Project.git
cd Data-Science-Project
```

Set up Python (macOS/Linux):

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r req.txt
```

Run the notebook:

```bash
cd code
jupyter notebook exploration.ipynb
```

Select the Python kernel and use **Run All**.

The cleaned dataset is already in `dataset/`, so you don't need Neo4j access to run the notebook. If you're using VS Code, you can also open `code/exploration.ipynb` directly and select the `.venv` kernel. Make sure the notebook runs from the `code/` folder so its dataset path works.

## Current dataset

The sample has 909 CVEs: 504 Medium, 322 High, and 83 Low. There are no Critical cases in this sample yet.