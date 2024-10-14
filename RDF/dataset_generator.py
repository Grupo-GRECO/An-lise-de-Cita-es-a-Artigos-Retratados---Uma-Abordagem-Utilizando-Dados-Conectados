import json
import math
import requests
from semanticscholar import SemanticScholar
sch = SemanticScholar()
import requests
from xml.sax.saxutils import escape
from xml.sax.saxutils import quoteattr
from datetime import date
from datetime import datetime
import time
s2_api_key = '' #insert your key
sch = SemanticScholar(api_key=s2_api_key)
sch = SemanticScholar(timeout=2500)


#from pprint import pprint
today = date.today()
doi_api = "https://doi.org/api/handles/"
headers = {'x-api-key': s2_api_key}

# Opening JSON retracted file
with open('retracted.json') as json_file:
    data = json.load(json_file)

    retratados = data['retratados']
    nomeArquivo = 'retracted-' + str(today) + '.rdf'
    with open(nomeArquivo,'w') as testwritefile:
      #escrevendo cabecalho do arquivo
      testwritefile.write("@base <http://example.org/> .\n")
      testwritefile.write("@prefix dc: <http://purl.org/dc/terms/>  .\n")
      testwritefile.write("@prefix rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#> . \n")
      testwritefile.write("@prefix rdfs: <http://www.w3.org/2000/01/rdf-schema#> . \n")
      testwritefile.write("@prefix foaf: <http://xmlns.com/foaf/0.1/> .\n")
      testwritefile.write("@prefix rel: <http://www.perceive.net/schemas/relationship/> .\n")
      testwritefile.write("@prefix fabio: <http://purl.org/spar/fabio/> .\n")
      testwritefile.write("@prefix cito: <http://purl.org/spar/cito/> . \n")
      testwritefile.write("@prefix c4o: <http://purl.org/spar/biro/> . \n")
      testwritefile.write("@prefix doco: <http://purl.org/spar/doco/> . \n")
      testwritefile.write("@prefix xsd: <http://www.w3.org/2001/XMLSchema#> .\n")
      testwritefile.write("@prefix doi: <http://prismstandard.org/namespaces/basic/2.0/doi#> .\n")
      testwritefile.write("@prefix prism: <http://prismstandard.org/namespaces/basic/2.0/> .  \n")
      testwritefile.write("@prefix greco: <http://www.greco.ufrj.br/> .  \n")



      j=0 #contador de Artigos nao encontrados no SEMANTIC SCHOLAR
      i=1
      #pprint(data)
      for artigos in retratados:

          artigo = artigos
          #print('doi: ' + str(artigo['doi']))

          #if i == 99:
          time.sleep(1)
          try:
            paper = sch.get_paper(artigo['doi'] + "")
          except Exception as e:
            j = j + 1
            print("Artigo DOI: " + artigo['doi'] + " nao encontrado no Semantic Scholar")
            continue

          #caso nao encontre o artigo na base, pula pra proxima iteracao
          #if not paper:
          #  j = j + 1
          #  print("Artigo DOI: " + artigo['doi'] + " nao encontrado no Semantic Scholar")
          #  continue

          if(artigo['OriginalPaperDate'] != None):
              publication_date =  artigo['OriginalPaperDate']
          else:
            article_url = doi_api + str(artigo['doi']) #obtendo data de publicacao
            r = requests.get(url = article_url)
            response = r.json()
            if "values" in response:
              publication_date = response["values"][0]["timestamp"].split('T')[0]#data de publicacao
            else:
              print("Artigo DOI: " + artigo['doi'] + " sem data de publicação")
              continue # se nao tem data de publicação, pula pro proximo

          #gravando arquivo
          testwritefile.write("<#"+str(paper['paperId'])+"> a fabio:Expression . \n")
          testwritefile.write("<#"+str(paper['paperId'])+"> a fabio:Article ; \n")
          testwritefile.write("\t doi:doi  \""+str(artigo['doi'])+"\" ; \n")
          testwritefile.write("\t fabio:hasRetractionDate   \""+str(artigo['RetractionDate'])+"\"^^xsd:date  ; \n")
          testwritefile.write("\t prism:publicationDate    \""+str(publication_date)+"\"^^xsd:date  ; \n")
          testwritefile.write("\t dc:abstract   \""+escape(str(paper['abstract'])).replace('"', '').replace('\n', '') +"\"@en-us  ; \n")
          testwritefile.write("\t dc:title   \""+escape(str(paper['title'])).replace('"', '').replace('\n', '') +"\"@en-us  ; \n")
          testwritefile.write("\t greco:hasRetractionType   \""+escape(str(artigo['kind'])) +"\"@en-us  ; \n") #substitui o fabio:Report por hasRetractionType fazendo uma extensão da ontologia
          testwritefile.write("\t rdfs:label   \""+escape(str(paper['title'])).replace('"', '').replace('\n', '') +"\"@en-us  ; \n")
          testwritefile.write("\t dc:publisher   \""+escape(str(paper['venue']).replace('"', '')) +"\"@en-us  ; \n")
          testwritefile.write("\t greco:hasProjectta \""+escape(str(artigo['Institution'])).replace('"', '').replace('\n', '') +"\"@en-us  ; \n") #cria a propriedade hasprojectta

          #mapeando o tipo de artigo, de acordo com
          #if(artigo['ArticleType'] == "Review Article"):
          #  testwritefile.write("<#"+str(paper['paperId'])+"> a fabio:ReviewPaper ; \n")
          #if(artigo['ArticleType'] == "Research Article"):
          #  testwritefile.write("<#"+str(paper['paperId'])+"> a fabio:ResearchPaper ; \n")
          #if(artigo['ArticleType'] == "Article in Press"):
          #  testwritefile.write("<#"+str(paper['paperId'])+"> a fabio:PressRelease ; \n")
          #if(artigo['ArticleType'] == "Preprint"):
          #  testwritefile.write("<#"+str(paper['paperId'])+"> a fabio:Preprint ; \n")
          #if(artigo['ArticleType'] == "Conference Abstract/Paper"):
          #  testwritefile.write("<#"+str(paper['paperId'])+"> a fabio:ConferencePaper ; \n")
          #if(artigo['ArticleType'] == "Conference Abstract/Paper"):
          #  testwritefile.write("<#"+str(paper['paperId'])+"> a fabio:Report ; \n")
          #  testwritefile.write("<#"+str(paper['paperId'])+"> a fabio:Letter ; \n")
          #if(artigo['ArticleType'] == "Letter"):
          #  testwritefile.write("<#"+str(paper['paperId'])+"> a fabio:Expression ; \n")
          #  testwritefile.write("<#"+str(paper['paperId'])+"> a fabio:Letter ; \n")
          #if(artigo['ArticleType'] == "Editorial"):
          #  testwritefile.write("<#"+str(paper['paperId'])+"> a fabio:Expression ; \n")
          #  testwritefile.write("<#"+str(paper['paperId'])+"> a fabio:Editorial ; \n")
          #if(artigo['ArticleType'] == "Revision"):
          #  testwritefile.write("<#"+str(paper['paperId'])+"> a fabio:Postprint ; \n")




          for autor in paper['authors'] :
            if autor['authorId'] != None :
              testwritefile.write("\t dc:creator   <#"+str(autor['authorId']) +">  ; \n")


          #for keyword in paper['topics']:
          #  testwritefile.write("\t prism:keywords   \""+escape(str(keyword['topic'])).replace('"', '')+"\"@en-us  ; \n")

          if (not paper['fieldsOfStudy'] is None) :
            for field in paper['fieldsOfStudy']:
              testwritefile.write("\t fabio:hasDiscipline   <#"+str((field))+">  ; \n")

          for reason in artigo['reasons']:
            testwritefile.write("\t fabio:hasRetractionMotive   \""+escape(str(reason)).replace('"', '')+"\"@en-us  ; \n")

          #for citacao in paper['citations'] :
          #  testwritefile.write("\t cito:isCitedBy   <#"+str(citacao['paperId']) +">  ; \n")


          cont = 1
          pontuacao = " ; "
          #if len (paper['references'] ) > 0 :
          #  pontuacao = " ; "

          for location in artigo['Countries']:
            cont = cont + 1
            testwritefile.write("\t dc:Location   \""+escape(str(location)).replace('"', '')+"\"@en-us  "+pontuacao+" \n")

          time.sleep(0.5)

          #referencias = sch.get_paper(str(paper['paperId']) + "/references" , fields=['contexts','paperId' ,'externalIds','intents','isInfluential','abstract','publicationDate','title','venue','authors','year'])
          #calculanndo o numero de paginas de referencias
          paginas = 0;
          if(paper['referenceCount'] > 0 and paper['referenceCount'] < 100):
              paginas = 1
          else:
            paginas = math.ceil(paper['referenceCount']/100);

          contador = 0;
          j=0
          for i in range(3):
              try:
                referencias = sch.get_paper_references(str(paper['paperId'])  , fields=['contexts','paperId' ,'externalIds','intents','isInfluential','abstract','publicationDate','title','venue','authors','year'])
                #API_URL = "https://api.semanticscholar.org/graph/v1/paper/" + str(paper['paperId']) + "/references?offset=" + str(contador) + "&limit=100&fields=contexts,externalIds,intents,isInfluential,abstract,publicationDate,title,venue,authors,year"
                #response = requests.get(API_URL,headers=headers,timeout=2000)
                #referencias = response.json()
                break
              except Exception as e:
                  print('Erro ao obter as citações do artigo. Tentando novamente...')
                  continue
                  if i == 2:
                    print('Não foi possível obter as citações do artigo após 3 tentativas.')
                    continue

          for referencia in referencias:
          #for referencia in referencias['data'] :
            doiref = referencia['citedPaper']['paperId']
            #print(referencia['contexts']);
            if referencia['isInfluential'] :
              testwritefile.write("\t cito:extends   <#"+str(doiref) +">  ; \n")
              #explicação de como verifica-se a influencia
              #https://www.semanticscholar.org/paper/Identifying-Meaningful-Citations-Valenzuela-Ha/1c7be3fc28296a97607d426f9168ad4836407e4b

            for intencao in referencia['intents'] :
              if intencao.upper() == "background".upper() :
                testwritefile.write("\t cito:obtainsBackgroundFrom   <#"+str(doiref) +">  ; \n")

              if intencao.upper() == "results".upper():
                testwritefile.write("\t cito:usesDataFrom   <#"+str(doiref) +">  ; \n")
                #    ou usesConclusionsFrom ?????????
              if intencao.upper() == "methods".upper() :
                testwritefile.write("\t cito:usesMethodIn   <#"+str(doiref) +">  ; \n")

          publicationYear = 0000
          if paper['year']  != None and  paper['year']  != 'None':
            publicationYear = paper['year']
          testwritefile.write("\t fabio:hasPublicationYear    "+str(publicationYear)+"  . \n")

          ##montando listagem de referencias
          for referencia in  referencias :
            if(referencia['citedPaper']['paperId'] == None): #validando para nao obter dados sem identificação
              continue


            #print(referencia['externalIds']['DOI'])
            if referencia['citedPaper']['externalIds'] is not None and 'DOI' in referencia['citedPaper']['externalIds']:
              teste = ''
            else:
              continue #se nao tiver DOI, não será usado

            if(referencia['citedPaper']['publicationDate'] != None):
              publication_date_reference = str(referencia['citedPaper']['publicationDate'])
             # testwritefile.write("\t prism:publicationDate    \""+str(referencia['citedPaper']['publicationDate'])+"\"^^xsd:date  ; \n")
            else:
              article_url = doi_api + str(referencia['citedPaper']['externalIds']['DOI']) #obtendo data de publicacao
              r = requests.get(url = article_url)
              response = r.json()
              if "values" in response:
                publication_date_reference = response["values"][0]["timestamp"].split('T')[0]#data de publicacao
              else:
                continue #se nao tem data deve pular par ao proximo

            testwritefile.write("<#"+str(referencia['citedPaper']['paperId'])+"> a fabio:Expression . \n")
            testwritefile.write("<#"+str(referencia['citedPaper']['paperId'])+"> a fabio:Article ; \n")
            testwritefile.write("\t doi:doi  \""+str(referencia['citedPaper']['externalIds']['DOI'])+"\" ; \n")
            testwritefile.write("\t prism:publicationDate    \""+str(publication_date_reference)+"\"^^xsd:date  ; \n")

#            if(publication_date_reference == 'vazio'):
#              continue #se não tiver data de publicação da referencia, ela será ignorada

            testwritefile.write("\t cito:isCitedBy   <#"+str(paper['paperId']) +">  ; \n")

            if(referencia['contexts'] is not None):
              for contexto in referencia['contexts'] :
                testwritefile.write("\t c4o:hasContext   \""+escape(str(contexto)).replace('"', '').replace('\n', '') +"\"@en-us  ; \n")



            testwritefile.write("\t dc:title   \""+escape(str(referencia['citedPaper']['title'])).replace('"', '').replace('\n', '') +"\"@en-us  ; \n")
            testwritefile.write("\t rdfs:label   \""+escape(str(referencia['citedPaper']['title'])).replace('"', '').replace('\n', '') +"\"@en-us  ; \n")

            testwritefile.write("\t dc:publisher   \""+escape(str(referencia['citedPaper']['venue'])) +"\"@en-us  ; \n")

            for autorReferencia in referencia['citedPaper']['authors'] : #carergando autores da referencia
              if autorReferencia['authorId'] != None :
                testwritefile.write("\t dc:creator   <#"+str(autorReferencia['authorId']) +">  ; \n")

            publicationYear = 0000
            if referencia['citedPaper']['year']  != None:
              publicationYear = referencia['citedPaper']['year']
            testwritefile.write("\t fabio:hasPublicationYear    "+str(publicationYear)+"  . \n")

          contador = contador + 100;
          #fim do for de referencias


          #criando listagem de autores das referencias
          for referencia in paper['references'] :
            for autorReferencia in referencia['authors'] :
              testwritefile.write("<#"+str((autorReferencia['authorId']))+"> a foaf:Person ; \n")
              testwritefile.write("\t foaf:name   \""+escape(str(autorReferencia['name'])) +"\"  ; \n")
              testwritefile.write("\t rdfs:label   \""+escape(str(autorReferencia['name'])) +"\"  . \n")
          ##fim inclusao de referencias

          #criando listagem de autores dos artigos retratados
          for autor in paper['authors'] :
            if autor['authorId'] != None:
              testwritefile.write("<#"+str((autor['authorId']))+"> a foaf:Person ; \n")
              testwritefile.write("\t foaf:name   \""+escape(str(autor['name'])) +"\"  ; \n")
              testwritefile.write("\t rdfs:label   \""+escape(str(autor['name'])) +"\"  . \n")


          #criando um dictionary de disciplinas
          if (not paper['fieldsOfStudy'] is None) :
            for field in paper['fieldsOfStudy']:
              testwritefile.write("<#"+str((field))+"> a fabio:SubjectDiscipline ; \n")
              testwritefile.write("\t rdfs:label   \""+escape(str(field)) +"\"@en-us  . \n")


          #obtendo dados sobre as citações do artigo
          paginas = 0;
          if(paper['citationCount'] > 0 and paper['citationCount'] < 100):
              paginas = 1
          else:
            paginas = math.ceil(paper['citationCount']/100);

          contador = 0;
          for i in range(3):

            try:
              #API_URL = "https://api.semanticscholar.org/graph/v1/paper/" + str(paper['paperId']) + "/citations?offset=" + str(contador) + "&limit=100&fields=contexts,externalIds,intents,isInfluential,abstract,publicationDate,title,venue,authors"
              #response = requests.get(API_URL,headers=headers,timeout=2000)
              #citacoes = response.json()
              citacoes = sch.get_paper_citations(str(paper['paperId'])  , fields=['contexts','paperId' ,'externalIds','intents','isInfluential','abstract','publicationDate','title','venue','authors','year'])

              break
            except Exception as e:
              print (e)
              print('Erro ao obter as citações do artigo. Tentando novamente...')
              continue

            if i == 2:
              print('Não foi possível obter as citações do artigo após 3 tentativas.')
              continue

        #citacoes = sch.get_paper(str(paper['paperId']) + "/citations" , fields=['contexts','paperId' ,'externalIds','intents','isInfluential','abstract','publicationDate','title','venue','authors','year'])

          for citacao in citacoes :

            if(citacao['citingPaper']['paperId'] == None): #validando para nao obter dados sem identificação
              continue



            if citacao['citingPaper']['externalIds'] is not None and  'DOI' in citacao['citingPaper']['externalIds']:
              teste = ''
            else:
              continue #se nao tiver doi pulo fora
            if(citacao['citingPaper']['publicationDate'] != None):
              publication_date_reference = str( citacao['citingPaper']['publicationDate'])
              #testwritefile.write("\t prism:publicationDate    \""+str( citacao['citingPaper']['publicationDate'])+"\"^^xsd:date  ; \n")
            else:
              article_url = doi_api + str(citacao['citingPaper']['externalIds']['DOI']) #obtendo data de publicacao
              r = requests.get(url = article_url)
              response = r.json()
              if "values" in response:
                publication_date_reference = response["values"][0]["timestamp"].split('T')[0]#data de publicacao
              else:
                print("citação Artigo DOI: " + artigo['doi'] + " sem data de publicação")
                continue

            testwritefile.write("<#"+str(paper['paperId'])+"> cito:isCitedBy   <#"+str(citacao['citingPaper']['paperId'])+"> . \n") #referencio a citação no artigo retratado
            testwritefile.write("<#"+str(citacao['citingPaper']['paperId'])+"> a fabio:Expression . \n")
            testwritefile.write("<#"+str(citacao['citingPaper']['paperId'])+"> a fabio:Article ; \n")
            testwritefile.write("\t doi:doi  \""+str(citacao['citingPaper']['externalIds']['DOI'])+"\" ; \n")
            testwritefile.write("\t prism:publicationDate    \""+str( publication_date_reference)+"\"^^xsd:date  ; \n")


            #if(publication_date_reference == 'vazio'):
            #  continue #se não tiver data de publicação da referencia, ela será ignorada

            testwritefile.write("\t cito:cites   <#"+str(paper['paperId']) +">  ; \n")

            if(citacao['contexts'] is not None):
              for contexto in citacao['contexts'] :
                testwritefile.write("\t c4o:hasContext   \""+escape(str(contexto)).replace('"', '').replace('\n', '') +"\"@en-us  ; \n")


            testwritefile.write("\t dc:title   \""+escape(str(citacao['citingPaper']['title'])).replace('"', '').replace('\n', '') +"\"@en-us  ; \n")
            testwritefile.write("\t dc:publisher   \""+escape(str(citacao['citingPaper']['venue'])) +"\"@en-us  ; \n")

            if citacao['isInfluential'] :
              testwritefile.write("\t cito:extends   <#"+str(paper['paperId']) +">  ; \n")
              #explicação de como verifica-se a influencia
              #https://www.semanticscholar.org/paper/Identifying-Meaningful-Citations-Valenzuela-Ha/1c7be3fc28296a97607d426f9168ad4836407e4b

            for intencao in citacao['intents'] :
              if intencao.upper() == "background".upper() :
                testwritefile.write("\t cito:obtainsBackgroundFrom   <#"+str(paper['paperId']) +">  ; \n")

              if intencao.upper() == "results".upper():
                  testwritefile.write("\t cito:usesDataFrom   <#"+str(paper['paperId']) +">  ; \n")
                  #    ou usesConclusionsFrom ?????????
              if intencao.upper() == "methods".upper() :
                  testwritefile.write("\t cito:usesMethodIn   <#"+str(paper['paperId']) +">  ; \n")

            for autorCitacao in citacao['citingPaper']['authors'] :
              if autorCitacao['authorId'] != None :
                testwritefile.write("\t dc:creator   <#"+str(autorCitacao['authorId']) +">  ; \n")

            publicationYear = 0000
            if 'year' in citacao['citingPaper']:
              publicationYear = citacao['citingPaper']['year']
            testwritefile.write("\t fabio:hasPublicationYear    "+str(publicationYear)+"  . \n")

                #criando listagem de autores das citacoes
            for autorCitacao in citacao['citingPaper']['authors'] :
                testwritefile.write("<#"+str((autorCitacao['authorId']))+"> a foaf:Person ; \n")
                testwritefile.write("\t foaf:name   \""+escape(str(autorCitacao['name'])) +"\"  ; \n")
                testwritefile.write("\t rdfs:label   \""+escape(str(autorCitacao['name'])) +"\"  . \n")

          contador = contador + 100;
                #fim do for de citações


          i = i + 1


