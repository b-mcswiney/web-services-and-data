import heapq # for priority queue
import numpy as np


def list_pages(terms: list, index: dict, urls: dict):
    # Check that all searched items are in index
    # if not in index, remove it
    for term in terms:
        if term not in index:
            terms.remove(term)
            print("Term not found in index:", term, "removed from search")    

    conjunctive_list = sort_conjunctive(terms, index, get_conjunctive(terms, index))

    print("--------------------------------------------------\nConjunctive list of documents (contains all search terms )\n--------------------------------------------------")
    if len(conjunctive_list) == 0:
        print("No documents found")
    else:
        for doc in conjunctive_list:
            print(urls[str(doc)])

    disjunctive_list = get_disjunctive(terms, index, conjunctive_list)

    print("--------------------------------------------------\nDisjunctive list of documents (contains some search terms not including conjunctive documents)\n--------------------------------------------------")
    if len(disjunctive_list) == 0:
        print("No documents found")
    else:
        for doc in disjunctive_list:
            print(urls[str(doc[1])])


def get_conjunctive(terms: list, index: dict):
    conjunctive_list = {}
    terms_docs = []

    for term in terms:
        term_data = []
        for doc in index[term]:
            term_data.append(doc["doc-id"])
        terms_docs.append(term_data)

    conjunctive_list = set(terms_docs[0]).intersection(*terms_docs)

    return conjunctive_list

def sort_conjunctive(terms: list, index: dict, conjunctive_list: list):
    sorted_conjunctive = {}
    positions_per_doc = {}

    for term in terms:
        for doc in conjunctive_list:
            if doc not in positions_per_doc:
                for item in index[term]:
                    if item["doc-id"] == doc:
                        positions_per_doc[doc] = item["locations"]
            else:
                for item in index[term]:
                    if item["doc-id"] == doc:
                        for location in item["locations"]:
                            positions_per_doc[doc].append(location)

    for doc in positions_per_doc:
        positions_per_doc[doc].sort()
        
        average_diff = np.diff(positions_per_doc[doc])
        
        score = np.average(average_diff)

        sorted_conjunctive[doc] = score

    return dict(sorted(sorted_conjunctive.items(), key=lambda item: item[1]))

def get_disjunctive(terms: list, index: dict, conjunctive_list: list):

    disjunctive_list = {}
    indexed_terms = []
    ratings = []

    for term in terms:
        if term in index:
            indexed_terms.append(index[term])
    
    for i in range(len(indexed_terms)):
        for doc in indexed_terms[i]:
            if doc["doc-id"] not in disjunctive_list and doc["doc-id"] not in conjunctive_list:
                disjunctive_list[doc["doc-id"]] = 0
            if doc["doc-id"] in disjunctive_list and not doc["doc-id"] in conjunctive_list:
                disjunctive_list[doc["doc-id"]] += 1

    for doc in disjunctive_list:
        heapq.heappush(ratings, (disjunctive_list[doc], doc))

    ratings.sort(reverse=True)

    return ratings