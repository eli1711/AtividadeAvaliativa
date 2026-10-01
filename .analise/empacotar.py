from pathlib import Path
from zipfile import ZipFile, ZIP_DEFLATED
import json
base=Path('entrega')
assert json.loads((base/'evidencias/resultados.json').read_text(encoding='utf-8'))['verificacoes']==298
arquivos=sorted(p for p in base.rglob('*') if p.is_file() and '__pycache__' not in p.parts)
with ZipFile('Entrega_Manutencao_Inteligente.zip','w',compression=ZIP_DEFLATED) as z:
 for p in arquivos:z.write(p,p.as_posix())
with ZipFile('Entrega_Manutencao_Inteligente.zip') as z:
 assert z.testzip() is None
 assert len(z.namelist())==len(arquivos)
print(f'Pacote validado: {len(arquivos)} arquivos, {Path("Entrega_Manutencao_Inteligente.zip").stat().st_size} bytes.')
