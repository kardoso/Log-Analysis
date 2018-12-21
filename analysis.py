#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
# Este programa responde as seguintes perguntas :
#
# 1. Quais são os três artigos mais populares de todos os tempos?
# 2. Quem são os autores de artigos mais populares de todos os tempos?
# 3. Em quais dias mais de 1% das requisições resultaram em erros?

import psycopg2


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
    return 'response'


def main():
    print(get_response)


main()