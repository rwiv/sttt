import asyncio

import aiohttp
from pyutils import sublist

from ..common import Sentence


class Translator:
    def __init__(self, tsvc_base_url: str, batch_size: int, ts_first: bool = True):
        self.__tsvc_base_url = tsvc_base_url
        self.__batch_size = batch_size
        self.__ts_first = ts_first

    def translate(self, sentences: list[Sentence]) -> tuple[list[Sentence], list[Sentence]]:
        translated_texts = asyncio.run(self._translate([s.text for s in sentences]))
        translated: list[Sentence] = []
        merged: list[Sentence] = []
        for i, ts_text in enumerate(translated_texts):
            src = sentences[i]
            translated.append(Sentence(start=src.start, end=src.end, text=ts_text))
            if self.__ts_first:
                merged_text = f"{ts_text}\n{src.text}"
            else:
                merged_text = f"{src.text}\n{ts_text}"
            merged.append(Sentence(start=src.start, end=src.end, text=merged_text))
        return translated, merged

    async def _translate(self, texts: list[str]) -> list[str]:
        co = []
        for sub in sublist(texts, self.__batch_size):
            co.append(self.request_tsvc(sub))
        result = []
        for res in await asyncio.gather(*co):
            result.extend(res)
        return result

    async def request_tsvc(self, texts: list[str]) -> list[str]:
        async with aiohttp.ClientSession() as session:
            url = f"{self.__tsvc_base_url}/translate/v1"
            res = await session.post(url, json={"texts": texts, "dest": "ko"})
            return await res.json()
