# Gerador de Dataset .ttl

Script Python com o código usado para gerar o dataset utilizado na dissertação de mestrado do aluno Hugo Duca

## Sobre os dados

Os artigos retratados sobre COVID-19 foram obtidos em  ***11/07/2024*** e as informações sobre as citações a esses atigos foram obtidas em ***21/07/2024***.

### Linguagem

> [Python 3.6](https://www.python.org/downloads/release/python-360/)

### Sources

* [Retraction Watch Database](https://retractionwatch.com/)
* [Semantic Scholar API](https://api.semanticscholar.org/)
* [DOI API](https://www.doi.org/factsheets/DOIProxy.html#rest-api)

### Dados de cada fonte

* **Retraction Watch Database**: Busca por todos artigos retratados com o filtro de título usando os termos “COVID-19” or “coronavirus disease 2019” or “coronavirus 2019” or “SARS- COV-2” or “2019-nCov”. Os artigos que não tinham informações sobre DOI foram descartados.
* **Semantic Scholar API**: Usado para obter as informações sobre os artigos obtidos no retraction Watch, bem como obter os dados dos artigos que fizeram citação aos retratados.
* **DOI API**: Usado para obter a data de publicação dos artigos, quando essa data não estava disponível nas fontes anteriores.

### Ontologias usadas na geração do dataset

* [FaBio](https://sparontologies.github.io/fabio/current/fabio.html#d4e5532)
* [CiTo](https://sparontologies.github.io/cito/current/cito.html#d4e1176)
* [c4o](https://sparontologies.github.io/c4o/current/c4o.html)

## Pastas no Repositório

* [**GRAPHML**](GRAPHML): Contém os dados da primeira análise, feita com técnicas de ARS
    * **dataset_generator.py**: Python script to create dataset
    * **rede-finalv2.gephi**: Gephi project with created graph
    * **rede-finalv2.graphml**: Graph generated by python script
    * **img folder**: Folder with images generated by Gephi using the created graph

* [**RDF**](RDF): Contem os arquivos e dados do segundo experimento, feito com técnicas de Dados Conectados
    * **dataset_generator.py**: Python script to create dataset
    * **retracted-2021-07-25.ttl**: Turtle file generated by python script
    * **retracted.json**: Artigos retratados extraídos do Retraction Watch


## Arquivos do repositório

  * **dataset_generator.py**: Script Python com o código usado para gerar o dataset
  * **retracted-2021-07-25.ttl**: Arquivo Turtle gerado pelo script
  * **retracted.json**: Artigos retratados extraídos do Retraction Watch

## Contato
hugo.duca@ppgi.ufrj.br ou hugoduca@gmail.com
