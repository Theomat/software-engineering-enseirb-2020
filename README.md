![main tests status](https://github.com/Theomat/software-engineering-enseirb-2020/workflows/Tests/badge.svg)

# Projet Ingiénérie Logicielle 2020


This repository is our work on the subject given [here](https://www.evernote.com/shard/s613/client/snv?noteGuid=79b20255-3a87-0f60-8c3b-2a97c4f84f44&noteKey=475d45236bb0671c2dc5da94049d7f7c&sn=https%3A%2F%2Fwww.evernote.com%2Fshard%2Fs613%2Fsh%2F79b20255-3a87-0f60-8c3b-2a97c4f84f44%2F475d45236bb0671c2dc5da94049d7f7c&title=Projet%2Bing%25C3%25A9nierie%2Blogicielle%2Bpour%2Bl%2527IA).


### Authors

With equals contributions:
  - Otavio Flores Jacobi
  - Dylan Hertay
  - Théo Matricon
  - Julien Mazué


### Commands

#### Base project

- Pull the docker image :

  ```sudo docker pull wiidiiremi/projet_industrialisation_ia_3a```
- Run the docker image on port 8080 :

  ```sudo docker run -p 8080:8080 wiidiiremi/projet_industrialisation_ia_3a```

#### Install Spacy dependencies for French text processing

- Install Spacy (with conda, recommended for development):

  ```conda install -c conda-forge spacy```

- Install Spacy french modules :

  ```python -m spacy download fr_core_news_sm```


#### Run our web api locally (with Docker):


- In order to run the application locally first build the image. To do so, run in the root of of the project:

  ```docker build -t engsw-project:1.0 .```

- Then, run the container and application will start on the port you define (in the example, port 8000):

  ```docker run -d -p 8000:80 engsw-project:1.0```

  ___note: it may take a few seconds for service to start up___


#### Run performance tests locally:
- Be sure to have [locust](https://locust.io/) load test tool installed

- In the `scripts` folder run the `./perf_test.sh` script and the performance tool will launch on `localhost:8089`

  ___note: the current model report can be found in the `reports` folder___


### Running on docker

This project is available on docker hub at [https://hub.docker.com/repository/docker/otaviojacobi/eng-soft-2020](https://hub.docker.com/repository/docker/otaviojacobi/eng-soft-2020)
