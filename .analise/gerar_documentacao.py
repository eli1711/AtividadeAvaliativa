from pathlib import Path
import itertools, re, html
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, LongTable, TableStyle, Preformatted, PageBreak, Image, KeepTogether
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.enums import TA_LEFT
from reportlab.lib.pagesizes import A4
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont

raiz=Path(__file__).resolve().parents[1]
docs=raiz/'entrega/documentacao'
p=docs/'Dossie.md'
s=p.read_text(encoding='utf-8')
cab='| Linha | T | V | N | K | I | T∧V∧N | K∧I | R04 |\n| --- | --- | --- | --- | --- | --- | --- | --- | --- |\n'
linhas=[]
for i,(T,V,N,K,I) in enumerate(itertools.product([True,False],repeat=5),1):
 a=T and V and N; c=K and I; imp=not a or c
 linhas.append('| '+str(i)+' | '+' | '.join('V' if x else 'F' for x in (T,V,N,K,I,a,c,imp))+' |')
if '<!-- TABELA_R04 -->' in s:
 s=s.replace('<!-- TABELA_R04 -->',cab+'\n'.join(linhas))
 p.write_text(s,encoding='utf-8')

# Diagrama textual vetorial, explicitamente exigido pela atividade.
svg=['<svg xmlns="http://www.w3.org/2000/svg" width="1100" height="1080" viewBox="0 0 1100 1080">',
 '<defs><marker id="arrow" markerWidth="10" markerHeight="10" refX="8" refY="5" orient="auto"><path d="M0,0 L10,5 L0,10" fill="#31465a"/></marker></defs>',
 '<rect width="1100" height="1080" fill="white"/>',
 '<style>text{font-family:Arial,sans-serif;fill:#172e43;font-size:20px}.event{font-size:16px}.box{fill:#edf3f8;stroke:#31465a;stroke-width:2}.edge{fill:none;stroke:#31465a;stroke-width:2;marker-end:url(#arrow)}</style>']
def box(x,y,w,h,*ls):
 svg.append(f'<rect class="box" x="{x}" y="{y}" width="{w}" height="{h}" rx="5"/>')
 for i,l in enumerate(ls): svg.append(f'<text text-anchor="middle" x="{x+w/2}" y="{y+29+27*i}">{html.escape(l)}</text>')
def edge(d): svg.append(f'<path class="edge" d="{d}"/>')
def label(x,y,t): svg.append(f'<text class="event" x="{x}" y="{y}">{html.escape(t)}</text>')
svg.append('<text x="45" y="40" font-size="28" font-weight="bold">Máquina de estados do chamado de manutenção</text>')
box(400,85,300,70,'Aguardando ocorrência')
box(400,235,300,70,'Em triagem')
box(55,435,290,90,'Triagem inconclusiva')
box(405,435,290,90,'Hipótese identificada')
box(755,435,290,90,'Hipóteses concorrentes')
box(375,735,350,80,'Encaminhado para inspeção')
box(400,925,300,70,'Encerrado')
edge('M550 155 V235');label(565,195,'ocorrência registrada')
edge('M450 305 V360 H200 V435');label(75,345,'nenhuma regra satisfeita')
edge('M550 305 V435');label(565,415,'uma regra satisfeita')
edge('M650 305 V360 H900 V435');label(775,345,'várias regras satisfeitas')
edge('M200 525 V665 H405 V735');label(215,580,'encaminhamento sem hipótese')
edge('M550 525 V735');label(565,610,'encaminhamento');label(565,635,'normal ou prioritário')
edge('M900 525 V665 H695 V735');label(750,580,'critério aplicado');label(750,605,'normal ou prioritário')
edge('M55 470 H25 V270 H400');label(45,315,'coleta complementar')
edge('M550 815 V925');label(565,875,'inspeção finalizada')
svg.append('<text x="45" y="1040" class="event">Estado inicial: Aguardando ocorrência. Estado final: Encerrado.</text>')
svg.append('</svg>')
(docs/'maquina_estados.svg').write_text('\n'.join(svg),encoding='utf-8')

pdfmetrics.registerFont(TTFont('Arial','C:/Windows/Fonts/arial.ttf'))
pdfmetrics.registerFont(TTFont('ArialBold','C:/Windows/Fonts/arialbd.ttf'))
pdfmetrics.registerFont(TTFont('Consolas','C:/Windows/Fonts/consola.ttf'))
pdfmetrics.registerFont(TTFont('Logic','C:/Windows/Fonts/seguisym.ttf'))
pdfmetrics.registerFontFamily('Arial',normal='Arial',bold='ArialBold',italic='Arial',boldItalic='ArialBold')
styles=getSampleStyleSheet()
styles.add(ParagraphStyle(name='Corpo',fontName='Arial',fontSize=10.5,leading=14,spaceAfter=8))
styles.add(ParagraphStyle(name='Celula',fontName='Arial',fontSize=9,leading=12,spaceAfter=0))
styles.add(ParagraphStyle(name='Titulo',fontName='ArialBold',fontSize=23,leading=29,spaceAfter=20,textColor=colors.HexColor('#172e43')))
styles.add(ParagraphStyle(name='Secao',fontName='ArialBold',fontSize=16,leading=20,spaceBefore=13,spaceAfter=12,keepWithNext=True,textColor=colors.HexColor('#172e43')))
styles.add(ParagraphStyle(name='Subsecao',fontName='ArialBold',fontSize=12,leading=16,spaceBefore=9,spaceAfter=8,keepWithNext=True))
styles.add(ParagraphStyle(name='Codigo',fontName='Consolas',fontSize=8.2,leading=11,spaceAfter=12))
def fmt(t):
 t=html.escape(t)
 t=re.sub(r'\*\*(.*?)\*\*',r'<b>\1</b>',t)
 t=re.sub(r'`(.*?)`',r'<font name="Consolas">\1</font>',t)
 for c in '∧∨¬δ₀₁₂→⁵':
  t=t.replace(c,'<font name="Logic">'+c+'</font>')
 return t
width=A4[0]-84
story=[]
ls=s.splitlines();i=0
while i<len(ls):
 line=ls[i].strip()
 if not line: i+=1;continue
 if line.startswith('```'):
  i+=1; code=[]
  while i<len(ls) and not ls[i].startswith('```'):code.append(ls[i]);i+=1
  story.append(Preformatted('\n'.join(code),styles['Codigo']));i+=1;continue
 if line.startswith('|'):
  rows=[]
  while i<len(ls) and ls[i].strip().startswith('|'):
   cells=[x.strip() for x in ls[i].strip().strip('|').split('|')]
   if not all(re.match(r'^:?-+:?$',c) for c in cells): rows.append(cells)
   i+=1
  n=len(rows[0])
  if n==9: widths=[40]+[40]*5+[85,60,width-385]
  elif n==5: widths=[width*x for x in (.13,.22,.22,.26,.17)]
  elif n==4: widths=[width*x for x in (.19,.22,.22,.37)]
  elif n==3: widths=[width*x for x in (.19,.39,.42)]
  else: widths=[width/n]*n
  data=[[Paragraph(('<b>'+fmt(c)+'</b>') if j==0 else fmt(c),styles['Celula']) for c in row] for j,row in enumerate(rows)]
  tab=LongTable(data,colWidths=widths,repeatRows=1,hAlign='LEFT')
  tab.setStyle(TableStyle([('BACKGROUND',(0,0),(-1,0),colors.HexColor('#e1ebf3')),('VALIGN',(0,0),(-1,-1),'TOP'),('GRID',(0,0),(-1,-1),.4,colors.HexColor('#bdcad5')),('LEFTPADDING',(0,0),(-1,-1),6),('RIGHTPADDING',(0,0),(-1,-1),6),('TOPPADDING',(0,0),(-1,-1),7),('BOTTOMPADDING',(0,0),(-1,-1),7),('ROWBACKGROUNDS',(0,1),(-1,-1),[colors.white,colors.HexColor('#f6f8fa')])]))
  story.extend([tab,Spacer(1,13)]);continue
 if line.startswith('# '): story.append(Paragraph(fmt(line[2:]),styles['Titulo']))
 elif line.startswith('## '):
  story.append(Paragraph(fmt(line[3:]),styles['Secao']))
 elif line.startswith('### '):story.append(Paragraph(fmt(line[4:]),styles['Subsecao']))
 else:story.append(Paragraph(fmt(line),styles['Corpo']))
 i+=1
def rodape(canvas,doc):
 canvas.setFont('Arial',8);canvas.setFillColor(colors.HexColor('#526577'))
 canvas.drawString(42,24,'Projeto Manutenção Inteligente | Situação de Aprendizagem 02')
 canvas.drawRightString(A4[0]-42,24,str(doc.page))
doc=SimpleDocTemplate(str(docs/'Dossie.pdf'),pagesize=A4,rightMargin=42,leftMargin=42,topMargin=40,bottomMargin=42,title='Dossiê técnico do Projeto Manutenção Inteligente',author='Projeto Manutenção Inteligente')
doc.build(story,onFirstPage=rodape,onLaterPages=rodape)
print('Dossiê PDF e diagrama gerados.')
