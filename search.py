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
        # 'query': {
        #     'match': {
        #         'text': query
        #     }
        # }
        # 'query': {
        #     'match': {
        #         'text': {
        #         'query': query,
        #         "operator": "and",
        #         "zero_terms_query": "all",
        #            "fuzziness": "AUTO",
        #         #    "zero_terms_query": "all",
        #         } 
                
        #     },
        # }

        # "query": {
        #     "bool": {
        #         "must": {
        #             "match_all": {}
        #         },
        #         "should": [
        #             { "match": { "text": query }, },
        #             # { "match": { "name.last": { "query": "banon", "_name": "last" } } }
        #         ],
        #     }
        # },

        'query': {
            'function_score': {
                "query": {
                    "bool": {
                        "must": {
                            "match_all": { 'boost': 0 }
                        },
                        "should": [
                            { "match": { "text": query }, },
                            # { "match": { "name.last": { "query": "banon", "_name": "last" } } }
                        ],
                    }
                },
                'functions': [
                    # {
                    #     # 'filter': { 'match_all': {} },
                    #     # 'random_score': {}, 
                    #     'weight': 1
                    # },
                    # {
                    #     'function_score': {
                    #         'query': {
                    #             'match': {
                    #                 'text': query
                    #             }
                    #         },
                    #         'weight': 2
                    #     }
                    # }
                    # {
                    #     'function_score': {
                    #         'query': {
                    #             'match': {
                    #                 'text': query
                    #             }
                    #         },
                    #         'weight': 2
                    #     }
                    # }

                    {
                        # 'filter': { 'match': { 'text': query } },
                        'script_score': {
                            # 'query': {'match_all': {}},
                            'script': {
                                'source': "_score",
                            }
                        },
                        'weight': 2
                    },
                    
                    # {
                    #     'filter': { 'match': { 'text': query } },
                    #     'weight': 2
                    # }
                ],
            }
        }

        # 'query': {
        #     'function_score': {
        #         # 'query': { 'match_all': {} },
        #         'query': {
        #             'match': {
        #                 'text': {
        #                    'query': query,
        #                    "operator": "and",
        #                    "zero_terms_query": "all"
        #                 #    "fuzziness": "AUTO",
        #                 #    "zero_terms_query": "all",
        #                 } 
                        
        #             },
        #             # "zero_terms_query": "all",
        #         },
        #         # 'boost': '5', 
        #         # 'functions': [
        #         #     {
        #         #         'filter': { 'match_all': {} },
        #         #         'random_score': {}, 
        #         #         'weight': 1
        #         #     },
        #         #     # {
        #         #     #     'function_score': {
        #         #     #         'query': {
        #         #     #             'match': {
        #         #     #                 'text': query
        #         #     #             }
        #         #     #         },
        #         #     #         'weight': 2
        #         #     #     }
        #         #     # }
        #         #     # {
        #         #     #     'function_score': {
        #         #     #         'query': {
        #         #     #             'match': {
        #         #     #                 'text': query
        #         #     #             }
        #         #     #         },
        #         #     #         'weight': 2
        #         #     #     }
        #         #     # }

        #         #     # {
        #         #     #     'filter': { 'match': { 'text': query } },
        #         #     #     'script_score': {
        #         #     #         # 'query': {'match_all': {}},
        #         #     #         'script': {
        #         #     #             'source': "_score",
        #         #     #         }
        #         #     #     },
        #         #     #     'weight': 1
        #         #     # },
                    
        #         #     # {
        #         #     #     'filter': { 'match': { 'text': query } },
        #         #     #     'weight': 2
        #         #     # }
        #         # ],
        #         # 'max_boost': 42,
        #         # 'score_mode': 'max',
        #         # 'boost_mode': 'multiply',
        #         # 'min_score': 42
        #     }
        # } 
    }

    
    res = es.search(index='text_index', body=body)
    click.echo("Search results:")
    click.echo(json.dumps(res, indent=2))
    for doc in res['hits']['hits']:
        click.echo(f"{doc['_source']['text']}")

cli.add_command(index)
cli.add_command(search)

if __name__ == "__main__":
    cli()