# Social Media Comment Analysis

This repository contains three Jupyter notebooks that perform various text analysis tasks on social media comments, including sentiment analysis, sarcasm detection, and applying machine learning models for classification.

## Notebooks

### 1. `machine_learning.ipynb`

This notebook performs sentiment analysis on social media comments using pandas, scikit-learn, NLTK, and other libraries to preprocess, analyze, and visualize the data. It includes:

- Data loading and preprocessing
- Sentiment analysis and visualization using word clouds
- Machine learning model training using SVM and RandomForest classifiers
- Performance evaluation using metrics like accuracy, precision, recall, F1 score, and ROC-AUC.

### 2. `roberta_model.ipynb`

Leverages the power of a pre-trained RoBERTa model from the `transformers` library to perform sentiment classification. Steps include:

- Data loading and preprocessing
- Tokenization and dataset preparation for the transformer model
- Model training and evaluation using custom metrics
- Results visualization using a confusion matrix.

### 3. `Sarcasm detection.ipynb`

Focuses on detecting sarcasm in social media comments. It includes:

- Data cleaning and preprocessing
- Sarcasm detection using an external API
- Visualization of sarcasm scores
- Advanced text processing and machine learning classification combining text features with sarcasm scores.

## Setup

To run these notebooks, you will need Python 3.x and the following packages:

- pandas
- numpy
- matplotlib
- seaborn
- scikit-learn
- nltk
- transformers
- datasets
- requests
- unidecode
- wordcloud
- plotly

You can install these packages via pip:

```bash
pip install pandas numpy matplotlib seaborn scikit-learn nltk transformers datasets requests unidecode wordcloud plotly
```

Additionally, make sure to have Jupyter Notebook or JupyterLab installed:

```bash
pip install notebook
```

Running the Notebooks
To open the notebooks, navigate to the cloned or downloaded repository directory and run:

```bash
jupyter notebook
```

Select the desired notebook in the interface to open and run it.
