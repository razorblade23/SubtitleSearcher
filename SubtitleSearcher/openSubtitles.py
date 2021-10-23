import requests
import struct, os
import json

main_search_url = 'https://rest.opensubtitles.org/search/'
headers = {'user-agent': 'TemporaryUserAgent'}

def search_by_imdb(imdb_id, language_code='eng'):
    request = requests.get('{}imdbid-{}/sublanguageid-{}'.format(main_search_url, imdb_id, language_code), headers=headers)
    json_req = json.loads(request.text)
    return json_req

def hashFile(name): 
      try: 
        longlongformat = '<q'  # little-endian long long
        bytesize = struct.calcsize(longlongformat) 
            
        f = open(name, "rb") 
            
        filesize = os.path.getsize(name) 
        hash = filesize 
            
        if filesize < 65536 * 2: 
                return "SizeError" 
            
        for x in range(65536/bytesize): 
                buffer = f.read(bytesize) 
                (l_value,)= struct.unpack(longlongformat, buffer)  
                hash += l_value 
                hash = hash & 0xFFFFFFFFFFFFFFFF #to remain as 64bit number  
                    

        f.seek(max(0,filesize-65536),0) 
        for x in range(65536/bytesize): 
                buffer = f.read(bytesize) 
                (l_value,)= struct.unpack(longlongformat, buffer)  
                hash += l_value 
                hash = hash & 0xFFFFFFFFFFFFFFFF 
            
        f.close() 
        returnedhash =  "%016x" % hash 
        return returnedhash 
    
      except(IOError): 
                return "IOError"