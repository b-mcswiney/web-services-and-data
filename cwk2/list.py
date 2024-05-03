
def list_pages(terms: list, index: dict, urls: list):
    documents = []
    print("Terms: ", end="")

    for term in terms:
        print(term + ", ", end="")
        term_docs = []

        if term not in index:
            print("\n", term, " NOT FOUND")
            return "fail"

        for doc in index[term]:
            term_docs.append(doc)
        documents.append(term_docs)

    print("\n-----------------------------------------------")
    print("Found in documents: ")
    same_docs = get_same(documents)
    for doc in same_docs:
        print(urls[doc - 1])

    return "not implemented"


def get_same(term_docs: list):
    same_docs = term_docs[0]
    to_remove = []

    for docs in same_docs:
        for terms in term_docs:
            if docs not in terms:
                to_remove.append(docs)

    for docs in to_remove:
        same_docs.remove(docs)

    return same_docs
