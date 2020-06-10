# Predict analyses
## Preparations
### Clone the repo and create python virtual environment <br>
`git clone https://github.com/ermteri/predict_analyses.git`<br>
`cd predict_analyses`<br>
`python3 -m venv venv`<br>
`source venv/bin/activate`<br>
`pip3 install -r requirements<br>`<br>

### Merge the csv files<br>
`./src/merge_csv_files.py -c data/*/*csv > data/total.csv`<br>
## Create basic ABT
`./src/create_abt.py -c data/total.csv > data/abt.csv`<br>
## Create visualizations for top cities, consumption and smart meter usage
Note, the diagram created are stacked on top of each other
`./src/create_visualizations.py -c data/total.csv -a city -n 10`<br>
## Analyze the data
`./src/create_abt.py -f -c data/total.csv`<br>
## Remove noise
`./src/rm_noise.py -c data/total.csv >data/noise_removed.csv`<br>
## Create regression data
`./src/regression_data.py -c data/noise_removed.csv > data/regression.csv`<br>


