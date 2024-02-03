import click
import json
from elasticsearch import Elasticsearch

@click.group()
def cli():
    pass

@click.command()
@click.option('--string', 'string', prompt=True)
def index(string):
    """Index a string in Elasticsearch."""
    es = Elasticsearch(['http://localhost:9200'])
    body = {'text': string}
    res = es.index(index='text_index', body=body)
    click.echo(f"Indexed {string} with id {res['_id']}")

@click.command()
@click.option('--query', 'query', prompt=True)
def search(query):
    """Search for a string in Elasticsearch."""
    es = Elasticsearch(['localhost:9200'])
    body = {
        "query": {
            "bool": {
                "must": {
                    "match_all": { 'boost': 0 }
                },
                "should": [
                    { 
                        "match": { 
                            "text": query
                        }
                    },
                    {
                        "match": {
                            "content": {
                                "query": query,
                                "operator": "and"
                            }
                        }
                    },
                    {
                        "match_phrase": {
                            "content": {
                                "query": query
                            }
                        }
                    }
                ],
            }
        },
    }

    
    res = es.search(index='text_index', body=body)
    click.echo("Search results:")
    # click.echo(json.dumps(res, indent=2))
    for doc in res['hits']['hits']:
        click.echo(f"'{doc['_id']}' {doc['_score']}: {doc['_source']['text']}")

cli.add_command(index)
cli.add_command(search)

if __name__ == "__main__":
    cli()