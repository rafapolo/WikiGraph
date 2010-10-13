#!/usr/bin/python
# -*- coding: UTF-8 -*-
# author: rafael polo

print "============"
print "Carregando libs..."
import sys, urllib2, re, htmlentitydefs
import networkx as nx
try:
    import matplotlib.pyplot as plt
except:
    raise

# pega html da url
def get_page(wiki):
	url = 'http://pt.wikipedia.org/w/index.php?title='+wiki+'&printable=yes'
	opener = urllib2.build_opener()
	opener.addheaders = [('User-agent', 'Mozilla/5.0')]
	print "Carregando " + url
	infile = opener.open(url)
	return infile.read()
	
def get_first_paragraph(page):
	# encontra tudo que estver entre <p>*</p>
	ps = re.findall(r'<p>\s*(.+?)\s*</p>', page)
	print "Encontrados %s parágrafos." % len(ps)
	return decode_htmlentities(remove_html_tags(ps[0].decode("utf-8").lower())) #primeiro
	
def remove_html_tags(txt):
	# retira tags html
	p = re.compile(r'<[^<]*?/?>')
	clean = p.sub('', txt)
	# retira espaços excedentes
	p = re.compile(r'\s+')
	return p.sub(' ', clean)

# decodifica tag html para string
def substitute_entity(match):
    ent = match.group(3)
    if match.group(1) == "#":
        if match.group(2) == '':
            return unichr(int(ent))
        elif match.group(2) == 'x':
            return unichr(int('0x'+ent, 16))
    else:
        cp = n2cp.get(ent)

        if cp:
            return unichr(cp)
        else:
            return match.group()

def decode_htmlentities(string):
    entity_re = re.compile(r'&(#?)(x?)(\d{1,5}|\w{1,8});')
    return entity_re.subn(substitute_entity, string)[0]


if len(sys.argv)==0:
	print "Qual?"
	exit()

wiki = ""
for arg in (sys.argv[1:len(sys.argv)]):
	wiki += arg+" "
wiki = wiki.strip()
wiki = wiki.replace(' ', '_')

paragrafo = get_first_paragraph(get_page(wiki))
# Retira tudo que não é alfanumérico e espaços extras.
p_limpo = re.sub('[\s\(),;:?.\s]', ' ', paragrafo)
frase = re.sub('\s+', ' ', p_limpo)
# Separa palavras
palavras = frase.split(" ")
while '' in palavras:
	palavras.remove('')
count = len(palavras)
print "%s palavras no primeiro." % count

print "Gerando Grafo..."
G=nx.Graph()
palavra_anterior = ""
for palavra in palavras:
	if (palavra != ""):
		if (G.has_node(palavra)):
			peso = G.node[palavra]['peso']
			peso += 1
			size = peso*200
			G.add_node(palavra, peso=peso, size=size)			
		else:
			G.add_node(palavra, peso=1, size=200)		
	if (palavra_anterior != ""):
		G.add_edge(palavra_anterior, palavra)
	palavra_anterior = palavra

#nx.draw_networkx_nodes(G,pos=nx.spring_layout(G))

print "Renderizando..."
nx.draw(G, node_size=[G.node[n]['size'] for n in G.nodes()])
print "Ok"
print "============"
plt.show()