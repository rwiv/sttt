from sttt.trans.schema import Sentence
from sttt.trans.translator import Translator

tsvc_base_url = ""


def test_translator():
    print()
    texts = ["hello world 1", "hello world 2", "hello world 3"]
    ts = Translator(tsvc_base_url=tsvc_base_url, batch_size=1)
    res = ts.translate([Sentence(start=0, end=0, text=text) for text in texts])
    assert len(res) == 3
    print(res)
