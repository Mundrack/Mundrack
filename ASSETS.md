# Arte del perfil

## Fases de la actualización de campañas y actividad

1. Arte: `assets/campaigns-cathedral.png`, cabecera original generada con ImageGen integrado. Las placas vectoriales incorporan mampostería, tracerías, velas y pequeños rosetones. Los archivos anteriores se conservan.
2. Datos: `data/activity.json` y `data/activity.csv` registran la vista pública de contribuciones, obtenida sin cookies ni credenciales de https://github.com/users/Mundrack/contributions . El rango corresponde a las semanas completas que muestra GitHub; no se inventan eventos ni se consultan repositorios privados. Los totales pueden diferir de la vista del propietario con sesión iniciada.
3. Presentación: `assets/activity-calendar.svg` para escritorio y `assets/activity-calendar-mobile.svg` para móvil mediante `<picture>`. GitHub sigue mostrando su calendario nativo fuera del README. Los gráficos son una copia fechada, no datos en vivo.

### Actualización manual

```sh
python scripts/refresh-activity.py
python scripts/design-profile.py
python -m unittest discover -s tests
```

El primer script solo usa la biblioteca estándar de Python. Si GitHub cambia su HTML, faltan días o la respuesta es inválida, falla antes de reemplazar la copia anterior. No hay servicios externos, tokens ni tareas programadas. `--offline` regenera los SVG usando la copia existente. Después de actualizar, hay que revisar y subir los archivos a GitHub.

### Prompt de la cabecera de campañas

Use case: stylized-concept. Final wide 3:1 chapter banner for Mundrack's medieval gothic GitHub profile. Original glorious dark fantasy cathedral armory. Elaborate carved black stone pointed arch spanning the frame, gold tracery, bronze heraldic shields and crossed swords at the sides, crimson velvet banners, candles, shadowy shelves of ancient books, golden dust in shafts of light. Rich painterly cinematic detail matching a premium gothic fantasy game title screen. In the quiet dark central area, large legible engraved antique gold serif words exactly 'CAMPAÑAS DEL REINO'. Underneath in smaller gold capitals exactly 'OBRAS · ALIANZAS · CONQUISTAS'. All lettering inside safe margins. Decorative detail concentrated at the borders, restrained center. No characters, no logos, no modern items, no UI mockup, no watermark. Rectangular artwork fills the image, not a photograph of an object.

Portada: `assets/mundrack-gothic-hero.png`. Generada con la herramienta integrada ImageGen; no se usó la API por CLI. Arte original de fantasía oscura, inspirado en la atmósfera gótica solicitada, sin personajes ni logotipos de Diablo. La portada es estática.

Los botones, placas de sección y separadores son SVG originales, sin JavaScript ni recursos externos. El texto profesional permanece como Markdown/HTML accesible. El archivo anterior `assets/realm-cinematic.webp` se conserva.

## Prompt de la portada

Create a finished premium GitHub profile hero banner for MUNDRACK, original epic medieval dark fantasy with the glorious gothic action RPG atmosphere of Diablo III, but no Diablo logos or existing characters. Wide landscape 3:1 composition. Blackened cathedral stone, intricately engraved aged gold frame, deep oxblood accents, embers, shafts of holy warm gold against smoky cold slate. Left third: imposing original fully armored knight with ornate gold and black plate, closed helmet, upright sword. Right third: distant ruined gothic citadel, a majestic dark dragon silhouette in clouds. Center: large extremely legible engraved antique gold serif title exactly 'MUNDRACK', underneath smaller spaced uppercase exactly 'THE KINGDOM OF CODE'. Center background quiet and dark for legibility. Cinematic painterly realism, rich material detail, glorious and solemn rather than cartoonish, restrained tasteful ornament. Entire title and frame inside safe margins. No extra text, no UI mockup, no watermark. This is the final rectangular banner image itself, edge to edge.

## Ornamentación completa del perfil

Las placas `royal-*.svg`, `craft-*.svg`, `quest-*.svg` y `tools-*.svg` se generan con `python scripts/design-profile.py`. Incluyen marcos grabados, detalles carmesí y tipografía serif de la familia Palatino/Georgia, con alternativas según el dispositivo. Son gráficos vectoriales originales, sin fuentes externas ni scripts. No cambian la interfaz externa de GitHub.

El README conserva el contenido completo en un desplegable de texto accesible y añade alternativas descriptivas a todas las placas. Los SVG no contienen enlaces internos: los enlaces navegables se encuentran en el README.

## Catedral y navegación

`assets/cathedral-finale.png`: nueva ilustración original creada con ImageGen integrado. La portada anterior permanece sin cambios. Las tarjetas ahora incorporan arcos apuntados, vitrales y pilares vectoriales. Los repositorios se enlazan mediante sus nombres reales en GitHub. Todas las imágenes tienen destino explícito en el README: portfolio, repositorio o transcripción accesible, evitando el visor automático de imágenes. Las tarjetas nativas de GitHub y el calendario de contribuciones no se pueden tematizar desde el README; la galería ornamental se añade dentro de este.

### Prompt del cierre

Create a finished wide 3:1 footer banner for a GitHub profile of MUNDRACK. Original glorious gothic medieval dark fantasy, premium painterly cinematic realism. Interior of a vast ruined cathedral: pointed arches, carved black stone pillars, intricate gold filigree framing ALL edges, dark crimson hanging banners, candlelit altar, luminous gold rose window high above. Center floor and background dark and calm, symmetrical monumental composition, great depth and real ornate architectural detail. Center extremely legible antique gold engraved serif text exactly 'THE KINGDOM OF MUNDRACK'. Below smaller exact text 'CONSTRUIR · APRENDER · VOLVER A FORJAR'. Rich contrast, aged gold highlights, smoky slate and warm torchlight, black obsidian. Match the mood of an epic fantasy game main menu, not a flat vector plaque. No other words, no buttons, no logos, no watermark. All text inside safe margins. Final artwork only.
