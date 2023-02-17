import httpx
import re
import html
import base64
import yarl

#some global shit
client = httpx.Client(headers={'user-agent':'uwu'},follow_redirects=True)
start_regex = r"#EXT-X-STREAM-INF(:.*?)?\n+(.+)"
res_regex = r"RESOLUTION=\d+x(\d+)"


class Anime:
    def __init__(self):
        self.main_url = "https://yugen.to"
        self.api_url = "https://yugen.to/api/embed/"
    

    
    def search(self,query:str, lst:list):
        """function to search anime

        Args:
            query (str): anime name

        Returns:
            list: anime_data 
        Format:
            anime_date : tuple (anime_id,anime_name)
        """
        query = query.replace(" ","+")
        r=client.get(f"{self.main_url}/discover/?q={query}")
        
        names = re.findall(r'"/anime/(.*?)/(.*?)/"',r.text)
        lst.extend(names)
    
    def anime_data(self,anime_data:tuple)->dict:
        """return all data about anime

        Args:
            anime_data : (anime_id,anime_name)
        """
        anime_id,name = (anime_data)
        r=client.get(
            f"{self.main_url}/anime/{anime_id}/{name}/watch/"
        )
        
        #collect sub episode
        try:
            sub_eps = re.findall('<div class="ap-.+?">Episodes</div><span class="description" .+?>(\d+)</span></div>',r.text)[0]
        except:
            #for hall print anime movies
            sub_eps = "0"
        
        #collect dub episode
        try:
            dub_eps = re.findall('<div class="ap-.+?">Episodes \(Dub\)</div><span class="description" .+?>(\d+)</span></div>',r.text)[0]
        except:
            dub_eps = "0"
        
        #collect description
        raw_desc = re.findall('<p class="description .+?">(.*)</p>',r.text)[0]
        raw_desc = re.sub(r'<.*?>',"",raw_desc) #clear any html tags
        desc = html.unescape(raw_desc)
        
        #collect thumbnail
        thumbnail_url = re.findall(r'<img src="(.*?)"',r.text)[1]
        
        return {'dub':dub_eps,'sub':sub_eps,'thumbnail':thumbnail_url,'desc':desc}
    
    def extract_link(self,id:str,ep:str,mode:str):
        """get the final streaming link

        Args:
            id (str): yugene anime id
            ep (str): ep to watch
            mode (str): sub or dub
    
        """
        raw_payload = f"{id}|{ep}" if mode == "sub" else f"{id}|{ep}|dub"
        
        r=client.post(
            self.api_url,
            data={
                'id':base64.b64encode(raw_payload.encode()).decode(),
                "ac":"0"
            },
            headers={
                "x-requested-with": "XMLHttpRequest"
            }
            
        ).json()
        streaming_link = r['hls'][0]
        x = client.get(streaming_link).text
        
       
        try:
            parent_url = str(yarl.URL(streaming_link).parent)+"/"
            for match in re.finditer(start_regex,x):
                res,link = match.groups()
                if not yarl.URL(link).is_absolute():
                    link = parent_url+link
                q=re.findall(res_regex,res)[0]

                yield {q:link}
        except:
            yield {'hls-p':streaming_link}
                    
        
        