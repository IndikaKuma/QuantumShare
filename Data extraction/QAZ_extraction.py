# %%
import requests
import string

# %%
url = "https://raw.githubusercontent.com/MIBbrandon/stephenjordan.github.io/master/src/storage/"

# %%
mapping = {
    "category":"QuantumAlgorithm:Algorithm_Class",
    "speedup": "QuantumAlgorithm:Speedup_Class",
    "description": "QuantumAlgorithm:Algorithm_Description",
    "name": "QuantumAlgorithm:Quantum_Algorithm"}

# %%
def triples_algorithms(url):
    '''Generates triples from QuantumAlgorithmZoo algorithms'''
    
    triples = []
    response_algo = requests.get(url + "algorithms.json")
    data_algos = response_algo.json()
    data_algo_ref = response_algo.json()
    prefix = "quantumshare:"
    punctuation = string.punctuation.replace('.', '') + '“”'

    ref_algorithms = {} #Maintain a library with identifiers of publications related to corresponding algorithms
    for i in data_algo_ref:
        for j in data_algo_ref[i]:
            ref_algorithms[data_algo_ref[i][j]['name']] = data_algo_ref[i][j]['references']

    for i in data_algos: #Maintain data about solely algorithm-related context
        for j in data_algos[i]:
            del data_algos[i][j]["alg_id"]
            del data_algos[i][j]["references"]
    categories = data_algos

    for i in categories: 
        for j in categories[i]: 
            algo = categories[i][j]
            
            for info in algo:
                classname = prefix + algo[info].translate(str.maketrans('','',punctuation)).replace(' ', '_') if type(algo[info]) == str else algo[info]
                label = algo[info]
                superclass = mapping[info]
                
                if info == "name":
                    category = prefix+algo['category'].translate(str.maketrans('','',punctuation)).replace(' ', '_')
                    triples.extend([{"s": classname, "p":"rdfs:subClassOf", "o": superclass},
                                        {"s":classname, "p":"rdfs:label", "o": label},
                                        {"s": classname, "p":"dul:isPartOf", "o": category}])
                    if "speedup" in algo:
                        speed = prefix+algo['speedup'].translate(str.maketrans('','',punctuation)).replace(' ', '_') if 'speedup' in algo else prefix+'unknown'
                        triples.extend([{"s": classname, "p":"dul:isPartOf", "o": speed}])

                    if label in ref_algorithms: #add corresponding publications to algorithm
                        for reference in ref_algorithms[label]:
                            triples.extend([{"s": prefix+str(reference), "p":"dul:isAbout", "o": classname}])

                if info == "category" or info == "speedup":
                    triples.extend([{"s": classname, "p":"rdfs:subClassOf", "o": superclass},
                                        {"s":classname, "p":"rdfs:label", "o": label}])
    
                if info == "description":
                    description = classname.replace('_', ' ')[14:] 
                    naam = prefix+algo['name'].translate(str.maketrans('','',punctuation)).replace(' ', '_')
                    triples.extend([{"s": naam, "p":"rdfs:comment", "o": description}])
    return triples

# %%
def triples_publications(url):
    '''Generates triples about publications from QuantumAlgorithmZoo'''
    
    triples = []
    response_ref = requests.get(url + "references.json")
    refs_data = response_ref.json()
    prefix = "quantumshare:"
    punctuation = string.punctuation
    punctuation2 = '!"#$%&\'()*+-/<>?@[\\]^`{|}~' 
    
    for i in refs_data:
        del (refs_data[i]['ref_id']) 
    references = refs_data 
    
    for i in references:
        for meta in references[i]:
            classname = prefix + meta #e.g. "quantumshare:author"
            value = references[i][meta] #e.g. "Daniel S. Abrams and Seth Lloyd"

            if 'links' in classname: #multiple links are often stored as value to this key
                for j in value:
                    identifier = str(value[j]).translate(str.maketrans('','',punctuation)).replace(' ', '_')
                    triples.extend([{"s": classname+identifier, "p": "rdfs:subClassOf", "o": "Publication:Metadata"},
                                    {"s": prefix+str(i), "p": "dul:hasParameter", "o": classname+identifier},
                                    {"s": classname+identifier, "p": "dul:hasParameterDataValue", "o": value[j]}])

            else:
                value = str(value).translate(str.maketrans('','',punctuation2))
                identifier = value.translate(str.maketrans('','',punctuation)).replace(' ', '_')
                triples.extend([{"s": prefix+str(i), "p": "rdfs:subClassOf", "o": "Publication:Publication"},
                                {"s": prefix+str(i), "p": "dul:hasParameter", "o": classname+identifier},
                                {"s": classname+identifier, "p": "rdfs:subClassOf", "o": "Publication:Metadata"},
                                {"s": classname+identifier, "p": "dul:hasParameterDataValue", "o": value}])
    return triples


