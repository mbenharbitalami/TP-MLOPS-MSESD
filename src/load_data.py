import argparse

import numpy as np
import pandas as pd
import yaml
import requests
from bs4 import BeautifulSoup
import zipfile
from sklearn import preprocessing


def read_params(config_path):
    """
    read parameters from the params.yaml file
    input: params.yaml location
    output: parameters as dictionary
    """
    with open(config_path) as yaml_file:
        config = yaml.safe_load(yaml_file)
    return config

def webscrapping(baseurl):
    # Creating a new file to store the zip file links
    newfile = open('zipfiles.txt','w')
    
    #Set variable for page to be opened and url to be concatenated 
    page = requests.get('https://archive.ics.uci.edu/ml/machine-learning-databases/00212/')
    
    #Use BeautifulSoup to clean up the page
    soup = BeautifulSoup(page.content,features="lxml")
    soup.prettify()
    
    #Find all the links on the page that end in .zip and write them into the text file
    for anchor in soup.findAll('a', href=True):
        links = anchor['href']
        if links.endswith('.zip'):
            newfile.write(links + '\n')
    newfile.close()

    #Fetching the links for the zip file and downloading the files
    with open('zipfiles.txt', 'r') as links:
        for link in links:
            if link:
                filename1= link.split('/')[-1]
                filename= filename1[:-1]
                link = baseurl + link
                response = requests.get(link[:-1])

                # Writing the zip file into local file system
                with open(filename,'wb') as output_file:
                    output_file.write(response.content)
                    
    with zipfile.ZipFile(filename,"r") as zip_ref:
        zip_ref.extractall("data")
    

def load_data(model_var,config_path):
    config = read_params(config_path)
    url = config["raw_data_config"]["baseurl"]
    file = config["raw_data_config"]["file"]
    webscrapping(url)
    df = pd.read_csv(file,delimiter=' ', header=None)
    df.columns =['pelvic_incidence', 'pelvic_tilt', 'lumbar_lordosis_angle', 'sacral_slope', 'pelvic_radius', 'grade_of_spondylolisthesis', 'target']
    # label_encoder object knows how to understand word labels.
    label_encoder = preprocessing.LabelEncoder()
  
    # Encode labels in column 'species'.
    df['target'] = label_encoder.fit_transform(df['target'])
  
    df['target'].unique()
    
    df = df[model_var]
    return df

def load_raw_data(config_path):
    """
    load data from external location(data/external) to the raw folder(data/raw) with train and teting dataset
    input: config_path
    output: save train file in data/raw folder
    """
    config = read_params(config_path)
    raw_data_path = config["raw_data_config"]["raw_data_csv"]
    model_var = config["raw_data_config"]["model_var"]

    df = load_data(model_var,config_path)
    df.to_csv(raw_data_path, index=False)


if __name__ == "__main__":
    args = argparse.ArgumentParser()
    args.add_argument("--config", default="params.yaml")
    parsed_args = args.parse_args()
    load_raw_data(config_path=parsed_args.config)
