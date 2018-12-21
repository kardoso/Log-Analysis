#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
# Este programa responde as seguintes perguntas :
#
# 1. Quais são os três artigos mais populares de todos os tempos?
# 2. Quem são os autores de artigos mais populares de todos os tempos?
# 3. Em quais dias mais de 1% das requisições resultaram em erros?

import psycopg2

import sys
arg = ''

# Argumentos para executar em web app ou não
try:
    arg = sys.argv[1]
except IndexError:
    arg = ''

response = ''
POP_ARTICLES = ''
POP_AUTHORS = ''
ERRONEOUS_DAY = ''

response = '''
1. Quais são os três artigos mais populares de todos os tempos?
%s

2. Quem são os autores de artigos mais populares de todos os tempos?
%s

3. Em quais dias mais de 1%% das requisições resultaram em erros?
%s
'''

POP_ARTICLES = '''
    %s — %s views
'''

POP_AUTHORS = '''
    %s — %s views
'''

ERRONEOUS_DAY = '''
    %s — %s%%
'''

# queries usadas
# 1. Quais são os três artigos mais populares de todos os tempos?
q1 = '''SELECT title, views FROM mostpopular LIMIT 3;'''
# 2. Quem são os autores de artigos mais populares de todos os tempos?
q2 = '''SELECT authors.name, SUM(mostpopular.views)
        FROM articles, mostpopular, authors
        WHERE mostpopular.title = articles.title AND authors.id=articles.author
        GROUP BY authors.name ORDER BY sum DESC;'''
# 3. Em quais dias mais de 1% das requisições resultaram em erros?
q3 = '''SELECT fails.day, ROUND((fails.quantity*100)/sums.quantity, 2)
        FROM (SELECT day, quantity FROM requests
            WHERE status like '404%' GROUP BY day, quantity) fails
        INNER JOIN (SELECT day, sum(quantity) AS quantity
                    FROM requests GROUP BY day) sums
        ON (fails.quantity > sums.quantity*0.01 AND fails.day = sums.day);'''


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
    resp1 = (
        "".join(POP_ARTICLES % (article, views)
                for article, views in get_query(q1))
    )
    resp2 = (
        "".join(POP_AUTHORS % (author, views)
                for author, views in get_query(q2))
    )
    resp3 = (
        "".join(ERRONEOUS_DAY % (day, errors)
                for day, errors in get_query(q3))
    )
    final_response = response % (resp1, resp2, resp3)
    return final_response


def main():
    r = get_response()
    print(r)
    text_file = open("output.txt", "w")
    text_file.write(r)
    text_file.close()


main()