# coding: utf-8

import urllib, urllib2, re

def guess_resolver(url):
    if 'google' in url: return obtem_url_google(url)
    


def obtem_url_google(url):

	html = urllib.urlopen(url.replace('/preview','/edit')).read()
	ow = open('C:\\Python27\\gdrive.html','w')
	ow.write(html)
	ow.close()
	soup = BeautifulSoup(html)
	dados = urllib2.unquote(soup('script')[4].prettify()).decode('unicode-escape')
	ttsurls = re.findall(r',\["ttsurl","(.*?)"\]\s', dados)[0]
	decoded = re.findall(r',\["url_encoded_fmt_stream_map","(.*?)"\]\s',dados)[0]
	qualidade = []
	url_video = []

	urls = [l for l in decoded.split('url=') if 'mp4' in l and l.startswith('https')]
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
	return [url_video[index],str(ttsurls) , '']