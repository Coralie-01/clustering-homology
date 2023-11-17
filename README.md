## projet-bin702

Author: Coralie Serrand
Description: This is a clustering model that detect homologuous genomes



## Initialisation du projet
------------


### Docker

1. Installer docker

verifier que docker est installé
```bash
chmod +x ./checkDocker.sh
./checkDocker.sh
```
Si ce n'est pas le cas, installer docker grace au commandes suivante
```bash
sudo apt-get update
sudo apt-get install -y ca-certificates curl gnupg
sudo install -m 0755 -d /etc/apt/keyrings
curl -fsSL https://download.docker.com/linux/ubuntu/gpg | sudo gpg --dearmor -o /etc/apt/keyrings/docker.gpg
sudo chmod a+r /etc/apt/keyrings/docker.gpg
echo \
    "deb [arch=$(dpkg --print-architecture) signed-by=/etc/apt/keyrings/docker.gpg] https://download.docker.com/linux/ubuntu \
    $(. /etc/os-release && echo "$VERSION_CODENAME") stable" | \
    sudo tee /etc/apt/sources.list.d/docker.list > /dev/null    
sudo apt-get update
sudo apt-get install -y docker-ce docker-ce-cli containerd.io docker-buildx-plugin docker-compose-plugin
```
2. Lancer le container

```bash
chmod +x ./buildandrunDocker.sh
./buildandrunDocker.sh
```

### Virtualenv

0. Installer python 11.6

```bash
sudo apt-get install python3.11
```

1. Installer virtualenv

```bash
sudo apt install python3.11-venv
```

2. Créer un environnement virtuel

```bash
python3.11 -m venv env
```

3. Activer l'environnement virtuel

```bash
source env/bin/activate
```

4. Installer les dépendances

```bash
pip install -e .
```

## Launch the model
```bash
python main.py
```



## Project Organization 
------------

(generated with [datasciencemvp](https://github.com/cliffclive/datasciencemvp/))

(modified from [cookiecutter-datascience](https://drivendata.github.io/cookiecutter-data-science/))

```
    ├── LICENSE
    ├── README.md          <- The top-level README for developers using this project.
    ├── data
    │   ├── external       <- Data from third party sources.
    │   ├── interim        <- Intermediate data that has been transformed.
    │   ├── processed      <- The final, canonical data sets for modeling.
    │   └── raw            <- The original, immutable data dump.
    │
    ├── models             <- Trained and serialized models, model predictions, or model summaries
    │
    ├── notebooks          <- Jupyter notebooks. Naming convention is a number (for ordering),
    │                         the creator's initials, and a short `-` delimited description, e.g.
    │                         `1.0-jqp-initial-data-exploration`.
    │
    ├── references         <- Data dictionaries, manuals, and all other explanatory materials.
    │
    ├── reports            <- Generated analysis as HTML, PDF, LaTeX, etc.
    │   └── figures        <- Generated graphics and figures to be used in reporting
    │
    ├── src                <- Source code for use in this project.
    │   ├── __init__.py    <- Makes src a Python module
    │   │
    │   ├── data           <- Scripts to download or generate data
    │   │   └── make_dataset.py
    │   │
    │   ├── features       <- Scripts to turn raw data into features for modeling
    │   │   └── build_features.py
    │   │
    │   ├── models         <- Scripts to train models and then use trained models to make
    │   │   │                 predictions
    │   │   ├── predict_model.py
    │   │   └── train_model.py
    │   │
    │   └── visualization  <- Scripts to create exploratory and results oriented visualizations
    │       └── visualize.py
```


