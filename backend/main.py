import asyncio

from flask import Flask, request
from duckduckgo_search import AsyncDDGS

app = Flask(__name__)


def check_request():
    if request.args.get("q") is None:
        raise Exception("No query")
    if request.args.get("ss") is not None and request.args.get("ss") != "off" and request.args.get("ss") != "moderate" and request.args.get("ss") != "strict":
        raise Exception("Invalid safe search")


@app.get("/text")
async def get_text():
    check_request()
    return await AsyncDDGS().text(request.args.get("q"), safesearch=request.args.get("ss") if request.args.get("ss") is not None else "moderate", max_results=100)


@app.get("/images")
async def get_images():
    check_request()
    return await AsyncDDGS().images(request.args.get("q"), safesearch=request.args.get("ss") if request.args.get("ss") is not None else "moderate", max_results=100)


@app.get("/videos")
async def get_videos():
    check_request()
    return await AsyncDDGS().videos(request.args.get("q"), safesearch=request.args.get("ss") if request.args.get("ss") is not None else "moderate", max_results=100)


@app.get("/news")
async def get_news():
    check_request()
    return await AsyncDDGS().news(request.args.get("q"), safesearch=request.args.get("ss") if request.args.get("ss") is not None else "moderate", max_results=100)


@app.get("/overview")
async def get_overview():
    check_request()

    text = AsyncDDGS().text(request.args.get("q"), safesearch=request.args.get("ss") if request.args.get("ss") is not None else "moderate", max_results=3)
    images = AsyncDDGS().images(request.args.get("q"), safesearch=request.args.get("ss") if request.args.get("ss") is not None else "moderate", max_results=3)
    videos = AsyncDDGS().videos(request.args.get("q"), safesearch=request.args.get("ss") if request.args.get("ss") is not None else "moderate", max_results=3)
    news = AsyncDDGS().news(request.args.get("q"), safesearch=request.args.get("ss") if request.args.get("ss") is not None else "moderate", max_results=3)

    res = await asyncio.gather(text, images, videos, news)

    return {
        'text': res[0],
        'images': res[1],
        'videos': res[2],
        'news': res[3],
    }


if __name__ == '__main__':
    print("Starting web server on port 25190...")
    app.run(debug=False, port=25190, host="127.0.0.1")
