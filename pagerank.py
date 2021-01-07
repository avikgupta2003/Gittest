import os
import random
import re
import sys
import copy


DAMPING = 0.85
SAMPLES = 10000


def main():
    #if len(sys.argv) != 2:
        #sys.exit("Usage: python pagerank.py corpus")
    #corpus = crawl(sys.argv[1])
    corpus = crawl("corpus0")
    ranks = sample_pagerank(corpus, DAMPING, SAMPLES)
    print(f"PageRank Results from Sampling (n = {SAMPLES})")
    for page in sorted(ranks):
        print(f"  {page}: {ranks[page]:.4f}")
    ranks = iterate_pagerank(corpus, DAMPING) # RG need to check, this is where issue is
    print(f"PageRank Results from Iteration")
    for page in sorted(ranks):
        print(f"  {page}: {ranks[page]:.4f}")


def crawl(directory):
    """
    Parse a directory of HTML pages and check for links to other pages.
    Return a dictionary where each key is a page, and values are
    a list of all other pages in the corpus that are linked to by the page.
    """
    pages = dict()

    # Extract all links from HTML files
    for filename in os.listdir(directory):
        if not filename.endswith(".html"):
            continue
        with open(os.path.join(directory, filename)) as f:
            contents = f.read()
            links = re.findall(r"<a\s+(?:[^>]*?)href=\"([^\"]*)\"", contents)
            pages[filename] = set(links) - {filename}

    # Only include links to other pages in the corpus
    for filename in pages:
        pages[filename] = set(
            link for link in pages[filename]
            if link in pages
        )

    return pages


def transition_model(corpus, page, damping_factor):
    """
    Return a probability distribution over which page to visit next,
    given a current page.

    With probability `damping_factor`, choose a link at random
    linked to by `page`. With probability `1 - damping_factor`, choose
    a link at random chosen from all pages in the corpus.
    """
    probability_distribution = {}
    no_of_links = len(corpus[page]) # RG corrected code here

    if no_of_links != 0:
        list_of_keys = [page]
        for element in corpus[page]: #RG corrected code here
            list_of_keys.append(element)
        
        initial_probability = damping_factor * 1/no_of_links
        added_probability = (1-damping_factor)/len(corpus.keys())
        list_of_values = [added_probability]
        for x in range(no_of_links):
            list_of_values.append(initial_probability+added_probability)
        
        for pages in list_of_keys:
            for probability in list_of_values:
                probability_distribution[pages] = probability 
        
        return probability_distribution
    
    elif no_of_links == 0:
        no_of_links = len(corpus.keys())
        probability = 1/no_of_links
        for pages in corpus.keys():
            probability_distribution[pages] = probability
        
        return probability_distribution



def sample_pagerank(corpus, damping_factor, n):
    """
    Return PageRank values for each page by sampling `n` pages
    according to transition model, starting with a page at random.

    Return a dictionary where keys are page names, and values are
    their estimated PageRank value (a value between 0 and 1). All
    PageRank values should sum to 1.
    """
    PageRank_dict = {}
    new_page = random.choice(list(corpus.keys())) #RG - Dic keys can't be indexed, so convert them to list
    
    samples = [new_page]
    
    for x in range(n-1):
        probs = transition_model(corpus, new_page, damping_factor)
        new_page = random.choice(random.choices(list(probs.keys()), weights=(probs.values()), k=1)) # RG to check if you want 1 page OR multiple pages.
        samples.append(new_page)

    for page in corpus.keys():
        PageRank_dict[page] = samples.count(page)/n

    return PageRank_dict


def iterate_pagerank(corpus, damping_factor):
    """
    Return PageRank values for each page by iteratively updating
    PageRank values until convergence.

    Return a dictionary where keys are page names, and values are
    their estimated PageRank value (a value between 0 and 1). All
    PageRank values should sum to 1.
    """
    copied_corpus = copy.deepcopy(corpus)
    list_of_keys = list(copied_corpus.keys())
    links_to_p = []
    PageRank_dict = {}
    d = damping_factor
    N = len(corpus.keys())
    for page in corpus:
        PageRank_dict[page] = 1/N
    for pages in list_of_keys:
        if len(copied_corpus[pages]) == 0:
            copied_corpus[pages] = list_of_keys
    
                    #need to listify my .keys function
                    #also need to adapt my program in case there is a page with no links.
    
    pageranks = []
    Rank = True
    while Rank:
        for key,value in copied_corpus.items():
            for pages in list_of_keys:
                if key in copied_corpus[pages]:
                    links_to_p.append(pages)
                    for q in links_to_p: #RG this is probelamtic, list is blank
                        PRi = sum(PageRank_dict[q]/len(copied_corpus[q]))
                        new_page_rank = (1-d)/N + PRi
                        old_page_rank = PageRank_dict[pages]
                        pageranks.append(abs(new_page_rank - old_page_rank))
        for pagerank in pageranks:
            if pagerank < 0.001:
                del list_of_keys[pageranks.index(pagerank)]
        if len(list_of_keys) == 0:
            Rank = False
        else:
            Rank = True
            


                        

    
    
    


if __name__ == "__main__":
    main()
