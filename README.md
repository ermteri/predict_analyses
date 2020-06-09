# Predict analyses
## Visualization tool
### Preparations
* clone the repo 
* create python virtual environment
* pip3 install -r requirements
* merge the csv files
./src/merge_csv.py -c data/*/*.csv > data/total.csv
### Present top cities consumption and smart meter usage
* ./src/create_visualizations.py -c data/total.csv -a city
### Present low tariff usage related to different providerss
* ./src/create_visualizations.py -c data/total.csv -a provider



