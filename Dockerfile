FROM continuumio/miniconda3

WORKDIR ./ivp24

COPY . .

RUN dir -s

RUN apt-get update && apt-get install -y \
    git

RUN conda env update --file environment.yml --name base

# If this line runs correctly,
# then environment activation has likely been completed correctly
RUN python ./test/test_docker.py

RUN pre-commit install

EXPOSE 8888
