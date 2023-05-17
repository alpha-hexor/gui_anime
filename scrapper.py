import httpx
import html
import re
import yarl
import base64
import re


#global stuff
client = httpx.Client(
    headers={
        'user-agent':'uwu'
    },
    follow_redirects=True,
    timeout= None
)
#dynamically get host for yugene
host = client.get("https://yugen.to").url.host
main_url = f"https://{host}"
api_url = f"{main_url}/api/embed/"
start_regex = r"#EXT-X-STREAM-INF(:.*?)?\n+(.+)"
res_regex = r"RESOLUTION=\d+x(\d+)"

def search_anime(anime:str)->list:
    anime = anime.replace(" ","+")
    r=client.get(f"{main_url}/discover/?q={anime}")
    names = re.findall(r'"/anime/(.*?)/(.*?)/"',r.text)
    images = re.findall(r'<img data-src="(.*?)"',r.text)
    
    return names,images

def get_anime_data(id,name):
    #return a json based anime data
    
    result={}
    
    r=client.get(
        f"{main_url}/anime/{id}/{name}/watch/"
    )
    
    try:
        sub_eps = re.findall('<div class="ap-.+?">Episodes</div><span class="description" .+?>(\d+)</span></div>',r.text)[0]
    except:
        sub_eps = '0'
    
    try:
        dub_eps = re.findall('<div class="ap-.+?">Episodes \(Dub\)</div><span class="description" .+?>(\d+)</span></div>',r.text)[0]
    except:
        dub_eps = '0'
        
    raw_desc = re.findall('<p class="description .+?">(.*)</p>',r.text)[0]
    raw_desc = re.sub(r'<.*?>',"",raw_desc) #clear any html tags
    desc = html.unescape(raw_desc)
    
    thumbnail_url = re.findall(r'<img src="(.*?)"',r.text)[1]
    banner_url = re.findall(r'''"background-image: url\('(.*?)'\);">''',r.text)[0]
    if not yarl.URL(banner_url).is_absolute():
        banner_url = "https://{host}"+banner_url
    
    result['banner_url'] = banner_url
    result['thumbnail_url'] = thumbnail_url
    result['desc'] = desc
    result['sub_eps'] = sub_eps
    result['dub_eps'] = dub_eps
    
    return result
    
def stream_link(id,ep,mode):
    l={}
    raw_payload = f"{id}|{ep}" if mode == "sub" else f"{id}|{ep}|dub"
    r=client.post(
        api_url,
        data={
            'id':base64.b64encode(raw_payload.encode()).decode(),
            'ac':'0'
        },
        headers={
            "x-requested-with": "XMLHttpRequest"
        }
    ).json()
    #print(r)
    streaming_link = r['hls'][0]
    x = client.get(streaming_link).text
    
    parent_url = str(yarl.URL(streaming_link).parent)+"/"
    for match in re.finditer(start_regex,x):
        res,link = match.groups()
        if not yarl.URL(link).is_absolute():
            link = parent_url+link
        q=re.findall(res_regex,res)[0]
        l[q] = link
    
    return l

    
        
    