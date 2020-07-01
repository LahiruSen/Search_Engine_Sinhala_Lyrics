# -*- coding: utf-8 -*-

import boto3
import json
import requests
from requests_aws4auth import AWS4Auth

region = 'us-east-1'  # For example, us-west-1
service = 'es'
credentials = boto3.Session().get_credentials()
awsauth = AWS4Auth(credentials.access_key, credentials.secret_key, region, service, session_token=credentials.token)

host = 'search-sinhalasongs-43aa74bvse5ss2dy2fyyl4zdg4.us-east-1.es.amazonaws.com'  # For example, search-mydomain-id.us-west-1.es.amazonaws.com
index = 'songs'
url = 'https://' + host + '/' + index + '/_search'


# Lambda execution starts here

def handler(event, context):
    # Put the user query into the query DSL for more accurate search results.
    # Note that certain fields are boosted (^).
    user_query = event['queryStringParameters']['q']

    query_normal = {
        "size": 25,
        "query": {
            "multi_match": {
                "query": user_query,
                "fields": ["track_name_en^4", "track_name_si^4", "album_name_en^2", "album_name_si^2", "artist_name_en",
                           "artist_name_si", "lyrics^2"]
            }
        }
    }

    # query =query_normal
    query = select_query(user_query)

    # ES 6.x requires an explicit Content-Type header
    headers = {"Content-Type": "application/json"}

    # Make the signed HTTP request
    r = requests.get(url, auth=awsauth, headers=headers, data=json.dumps(query))

    # Create the response and add some extra content to support CORS
    response = {
        "statusCode": 200,
        "headers": {
            "Access-Control-Allow-Origin": '*'
        },
        "isBase64Encoded": False
    }

    # Add the search results to the response
    response['body'] = r.text
    return response


def my_handler(event, context):
    message = "hello lahiru"
    return {
        'message': message
    }


def select_query(user_query):
    query_normal = {
        "size": 25,
        "query": {
            "multi_match": {
                "query": user_query,
                "fields": ["track_name_en^4", "track_name_si^4", "album_name_en^2", "album_name_si^2",
                           "artist_name_en^2", "artist_name_si^2", "lyrics^2"]
            }
        }
    }

    query_ranking = {
        "size": 25,
        "query": {
            "multi_match": {
                "query": user_query,
                "fields": ["track_name_en^4", "track_name_si^4", "album_name_en^2", "album_name_si^2",
                           "artist_name_en^2", "artist_name_si^2", "lyrics^2"]
            }
        },
        "sort": [
            {"track_rating": {"order": "desc"}},
            "_score"
        ]
    }

    query_movies = {
        "size": 25,
        "query": {
            "multi_match": {
                "query": user_query,
                "fields": ["fields.title^4", "fields.plot^2", "fields.actors", "fields.directors"]
            }
        }
    }

    if (check_ranking_words(user_query)):
        return query_ranking
    else:
        return query_normal


def check_ranking_words(query):
    ranking_word_list = ['හොදම්',
     'හොදමකම',
     'හොදමට',
     'හොඳම',
     'හොදමයි',
     'හොදමුන',
     'හොදමදේ',
     'හොදමදී',
     'හොදම්ටම',
     'හොහොඳම',
     'එහලම',
     'ඉහලමට්ටමක',
     'ඉහලකුල',
     'ඉහලටම',
     'ඉහලන',
     'ඉහලකට',
     'පහලම',
     'ඉහලගිය',
     'ඉහල',
     'ඉහලටයන්න',
     'ඉහලම']
    q_list = query.split(" ")
    intersection = set(ranking_word_list) & set(q_list)

    return bool(intersection)
