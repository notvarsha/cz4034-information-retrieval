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

## Classification
- Nagivate to the Classifications followed by the preprocessing_and_NLTK folder
- Ensure that the relevant packages such as nltk, pandas, re, scikit-learn are installed by running <code>pip install nltk, pandas, re, scikit-learn</code>
- Download the pre-trained models, corpora and other resources that NLTK uses by running <code>nltk.download('all')</code> in the terminal
- Unzip the dataset.zip file and move the combined_excel_dataset into the same folder as the main.py file
- Run the python file
- If the main() python file cannot run due to any issues, the final_results.csv file in the the dataset.zip file contains the data after running the main.py file
