import asyncio

from sttt.trans import Translator

tsvc_base_url = ""


def test_translator():
    print()
    texts = ["hello world 1", "hello world 2", "hello world 3"]
    ts = Translator(tsvc_base_url=tsvc_base_url, batch_size=1, dest_lang="ko")
    res = asyncio.run(ts._translate(texts))
    assert len(res) == 3
    print(res)
