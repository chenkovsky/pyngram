__author__ = 'chenkovsky'
from ctypes import *
import os
from arpa import arpa
libngram = cdll.LoadLibrary(os.path.dirname(os.path.realpath(__file__)) + '/../libngram.so')
libngram.NgramBuilder_init.restype = POINTER(c_byte)
libngram.Ngram_init_from_bin.restype = POINTER(c_byte)
libngram.Ngram_init_from_bin.argtypes = [POINTER(c_byte)]
def arpa_to_bin(dst_path, arpa_fp):
    builder = [None]

    def init_ngram_builder(lm_info):
        gram_nums = [y[1] for y in sorted(list(lm_info.items()), key=lambda x: x[0])]
        arr = (c_longlong * len(gram_nums))(*gram_nums)
        builder[0] = libngram.NgramBuilder_init(arr,len(gram_nums))

    def gram(lm_info, section, words, prob, bow):
        prob = int(prob*-1000000)
        bow =  int(bow*-1000000)
        if len(words) > 1:
            arr = (c_char_p * len(words))(*[c_char_p(w.encode("utf8")) for w in words])
            libngram.NgramBuilder_add_ngram2(builder[0], arr, section, prob, bow)
        else:
            libngram.NgramBuilder_add_word(builder[0], c_char_p(words[0].encode("utf8")), prob, bow)

    arpa(arpa_fp, header_end=init_ngram_builder, gram=gram)
    libngram.NgramBuilder_save(builder[0], c_char_p(dst_path.encode("utf8")))
    if builder[0] is not None:
        arr = (POINTER(c_byte) * 1)(builder[0])
        libngram.NgramBuilder_free(arr)


class Ngram:
    def __init__(self, path):
        import array
        array = array.array('b')
        fd = os.open(path, os.O_RDONLY)
        sz = os.fstat(fd).st_size
        fp = os.fdopen(fd, 'rb')
        array.fromfile(fp, sz)
        os.close(fd)
        addr, count = array.buffer_info()
        self.lm = libngram.Ngram_init_from_bin(cast(addr, POINTER(c_byte)))

    def prob(self, words):
        arr = (c_char_p * len(words))(*[c_char_p(w.encode("utf8")) for w in words])
        return libngram.Ngram_prob2(self.lm, arr, len(words))

    def bow(self, words):
        arr = (c_char_p * len(words))(*[c_char_p(w.encode("utf8")) for w in words])
        return libngram.Ngram_bow2(self.lm, arr, len(words))

    def __del__(self):
        arr = (POINTER(c_byte) * 1)(self.lm)
        libngram.Ngram_free(arr)

if __name__ == '__main__':
    import gzip
    from docopt import docopt
    args = docopt("""
Usage:
    pyngram.py <dst> <src>
    """)
    with gzip.open(args["<src>"],"rt") as fi:
        arpa_to_bin(args["<dst>"], fi)

