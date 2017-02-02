# bioschemas-validator-cli
Command line client to validate Bioschemas Data items in a specific URL.


## Installation
```{r, engine='bash', count_lines}
git clone https://github.com/ficolo/bioschemas-validator-cli.git
cd bioschemas-validator-cli
virtualenv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

##Usage
```{r, engine='bash', count_lines}
python bioschemas_validate.py https://tess.elixir-europe.org/events/introduction-to-high-throughput-screening-2-ects
```
