from SPARQLWrapper import SPARQLWrapper, JSON, XML
sparql = []
results = []
#SELECT 
sparql.append ( SPARQLWrapper(
    "http://vocabs.ardc.edu.au/repository/api/sparql/"
    "csiro_international-chronostratigraphic-chart_geologic-time-scale-2020"
))

# gets the first 3 geological ages
# from a Geological Timescale database,
# via a SPARQL endpoint
sparql[0].setQuery("""
    PREFIX gts: <http://resource.geosciml.org/ontology/timescale/gts#>

    SELECT *
    WHERE {
        ?a a gts:Age .
    }
    ORDER BY ?a
    LIMIT 3
    """
)

#ASK 
sparql.append( SPARQLWrapper("http://dbpedia.org/sparql"))
sparql[1].setQuery("""
    ASK WHERE {
        <http://dbpedia.org/resource/Asturias> rdfs:label "Asturias"@es
    }
""")

#CONSTRUCT 
sparql.append(SPARQLWrapper("http://dbpedia.org/sparql")) 

sparql[2].setQuery("""
    PREFIX dbo: <http://dbpedia.org/ontology/>
    PREFIX sdo: <https://schema.org/>

    CONSTRUCT {
      ?lang a sdo:Language ;
      sdo:alternateName ?iso6391Code .
    }
    WHERE {
      ?lang a dbo:Language ;
      dbo:iso6391Code ?iso6391Code .
      FILTER (STRLEN(?iso6391Code)=2) # to filter out non-valid values
    }
    LIMIT 3
""")

#DESCRIBE 
sparql.append(SPARQLWrapper("http://dbpedia.org/sparql")) 
sparql[3].setQuery("DESCRIBE <http://dbpedia.org/resource/Asturias> LIMIT 3")




sparql[0].setReturnFormat(JSON)
sparql[1].setReturnFormat(JSON)
results.append(sparql[0].queryAndConvert()) 
results.append(sparql[1].query().convert()) 
results.append(sparql[2].queryAndConvert())
results.append(sparql[3].queryAndConvert()) 


try:
    
    print("SELECT example", "\n".join(map(str, results[0]["results"]["bindings"])))
    print("ASK example: ", results[1]['boolean'])
    print("CONSTRUCT example: ", results[2].serialize())
    print("DESCRIBE  example: ", results[3].serialize(format="json-ld").split(",")[:3])
except Exception as e:
    print(e)


