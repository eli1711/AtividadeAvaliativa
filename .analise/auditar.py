from pathlib import Path
from pypdf import PdfReader
from zipfile import ZipFile
from lxml import etree
import json,re
r=Path('entrega')
assert len(PdfReader(r/'documentacao/Dossie.pdf').pages)==14
with ZipFile(r/'apresentacao/Apresentacao.pptx') as z:
 slides=[n for n in z.namelist() if re.fullmatch(r'ppt/slides/slide\d+\.xml',n)]
 assert len(slides)==20
 assert len([n for n in z.namelist() if re.fullmatch(r'ppt/notesSlides/notesSlide\d+\.xml',n)])==20
 namespace={'a':'http://schemas.openxmlformats.org/drawingml/2006/main'}
 assert all(etree.fromstring(z.read(n)).xpath('//a:t/text()',namespaces=namespace) for n in slides)
for name in ['base_original.pl','base_fato_alterado.pl','base_regra_nova.pl','base_regra_nova_teste.pl','maquina_estados.pl']:
 t=(r/'prolog'/name).read_text(encoding='utf-8')
 codigo='\n'.join(l.split('%')[0] for l in t.splitlines())
 assert not any(x in codigo for x in ['\\+','not(', 'assert(', 'retract(', '[', '!', 'findall(', 'member(']),name
assert all(f'## Etapa {i} ' in (r/'documentacao/Dossie.md').read_text(encoding='utf-8') for i in range(1,13))
# Conferencia de preservacao das quatro regras entre as versoes.
s=(r/'prolog/base_original.pl').read_text(encoding='utf-8')
originais=re.findall(r'hipotese\(Caso,.*?\.',s,re.S)
for nome in ['base_fato_alterado.pl','base_regra_nova.pl','base_regra_nova_teste.pl']:
 t=(r/'prolog'/nome).read_text(encoding='utf-8')
 assert all(regra in t for regra in originais),nome
print('Conferência final: 14 páginas, 20 slides com notas, 12 etapas e regras originais preservadas.')
