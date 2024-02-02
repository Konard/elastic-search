#!/bin/bash
python vector_search.py create
python vector_search.py index --string "dog"
python vector_search.py search --query "dog"
curl -X DELETE 'http://localhost:9200/_all'
echo ""
