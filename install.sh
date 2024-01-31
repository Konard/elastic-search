#!/bin/bash
docker run -d -p 9200:9200 -p 9300:9300 -e "discovery.type=single-node" docker.elastic.co/elasticsearch/elasticsearch:7.13.1
pyenv install 3.11
pyenv global 3.11
pip install click 'elasticsearch<7.14.0' tensorflow tensorflow_text tensorflow_hub