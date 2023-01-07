import httpx
import re
import json


#some global shit
client = httpx.Client(headers={'user-agent':'uwu'})
EXTENSION = '%7B%22persistedQuery%22%3A%7B%22version%22%3A1%2C%22sha256Hash%22%3A%229c7a8bc1e095a34f2972699e8105f7aaf9082c6e1ccd56eab99c2f1a971152c6%22%7D%7D'
start_regex = r"#EXT-X-STREAM-INF(:.*?)?\n+(.+)"
res_regex = r"RESOLUTION=\d+x(\d+)"


class Anime:
    def __init__(self):
        self.main_url = "https://allanime.site"
        self.api_url = "https://blog.allanime.pro/apivtwo/clock.json"
        self.r = ""
    
    def search(self,query:str)->list:
        """function to search anime

        Args:
            query (str): anime name

        Returns:
            list: anime_id and names
        """
        query = query.replace(" ","%20")
        SEARCH_SLUG = f"%7B%22search%22%3A%7B%22allowAdult%22%3Afalse%2C%22allowUnknown%22%3Afalse%2C%22query%22%3A%22{query}%22%7D%2C%22limit%22%3A26%2C%22page%22%3A1%2C%22translationType%22%3A%22sub%22%2C%22countryOrigin%22%3A%22ALL%22%7D"
        self.r = client.get(
            f"{self.main_url}/allanimeapi?variables={SEARCH_SLUG}&extensions={EXTENSION}",
            headers={'referer':f'{self.main_url}/search-anime'}
        ).text
        
        r=json.loads(self.r)
        anime_ids = [i['_id'] for i in r['data']['shows']['edges']]
        names = [i['name'] for i in r['data']['shows']['edges']]
        #fix the names
        names = [i.replace(" ","-") for i in names]
        return anime_ids,names
    
    def sub_dub_episode(self,index:int):
        """return available sub and dub episode

        Args:
            index (int): index of the name in the list
        """
        r=json.loads(self.r)
        dub_eps = r['data']['shows']['edges'][index]['availableEpisodes']['dub']
        sub_eps = r['data']['shows']['edges'][index]['availableEpisodes']['sub']
        
        return sub_eps,dub_eps
    
    def extract_link(self,id:str,name:str,ep:str,mode:str):
        """get the final streaming link

        Args:
            id (str): allanime anime id
            name (str): anime to watch
            ep (str): ep to watch
            mode (str): sub or dub
    
        """
        r=client.get(
            f"{self.main_url}/watch/{id}/{name}/episode-{ep}-{mode}"
            
        ).text
        gogo_id =re.findall(r'".*\.php\?id=(.*?)\&.*"',r)[0]
        print(gogo_id)
        api_id = re.findall('id=(.*?)&',re.findall(r'"embedUrl":"(.*?)"',r)[0])[0]
        r=client.get(f"{self.api_url}?id={api_id}").json()
        
        #extract link from the json
        try:
            link = r['links'][0]['src']
        except:
            link = r['links'][0]['link']
            
        #extract quality
        r=client.get(link).text
        print(r)
        
        for match in re.finditer(start_regex,r):
            res,link = match.groups()
            q=re.findall(res_regex,res)[0]
            yield {q:link}
                
        
        