FROM continuumio/miniconda3

WORKDIR ./ivp24

RUN git clone --single-branch --branch main https://gitlab.developers.cam.ac.uk/phy/data-intensive-science-mphil/c1_assessment/ivp24.git

RUN apt-get update && apt-get install -y \
    git

RUN conda env update --file environment.yml --name base

RUN pre-commit install
