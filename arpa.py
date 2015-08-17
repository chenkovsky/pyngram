__author__ = 'chenkovsky'
from rex import rex
import sys
def arpa(fp, gram=None, header_start = None, header_end = None, section_start = None, section_end = None, file_end = None):
    section = None
    lm_info = {}
    max_gram = 0
    for l in fp:
        #print(l)
        if l.startswith("\\"):
            if l == "\\data\\\n":
                section = 0
                print("loading header", file=sys.stderr)
                if header_start and header_start() == False:
                    break
            elif l=="\\end\\\n":
                if file_end:
                    file_end(lm_info)
                break
            else:
                res = (l == rex("/^\\\\(\\d+)-grams/"))
                if res is not None:
                    section = int(res[1])
                    print("loading %d-grams" % section, file=sys.stderr)
                    if section_start and section_start(lm_info,section) == False:
                        break
            continue
        if l == "\n":
            if section == 0 and header_end and header_end(lm_info)== False:
                break
            elif section is not None and section > 0 and section_end and section_end(lm_info,section) == False:
                break
            section = None
            continue
        if section == 0:
            res = (l == rex("/^ngram (\d+)=(\d+)/"))
            lm_info[int(res[1])] = int(res[2])
            print("ngram %d=%d"%(int(res[1]), int(res[2])), file=sys.stderr)
            max_gram = max(max_gram, int(res[1]))
        else:
            larr = l.strip("\n").split("\t")
            bow = None
            if len(larr) == 3:
                bow = float(larr[-1])
            elif len(larr) < 2:
                continue
            if bow is None:
                bow = 0
            prob = float(larr[0])
            words = larr[1].split(" ")
            if gram and gram(lm_info, section, words, prob, bow) == False:
                break