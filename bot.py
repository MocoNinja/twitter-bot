#!/usr/bin/python
# -*- coding: utf-8 -*-

from time import sleep
from pymongo import MongoClient

import tweepy
import json
import os

auth = None
api = None


class EscuchadorDeFlujos(tweepy.StreamListener):

    def on_connect(self):
        print("Conexion con la API de streaming correcta :)")

    def on_error(self, status_code):
        print("Ha habido un error con codigo: {}".format(repr(status_code)))
        return False

    def on_data(self, data):
        try:
            HOST = os.environ['HOST_MONGODB']
            client = MongoClient(HOST)
            db = client.twitterdb
            print("He leido un bocadito de datos...")
            datos = json.loads(data)
            datos_str = repr(datos).encode('utf-8')
            fecha_creacion = datos['created_at']
            print("Data dump:\n\t{}\n=============\n".format(datos_str))
            db.twitter_search.insert(datos)
        except Exception as e:
            print("Se ha pinyado con la excepcion: {}".format(e))


def cargar_credenciales():
    global api
    global auth

    CONSUMER_KEY = os.environ['CONSUMER_KEY']
    CONSUMER_SECRET = os.environ['CONSUMER_SECRET']
    ACCESS_TOKEN = os.environ['ACCESS_TOKEN']
    ACCESS_SECRET = os.environ['ACCESS_SECRET']

    auth = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
    auth.set_access_token(ACCESS_TOKEN, ACCESS_SECRET)
    api = tweepy.API(auth)


def preparar_flujo():
    global auth
    global api

    WORDS = [i for i in os.environ['SEARCH_TERMS'].split(" ")]

    msg = "Procesando las siguientes palabras:"

    for WORD in WORDS:
        msg += "\n\t{}".format(WORD)
    print(msg)

    print("Empezando a escuchar el flujillo...")

    listener = EscuchadorDeFlujos(api=tweepy.API(wait_on_rate_limit=True))
    streamer = tweepy.Stream(auth=auth, listener=listener)
    lista_palabras = u''
    for WORD in WORDS:
        lista_palabras += "{},".format(WORD.encode('ascii', 'ignore'))

    print(lista_palabras)
    streamer.filter(track=lista_palabras)

    print("Acabe...")


def hola_twitter_write():
    global auth
    global api

    for i in range(5):
        print("Voy a decir una gilipollez...")
        api.update_status("Por vez #{}: soy un frigging robot...".format(i))
        print("He dicho mi gilipollez...")
        sleep(10)


def hola_twitter_read():
    global auth
    global api

    public_tweets = api.home_timeline()
    for tweet in public_tweets:
        value = tweet.text  # .encode('utf-8')
        print(str(value))


if __name__ == "__main__":
    cargar_credenciales()
    preparar_flujo()
