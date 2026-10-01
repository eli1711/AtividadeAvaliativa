from pathlib import Path
from pypdf import PdfReader
for p in Path('.').glob('*.pdf'):
 r=PdfReader(p)
 s='\n\n'.join(f'=== PAGINA {i+1} ===\n'+(pg.extract_text() or '') for i,pg in enumerate(r.pages))
 (Path('.analise')/(p.stem+'.txt')).write_text(s,encoding='utf-8')
 print(p.name,len(r.pages),len(s))
