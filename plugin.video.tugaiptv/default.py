# -*- coding: utf-8 -*-
import xbmc,xbmcaddon,xbmcgui,xbmcplugin,urllib,urllib2,os,re,sys,datetime,time
from BeautifulSoup import BeautifulSoup
from BeautifulSoup import BeautifulStoneSoup, BeautifulSoup, BeautifulSOAP
from metahandlerpt import metahandlerspt
from datetime import date

import re, htmlentitydefs

##
# Removes HTML or XML character references and entities from a text string.
#
# @param text The HTML (or XML) source text.
# @return The plain text, as a Unicode string, if necessary.

def unescape(text):
    def fixup(m):
        text = m.group(0)
        if text[:2] == "&#":
            # character reference
            try:
                if text[:3] == "&#x":
                    return unichr(int(text[3:-1], 16))
                else:
                    return unichr(int(text[2:-1]))
            except ValueError:
                pass
        else:
            # named entity
            try:
                text = unichr(htmlentitydefs.name2codepoint[text[1:-1]])
            except KeyError:
                pass
        return text # leave as is
    return re.sub("&#?\w+;", fixup, text)

####################################################### CONSTANTES #####################################################

versao = '0.2.0'
addon_id = 'plugin.video.tugaiptv'
selfAddon = xbmcaddon.Addon(id=addon_id)
addonfolder = selfAddon.getAddonInfo('path')
art = addonfolder + '/resources/art/'
metagetpt = metahandlerspt.MetaData(preparezip=False)
selfAddon = xbmcaddon.Addon(id=addon_id)
username = urllib.quote(selfAddon.getSetting('username'))
password = selfAddon.getSetting('password')
ver_intro = True

#######################################################################################################################

def guess_resolver(url):
    if 'google' in url: return obtem_url_google(url)
    


def obtem_url_google(url):

    html = urllib.urlopen(url).read()
    soup = BeautifulSoup(html)
    dados = urllib2.unquote(soup('script')[4].prettify()).decode('unicode-escape')
    ttsurls = re.findall(r',\["ttsurl","(.*?)"\]\s', dados)[0]
    decoded = re.findall(r',\["url_encoded_fmt_stream_map","(.*?)"\]\s',dados)[0]
    qualidade = []
    url_video = []

    urls = [l for l in decoded.split('url=') if 'mp4' in l and l.startswith('https')]
    print urls
    url_video = []
    for u in urls:
	    itags = {5:'Baixa Qualidade, 240p, FLV, 400x240',
		     17:'Baixa Qualidade, 144p, 3GP, 0x0',
		     18:'Media Qualidade, 480p, MP4, 480x360',
		     59:'Media Qualidade, 360p, MP4, 480x360',
		     22:'Alta Qualidade, 720p, MP4, 1280x720',
		     34:'Media Qualidade, 360p, FLV, 640x360',
		     35:'Standard Definition, 480p, FLV, 854x480',
		     36:'Baixa Qualidade, 240p, 3GP, 0x0',
		     37:'Alta Qualidade, 1080p, MP4, 1920x1080',
		     38:'Original Definition, MP4, 4096x3072',
		     43:'Media Qualidade, 360p, WebM, 640x360',
		     44:'Standard Definition, 480p, WebM, 854x480',
		     45:'Alta Qualidade, 720p, WebM, 1280x720',
		     46:'Alta Qualidade, 1080p, WebM, 1280x720',
		     82:'Media Qualidade 3D, 360p, MP4, 640x360',
		     84:'Alta Qualidade 3D, 720p, MP4, 1280x720',
		     100:'Media Qualidade 3D, 360p, WebM, 640x360',
		     102:'Alta Qualidade 3D, 720p, WebM, 1280x720'}
	    q = 'quality='
	    i = 'itag='
	    quality = u[u.find(q) + len(q): u.find(',', u.find(q))]
	    itag = u[u.find(i) + len(i): u.find('&', u.find(i))]
	    #print "ORG qualitys: " + quality
	    #print "ORG itag: " + itag
	    try:
		    quality = itags[int(itag)]
	    except:
		    pass
	    qualidade.append(quality)
	    url_video.append(u[:-1])
    index = 0
    index = xbmcgui.Dialog().select('Qualidade do vídeo:', qualidade)
    if index == -1: return['-','-'] # Tive que alterar esta linha para corrigir um pequeno erro
    return [url_video[index]]

################################################### MENUS PLUGIN ######################################################

canal_sigla_epg = {'History':'HIS',
                   'MTV':'MTV',
                   'Band 1':'BAN',
                   'Band 2':'BAN',
                   'Globo 1':'GSP',
                   'Globo 2':'GSP',
                   'Globo News':'GLN',
                   'HBO':'HBO',
                   'HBO - 2':'HBO',
                   'HBO 2':'HB2',
                   'HBO Family':'HFA',
                   'Max hd':'MHD',
                   'Fox Sports 1':'FSP',
                   'Fox Sports 2':'FSP',
                   'Megapix':'MPH',
                   'Multishow':'MSW',
                   'Nat Geo Wild':'NGH',
                   'National Geographic':'SUP',
                   'Nick HD':'NIH',
                   'PFC 24 Horas':'121',
                   'Sbt 1':'SBT',
                   'Sbt 3':'SBT',
                   'Rede TV 1':'RTV',
                   'Rede TV 2':'RTV',
                   'Rede TV 3':'RTV',
                   'Record 1':'REC',
                   'Record 2':'REC',
                   'Sony':'SET',
                   'Space':'SPA',
                   'SporTV':'SPO',
                   'SporTV - 2':'SPO',
                   'SporTV 2':'SP2',
                   'SporTV 2 - 2':'SP2',
                   'TBS':'TBS',
                   'TNT':'TNT',
                   'TV Cultura':'CUL',
                   'Telecine Action':'TC2',
                   'Telecine Action - 2':'TC2',
                   'Telecine Cult':'TC5',
                   'Telecine Pipoca - 2':'TC4',
                   'Telecine Pipoca':'TC4',
                   'Telecine Premium - 2':'TC1',
                   'Telecine Premium':'TC1',
                   'Tv Escola':'ESC',
                   'Universal':'USA',
                   'Universal - 2':'USA',
                   'VH1':'VH1',
                   'Warner':'WBT',
                   'EI':'SPI'}

PUBLIC_TRACKERS = [
    "udp://tracker.publicbt.com:80/announce",
    "udp://tracker.openbittorrent.com:80/announce",
    "udp://open.demonii.com:1337/announce",
    "udp://tracker.istole.it:6969",
    "udp://tracker.coppersurfer.tk:80",
    "udp://tracker.ccc.de:80",
    "udp://tracker.istole.it:80",
    "udp://tracker.1337x.org:80/announce",
    "udp://pow7.com:80/announce",
    "udp://tracker.token.ro:80/announce",
    "udp://9.rarbg.me:2710/announce",
    "udp://ipv4.tracker.harry.lu:80/announce",
    "udp://coppersurfer.tk:6969/announce",
    "udp://bt.rghost.net:80/announce",
    "udp://tracker.publichd.eu/announce",
    "udp://www.eddie4.nl:6969/announce",
    "http://tracker.ex.ua/announce",
    "http://mgtracker.org:2710/announce",
]

def torrent2magnect(url):
    import base64
    import bencode
    import hashlib
    import urllib
    #from xbmctorrent.utils import url_get
    torrent_data = urllib2.urlopen(url).read()
    try:
        import zlib
        torrent_data = zlib.decompressobj(16 + zlib.MAX_WBITS).decompress(torrent_data)
    except:
        pass
    metadata = bencode.bdecode(torrent_data)
    hashcontents = bencode.bencode(metadata['info'])
    digest = hashlib.sha1(hashcontents).digest()
    b32hash = base64.b32encode(digest)
    params = {
        'dn': metadata['info']['name'],
        'tr': metadata['announce'],
    }
    paramstr = urllib.urlencode(params)
    
    def _boost_magnet(magnet):
        from urllib import urlencode
        return "%s&%s" % (magnet, urlencode({"tr": PUBLIC_TRACKERS}, True))

    magnet = 'magnet:?%s&%s' % ('xt=urn:btih:%s' % b32hash, paramstr)
    return urllib.quote_plus(_boost_magnet(magnet))

def abrir_cookie(url):
        import mechanize
        import cookielib

        br = mechanize.Browser()
        cj = cookielib.LWPCookieJar()
        br.set_cookiejar(cj)
        br.set_handle_equiv(True)
        br.set_handle_gzip(True)
        br.set_handle_redirect(True)
        br.set_handle_referer(True)
        br.set_handle_robots(False)
        br.set_handle_refresh(mechanize._http.HTTPRefreshProcessor(), max_time=1)
        br.addheaders = [('User-agent', 'Mozilla/5.0 (X11; U; Linux i686; en-US; rv:1.9.0.1) Gecko/2008071615 Fedora/3.0.1-1.fc9 Firefox/3.0.1')]
        br.open('http://89.163.212.78:8009/admin/')
        br.select_form(nr=0)
        br.form['password']=password
        br.form['username']=username
        br.submit()
        br.open(url)
        return br.response().read()


def makeRequest(url, headers=None):
        try:
            if headers is None:
                headers = {'User-agent' : 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:19.0) Gecko/20100101 Firefox/19.0'}
            req = urllib2.Request(url,None,headers)
            response = urllib2.urlopen(req)
            data = response.read()
            response.close()
            return data
        except urllib2.URLError, e:
            print 'URL: '+url
            if hasattr(e, 'code'):
                print 'We failed with error code - %s.' % e.code
                xbmc.executebuiltin("XBMC.Notification(BrasilOnline,We failed with error code - "+str(e.code)+",10000,"+icon+")")
            elif hasattr(e, 'reason'):
                addon_log('We failed to reach a server.')
                addon_log('Reason: %s' %e.reason)
                xbmc.executebuiltin("XBMC.Notification(BrasilOnline,We failed to reach a server. - "+str(e.reason)+",10000,"+icon+")")


spc = (('&#192;','A'),	('&#193;','A'),	('&#194;','A'),	('&#195;','A'),	('&#196;','A'),	('&#199;','C'),	('&#200;','E'),	('&#201;','E'), ('&#198;','AE'),
	('&#202;','E'),	('&#203;','E'),	('&#204;','I'),	('&#205;','I'),	('&#207;','I'),	('&#217;','U'),	('&#218;','U'),	('&#220;','U'),
	('&#219;','U'),	('&#224;','a'),	('&#225;','a'),	('&#226;','a'),	('&#227;','a'),	('&#228;','a'),	('&#231;','ç'),	('&#232;','e'),
	('&#233;','e'),	('&#234;','e'),	('&#235;','e'),	('&#236;','i'),	('&#237;','i'),	('&#238;','i'),	('&#239;','i'),	('&#242;','o'),
	('&#243;','o'),	('&#244;','o'),	('&#245;','o'),	('&#249;','u'),	('&#250;','u'),	('&#251;','u'),	('&#252;','u'),	('&#221;','Y'),	('&#253;','y'), ('A&#161;','a'),('A&#173;','i'),('A&#169;','e'))

def html_replace_clean(s):
	s = cleanHtml(s)
	for code,caracter in spc:
		s = s.replace(code,caracter)
	return s

def cleanHtml(dirty):
    clean = re.sub('&quot;', '\"', dirty)
    clean = re.sub('&#039;', '\'', clean)
    clean = re.sub('&#215;', 'x', clean)
    clean = re.sub('&#038;', '&', clean)
    clean = re.sub('&#8216;', '\'', clean)
    clean = re.sub('&#8217;', '\'', clean)
    clean = re.sub('&#8211;', '-', clean)
    clean = re.sub('&#8220;', '\"', clean)
    clean = re.sub('&#8221;', '\"', clean)
    clean = re.sub('&#8212;', '-', clean)
    clean = re.sub('&amp;', '&', clean)
    clean = re.sub("`", '', clean)
    clean = re.sub('<em>', '[I]', clean)
    clean = re.sub('</em>', '[/I]', clean)
    return clean

def getSoup(url):
        data = abrir_cookie(url).decode('utf8')
        return BeautifulSOAP(data, convertEntities=BeautifulStoneSoup.XML_ENTITIES)

def Ver_intro():
    if os.path.exists(os.path.join(xbmc.translatePath("special://temp"),"tuga_today")):
	ftoday = open(os.path.join(xbmc.translatePath("special://temp"),"tuga_today")).read()
	today = str(date.today())
    else:
	ftoday = ''
	today = str(date.today())
    if ftoday != today:
	xbmc.Player(xbmc.PLAYER_CORE_AUTO).play(art+'intro.mp4')
	while xbmc.Player().isPlaying():
	    ftoday = open(os.path.join(xbmc.translatePath("special://temp"),"tuga_today"),'w')
	    #today = str(date.today())
	    ftoday.write(today)
	    ftoday.close()
	    time.sleep(1)
	return True

def Menu_inicial():
    	#intro = Ver_intro()
    	try:
	    abrir_cookie('http://89.163.212.78:8009/canais/liberar/')
	    addDir("Tv","",1,"http://www.apkdad.com/wp-content/uploads/2013/02/Live-TV-for-Android-Icon.png")
	    addDir("Filmes","1",1002,"http://icons.iconarchive.com/icons/hadezign/hobbies/256/Movies-icon.png")
	    #addDir("Series","1",1003,"http://icons.iconarchive.com/icons/hadezign/hobbies/256/Movies-icon.png")
	    xbmc.executebuiltin("Container.SetViewMode(51)")
	except:
	    addDir("Apenas para usuários.","","-","https://cdn0.iconfinder.com/data/icons/simple-web-navigation/165/574949-Exclamation-512.png")
	    addDir("Caso já tenha login/senha, insira na configuração do addon.","","-","https://cdn0.iconfinder.com/data/icons/simple-web-navigation/165/574949-Exclamation-512.png")
	    while xbmc.Player().isPlaying():
		time.sleep(1)
	    xbmc.executebuiltin("Container.SetViewMode(502)")



def Menu_Inicial_Tv():
	    addDir("Opção 1","",1,"http://www.apkdad.com/wp-content/uploads/2013/02/Live-TV-for-Android-Icon.png")
	    addDir("Opção 2","",1000,"http://www.apkdad.com/wp-content/uploads/2013/02/Live-TV-for-Android-Icon.png")
	    addDir("Opção 3","",2000,"http://www.apkdad.com/wp-content/uploads/2013/02/Live-TV-for-Android-Icon.png")
	    addDir("Opção 4","",3000,"http://www.apkdad.com/wp-content/uploads/2013/02/Live-TV-for-Android-Icon.png")
	    xbmcplugin.setContent(int(sys.argv[1]), 'Movies')
	    xbmc.executebuiltin("Container.SetViewMode(51)")

def Menu_Inicial_Filmes():
	    addDir("Opção 1 [COLOR green](Torrents)[/COLOR]","1",200,"http://icons.iconarchive.com/icons/hadezign/hobbies/256/Movies-icon.png")
	    addDir("Opção 2 [COLOR green](VoD do Forum)[/COLOR][COLOR red][Em Desenvolvimento][/COLOR]","1",201,"http://icons.iconarchive.com/icons/hadezign/hobbies/256/Movies-icon.png")
	    xbmcplugin.setContent(int(sys.argv[1]), 'Movies')
	    xbmc.executebuiltin("Container.SetViewMode(51)")
	    
def Menu_Inicial_Series():
	    addDir("Opção 1 [COLOR green](VoD do Forum)[/COLOR][COLOR red][Em Desenvolvimento][/COLOR]","1",0,"http://icons.iconarchive.com/icons/hadezign/hobbies/256/Movies-icon.png")
	    xbmcplugin.setContent(int(sys.argv[1]), 'Movies')
	    xbmc.executebuiltin("Container.SetViewMode(51)")

def canais_master():
    canais = getSoup('https://www.dropbox.com/s/ju2tycbdzwviviy/NovaLista.xml?dl=1')
    for canal in canais('item'):
	addLink(canal.title.text,canal.link.text,canal.thumbnail.text)
    xbmc.executebuiltin("Container.SetViewMode(500)")


def canais_playtvfr():
    canais = eval(abrir_cookie('http://89.163.212.78:8009/canais/playtvfr?action=1'))
    for canal in canais:
	addDir(canal[0].encode('utf-8', 'ignore'),canal[2],'3001',canal[1],len(canais),False)
    xbmc.executebuiltin("Container.SetViewMode(500)")

def play_playtvfr(url):
    m3u8 = abrir_cookie('http://89.163.212.78:8009/canais/playtvfr?action=2&ch=%s' % url)
    xbmcPlayer = xbmc.Player()
    xbmcPlayer.play(m3u8+'|User-agent=')


def canais_tvzune():
    canais = eval(abrir_cookie('http://89.163.212.78:8009/canais/tvzune?action=1'))
    for canal in canais:
	addDir(canal[0],canal[1],'2001',canal[2],len(canais),False)
    xbmc.executebuiltin("Container.SetViewMode(500)")

def play_tvzune(url):
    m3u8 = abrir_cookie('http://89.163.212.78:8009/canais/tvzune?action=2&ch=%s' % url)
    xbmcPlayer = xbmc.Player()
    xbmcPlayer.play(m3u8+'|User-agent=')

def menu_filmes():
	addDir("Pesquisar...","sort=year&cb=0.5470752841793001&quality=720p,1080p,3d&page=1&genre=mystery|1",2,"https://www.ibm.com/developerworks/mydeveloperworks/blogs/e8206aad-10e2-4c49-b00c-fee572815374/resource/images/Search-icon.png")
        addDir("+Populares","sort=year&cb=0.5470752841793001&quality=720p,1080p,3d&page=1|1",2,"http://icons.iconarchive.com/icons/hadezign/hobbies/256/Movies-icon.png")
        addDir("Sci-Fi","sort=year&cb=0.5470752841793001&quality=720p,1080p,3d&page=1&genre=sci-fi|1",2,"http://icons.iconarchive.com/icons/hadezign/hobbies/256/Movies-icon.png")
        addDir("Acão","sort=year&cb=0.5470752841793001&quality=720p,1080p,3d&page=1&genre=action|1",2,"http://icons.iconarchive.com/icons/hadezign/hobbies/256/Movies-icon.png")
        addDir("Comédia","sort=year&cb=0.5470752841793001&quality=720p,1080p,3d&page=1&genre=comedy|1",2,"http://icons.iconarchive.com/icons/hadezign/hobbies/256/Movies-icon.png")
        addDir("Thriller","sort=year&cb=0.5470752841793001&quality=720p,1080p,3d&page=1&genre=thriller|1",2,"http://icons.iconarchive.com/icons/hadezign/hobbies/256/Movies-icon.png")
        addDir("Romance","sort=year&cb=0.5470752841793001&quality=720p,1080p,3d&page=1&genre=romance|1",2,"http://icons.iconarchive.com/icons/hadezign/hobbies/256/Movies-icon.png")
	addDir("Animação","sort=year&cb=0.5470752841793001&quality=720p,1080p,3d&page=1&genre=animation|1",2,"http://icons.iconarchive.com/icons/hadezign/hobbies/256/Movies-icon.png")
	addDir("Documentários","sort=year&cb=0.5470752841793001&quality=720p,1080p,3d&page=1&genre=documentary|1",2,"http://icons.iconarchive.com/icons/hadezign/hobbies/256/Movies-icon.png")
	addDir("Horror","sort=year&cb=0.5470752841793001&quality=720p,1080p,3d&page=1&genre=horror|1",2,"http://icons.iconarchive.com/icons/hadezign/hobbies/256/Movies-icon.png")
	addDir("Drama","sort=year&cb=0.5470752841793001&quality=720p,1080p,3d&page=1&genre=drama|1",2,"http://icons.iconarchive.com/icons/hadezign/hobbies/256/Movies-icon.png")
	addDir("Thriller","sort=year&cb=0.5470752841793001&quality=720p,1080p,3d&page=1&genre=thriller|1",2,"http://icons.iconarchive.com/icons/hadezign/hobbies/256/Movies-icon.png")
	addDir("Mistério","sort=year&cb=0.5470752841793001&quality=720p,1080p,3d&page=1&genre=mystery|1",2,"http://icons.iconarchive.com/icons/hadezign/hobbies/256/Movies-icon.png")
	
	
def listar_filmes(request):
        import json
        pagina = request.split('|')[1]
        request = request.split('|')[0]
        filmes = json.loads(abrir_cookie('http://89.163.212.78:8009/filme/filmes?%s' % request))
        print filmes
        for filme in filmes['MovieList']:
                meta_imdb = metagetpt.get_meta('movie', '', imdb_id=filme['imdb'])
                total = len(filmes)
                try:
                        addDirM(filme['title'],str({'torrents':filme['items'], 'imdb':filme['imdb'], 'poster':filme['poster_big']}),6,filme['poster_big'],total,True,meta_imdb)
                except:
                        pass
        addDir("Proximos >>",request.replace("page=%s" % pagina,"page=%s" % str(int(pagina)+1)) + "|" + str(int(pagina)+1),2,"")
        xbmcplugin.setContent(int(sys.argv[1]), 'movies')
        xbmc.executebuiltin('Container.SetViewMode(503)')

def listar_torrents(url):
        _dict = eval(url)
        torrents = _dict['torrents']
        for torrent in torrents:
                url = torrent['torrent_url']
                print torrent
                addDir('[COLOR green](S:%s)[/COLOR][COLOR red](L:%s)[/COLOR]-%s' % (torrent['torrent_seeds'],torrent['torrent_peers'],torrent['file'].encode('utf-8')),str({'torrent':url, 'imdb':_dict['imdb']}),3,_dict['poster'],1,False)
        xbmcplugin.setContent(int(sys.argv[1]), 'Movies')
        xbmc.executebuiltin("Container.SetViewMode(51)")

def play_filme(url):
        import thread
        def set_sub(url):
                import os.path
                import glob
                import zipfile
                #os.chdir(xbmc.translatePath("special://temp"))
                #for file_ in glob.glob("*.srt"):
                #        os.remove(file_)
                zip_file = os.path.join(xbmc.translatePath("special://temp"),'sub2.zip')
                urllib.urlretrieve(url,zip_file)
                zfile = zipfile.ZipFile(zip_file)
                print zfile.namelist()
                #XBMC.Extract(zip_file, xbmc.translatePath("special://temp"))
                #xbmc.executebuiltin("XBMC.Extract(%s, %s)" % (zip_file, xbmc.translatePath("special://temp")))
                print "Sub: " + os.path.join(xbmc.translatePath("special://temp"),zfile.namelist()[0])
                zfile.extract(zfile.namelist()[0], xbmc.translatePath("special://temp"))
                while not xbmc.Player().isPlaying():
                    time.sleep(1)
                xbmc.Player().setSubtitles(os.path.join(xbmc.translatePath("special://temp"),zfile.namelist()[0]))
        
        import json
        filme = eval(url)
        print filme['torrent']
        subs = json.loads(abrir_cookie('http://89.163.212.78:8009/filme/subs/%s/' % filme['imdb']))
	try:
	    sub_url = 'http://www.yifysubtitles.com' + subs['subs'][filme['imdb']]['brazilian-portuguese'][0]['url']
	except:
	    sub_url = ''
        #set_sub(sub_url)
        thread.start_new_thread(set_sub, (sub_url,))
        magnect = torrent2magnect(filme['torrent'])

        #thread.start_new_thread(set_sub, (sub_url,))
        xbmcPlayer = xbmc.Player()
        xbmcPlayer.play('plugin://plugin.video.pulsar/play?uri=' + magnect)
	

def play_filme_vod(url,sub,server):
        import thread
        def set_sub(url):
                import os.path
                import glob
                import zipfile
                #os.chdir(xbmc.translatePath("special://temp"))
                #for file_ in glob.glob("*.srt"):
                #        os.remove(file_)
                zip_file = os.path.join(xbmc.translatePath("special://temp"),'sub2.zip')
                urllib.urlretrieve(url,zip_file)
                zfile = zipfile.ZipFile(zip_file)
                print zfile.namelist()
                #XBMC.Extract(zip_file, xbmc.translatePath("special://temp"))
                #xbmc.executebuiltin("XBMC.Extract(%s, %s)" % (zip_file, xbmc.translatePath("special://temp")))
                print "Sub: " + os.path.join(xbmc.translatePath("special://temp"),zfile.namelist()[0])
                zfile.extract(zfile.namelist()[0], xbmc.translatePath("special://temp"))
                while not xbmc.Player().isPlaying():
                    time.sleep(1)
                xbmc.Player().setSubtitles(os.path.join(xbmc.translatePath("special://temp"),zfile.namelist()[0]))
        
        #thread.start_new_thread(set_sub, (sub,))
	if server == 'GD':
	    url = obtem_url_google(url)[0]
	if url != '-':
	    xbmcPlayer = xbmc.Player(xbmc.PLAYER_CORE_AUTO)
	    xbmcPlayer.play(url)

def play_mult_canal(arg):
    try:
	tuple_ = eval(arg)
	playlist = xbmc.PlayList(xbmc.PLAYLIST_VIDEO)
	playlist.clear()
	for link in tuple_:
	    listitem = xbmcgui.ListItem('Stream', thumbnailImage='')
	    listitem.setInfo('video', {'Title': 'Stream'})
	    playlist.add(url=link, listitem=listitem, index=7)
	xbmc.Player(xbmc.PLAYER_CORE_AUTO).play(playlist)
	
    except:
	xbmc.Player(xbmc.PLAYER_CORE_AUTO).play(arg)

def listar_categorias_filmes(url):
    soup = getSoup(url)
    categorias = soup('categoria')
    print 'Categorias:' + str(soup)
    import HTMLParser
    pars = HTMLParser.HTMLParser()
    pars.unescape('&copy; &euro;')
    for categoria in categorias:
	addDir(unescape(categoria.nome.text).encode('utf8'),'http://89.163.212.78:8009/vod/xml/?action=categoria&categoria_pk=%s' % categoria.pk.text,103,categoria.logo.text)
    xbmc.executebuiltin("Container.SetViewMode(500)")

def listar_filmes_vod(url):
        
        soup = getSoup(url)
        filmes = soup('filme')
        
        for filme in filmes:
		addDir('%s [COLOR red]%s[/COLOR] [COLOR green]%s[/COLOR]' % (unescape(filme.nome.text), filme.vdr.text, filme.server.text), str((filme.link.text, filme.sub.text, filme.server.text)),4,filme.thumbnail.text)
        xbmc.executebuiltin("Container.SetViewMode(500)")

def listar_categorias(url):
    soup = getSoup(url)
    categorias = soup('categoria')
    for categoria in categorias:
	#print categoria.nome
	if categoria.nome.text == 'XXX':
	    addDir(categoria.nome.text,'http://89.163.212.78:8009/canais/xml/?action=categoria&categoria_pk=%s' % categoria.pk.text,104,categoria.logo.text)
	else:
	    addDir(categoria.nome.text,'http://89.163.212.78:8009/canais/xml/?action=categoria&categoria_pk=%s' % categoria.pk.text,102,categoria.logo.text)

    xbmc.executebuiltin("Container.SetViewMode(500)")

def listar_canais_xxx(url):
    keyb = xbmc.Keyboard('', 'XXX') #Chama o keyboard do XBMC com a frase indicada
    keyb.doModal() #Espera ate que seja confirmada uma determinada string
    if (keyb.isConfirmed()):
            if keyb.getText() == '0000':
		epg = eval(abrir_cookie('http://89.163.212.78:8009/canais/epg/'))
		
		soup = getSoup(url)
		canais = soup('canal')
		print epg
		
		for canal in canais:
		    try:
			      canal_programa = epg[canal.epg.text]['programa']
		    except:
			      canal_programa = ''
		    if canal_programa:
			      addDir(canal.nome.text + ' - [COLOR green](%s)[/COLOR]' % canal_programa ,canal.link.text,105,canal.logo.text,1,False)
		    else:
			      addDir(canal.nome.text,canal.link.text,105,canal.logo.text,1,False)
    xbmc.executebuiltin("Container.SetViewMode(500)")

#addDir(name,url,mode,iconimage,total=0,pasta=True)
def listar_canais(url):
        
        epg = eval(abrir_cookie('http://89.163.212.78:8009/canais/epg/'))
        
        soup = getSoup(url)
        canais = soup('canal')
        print epg
        
        for canal in canais:
              try:
                        canal_programa = epg[canal.epg.text]['programa']
              except:
                        canal_programa = ''
              if canal_programa:
                        addDir(canal.nome.text.encode('utf8') + ' - [COLOR green](%s)[/COLOR]' % canal_programa ,canal.link.text,105,canal.logo.text,1,False)
              else:
                        addDir(canal.nome.text.encode('utf8'),canal.link.text,105,canal.logo.text,1,False)
        
        xbmc.executebuiltin("Container.SetViewMode(500)")


################################################## PASTAS ################################################################

def addLink(name,url,iconimage):
      liz=xbmcgui.ListItem(name, iconImage="DefaultVideo.png", thumbnailImage=iconimage)
      liz.setInfo( type="Video", infoLabels={ "Title": name } )
      liz.setProperty('fanart_image', "%s/fanart.jpg"%selfAddon.getAddonInfo("path"))
      return xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=url,listitem=liz)

def addDir(name,url,mode,iconimage,total=0,pasta=True):
      u=sys.argv[0]+"?url="+urllib.quote_plus(url)+"&mode="+str(mode)+"&name="+urllib.quote_plus(name)
      liz=xbmcgui.ListItem(name,iconImage="DefaultFolder.png", thumbnailImage=iconimage)
      liz.setInfo( type="Video", infoLabels={ "Title": name} )
      liz.setProperty('fanart_image', "%s/fanart.jpg"%selfAddon.getAddonInfo("path"))
      return xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=u,listitem=liz,isFolder=pasta,totalItems=total)

def addDirM(name,url,mode,iconimage,pasta=True,total=1,meta=metagetpt.get_meta('movie','' ,''),plot=''):
	if plot and not meta['plot'] or meta['plot']=='N/A':
		meta['plot'] = plot
	if iconimage and not meta['cover_url']:
		meta['cover_url'] = iconimage
	u=sys.argv[0]+"?url="+urllib.quote_plus(url)+"&mode="+str(mode)+"&name="+urllib.quote_plus(name)+"&iconimage="+urllib.quote_plus(iconimage)
	ok=True
        liz=xbmcgui.ListItem(name, iconImage='http://image.tmdb.org/t/p/original/' + os.path.split(meta['cover_url'])[1], thumbnailImage=iconimage)
        liz.setInfo( type="Video", infoLabels= meta )
        contextMenuItems = []
        contextMenuItems.append(('Movie Information', 'XBMC.Action(Info)'))
        liz.addContextMenuItems(contextMenuItems, replaceItems=True)
        if not meta['backdrop_url'] == '':
	    liz.setProperty('fanart_image', 'http://image.tmdb.org/t/p/original/' + os.path.split(meta['backdrop_url'])[1])
        else:
	    try:
		liz.setProperty('fanart_image', fanart)
	    except:
		liz.setProperty('fanart_image', '')
        ok=xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=u,listitem=liz,isFolder=pasta,totalItems=total)
#        xbmcplugin.setContent(int(sys.argv[1]), 'movies')
#	xbmc.executebuiltin('Container.SetViewMode(51)')
        return ok


######################################################## OUTRAS FUNCOES ###############################################

def get_params():
      param=[]
      paramstring=sys.argv[2]
      if len(paramstring)>=2:
            params=sys.argv[2]
            cleanedparams=params.replace('?','')
            if (params[len(params)-1]=='/'):
                  params=params[0:len(params)-2]
            pairsofparams=cleanedparams.split('&')
            param={}
            for i in range(len(pairsofparams)):
                  splitparams={}
                  splitparams=pairsofparams[i].split('=')
                  if (len(splitparams))==2:
                        param[splitparams[0]]=splitparams[1]                 
      return param

params=get_params()
url=None
name=None
mode=None
tamanhoparavariavel=None

try: url=urllib.unquote_plus(params["url"])
except: pass
try: tamanhoparavariavel=urllib.unquote_plus(params["tamanhof"])
except: pass
try: name=urllib.unquote_plus(params["name"])
except: pass
try: mode=int(params["mode"])
except: pass

print "Mode: "+str(mode)
print "URL: "+str(url)
print "Name: "+str(name)
print "Name: "+str(tamanhoparavariavel)

if mode==None:
        Menu_inicial()
elif mode==1001:
	Menu_Inicial_Tv()
elif mode==1002:
	Menu_Inicial_Filmes()
elif mode==1:
        listar_categorias('http://89.163.212.78:8009/canais/xml?action=categorias')
elif mode==102:
        listar_canais(url)
elif mode==103:
	listar_filmes_vod(url)
elif mode==104:
	listar_canais_xxx(url)
elif mode==105:
	play_mult_canal(url)
elif mode==200:
        menu_filmes()
elif mode==201:
	listar_categorias_filmes('http://89.163.212.78:8009/vod/xml/?action=categorias')
elif mode==2:
        listar_filmes(url)
elif mode==3:
        play_filme(url)
elif mode==4:
    params = eval(url)
    play_filme_vod(params[0],params[1], params[2])
elif mode==6:
        listar_torrents(url)
elif mode==1000:
	canais_master()
elif mode==2000:
	canais_tvzune()
elif mode==2001:
	play_tvzune(url)
elif mode==3000:
	canais_playtvfr()
elif mode==3001:
	play_playtvfr(url)


xbmcplugin.endOfDirectory(int(sys.argv[1]))
