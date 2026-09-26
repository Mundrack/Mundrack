"""Public GitHub activity snapshot; no credentials, external service or invented data.
Run manually: python scripts/refresh-activity.py. Fail closed on markup changes.
"""
from datetime import date, datetime, timedelta, timezone
from html import escape
from html.parser import HTMLParser
from pathlib import Path
from urllib.request import Request, urlopen
import argparse, csv, io, json, re
ROOT = Path(__file__).resolve().parents[1]
SOURCE = 'https://github.com/users/Mundrack/contributions'

class CalendarParser(HTMLParser):
    def __init__(self):
        super().__init__(); self.cells = {}; self.tips = {}; self.current = None; self.buffer = []
    def handle_starttag(self, tag, attrs):
        a = dict(attrs)
        if tag == 'td' and 'data-date' in a:
            key = a['id']
            if key in self.cells: raise ValueError('Duplicate calendar cell')
            self.cells[key] = {'date': a['data-date'], 'level': int(a['data-level'])}
        if tag == 'tool-tip': self.current = a.get('for'); self.buffer = []
    def handle_data(self, text):
        if self.current: self.buffer.append(text)
    def handle_endtag(self, tag):
        if tag == 'tool-tip' and self.current:
            self.tips[self.current] = ''.join(self.buffer).strip(); self.current = None

def parse_calendar(html, today):
    parser = CalendarParser(); parser.feed(html)
    days = []
    for key, cell in parser.cells.items():
        day = date.fromisoformat(cell['date'])
        if day > today: continue
        tip = parser.tips.get(key, '')
        match = re.match(r'(No|[\d,]+) contributions? on ', tip)
        if not match or cell['level'] not in range(5): raise ValueError('Unrecognized calendar markup; retaining old files')
        count = 0 if match[1] == 'No' else int(match[1].replace(',', ''))
        if (count == 0) != (cell['level'] == 0): raise ValueError('Inconsistent activity level')
        days.append({**cell, 'count': count})
    days.sort(key=lambda d: d['date'])
    if not 365 <= len(days) <= 371: raise ValueError('Incomplete public calendar')
    dates = [date.fromisoformat(d['date']) for d in days]
    if any(b-a != timedelta(days=1) for a,b in zip(dates, dates[1:])): raise ValueError('Duplicate or missing dates')
    if not 0 <= (today-dates[-1]).days <= 1: raise ValueError('Stale source calendar')
    return days

COLORS = ['#211d24', '#583039', '#8f4141', '#bd884d', '#f1ce83']
MONTHS = ['ENE','FEB','MAR','ABR','MAY','JUN','JUL','AGO','SEP','OCT','NOV','DIC']
def render(snapshot, mobile=False):
    days = snapshot['days']; first = date.fromisoformat(days[0]['date'])
    sunday = first - timedelta(days=(first.weekday()+1)%7)
    totalweeks = ((date.fromisoformat(days[-1]['date'])-sunday).days//7)+1
    width = 460 if mobile else 960; columns = 14 if mobile else totalweeks
    blocks = (totalweeks+columns-1)//columns
    pitch = 26 if mobile else 16; cell = pitch-3
    height = 245+blocks*235 if mobile else 390
    total = sum(d['count'] for d in days)
    text = lambda x,y,label,size=18,color='#d6c9b1',anchor='start': f'<text x="{x}" y="{y}" font-family="Georgia,serif" font-size="{size}" fill="{color}" text-anchor="{anchor}">{escape(str(label))}</text>'
    out=[f'<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}" viewBox="0 0 {width} {height}" role="img" aria-labelledby="title desc"><title id="title">Crónicas de actividad de Mundrack</title><desc id="desc">{total} contribuciones visibles sin sesión. Del {days[0]["date"]} al {days[-1]["date"]}. Copia actualizada {snapshot["fetchedAt"]}.</desc>',
      '<defs><linearGradient id="stone" x2="0" y2="1"><stop stop-color="#28212a"/><stop offset="1" stop-color="#0f1015"/></linearGradient><linearGradient id="gold"><stop stop-color="#6e4825"/><stop offset=".5" stop-color="#e4c37c"/><stop offset="1" stop-color="#6e4825"/></linearGradient></defs>',
      f'<path d="M24 3 H{width-24} L{width-3} 24 V{height-24} L{width-24} {height-3} H24 L3 {height-24} V24 Z" fill="url(#stone)" stroke="url(#gold)" stroke-width="2"/>',
      f'<rect x="12" y="12" width="{width-24}" height="{height-24}" rx="10" fill="none" stroke="#635032"/>',
      text(width/2,48,'CRÓNICAS DE ACTIVIDAD',25 if mobile else 32,'#ebcf96','middle'),
      text(width/2,84,f'{total} contribuciones visibles',23,'#ebcf96','middle'),
      text(width/2,112,f'{days[0]["date"]} — {days[-1]["date"]}',17,'#c3b49e','middle')]
    for block in range(blocks):
        base_y=160+block*235; base_x=55 if mobile else 80
        last_month=None
        for week in range(block*columns,min((block+1)*columns,totalweeks)):
            day=sunday+timedelta(weeks=week)
            # A partial month at the left edge may have only one column;
            # omit its label so it does not collide with the next month.
            if week == block*columns and (day+timedelta(days=7)).month != day.month:
                last_month=day.month
                continue
            if day.month!=last_month and (week%columns)<columns-2:
                out.append(text(base_x+(week%columns)*pitch,base_y-10,MONTHS[day.month-1],14)); last_month=day.month
        for row,label in [(1,'L'),(3,'M'),(5,'V')]: out.append(text(base_x-23,base_y+row*pitch+cell-2,label,14))
        for item in days:
            dt=date.fromisoformat(item['date']); offset=(dt-sunday).days; week=offset//7
            if week//columns != block: continue
            x=base_x+(week%columns)*pitch; y=base_y+(offset%7)*pitch
            out.append(f'<rect x="{x}" y="{y}" width="{cell}" height="{cell}" rx="2" fill="{COLORS[item["level"]]}" stroke="#695137" stroke-width=".5"><title>{item["date"]}: {item["count"]} contribuciones</title></rect>')
    y=height-76
    out.append(text(width/2-122,y+14,'Menos',15))
    for level,color in enumerate(COLORS): out.append(f'<rect x="{width/2-55+level*23}" y="{y}" width="18" height="18" rx="2" fill="{color}" stroke="#695137"/>')
    out.append(text(width/2+69,y+14,'Más',15))
    out.append(text(width/2,height-35,'Vista pública · '+snapshot['fetchedAt'][:10]+' UTC',16,'#b9aa93','middle'))
    out.append('</svg>'); return '\n'.join(out)

def main():
    parser=argparse.ArgumentParser(); parser.add_argument('--offline',action='store_true'); args=parser.parse_args()
    target=ROOT/'data/activity.json'
    if args.offline: snapshot=json.loads(target.read_text(encoding='utf-8'))
    else:
        now=datetime.now(timezone.utc)
        request=Request(SOURCE,headers={'User-Agent':'Mundrack-Profile/1.0','Accept-Language':'en'})
        with urlopen(request,timeout=30) as response: html=response.read().decode('utf-8')
        snapshot={'source':SOURCE,'visibility':'public-unauthenticated','fetchedAt':now.isoformat(timespec='seconds'),'days':parse_calendar(html,now.date())}
    # Render everything before replacing valid files; failures never publish zeros.
    desktop=render(snapshot); mobile=render(snapshot,True)
    target.parent.mkdir(exist_ok=True)
    target.write_text(json.dumps(snapshot,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
    (ROOT/'assets/activity-calendar.svg').write_text(desktop,encoding='utf-8')
    (ROOT/'assets/activity-calendar-mobile.svg').write_text(mobile,encoding='utf-8')
    output=io.StringIO(); writer=csv.writer(output,lineterminator='\n'); writer.writerow(['date','contributions','github_level'])
    writer.writerows((d['date'],d['count'],d['level']) for d in snapshot['days'])
    (ROOT/'data/activity.csv').write_text(output.getvalue(),encoding='utf-8')
    print(f'Public activity: {sum(d["count"] for d in snapshot["days"])} contributions, {len(snapshot["days"])} days. Updated {snapshot["fetchedAt"]}.')
if __name__=='__main__': main()
