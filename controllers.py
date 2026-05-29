'''YouTube transcript extraction controllers.'''

from typing import Any, cast, List
from models import Yturl
import yt_dlp
from requests.exceptions import RetryError
from youtube_transcript_api import YouTubeTranscriptApi
from youtube_transcript_api._errors import TranscriptsDisabled, NoTranscriptFound, IpBlocked
from langchain_classic.text_splitter import RecursiveCharacterTextSplitter
from langchain_chroma.vectorstores import Chroma
from langchain_google_genai import GoogleGenerativeAIEmbeddings
from langchain_core.documents import Document
from pydantic import SecretStr
import os
import uuid
gemini_api = SecretStr(os.getenv("GOOGLE_API_KEY",""))

tenant = os.getenv("tenant","")
database = os.getenv("database","")
chroma_api_key = os.getenv("chroma_api_key","")

recursive_text_splitter = RecursiveCharacterTextSplitter(
    chunk_size = 2500,
    chunk_overlap = 100
)

def _transcript(video_id: str) -> str:
    api = YouTubeTranscriptApi()
    try:
        return " ".join(s.text for s in api.fetch(video_id, languages=["en", "hi"]))
    except (NoTranscriptFound, TranscriptsDisabled, IpBlocked, RetryError) as e:
        print(f"[transcript] {type(e).__name__}: {e}")
        return "No transcript found."


def handle_url_and_prompt(yt_object: Yturl) -> List[Document]:
    '''Main entry point controller.'''
    url = yt_object.url.strip()
    opts: dict[str, Any] = {"skip_download": True, "quiet": True, "extract_flat": True}

    with yt_dlp.YoutubeDL(cast(Any, opts)) as ydl:
        info = ydl.extract_info(url, download=False)

    if info.get("_type") == "playlist" or "entries" in info:
        transcript = " ".join(
            _transcript(e["id"])
            for e in info.get("entries", [])
            if e and e.get("id")
        )
    else:
        transcript = _transcript(cast(dict, info)["id"])

    vector_store = Chroma(
        chroma_cloud_api_key = chroma_api_key,
        collection_name = f"default-collection {uuid.uuid4()}",
        create_collection_if_not_exists=True,
        database = database,
        tenant = tenant,
        embedding_function = GoogleGenerativeAIEmbeddings(
            api_key = gemini_api,
            model = "models/gemini-embedding-001"
        )
    )
    response = whole_workflow(
        prompt = yt_object.chat,
        transcripts = transcript,
        vector_store = vector_store
    )
    return response
def whole_workflow( prompt : str, transcripts: str, vector_store : Chroma) -> List[Document]:
    '''This is the whole workflowwwww '''
    if (not transcripts) or (not prompt) :
        raise ValueError("We require transcripts and prompt to be non empty")
    if transcripts and prompt: #ik this is uncessary but coool
        return _workflow(transcripts=transcripts,prompt=prompt,vector_store=vector_store)
    else:
        raise SystemError("This is an Extra Terrestrial call which we can't intercept")



def _workflow( transcripts : str, vector_store : Chroma, prompt : str = "" ) -> List[Document]:
    docs = recursive_text_splitter.create_documents([transcripts])
    list_of_ids = vector_store.add_documents(docs)

    retriver = vector_store.as_retriever(k = 5, search_type = "mmr")
    documents = retriver.invoke(input=prompt)
    print(f" prompt : {prompt}")
    print(list_of_ids)
    return documents
