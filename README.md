# ColaHeat
Project for the 2018 ColaHacks Hackathon

Display general sentiment of social media activity in the Columbia area in the form of a heat map.

# Tech Stack
- Database
  - MongoDB

- Data parser
  - Python 2.7
  - Tweepy - python client for twitter api
  - Textblob - python library for processing textual data

- Map Display
  - Expressjs
  - Javascript
  - HTML
  - Bootstrap

## Usage
- [Create a virtualenv](https://packaging.python.org/guides/installing-using-pip-and-virtualenv/)
- Install requirements: `pip install -r requirements.txt`
- Install: python -m textblob.download_corpora
- run MongoDB:
  - `sudo service mongodb start`
- import MongoDB data
  - From project root: `mongorestore DataParser/dump`
- Install dependencies and run Expressjs
  - From MapDisplay dir: `npm install` & `npm start`
- Open web browser and go to: `localhost:3000`

# Contributors
  - Tyler Moon
  - Tyler Hall
  - Lawton C Mizell
