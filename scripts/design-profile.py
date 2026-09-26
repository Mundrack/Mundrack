from pathlib import Path
from html import escape
import textwrap
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
def row(images): return '<p align="center">'+'\n'.join(images)+'</p>\n'
def section(name,alt): return f'\n<img src="assets/{name}.svg" width="100%" alt="{alt}" />\n\n'
buttons='<p align="center"><a href="https://mundrack.github.io"><img src="assets/enter-realm.svg" width="280" alt="Entrar al reino: portfolio" /></a> <a href="https://github.com/Mundrack?tab=repositories"><img src="assets/view-repositories.svg" width="235" alt="Mis repositorios" /></a></p>'
s='<div align="center">\n<a href="https://mundrack.github.io"><img src="assets/mundrack-gothic-hero.png" width="100%" alt="Mundrack — The Kingdom of Code. Caballero dorado, catedral y dragón." /></a>\n</div>\n\n'+intro+'\n\n'+buttons+'\n\n'+bio+'\n\n'
s+=row(cards[:2])+row(cards[2:])+section('campaigns','Campañas y colaboraciones')+row(projects[:2])+row(projects[2:])
s+=section('arsenal','Arsenal: herramientas y disciplinas')+row(arsenal[:2])+row(arsenal[2:])+'\n'+relic+'\n\n'
s+='[Interconexión de sistemas](https://github.com/Mundrack/Interconexion_de_sistemas) · [Proyecto IA Accidentes](https://github.com/Mundrack/Proyecto_IA_Accidentes)\n\n'
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

[Interconexión de sistemas](https://github.com/Mundrack/Interconexion_de_sistemas) y [Proyecto IA Accidentes](https://github.com/Mundrack/Proyecto_IA_Accidentes) conservan mis primeros aprendizajes. Sigo explorando automatización, inteligencia artificial y seguridad.

[Entrar al portfolio](https://mundrack.github.io) · [Ver repositorios](https://github.com/Mundrack?tab=repositories)

El portfolio incluye una batalla 3D en evolución; los proyectos pueden explorarse sin reproducirla. El arte del perfil es original y estático.

</details>
'''
(ROOT/'README.md').write_text(s,encoding='utf-8')
print('Generated ornamental profile panels and accessible README.')
