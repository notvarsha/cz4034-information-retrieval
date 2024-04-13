# cz4034-information-retrieval

## Crawling

- Get your Client ID, Client Secret by following this link https://docs.google.com/document/d/1wHvqQwCYdJrQg4BKlGIVDLksPN0KpOnJWniT6PbZSrI/edit
- Insert your new credentials with this client id, secret, username and password
- Run the whole jupyter notebook Reddit Crypto Webcrawling
- Results are within the zipfile

## Indexing

- Begin by downloading the Solr 8.11.3 binary release from the official Solr website (https://solr.apache.org/downloads.html).
- Once downloaded, extract the files and navigate to the extracted folder using your terminal.l
- Start Solr by running the command <code>bin/solr start</code>
- Upon successful startup, the Solr Admin page should be accessible at http://localhost:8983/solr/#/
- Refer to the Solr Documentation to create a new core named 'new_core' and upload the file 'cryptocurrency_file.csv' for indexing.
- Our API follows the standard Solr query format, for example: http://localhost:8983/solr/#/new_core/query?q=:&q.op=OR&indent=true.

## UI

- Navigate to the Indexing folder
- Ensure you have Streamlit installed by running <code>pip install streamlit</code>
- Launch the frontend using <code>streamlit run indexing_ui.py</code> in your terminal
- The results of the five sample queries are in the Indexing folder

## Classification (Preprocessing and NLTK)

- Nagivate to the Classifications followed by the preprocessing_and_NLTK folder
- Ensure that the relevant packages such as nltk, pandas, re, scikit-learn are installed by running <code>pip install nltk, pandas, re, scikit-learn</code>
- Download the pre-trained models, corpora and other resources that NLTK uses by running <code>nltk.download('all')</code> in the terminal
- Unzip the dataset.zip file and move the combined_excel_dataset into the same folder as the main.py file
- Run the python file
- If the main.py python file cannot run due to any issues, the final_results.csv file in the the dataset.zip file contains the data after running the main.py file

## Classification (Model Construction)

This section of the project focuses on constructing and evaluating machine learning models to classify sentiment based on preprocessed social media comments. Here is how to set it up and run it:

- Navigate to the `model_monstruction` directory where the model construction scripts are located.
- Ensure that Python and all required packages are installed. You can install the necessary libraries by running:

```bash
pip install pandas numpy matplotlib seaborn scikit-learn nltk transformers datasets requests unidecode wordcloud plotly
```

- Use Jupyter Notebook or an IDE installed with the extensions to run .ipynb files
- Execute the script
- The script will output the performance metrics of the trained models, such as accuracy, precision, recall, and F1-score. Additionally, it will generate confusion matrices and other plots to visualize the model's performance.
- If the script fails to run, ensure that all dependencies are correctly installed. Check the Python error logs for more specific troubleshooting.
