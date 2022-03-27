from http.client import HTTPResponse
from urllib import response
from django.shortcuts import render
from django.http import JsonResponse, HttpResponse
from django.core import serializers
import json
from pymongo import MongoClient
from rest_framework.decorators import api_view
from rest_framework.parsers import JSONParser
from rest_framework.decorators import parser_classes

client = MongoClient(
    'mongodb+srv://testSait:test123Q@cluster0.obuew.mongodb.net/myFirstDatabase?retryWrites=true&w=majority')
db = client.catalog
Catalog = db["Catalog"]
Category = db["Category"]


def CursorIntoList(res, deleteParams = []):
    tmp = []
    for doc in res:
        doc["_id"] = str(doc['_id'])
        if len(deleteParams) > 0:
            for param in deleteParams:
                if(param in doc):
                    del doc[param]
        
        tmp.append(doc)
    return tmp
def buildQuerySearch(search):
    tmp = []
    for word in search:
        tmpWord = "("
        for letter in word:
            tmpWord += f'[{letter}{letter.upper()}]'+'{1}'
        tmpWord += ")"
        tmp.append(tmpWord)
    return tmp

@api_view(['POST'])
@parser_classes((JSONParser,))
def getAllProduct(request):
    body = json.loads(request.body.decode('utf-8'))

    skip = 0
    query = {}
    if("search" in body):
        query.update({"title": { "$regex": "|".join(buildQuerySearch(body['search'].split(" "))) }})
    if("category" in body):
        query.update({"category": { "$regex": "|".join([f'({word})' for word in body['category']]) }})
    if("skip" in body):
        skip = body["body"]
    if("sortedBy" in body):
        pass
    print(query)
    return JsonResponse(CursorIntoList(Catalog.find(query, limit=30, skip=skip), ["category"]), safe=False)


@api_view(['POST'])
def getCategory(request):
    return JsonResponse(CursorIntoList(Category.find({}), ["_id"]), safe=False)
