from pathlib import Path
from html import escape
import textwrap
import re
import json
ROOT=Path(__file__).resolve().parents[1]
A=ROOT/'assets'
def panel(name,title,lines,kicker='',w=460):
    wrapped=[]
    for line in lines: wrapped.extend(textwrap.wrap(line, 31 if w==460 else 58) or [''])
    h=148+len(wrapped)*33
    parts=[f'<svg xmlns="http://www.w3.org/2000/svg" width="{w}" height="{h}" viewBox="0 0 {w} {h}" role="img" aria-labelledby="title desc"><title id="title">{escape(title)}</title><desc id="desc">{escape(" ".join(lines))}</desc>',
    '<defs><linearGradient id="stone" x2="0" y2="1"><stop stop-color="#252126"/><stop offset=".55" stop-color="#151419"/><stop offset="1" stop-color="#201517"/></linearGradient><linearGradient id="gold"><stop stop-color="#6e4825"/><stop offset=".4" stop-color="#ebcb86"/><stop offset=".6" stop-color="#c39a54"/><stop offset="1" stop-color="#6e4825"/></linearGradient></defs>',
    f'<path d="M22 3 H{w-22} L{w-3} 22 V{h-22} L{w-22} {h-3} H22 L3 {h-22} V22 Z" fill="url(#stone)" stroke="url(#gold)" stroke-width="2"/>',
    f'<path d="M28 12 H{w-28} L{w-12} 28 V{h-28} L{w-28} {h-12} H28 L12 {h-28} V28 Z" fill="none" stroke="#57402b"/>']
    # Carved masonry courses, heraldic tracery and candle niches.
    for y in range(32,h-16,22):
        parts.append(f'<path d="M16 {y} H{w-16}" stroke="#544338" opacity=".16"/>')
    for x in [42,w-42]:
        for y in range(65,h-42,25):
            parts.append(f'<path d="M{x} {y} q-16 -13 -17 0 q1 13 17 0 q16 -13 17 0 q-1 13 -17 0" fill="none" stroke="#b18b4f" opacity=".36"/>')
    # Recessed gothic windows and pillars behind the inscriptions.
    for x in [42,w-92]:
        parts.append(f'<g opacity=".48"><path d="M{x} {h-26} V80 Q{x} 46 {x+25} 27 Q{x+50} 46 {x+50} 80 V{h-26} Z" fill="#291b25" stroke="#947047"/><path d="M{x+6} {h-28} V82 Q{x+6} 52 {x+25} 37 Q{x+44} 52 {x+44} 82 V{h-28} M{x+25} 38 V{h-28} M{x+2} 91 H{x+48}" fill="none" stroke="#8d673b"/><path d="M{x+5} 76 L{x+25} 56 L{x+45} 76 L{x+25} 96 Z" fill="#682d32" stroke="#b5894b"/></g>')
    parts.append(f'<path d="M88 {h-22} V85 Q88 35 {w/2} 15 Q{w-88} 35 {w-88} 85 V{h-22}" fill="none" stroke="#7e5e37" opacity=".45"/>')
    # Keep lettering on a quiet central surface, architecture at the margins.
    parts.append(f'<rect x="65" y="22" width="{w-130}" height="{h-44}" rx="20" fill="#141216" opacity=".77"/>')
    for x in [27,w-27]:
        parts.append(f'<path d="M{x-4} 61 V{h-61} M{x+4} 61 V{h-61}" stroke="#b49157" opacity=".5"/>')
        parts.append(f'<g fill="#b89960" stroke="#715430"><path d="M{x-7} {h-32} h14 l-3 -7 h-8 Z"/><rect x="{x-2}" y="{h-60}" width="4" height="21"/><path d="M{x} {h-73} q-6 9 0 13 q6 -4 0 -13" fill="#f1ce85"/></g>')
    # A tiny rose-window seal at the foot of every card.
    parts.append(f'<g transform="translate({w/2} {h-17})" stroke="#b58b4c" fill="none"><circle r="9"/><circle r="12"/>')
    for angle in range(0,360,45):
        parts.append(f'<ellipse cx="0" cy="-4" rx="2" ry="4" transform="rotate({angle})"/>')
    parts.append('</g>')
    # Engraved corner ornaments, mirrored rather than large external textures.
    for x,y,sx,sy in [(16,16,1,1),(w-16,16,-1,1),(16,h-16,1,-1),(w-16,h-16,-1,-1)]:
        parts.append(f'<g transform="translate({x} {y}) scale({sx} {sy})" fill="none" stroke="#b38b4e"><path d="M0 42 V12 Q0 0 12 0 H42 M6 32 Q24 32 17 17 Q32 24 32 6 M3 3 L20 20 M10 5 Q25 5 25 15"/><path d="M8 8 l4 -4 4 4 -4 4 Z" fill="#b38b4e"/></g>')
    parts += [f'<text x="{w/2}" y="39" text-anchor="middle" font-family="Georgia,serif" font-size="14" letter-spacing="3" fill="#c19a62">{escape(kicker)}</text>',
      f'<text x="{w/2}" y="80" text-anchor="middle" font-family="Palatino Linotype,Palatino,Georgia,serif" font-size="{30 if w==460 else 38}" letter-spacing="1.5" fill="#f1d9a0">{escape(title)}</text>',
      f'<path d="M55 100 H{w/2-18} M{w/2+18} 100 H{w-55}" stroke="url(#gold)"/><path d="M{w/2} 92 l8 8 -8 8 -8 -8 Z" fill="#852d35" stroke="#c7a56a"/>']
    for i,line in enumerate(wrapped):
        parts.append(f'<text x="{w/2}" y="{140+i*33}" text-anchor="middle" font-family="Palatino Linotype,Palatino,Georgia,serif" font-size="{23 if w==460 else 29}" fill="#ded5c3">{escape(line)}</text>')
    parts.append('</svg>')
    (A/(name+'.svg')).write_text('\n'.join(parts),encoding='utf-8')
    return f'<img src="assets/{name}.svg" width="{440 if w==460 else "100%"}" alt="{escape(title+": "+" ".join(lines),quote=True)}" />'
intro=panel('royal-oath','THE KINGDOM OF MUNDRACK',['Cada línea de código, un guerrero.','Cada proyecto, una conquista.'],'SOFTWARE · CALIDAD · IA · AUTOMATIZACIÓN',960)
bio=panel('royal-chronicle','CRÓNICAS DEL REINO',['Mateo Gabriel Puga Montesdeoca','Ingeniería de Software · UDLA · Quito, Ecuador','','Construyo sistemas y automatizo procesos.','Pruebas, documentación y mejora continua:','calidad desde la primera línea.'],'EL ARTÍFICE DEL REINO',960)
cards=[]
for name,title,lines,kicker in [
 ('craft-forge','FORJAR',['Desarrollo de software','e integración de sistemas.'],'I · ACERO Y PROPÓSITO'),
 ('craft-guard','PROTEGER',['QA, testing y validación.','Construir con confianza.'],'II · EL JURAMENTO'),
 ('craft-discover','DESCUBRIR',['Inteligencia artificial','y análisis de desinformación.'],'III · CONOCIMIENTO'),
 ('craft-connect','CONECTAR',['Automatización con n8n','y Docker. Procesos unidos.'],'IV · ALIANZAS')]: cards.append(panel(name,title,lines,kicker))
projects=[]
for name,title,lines,kicker in [
 ('quest-veritai','VERITAI',['Detección de contenido por IA','y análisis de desinformación.'],'EN DESARROLLO'),
 ('quest-risk','RISK PLATFORM',['Auditorías y gestión','organizacional.'],'PARTICIPACIÓN COMPLETADA'),
 ('quest-cyber','CYBERLAB',['Plataforma educativa','de ciberseguridad.'],'PARTICIPACIÓN COMPLETADA'),
 ('quest-eos','EOS',['Migración e integración','de sistemas empresariales.'],'PARTICIPACIÓN COMPLETADA')]: projects.append(panel(name,title,lines,kicker))
arsenal=[]
for name,title,lines,kicker in [
 ('tools-languages','LENGUAJES',['Python · JavaScript','TypeScript · React'],'RUNAS DE CREACIÓN'),
 ('tools-data','DATOS',['MySQL · Supabase','Estructura y persistencia.'],'LOS ARCHIVOS'),
 ('tools-workflow','AUTOMATIZACIÓN',['n8n · Docker','Procesos e integraciones.'],'LA FORJA'),
 ('tools-quality','CALIDAD',['Git · GitHub','QA · Testing · Validación'],'EL ESCUDO')]: arsenal.append(panel(name,title,lines,kicker))
relic=panel('royal-archive','EL CAMINO RECORRIDO',['Primeras campañas, aprendizajes y experimentos.','Cada paso también forma parte del reino.'],'ARCHIVO DE MUNDRACK',960)
footer=panel('royal-finale','THIS IS MY KINGDOM',['THE KINGDOM OF MUNDRACK','','Calidad sobre cantidad.','Construir, aprender y volver a forjar.'],'EL REINO SIGUE CRECIENDO',960)
def row(images): return '<p align="center">'+' '.join(images)+'</p>\n'
def section(name,alt):
    filename = 'campaigns-cathedral.png' if name == 'campaigns' else name+'.svg'
    return f'\n<img src="assets/{filename}" width="100%" alt="{alt}" />\n\n'
buttons='<p align="center"><a href="https://mundrack.github.io"><img src="assets/enter-realm.svg" width="280" alt="Entrar al reino: portfolio" /></a> <a href="https://github.com/Mundrack?tab=repositories"><img src="assets/view-repositories.svg" width="235" alt="Mis repositorios" /></a></p>'
s='<div align="center">\n<a href="https://mundrack.github.io"><img src="assets/mundrack-gothic-hero.png" width="100%" alt="Mundrack — The Kingdom of Code. Caballero dorado, catedral y dragón." /></a>\n</div>\n\n'+intro+'\n\n'+buttons+'\n\n'+bio+'\n\n'
s+=row(cards[:2])+row(cards[2:])+section('campaigns','Campañas y colaboraciones')+row(projects[:2])+row(projects[2:])
s+=section('arsenal','Arsenal: herramientas y disciplinas')+row(arsenal[:2])+row(arsenal[2:])+'\n'+relic+'\n\n'
s+='[Interconexión de sistemas](https://github.com/Mundrack/Interconeccion_de_sistemas) · [Proyecto IA Accidentes](https://github.com/Mundrack/Proyecto_IA_Accidentes)\n\n'
s+=footer+'\n\n'+buttons+'\n\n'
s+='''<details>
<summary>Leer el perfil en texto · Información y enlaces accesibles</summary>

## Mateo Gabriel Puga Montesdeoca

Estudiante de Ingeniería de Software en la UDLA, Quito, Ecuador. Construyo sistemas, analizo requerimientos y automatizo procesos. Trabajo con pruebas, documentación y mejora continua.

- **Desarrollo:** software e integración de sistemas.
- **Calidad:** QA, testing y validación.
- **Investigación:** inteligencia artificial y análisis de desinformación.
- **Automatización:** n8n y Docker.

### Proyectos y colaboraciones

- **VERITAI:** detección de contenido generado por IA y análisis de desinformación. En desarrollo.
- **Risk Platform:** auditorías y gestión organizacional. Participación completada.
- **CyberLab:** plataforma educativa de ciberseguridad. Participación completada.
- **EOS:** migración e integración de sistemas empresariales. Participación completada.

### Herramientas

Python, JavaScript, TypeScript, React, MySQL, Supabase, n8n, Docker, Git y GitHub.

### Archivo y laboratorio

[Interconexión de sistemas](https://github.com/Mundrack/Interconeccion_de_sistemas) y [Proyecto IA Accidentes](https://github.com/Mundrack/Proyecto_IA_Accidentes) conservan mis primeros aprendizajes. Sigo explorando automatización, inteligencia artificial y seguridad.

[Entrar al portfolio](https://mundrack.github.io) · [Ver repositorios](https://github.com/Mundrack?tab=repositories)

El portfolio incluye una batalla 3D en evolución; los proyectos pueden explorarse sin reproducirla. El arte del perfil es original y estático.

</details>
'''
# Decorative plates link to the accessible transcript instead of GitHub's
# automatic image-file viewer. Existing explicit navigation remains intact.
def link_image(match):
    before,img,after=match.groups()
    if before: return match.group(0)
    return '<a href="#perfil-en-texto">'+img+'</a>'
s=re.sub(r'(<a\b[^>]*>)?(<img\b[^>]*>)(</a>)?',link_image,s)
s=s.replace('<details>', '<a name="perfil-en-texto"></a>\n<details>')
repositories=[
 ('semester','SEGUNDO SEMESTRE','SegundoSemestre','C'),
 ('files','ARCHIVOS','PraticaArchivos','C'),
 ('security','SEGURIDAD','proyectoFinalSeguirdadInformatica','HTML'),
 ('accidents','IA · ACCIDENTES','Proyecto_IA_Accidentes','HTML'),
 ('systems','INTERCONEXIÓN','Interconeccion_de_sistemas','JavaScript'),
 ('guild','GREMIO','Gremio','Proyecto público'),
]
gallery=[]
for key,title,repo,language in repositories:
    card=panel('repository-'+key,title,[language,'Abrir repositorio en GitHub →'],'LOS ARCHIVOS DEL REINO')
    gallery.append(f'<a href="https://github.com/Mundrack/{repo}">{card}</a>')
gallery_html='\n'+''.join(row(gallery[i:i+2]) for i in range(0,len(gallery),2))
cathedral='<p align="center"><a href="https://mundrack.github.io"><img src="assets/cathedral-finale.png" width="100%" alt="The Kingdom of Mundrack: una catedral de piedra, vitrales y oro. Abrir el portfolio." /></a></p>\n'
s=s.replace('<a href="#perfil-en-texto"><img src="assets/royal-finale.svg"',gallery_html+'<a href="#perfil-en-texto"><img src="assets/royal-finale.svg"')
s=s.replace('<a name="perfil-en-texto"></a>',cathedral+'\n<a name="perfil-en-texto"></a>')
activity=json.loads((ROOT/'data/activity.json').read_text(encoding='utf-8'))
days=activity['days']; total=sum(d['count'] for d in days)
calendar=f'''<a name="cronicas-de-actividad"></a>
<p align="center"><a href="https://github.com/Mundrack?tab=overview"><picture><source media="(max-width: 600px)" srcset="assets/activity-calendar-mobile.svg" /><img src="assets/activity-calendar.svg" width="100%" alt="Crónicas de actividad: {total} contribuciones visibles sin sesión, del {days[0]['date']} al {days[-1]['date']}." /></picture></a></p>

<p align="center"><sub>Copia de la vista pública · Actualizada {activity['fetchedAt'][:10]} UTC · Puede diferir de tu vista con sesión iniciada.</sub><br><a href="data/activity.csv">Consultar datos por día</a> · <a href="https://github.com/users/Mundrack/contributions">Ver fuente en GitHub</a></p>

'''
s=s.replace(cathedral,calendar+cathedral)
(ROOT/'README.md').write_text(s,encoding='utf-8')
print('Generated ornamental profile panels and accessible README.')
