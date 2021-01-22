# Download Taric files

## Implementation steps

- Create and activate a virtual environment, e.g.

  `python3 -m venv venv/`
  `source venv/bin/activate`

- Install necessary Python modules 

  - autopep8==1.5.4
  - certifi==2020.11.8
  - chardet==3.0.4
  - idna==2.10
  - pycodestyle==2.6.0
  - python-dotenv==0.15.0
  - requests==2.25.0
  - toml==0.10.2
  - urllib3==1.26.2

  via `pip3 install -r requirements.txt`


## Usage

### To download Taric files:
`python3 download.py`

### To retrieve usefl information from Taric files for validation purposes:
`python3 parse.py`
