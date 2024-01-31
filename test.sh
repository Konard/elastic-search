#!/bin/bash
python vector_search.py create
python vector_search.py index --str "dog"
python vector_search.py search --search "dog"
curl -X DELETE 'http://localhost:9200/_all'