import json
import requests
import urllib.parse
import time
import datetime
import random
import os
import subprocess
from cache import cache
ver = "2.7.9.1" # バージョン    
update = "YUKIBBSのID認証に対応" # アップデート内容
token = "e4f5c13f-4f31-4ae1-ac5c-b3f1df232073" # hcaptchaのサイトキー
max_api_wait_time = 5
max_time = 10
# "https://invidious.adminforge.de/",
apis = ["https://invidious.ducks.party/","https://invidious.f5.si/","https://lekker.gay/",'https://inv.nadeko.net/','https://inv1.nadeko.net/', 'https://inv2.nadeko.net/','https://inv3.nadeko.net/','https://inv4.nadeko.net/','https://inv5.nadeko.net/','https://inv.zzls.xyz/', 'https://invidious.nerdvpn.de/', 'https://iv.melmac.space/', 'https://invidious.0011.lt/', 'https://invidious.nietzospannend.nl/', 'https://rust.oskamp.nl/', 'https://youtube.lurkmore.com/', 'https://yt.yoc.ovh/']
version = "1.0"
adminannounce = requests.get(r'https://ztttas1.github.io/yuki00000000000000000000000000000/AN.txt').text.rstrip()

os.system("chmod 777 ./yukiverify")

# フォーク元:https://github.com/mochidukiyukimi/yuki-youtube-slim-2
# このyuki:https://github.com/Skype-GitHub/YUKI-GOD
# フォークした場合hcaptchaのサイトキーを自分で作り直して使用してください

url = r"https://yukibbs-server.onrender.com/"

version = "1.0"
apichannels = []
apicomments = []
[[apichannels.append(i),apicomments.append(i)] for i in apis]
class APItimeoutError(Exception):
    pass

def is_json(json_str):
    result = False
    try:
        json.loads(json_str)
        result = True
    except json.JSONDecodeError as jde:
        pass
    return result

def apirequest(url):
    global apis
    global max_time
    starttime = time.time()
    for api in apis:
        if  time.time() - starttime >= max_time -1:
            break
        try:
            res = requests.get(api+url,timeout=max_api_wait_time)
            if res.status_code == 200 and is_json(res.text):
                return res.text
            else:
                print(f"エラー:{api}")
                apis.append(api)
                apis.remove(api)
        except:
            print(f"タイムアウト:{api}")
            apis.append(api)
            apis.remove(api)
    raise APItimeoutError("APIがタイムアウトしました")

def apichannelrequest(url):
    global apichannels
    global max_time
    starttime = time.time()
    for api in apichannels:
        if  time.time() - starttime >= max_time -1:
            break
        try:
            res = requests.get(api+url,timeout=max_api_wait_time)
            if res.status_code == 200 and is_json(res.text):
                return res.text
            else:
                print(f"エラー:{api}")
                apichannels.append(api)
                apichannels.remove(api)
        except:
            print(f"タイムアウト:{api}")
            apichannels.append(api)
            apichannels.remove(api)
    raise APItimeoutError("APIがタイムアウトしました")

def apicommentsrequest(url):
    global apicomments
    global max_time
    starttime = time.time()
    for api in apicomments:
        if  time.time() - starttime >= max_time -1:
            break
        try:
            res = requests.get(api+url,timeout=max_api_wait_time)
            if res.status_code == 200 and is_json(res.text):
                return res.text
            else:
                print(f"エラー:{api}")
                apicomments.append(api)
                apicomments.remove(api)
        except:
            print(f"タイムアウト:{api}")
            apicomments.append(api)
            apicomments.remove(api)
    raise APItimeoutError("APIがタイムアウトしました")


def get_info(request):
    global version
    return json.dumps([version,os.environ.get('RENDER_EXTERNAL_URL'),str(request.scope["headers"]),str(request.scope['router'])[39:-2]])

def get_data(videoid):
    global logs
    t = json.loads(apirequest(r"api/v1/videos/"+ urllib.parse.quote(videoid)))
    return [{"id":i["videoId"],"title":i["title"],"authorId":i["authorId"],"author":i["author"]} for i in t["recommendedVideos"]],list(reversed([i["url"] for i in t["formatStreams"]]))[:2],t["descriptionHtml"].replace("\n","<br>"),t["title"],t["authorId"],t["author"],t["authorThumbnails"][-1]["url"]

def get_data2(videoid):
    global logs
    response = apirequest(r"api/v1/videos/" + urllib.parse.quote(videoid))
    data = json.loads(response)
    # "viewCountText" を抽出
    view_count_text = data.get("viewCount")
    return view_count_text
def get_like(videoid):
    global logs
    response = apirequest(r"api/v1/videos/" + urllib.parse.quote(videoid))
    data = json.loads(response)
    # "viewCountText" を抽出
    view_count_text = data.get("likeCount")
    return view_count_text
def get_genre(videoid):
    global logs
    response = apirequest(r"api/v1/videos/" + urllib.parse.quote(videoid))
    data = json.loads(response)
    # "viewCountText" を抽出
    view_count_text = data.get("genre")
    return view_count_text
"""
def get_1040(videoid):
    global logs
    response = apirequest(r"api/v1/videos/" + urllib.parse.quote(videoid))
    data = json.loads(response)
    for adaptiveFormats in data['adaptiveFormats']:
        if adaptiveFormats['size'] == '1920x1080' and adaptiveFormats['container'] == 'webm':
            return adaptiveFormats['url']
    return None  # 一致するフォーマットが見つからなかった場合にNoneを返す
"""
def get_search(q,page):
    global logs
    t = json.loads(apirequest(fr"api/v1/search?q={urllib.parse.quote(q)}&page={page}&hl=jp"))
    def load_search(i):
        if i["type"] == "video":
            try:
                title = i["title"]
            except Exception:
                title = "er"
            try:
                videoId = i["videoId"]
            except Exception:
                videoId = "er"
            try:
                authorId = i["authorId"]
            except Exception:
                authorId = "er"
            try:
                author = i["author"]
            except Exception:
                author = "er"
            try:
                publishedText = i["publishedText"]
            except Exception:
                publishedText="er"
            try:
                lengthSeconds = i["lengthSeconds"]
            except Exception:
                lengthSeconds = "er"
            return {"title":title,"id":videoId,"authorId":authorId,"author":author,"length":str(datetime.timedelta(seconds=lengthSeconds)),"published":publishedText,"type":"video"}
        elif i["type"] == "playlist":
            try:
                videoCount = i["videoCount"]
            except Exception:
                videoCount = "er"
            try:
                title = i["title"]
            except Exception:
                title = "er"
            try:
                playlistId = i["playlistId"]
            except Exception:
                playlistId = "er"
            try:
                thumbnail = i["videos"][0]["videoId"]
            except Exception:
                thumbnail = "er"
            return {"title":title,"id":playlistId,"thumbnail":thumbnail,"count":videoCount,"type":"playlist"}
        else:
            if i["authorThumbnails"][-1]["url"].startswith("https"):
                author = i["author"]
                authorId = i["authorId"]
                thumbnail = i["authorThumbnails"][-1]["url"]
                return {"author":author,"id":authorId,"thumbnail":thumbnail,"type":"channel"}
            else:
                return {"author":i["author"],"id":i["authorId"],"thumbnail":r"https://"+i["authorThumbnails"][-1]["url"],"type":"channel"}
    return [load_search(i) for i in t]

def get_channel(channelid):
    global apichannels
    t = json.loads(apichannelrequest(r"api/v1/channels/"+ urllib.parse.quote(channelid)))
    if t["latestVideos"] == []:
        print("APIがチャンネルを返しませんでした")
        apichannels.append(apichannels[0])
        apichannels.remove(apichannels[0])
        raise APItimeoutError("APIがチャンネルを返しませんでした")
    return [[{"title":i["title"],"id":i["videoId"],"authorId":t["authorId"],"author":t["author"],"published":i["publishedText"],"type":"video"} for i in t["latestVideos"]],{"channelname":t["author"],"channelicon":t["authorThumbnails"][-1]["url"],"channelprofile":t["descriptionHtml"]}]

def get_playlist(listid,page):
    t = json.loads(apirequest(r"/api/v1/playlists/"+ urllib.parse.quote(listid)+"?page="+urllib.parse.quote(page)))["videos"]
    return [{"title":i["title"],"id":i["videoId"],"authorId":i["authorId"],"author":i["author"],"type":"video"} for i in t]

def get_comments(videoid):
    t = json.loads(apicommentsrequest(r"api/v1/comments/"+ urllib.parse.quote(videoid)+"?hl=jp"))["comments"]
    return [{"author":i["author"],"authoricon":i["authorThumbnails"][-1]["url"],"authorid":i["authorId"],"body":i["contentHtml"].replace("\n","<br>")} for i in t]

def get_replies(videoid,key):
    t = json.loads(apicommentsrequest(fr"api/v1/comments/{videoid}?hmac_key={key}&hl=jp&format=html"))["contentHtml"]

def get_level(word):
    for i1 in range(1,13):
        with open(f'Level{i1}.txt', 'r', encoding='UTF-8', newline='\n') as f:
            if word in [i2.rstrip("\r\n") for i2 in f.readlines()]:
                return i1
    return 0


def check_cokie(cookie):
    print(cookie)
    if cookie == "True":
        return True
    return False

def get_verifycode():
    try:
        result = subprocess.run(["./yukiverify"], encoding='utf-8', stdout=subprocess.PIPE)
        hashed_password = result.stdout.strip()
        return hashed_password
    except subprocess.CalledProcessError as e:
        print(f"Error: {e}")
        return None




from fastapi import FastAPI, Depends,HTTPException
from fastapi import Response,Cookie,Request,Form
from fastapi.responses import HTMLResponse,PlainTextResponse
from fastapi.responses import RedirectResponse as redirect
from fastapi.middleware.gzip import GZipMiddleware
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel
from typing import Union
from fastapi.security import HTTPBasic, HTTPBasicCredentials#BASIC
security = HTTPBasic()#BASIC

app = FastAPI(docs_url=None, redoc_url=None, openapi_url=None)
app.mount("/css", StaticFiles(directory="./css"), name="static")
app.mount("/js", StaticFiles(directory="./js"), name="static")
app.mount("/word", StaticFiles(directory="./Blog", html=True), name="static")

app.add_middleware(GZipMiddleware, minimum_size=1000)
from fastapi.templating import Jinja2Templates
template = Jinja2Templates(directory='templates').TemplateResponse

USERNAME = "TEST1"#BASIC
PASSWORD = "TESTPAS"#BASIC
def authenticate(credentials: HTTPBasicCredentials = Depends(security)):
    if credentials.username != USERNAME or credentials.password != PASSWORD:
        raise HTTPException(status_code=401, detail="Unauthorized")
    return credentials

from fastapi.templating import Jinja2Templates
template = Jinja2Templates(directory='templates').TemplateResponse





@app.get("/", response_class=HTMLResponse)
def home(response: Response,request: Request,yuki: Union[str] = Cookie(None)):
    if check_cokie(yuki):
        response.set_cookie("yuki","True",max_age=60 * 60 * 24 * 7)
        return template("home.html",{"request": request})
    print(check_cokie(yuki))
    return redirect("/word")


@app.get('/watch', response_class=HTMLResponse)
def video(v:str,response: Response,request: Request,yuki: Union[str] = Cookie(None),proxy: Union[str] = Cookie(None)):
    global apis,apichannels,apicomments
    if not(check_cokie(yuki)):
        return template("404.html", {"request": request})
    response.set_cookie(key="yuki", value="True",max_age=7*24*60*60)
    videoid = v
    t = get_data(videoid)
    t2 = get_data2(videoid)
    like = get_like(videoid)
    genre = get_genre(videoid)
    """
    video1040 = get_1040(videoid)
    """# "video1040":video1040,
    response.set_cookie("yuki","True",max_age=60 * 60 * 24 * 7)
    return template('video.html', {"request": request,"videoid":videoid,"invser":apis[0],"videourls":t[1],"res":t[0],"description":t[2],"videotitle":t[3],"authorid":t[4],"authoricon":t[6],"author":t[5],"viewCountText":t2,"likeCountText":like,"genre":genre,"proxy":proxy})


@app.get("/search", response_class=HTMLResponse,)
def search(q:str,response: Response,request: Request,page:Union[int,None]=1,yuki: Union[str] = Cookie(None),proxy: Union[str] = Cookie(None)):
    if not(check_cokie(yuki)):
        return template("404.html", {"request": request})
    response.set_cookie("yuki","True",max_age=60 * 60 * 24 * 7)
    return template("search.html", {"request": request,"results":get_search(q,page),"word":q,"next":f"/search?q={q}&page={page + 1}","proxy":proxy})

@app.get("/hashtag/{tag}")
def search(tag:str,response: Response,request: Request,page:Union[int,None]=1,yuki: Union[str] = Cookie(None)):
    if not(check_cokie(yuki)):
        return template("search.html", {"request": request})
    return redirect(f"/search?q={tag}")


@app.get("/channel/{channelid}", response_class=HTMLResponse)
def channel(channelid:str,response: Response,request: Request,yuki: Union[str] = Cookie(None),proxy: Union[str] = Cookie(None)):
    if not(check_cokie(yuki)):
        return template("404.html", {"request": request})
    response.set_cookie("yuki","True",max_age=60 * 60 * 24 * 7)
    t = get_channel(channelid)
    return template("channel.html", {"request": request,"results":t[0],"channelname":t[1]["channelname"],"channelicon":t[1]["channelicon"],"channelprofile":t[1]["channelprofile"],"proxy":proxy})

@app.get("/answer", response_class=HTMLResponse)
def set_cokie(q:str):
    t = get_level(q)
    if t > 5:
        return f"level{t}\n推測を推奨する"
    elif t == 0:
        return "level12以上\nほぼ推測必須"
    return f"level{t}\n覚えておきたいレベル"

@app.get("/playlist", response_class=HTMLResponse)
def playlist(list:str,response: Response,request: Request,page:Union[int,None]=1,yuki: Union[str] = Cookie(None),proxy: Union[str] = Cookie(None)):
    if not(check_cokie(yuki)):
        return template("404.html", {"request": request})
    response.set_cookie("yuki","True",max_age=60 * 60 * 24 * 7)
    return template("search.html", {"request": request,"results":get_playlist(list,str(page)),"word":"","next":f"/playlist?list={list}","proxy":proxy})

@app.get("/info", response_class=HTMLResponse)
def viewlist(response: Response,request: Request,yuki: Union[str] = Cookie(None)):
    global apis,apichannels,apicomments
    if not(check_cokie(yuki)):
        return template("404.html", {"request": request})
    response.set_cookie("yuki","True",max_age=60 * 60 * 24 * 7)
    return template("info.html",{"request": request,"Youtube_API":apis[0],"Channel_API":apichannels[0],"Comments_API":apicomments[0]})

@app.get("/suggest")
def suggest(keyword:str):
    return [i[0] for i in json.loads(requests.get(r"http://www.google.com/complete/search?client=youtube&hl=ja&ds=yt&q="+urllib.parse.quote(keyword)).text[19:-1])[1]]

@app.get("/comments")
def comments(request: Request,v:str):
    return template("comments.html",{"request": request,"comments":get_comments(v)})

@app.get("/thumbnail")
def thumbnail(v:str):
    return Response(content = requests.get(fr"https://img.youtube.com/vi/{v}/0.jpg").content,media_type=r"image/jpeg")

@app.get("/bbs",response_class=HTMLResponse)
def view_bbs(request: Request,name: Union[str, None] = "",seed:Union[str,None]="",channel:Union[str,None]="main",verify:Union[str,None]="false",yuki: Union[str] = Cookie(None)):
    if not(check_cokie(yuki)):
        return template("404.html", {"request": request})
    res = HTMLResponse(requests.get(fr"{url}bbs?name={urllib.parse.quote(name)}&seed={urllib.parse.quote(seed)}&channel={urllib.parse.quote(channel)}&verify={urllib.parse.quote(verify)}",cookies={"yuki":"True"}).text)
    return res

@cache(seconds=5)
def bbsapi_cached(verify,channel):
    return requests.get(fr"{url}bbs/api?t={urllib.parse.quote(str(int(time.time()*1000)))}&verify={urllib.parse.quote(verify)}&channel={urllib.parse.quote(channel)}",cookies={"yuki":"True"}).text

@app.get("/bbs/api",response_class=HTMLResponse)
def view_bbs(request: Request,t: str,channel:Union[str,None]="main",verify: Union[str,None] = "false"):
    print(fr"{url}bbs/api?t={urllib.parse.quote(t)}&verify={urllib.parse.quote(verify)}&channel={urllib.parse.quote(channel)}")
    return bbsapi_cached(verify,channel)

@app.get("/bbs/result")
def write_bbs(request: Request,name: str = "",message: str = "",seed:Union[str,None] = "",channel:Union[str,None]="main",verify:Union[str,None]="false",yuki: Union[str] = Cookie(None)):
    t = requests.get(fr"{url}bbs/result?name={urllib.parse.quote(name)}&message={urllib.parse.quote(message)}&seed={urllib.parse.quote(seed)}&channel={urllib.parse.quote(channel)}&verify={urllib.parse.quote(verify)}&info={urllib.parse.quote(get_info(request))}&serververify={get_verifycode()}",cookies={"yuki":"True"}, allow_redirects=False)
    if t.status_code != 307:
        return HTMLResponse(t.text)
    return redirect(f"/bbs?name={urllib.parse.quote(name)}&seed={urllib.parse.quote(seed)}&channel={urllib.parse.quote(channel)}&verify={urllib.parse.quote(verify)}")

@cache(seconds=30)
def how_cached():
    return requests.get(fr"{url}bbs/how").text

@app.get("/bbs/how",response_class=PlainTextResponse)
def view_commonds(request: Request,yuki: Union[str] = Cookie(None)):
    if not(check_cokie(yuki)):
        return template("404.html", {"request": request})
    return how_cached()

@app.get("/load_instance")
def home():
    global url
    url = requests.get(r'https://raw.githubusercontent.com/taiga905/yuki-youtube-instance/main/instance.txt').text.rstrip()


@app.get("/reload_inv")
def home():
    global apis,apichannels,apicomments
    stopinv = apis[0]
    apis.append(stopinv)
    apis.remove(stopinv)
    print(f"invリロード/{stopinv}")
@app.exception_handler(500)
def page(request: Request,__):
    return template("APIwait.html",{"request": request},status_code=500)
@app.exception_handler(404)
def page(request: Request,__):
    return template("404.html", {"request": request})

@app.exception_handler(APItimeoutError)
def APIwait(request: Request,exception: APItimeoutError):
    return template("APIwait.html",{"request": request},status_code=500)

@app.get("/updateinfo", response_class=HTMLResponse)
def home(response: Response,request: Request,yuki: Union[str] = Cookie(None)):
    if check_cokie(yuki):
        response.set_cookie("yuki","True",max_age=60 * 60 * 24 * 7)
        return template("apd1.html",{"request": request,"ver":ver,"update":update})
    print(check_cokie(yuki))
    return template("404.html", {"request": request})
@app.get("/vtt")
async def get_captions(id: str):
    global apis,apichannels,apicomments
    url = f"{apis[0]}api/v1/captions/{id}?label=Japanese+(auto-generated)"
    response = apirequest(url)
    return response

@app.get("/verify", response_class=HTMLResponse)
def get_form(seed=""):
    return requests.get(fr"{url}verify?seed={urllib.parse.quote(seed)}").text

@app.post("/submit", response_class=HTMLResponse)
def submit(h_captcha_response: str = Form(alias="h-captcha-response"), seed: str = Form(...)):
    return requests.post(fr"{url}submit",data={"h-captcha-response": h_captcha_response, "seed": seed}).text

"""
@app.get("/verify", response_class=HTMLResponse)
def home(response: Response,request: Request,yuki: Union[str] = Cookie(None)):
    if not(check_cokie(yuki)):
        return template("404.html", {"request": request})
    return "ID認証は対応していません。対応するまでしばらくお待ちください。"
"""
