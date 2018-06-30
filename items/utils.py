import os,sys,re,requests,shutil
from urllib.parse import urlparse

class Utils(object):
        def __init__(self):
                self.basepath = sys.path[0]

        def makeValidFilename(self,path):
                return re.sub('[<>:"/\|?*]', '', path)

        def saveContents(self,contents,filename,path=''):
                folderPath = os.path.join(self.basepath,path)
                self.makeFolder(folderPath)
                
                handler = open(os.path.join(folderPath,filename),'w', encoding='utf-8')
                handler.write(contents)
                handler.close()

        def makeFolder(self,path):
                if not os.path.exists(path):
                        os.makedirs(path)

        def downloader(self,url,path,session = requests.Session()):
                self.makeFolder(os.path.dirname(path))
                response = session.get(url, stream=True)
                with open(path, 'wb') as out_file:
                    shutil.copyfileobj(response.raw, out_file)
                del response
        
        def getFileNameFromLink(self,url):
                return os.path.basename(urlparse(url).path)

        def copyModulesFolder(self,dest):
                self.makeFolder(os.path.join(self.basepath,dest))
                        
                src = os.path.join(self.basepath,'modules')
                dest = os.path.join(self.basepath,dest,'_modules')

                if os.path.exists(dest):
                        shutil.rmtree(dest)
                
                shutil.copytree(src, dest)
