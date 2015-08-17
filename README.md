# pyngram
python binding for ngram query library

install:

    python3 setup.py install


example usage:

    __author__ = 'chenkovsky'
    from pyngram import Ngram
    from arpa import arpa
    import gzip
    from docopt import docopt
    args = docopt("""
    Usage:
    test.py <bin> <src>
    """)
    ngram = Ngram(args["<bin>"])
    def gram(lm_info, section, words, prob, bow):
        prob = int(prob*-1000000)
        bow =  int(bow*-1000000)
        prob_query = ngram.prob(words)
        bow_query = ngram.bow(words)
        if prob != prob_query or bow != bow_query:
            print("words:%s, prob:%d, bow:%d, prob_query:%d, bow_query:%d"% (words, prob, bow, prob_query, bow_query))
            exit()
    with gzip.open(args["<src>"],"rt") as fi:
        arpa(fi, gram=gram)
