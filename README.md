# cz4034-information-retrieval

## Crawling

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