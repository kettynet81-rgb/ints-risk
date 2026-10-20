import re,json,sys
h=open('plan.html',encoding='utf-8').read()
h=re.sub(r'</strong><strong>','',h)
h=re.sub(r'<ol type="1">','<ul class="dash">',h); h=h.replace('</ol>','</ul>')
h=re.sub(r'</ul>\s*<ul class="dash">','',h)
h=h.replace('<blockquote>','<div class="ind">').replace('</blockquote>','</div>')
h=re.sub(r'<p>- \d+ -</p>\s*','',h)
h=re.sub(r'<img src="\./media/image1\.png"[^>]*>','<img src="org.png" alt="위험성평가 추진 조직도" style="width:100%">',h,flags=re.S)
h=re.sub(r'<colgroup>.*?</colgroup>','',h,flags=re.S)
h=re.sub(r' class="(odd|even|header)"','',h)
marks=[('cover','표지',None),
 ('policy','안전보건경영방침','<p><strong>안전보건경영방침</strong></p>'),
 ('goal','안전보건 목표','<p><strong>2026년 안전보건 목표</strong></p>'),
 ('plan','실시계획서 본문','<p><strong>위험성평가 실시계획서</strong></p>\n<p><strong>1.'),
 ('annual','연간계획서','<table>\n<tbody>\n<tr>\n<td rowspan="2"></td>'),
 ('notice','실시 공고','<p><strong>위험성평가 실시 공고</strong></p>'),
 ('meeting','회의결과(양식)','<p><strong>위험성평가 회의결과</strong></p>'),
 ('edu','교육결과 보고서(양식)','<p><strong>위험성평가 교육실시 결과 보고서</strong></p>'),
 ('budget','예산 편성·집행','<p><strong>위험성평가 예산 편성 및 집행 내역</strong></p>'),
 ('attach','첨부 목록','<p><strong>첨부 (2025'),]
pos=[0]
for k,t,m in marks[1:]:
    i=h.rfind('<table>',0,h.find('<strong>결</strong>')) if k=='annual' else h.find(m)
    if i<0: print('MISSING',k,file=sys.stderr); sys.exit(1)
    pos.append(i)
pos.append(len(h))
out=[]
TITLES=['위험성평가 실시계획서','안전보건경영방침','2026년 안전보건 목표','위험성평가 연간계획서','위험성평가 실시 공고','위험성평가 회의결과','위험성평가 교육실시 결과 보고서','위험성평가 예산 편성 및 집행 내역','첨 부 양 식']
def fmt(k,x):
    for t in TITLES:
        x=x.replace('<p><strong>'+t+'</strong></p>','<h1>'+t+'</h1>',1)
    x=re.sub(r'<p><strong>(\d+\. [^<]+)</strong></p>',r'<h2>\1</h2>',x)
    x=x.replace('<p>주식회사 아이엔티에스</p>','<p class="c">주식회사 아이엔티에스</p>')
    x=re.sub(r'<p>(\d{4}년 \d{2}월 \d{2}일|2026년 +월 +일)</p>',r'<p class="c">\1</p>',x)
    x=re.sub(r'<p>(<strong>㈜아이엔티에스 대표 박 종 성</strong> \(인\))</p>',r'<p class="c">\1</p>',x)
    if k=='cover':
        x=x.replace('<p>2026년</p>','<p class="c" style="font-size:20pt;margin-top:40mm">2026년</p>').replace('<h1>위험성평가 실시계획서</h1>','<h1 style="font-size:28pt;margin:6mm 0">위험성평가 실시계획서</h1>').replace('<p>Risk Assessment Implementation Plan</p>','<p class="c" style="margin-bottom:60mm">Risk Assessment Implementation Plan</p>')
        x=x.replace('<table>','<table style="width:70%;margin:0 auto;font-size:13pt">')
    return x
for n,(k,t,m) in enumerate(marks):
    out.append({'id':k,'title':t,'html':fmt(k,h[pos[n]:pos[n+1]].strip())})
for o in out: print(o['id'],len(o['html']),re.sub('<[^>]+>','',o['html'])[:40].replace('\n',' '))
open('../docs-seed.js','w',encoding='utf-8').write('window.DOCS_SEED='+json.dumps(out,ensure_ascii=False)+';\n')
