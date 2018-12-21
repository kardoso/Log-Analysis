#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
# Este programa responde as seguintes perguntas :
#
# 1. Quais são os três artigos mais populares de todos os tempos?
# 2. Quem são os autores de artigos mais populares de todos os tempos?
# 3. Em quais dias mais de 1% das requisições resultaram em erros?

import psycopg2


# executar uma query
def get_query(query):
    conn = psycopg2.connect("dbname=news")
    cursor = conn.cursor()
    cursor.execute(query)
    results = cursor.fetchall()
    conn.close()
    return results


# executa as queries e retorna o documento com as respostas
def get_response():
    return 'response'


def main():
    print(get_response)


main()