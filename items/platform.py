import requests,re,os,sys
from .utils import Utils

from jinja2 import Environment, FileSystemLoader
from bs4 import BeautifulSoup


class Platform(object):
        def __init__(self,username,password):
                self.username = username
                self.password = password
                self.requestSession = requests.Session()
                self.utils = Utils()
                self.baseFolderName = "Unidades Curriculares"
                self.eadBaseUrl = "https://ead.ipleiria.pt/2017-18"
                self.kwargs = []

        def getGlobalHeaders(self):
                headers = {'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
                'Accept-Encoding': 'gzip, deflate, br',
                'Accept-Language': 'en-US,en;q=0.9',
                'Cache-Control': 'max-age=0',
                'Connection': 'keep-alive',
                'Content-Type': 'application/x-www-form-urlencoded',
                'Host': 'ead.ipleiria.pt',
                'Origin': 'https://ead.ipleiria.pt',
                'Upgrade-Insecure-Requests': '1',
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.87 Safari/537.36'}
                return headers
        
        def doLogin(self):
                data = {'username': self.username,
                        'password': self.password,
                        'anchor': ''}

                info = self.requestSession.post(self.eadBaseUrl + '/login/index.php',headers=self.getGlobalHeaders(), data=data).text
                return self.isLogged(info)
                
        def isLogged(self,info):
                if '<div id="content-wrapper">' in info:
                        print("Login OK")
                        return True
                else:
                        print("Login falhou")
                        return False

        def getUcs(self):
                listing = []
                info = self.requestSession.get(self.eadBaseUrl + '/my',headers=self.getGlobalHeaders()).text
                soup = BeautifulSoup(info, "html.parser")
                sections = soup.find_all("a", {"id": re.compile('label_3_.+?')})
                for x in sections:
                        item = {}
                        item['name'] = x.attrs['title'].replace('Á','A')
                        item['url'] = x.attrs['href']
                        item['cleanname'] = self.utils.makeValidFilename(item['name'])
                        listing.append(item)

                listing = sorted(listing, key=lambda k: k['name']) 
                return listing

        def getUcContent(self,item):                
                info = self.requestSession.get(item['url'],headers=self.getGlobalHeaders()).text                
                soup = BeautifulSoup(info, "html.parser")
                region = str(soup.find("section", {"id": "region-main"}))
                region = self.handleIcons(region)
                
                soup = BeautifulSoup(region, "html.parser")            
                sections = soup.find_all("li", {"id": re.compile('section-*')})
                for x in sections:
                        region = self.handleSectionItems(region, x, item)
                item['source'] = region
                return item
        
        def saveMainContent(self,item,ucList,ucMainList):
                index = self.getFilledHtml('template_index.html', uc_list = ucList, uc_content = ucMainList)
                self.utils.saveContents(index,'index.html',path=self.baseFolderName)

        def saveUcContent(self,item,ucList):
                index = self.getFilledHtml('template_uc.html', uc_name = item['name'], uc_content = item['source'], uc_list = ucList)
                ucpath = os.path.join(self.baseFolderName,item['cleanname'])
                self.utils.saveContents(index,'index.html',path=ucpath)

        def handleIcons(self,item):
                soup = BeautifulSoup(str(item), "html.parser")
                sections = set(soup.find_all("img", {"src": re.compile('ead.ipleiria.pt/*')}))
                for x in sections:
                        if '/folder/' in x['src']: item = item.replace(x['src'],'../_modules/icons/foldericon.svg')
                        elif '/forum/' in x['src']: item = item.replace(x['src'],'../_modules/icons/forumicon.svg')
                        elif '/page/' in x['src']: item = item.replace(x['src'],'../_modules/icons/pageicon.svg')
                        elif '/url/' in x['src']: item = item.replace(x['src'],'../_modules/icons/urlicon.svg')
                        elif '/quiz/' in x['src']: item = item.replace(x['src'],'../_modules/icons/quizicon.svg')
                        elif '/assign/' in x['src']: item = item.replace(x['src'],'../_modules/icons/assignicon.svg')
                        elif '/feedback/' in x['src']: item = item.replace(x['src'],'../_modules/icons/feedbackicon.svg')
                        elif '/spacer' in x['src']: item = item.replace(x['src'],'../_modules/icons/spacer.gif')
                        elif '/f/text-24' in x['src']: item = item.replace(x['src'],'../_modules/icons/texticon.png')
                        elif '/f/image-24' in x['src']: item = item.replace(x['src'],'../_modules/icons/imageicon.png')
                        elif '/f/pdf-24' in x['src']: item = item.replace(x['src'],'../_modules/icons/pdficon.png')
                        elif '/f/powerpoint-24' in x['src']: item = item.replace(x['src'],'../_modules/icons/powerpointicon.png')
                        elif '/f/spreadsheet-24' in x['src']: item = item.replace(x['src'],'../_modules/icons/spreadsheeticon.png')
                        elif '/f/archive-24' in x['src']: item = item.replace(x['src'],'../_modules/icons/archiveicon.png')
                        elif '/f/audio-24' in x['src']: item = item.replace(x['src'],'../_modules/icons/audioicon.png')
                        elif '/f/bmp-24' in x['src']: item = item.replace(x['src'],'../_modules/icons/bmpicon.png')
                        elif '/f/gif-24' in x['src']: item = item.replace(x['src'],'../_modules/icons/gificon.png')
                        elif '/f/jpeg-24' in x['src']: item = item.replace(x['src'],'../_modules/icons/jpegicon.png')
                        elif '/f/png-24' in x['src']: item = item.replace(x['src'],'../_modules/icons/pngicon.png')
                return item                

        def handleSectionItems(self,region,soup,item):
                sectionsrc = str(soup)
                sections = soup.find_all("img", {"src": re.compile('ead.ipleiria.pt/*')})
                
                for x in sections:
                        filename = self.utils.getFileNameFromLink(x['src'])
                        self.utils.downloader(x['src'],os.path.join(self.baseFolderName,item['cleanname'],filename),session = self.requestSession)
                        region = region.replace(x['src'], filename)
                        
                return region
                #sections = item.find_all("a", {"href": re.compile('ead.ipleiria.pt/*')})
                        #print(sections)
                        #exit(1)
                        
                        #soup.select("li.activity.page")
                #except:
                        #pass
                #pass

        def renderUcList(self,info,parent = False):
                text = ""
                if parent: add = ""
                else: add = "../"
                
                for x in info:
                        text += '<li class="type_course depth_3 item_with_icon"><p class="tree_item hasicon" role="treeitem"><a tabindex="-1" title="' + x['name'] + '" href="' + add + x['cleanname'] + '/index.html"><span class="item-content-wrap">' + x['name'] + '</span></a></p></li>';
                return text

        def renderUcMainList(self,info):
                text = ""
                for x in info:
                        text += '<li class="r0"><div class="column c1"><a href="' + x['cleanname'] + '/index.html"><img class="icon " alt="Unidade curricular" title="Unidade curricular" src="https://ead.ipleiria.pt/2017-18/theme/image.php/ead/core/1529077139/i/course" />'+x['name']+'</a></div></li>';
                return text

        def generateIndex(self,ucs):
                ucList = self.renderUcList(ucs, parent = True)
                ucMainList = self.renderUcMainList(ucs)
                
                self.saveMainContent(self,ucList,ucMainList)

        def generateUcs(self,ucs):
                ucList = self.renderUcList(ucs)
                for x in ucs:
                        content = self.getUcContent(x)
                        self.saveUcContent(content,ucList)                
                
        def retrieveContentsFromUcs(self):
                self.utils.copyModulesFolder(self.baseFolderName)
                
                ucs = self.getUcs()
                self.generateIndex(ucs)
                self.generateUcs(ucs)
                print("Conteudo gerado no caminho: %s" % (os.path.join(sys.path[0],self.baseFolderName)))
                                                      
        def getFilledHtml(self, renderfilename, **kwargs):
                j2_env = Environment(loader=FileSystemLoader(os.path.join(self.utils.basepath,'templates')), trim_blocks=True)
                return j2_env.get_template(renderfilename).render(**kwargs)
