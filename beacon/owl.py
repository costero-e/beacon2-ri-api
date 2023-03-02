#This version simply retrieves all classes for a given ancestor from an .owl ontology provided locally, creating a .txt dictionary 

import owlready2

#input to provide

#wanted_classes_and_new_labels = {'Abnormal Cell' : 'Cell', 'Tissue Culture' : 'ResearchTechnique' , 'Cellular Process': 'AssociatedBiologicalProcess'}
#new_dictionary = 'name.txt'


# load ontology
from owlready2 import *


#lists
ontology = '/Users/oriol/Desktop/ncit.owl'
onto = get_ontology(ontology).load()
namespace = onto.get_namespace(ontology)
class_list = list(onto.classes())
label_list = []
ancestor_list = []
relevant_terms = []

#get all classes (if needed)
'''
for c in class_list:
    label_list.append(c.label)
'''

#get all classes from wanted ancestors
for c in class_list:
    ancestors = list(c.ancestors())
    print(ancestors)
'''
    for a in ancestors:
        x = str(a.label)
        for term, label in wanted_classes_and_new_labels.items():
            if term == x[2:-2] and c not in relevant_terms:
                relevant_terms.append(c)
                with open(new_dictionary, 'a') as n:
                    n.write(c.label[0] + '\t' + 'LABEL=' + label + '\t' + 'ID=' + str(c) + '\n')
'''

'''
#add synonyms and their preferred label
for c in relevant_terms:
    ancestors = list(c.ancestors())
    for a in ancestors:
        x = str(a.label)
        for term, label in new_labels.items():
            if term == x[2:-2]:
                try:
                    s = list(onto.search_one(label=c.label).hasExactSynonym)
                    print(s)
                    for term in s:
                        with open(new_dictionary, 'a') as n:
                            n.write(term + '\t' + 'LABEL=' + label + '\t' + 'ID=' + str(c) + '\t' + 'PrefSynonym=' + c.label[0] + '\n')
                except:
                    print('no synonym')
                    continue
'''
