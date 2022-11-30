# %%
import requests
import string

# %%
url = "https://raw.githubusercontent.com/PlanQK/semantic-services/master/extracted%20knowledge/"

# %%
mapping = {'Framework for Quantum Computing': 'Implementation:Quantum_Implementation',
'SDK for Quantum Computing': 'Implementation:Software_Development_Kit',
'Library for Quantum Computing': "Implementation:Library",
"Artificial Intelligence Problem": "ProblemExecution:ArtificialIntelligenceProblem",
"Machine Learning Problem" : "ProblemExecution:MachineLearningProblem",
"Mathematical Problem" : "ProblemExecution:MathematicalProblem",
"Search" : "ProblemExecution:SearchProblem",
"Sorting" : "ProblemExecution:SortingProblem"}

# %%
def triples_applicationareas(url):
    '''Application area hierarchy triples from PlanQK catalogue'''
    
    triples = []
    response_area = requests.get(url + "ApplicationAreas.json")
    data = response_area.json()
    comment = data["_comment"].replace("'", "")
    areas = data['result']["children"]
    prefix = "quantumshare:"

    for j in areas: #iterate through the 3 areas
        superclass = prefix + j['label'].translate(str.maketrans('','',string.punctuation)).replace(' ', '_')
        triples.extend([{"s": superclass, "p":"rdfs:subClassOf", "o": "ProblemExecution:Application_Area"},
                        {"s": superclass, "p":"rdfs:comment", "o": comment}])
        
        if len(j['children']) > 0: #check for subclasses
            childs = j['children']
            for h in childs:
                child = prefix + h["label"].translate(str.maketrans('','',string.punctuation)).replace(' ', '_')
                triples.extend([{"s": child, "p":"rdfs:subClassOf", "o": superclass},
                                {"s":child, "p":"rdfs:comment", "o": comment}])

                if 'children' in h and len(h['children']) > 0: #check for subclasses
                    childs2 = h['children']
                    for k in childs2:
                        child2 = prefix + k['label'].translate(str.maketrans('','',string.punctuation)).replace(' ', '_')
                        triples.extend([{"s": child2, "p":"rdfs:subClassOf", "o": child},
                                        {"s":child2, "p":"rdfs:comment", "o": comment}])
                        
                        if 'children' in k and len(k['children']) > 0: #check for subclasses
                            childs3 = k['children']
                            for l in childs3:
                                child3 = prefix + l['label'].translate(str.maketrans('','',string.punctuation)).replace(' ', '_')
                                triples.extend([{"s": child3, "p":"rdfs:subClassOf", "o": child2},
                                                {"s":child3, "p":"rdfs:comment", "o": comment}])
                                
                                if 'children' in l and len(l['children']) > 0: #check for subclasses
                                    childs4 = l['children']
                                    for r in childs4:
                                        child4 = prefix + r['label'].translate(str.maketrans('','',string.punctuation)).replace(' ', '_')
                                        triples.extend([{"s": child4, "p":"rdfs:subClassOf", "o": child3},
                                                        {"s":child4, "p":"rdfs:comment", "o": comment}])
                                        
                                        if 'children' in r and len(r['children']) > 0: #check for subclasses
                                            childs5 = r['children']
                                            for s in childs5:
                                                child5 = prefix + s['label'].translate(str.maketrans('','',string.punctuation)).replace(' ', '_')
                                                triples.extend([{"s": child5, "p":"rdfs:subClassOf", "o": child4},
                                                                {"s":child5, "p":"rdfs:comment", "o": comment}])

                                                if 'children' in s and len(s['children']) > 0: #check for subclasses
                                                    childs6 = r['children']
                                                    for t in childs6:
                                                        child6 = prefix+t['label'].translate(str.maketrans('','',string.punctuation)).replace(' ', '_')
                                                        triples.extend([{"s": child6, "p":"rdfs:subClassOf", "o": child5},
                                                                        {"s":child6, "p":"rdfs:comment", "o": comment}])
    
    return triples

# %%
def triples_software(url):
    '''Obtaines triples concerning software from PlanQK catalogue (implementation frameworks, SDKs, and libraries'''
    
    triples = []
    response_software = requests.get(url + 'SoftwareTool_Hierarchy.json')
    data = response_software.json()
    softwares = data['result']["children"]
    prefix = "quantumshare:"
    
    for j in softwares:
        childs = j['children']
        
        if j['label'] == 'SDK':
            for i in childs:
                if i['label'] == "SDK for Quantum Computing":
                    for k in i['children']:
                        superclass = mapping[i['label']]
                        classname = prefix + k['label'].translate(str.maketrans('','',string.punctuation)).replace(' ', '_')
                        triples.extend([{"s": classname, "p":"rdfs:subClassOf", "o": superclass}])
                    
        if j['label'] == 'Framework':
            for i in childs:
                if i['label'] == 'Framework for Quantum Computing':
                    for k in i['children']:
                        superclass = mapping[i['label']]
                        classname = prefix + k['label'].translate(str.maketrans('','',string.punctuation)).replace(' ', '_')
                        triples.extend([{"s": classname, "p":"rdfs:subClassOf", "o": superclass}])
        
        if j['label'] == 'Library':
            for i in childs:
                if i['label'] == 'Library for Quantum Computing':
                    for k in i['children']:
                        superclass = mapping[i['label']]
                        classname = prefix + k['label'].translate(str.maketrans('','',string.punctuation)).replace(' ', '_')
                        triples.extend([{"s": classname, "p":"rdfs:subClassOf", "o": superclass}])
        
    return triples

# %%
def triples_problems(url):
    '''Problem types hierarchy triples from PlanQK catalogue'''
    
    triples = []
    response_problems = requests.get(url + "ProblemTypes.json")
    data = response_problems.json()
    comment = data["_comment"].replace("'", "")
    problems = data['result']["children"]
    prefix= "quantumshare:"

    for j in problems: 
        superclass = mapping[j['label']]
        
        if len(j['children']) > 0:
            childs = j['children']
            for h in childs:
                child = prefix+h["label"].translate(str.maketrans('','',string.punctuation)).replace(' ', '_')
                triples.extend([{"s": child, "p":"rdfs:subClassOf", "o": superclass},
                                {"s":child, "p":"rdfs:comment", "o": comment}])
            
                if 'children' in h and len(h['children']) > 0:
                    childs2 = h['children']
                    for k in childs2:
                        child2 = prefix+k['label'].translate(str.maketrans('','',string.punctuation)).replace(' ', '_')
                        triples.extend([{"s": child2, "p":"rdfs:subClassOf", "o": child},
                                        {"s":child2, "p":"rdfs:comment", "o": comment}])
                        
                        if 'children' in k and len(k['children']) > 0:
                            childs3 = k['children']
                            for l in childs3:
                                child3 = prefix+l['label'].translate(str.maketrans('','',string.punctuation)).replace(' ', '_')
                                triples.extend([{"s": child3, "p":"rdfs:subClassOf", "o": child2},
                                                {"s":child3, "p":"rdfs:comment", "o": comment}])
                                
                                if 'children' in l and len(l['children']) > 0:
                                    childs4 = l['children']
                                    for r in childs4:
                                        child4 = prefix+r['label'].translate(str.maketrans('','',string.punctuation)).replace(' ', '_')
                                        triples.extend([{"s": child4, "p":"rdfs:subClassOf", "o": child3},
                                                        {"s":child4, "p":"rdfs:comment", "o": comment}])
                                        
                                        if 'children' in r and len(r['children']) > 0:
                                            childs5 = r['children']
                                            for s in childs5:
                                                child5 = prefix+s['label'].translate(str.maketrans('','',string.punctuation)).replace(' ', '_')
                                                triples.extend([{"s": child5, "p":"rdfs:subClassOf", "o": child4},
                                                                {"s":child5, "p":"rdfs:comment", "o": comment}])
                    
    return triples               


