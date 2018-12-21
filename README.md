# Análise de Logs
Este programa análisa um banco de dados e responde as seguintes perguntas:
1. Quais são os três artigos mais populares de todos os tempos?
2. Quem são os autores de artigos mais populares de todos os tempos?
3. Em quais dias mais de 1% das requisições resultaram em erros?

O resultado pode ser exibido no terminal e gerar um arquivo txt com o mesmo conteúdo ou ser executado por uma aplicação web e ser acessado através no navegador web.


## Requerimentos
[Python3](https://www.python.org/downloads/)

[Virtual Box](https://www.virtualbox.org/wiki/Downloads)

[Vagrant](https://www.vagrantup.com) ou o arquivo com a máquina configurada [aqui](https://d17h27t6h515a5.cloudfront.net/topher/2017/June/5948287e_fsnd-virtual-machine/fsnd-virtual-machine.zip)

[Dados](https://d17h27t6h515a5.cloudfront.net/topher/2016/August/57b5f748_newsdata/newsdata.zip) - O arquivo sql para ser analisado

[PostgreSQL](https://www.postgresql.org/) (É automáticamente iniciado dentro da máquina virtual, não é preciso instalar)

[Flask](http://flask.pocoo.org/) (Caso queira exibir o resultado em um browser através de um servidor local. Também já está dentro da máquina configurada, não é preciso instalar)

E um **terminal**.


## Prepare o ambiente
Inicie a máquina virtual no diretório da pasta vagrant com `vagrant up` (Isso pode demorar um pouco se for a primeira vez).

Faça o login na máquina usando o comando `vagrant ssh`

Os arquivos `analysis.py` e `newsdala.sql` devem estar na pasta compartilhada(a pasta vagrant).

Já logado na máquina virtual acesse a pasta com o comando `cd /vagrant`.

Será preciso criar algumas views para o programa rodar sem interrupções.

Use o comando `psql -d news -f newsdata.sql` para abrir a linha de comando, criar o banco de dados **_news_** e executar as declarações SQL do arquivo **_newsdata.sql_**.

Abra a linha de comando PostgreSQL novamente utilizando o comando `psql news`

Crie uma _view_ chamada _mostpopular_ com o seguinte comando:
```sql
CREATE VIEW mostpopular AS
  SELECT 
    articles.author, 
    articles.title, 
    COUNT(*) as views
  FROM articles 
  JOIN log 
  ON log.path LIKE concat('%', articles.slug) 
  GROUP BY
    articles.title,
    articles.author 
  ORDER BY views DESC;
```

Crie outra view, agora chamada requests com o seguinte comando:
```sql
CREATE VIEW requests AS
  SELECT 
    date(time) AS day,
    COUNT(*) AS quantity,
    status
  FROM log 
  GROUP BY
    day,
    status;
```

Saia da linha de comando com o atalho `Ctrl + d`

## Execute o programa
Agora você pode finalmente executar o programa!
Com o comando `python analysis.py` o programa é excutado mostrando o resultado no terminal e gerando um arquivo no formato txt no mesmo diretório em que o programa foi executado.

Opcionalmente você pode usar o argumento _web_ para executar o programa como web app e acessá-lo a partir de um localhost.
O comando com argumento é `python analysis.py web`
