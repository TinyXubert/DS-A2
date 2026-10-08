"""Refresh the opening abstract from the saved completed run, then export HTML/PDF."""
from pathlib import Path
import os, re, json, hashlib, argparse
BASE = Path(__file__).resolve().parent
for key, sub in {'TMPDIR':'tmp', 'JUPYTER_CONFIG_DIR':'jupyter', 'IPYTHONDIR':'ipython'}.items():
    path = BASE / '.runtime' / sub
    path.mkdir(parents=True, exist_ok=True)
    os.environ[key] = str(path)
os.environ.setdefault('PLAYWRIGHT_BROWSERS_PATH', str(BASE / '.runtime/browsers'))
import nbformat
from nbconvert import HTMLExporter, MarkdownExporter
parser = argparse.ArgumentParser()
parser.add_argument('--pdf', action='store_true', help='Also print PDF using local Playwright Chromium')
args = parser.parse_args()
nb = nbformat.read(BASE / 'A2.ipynb', as_version=4)
nbformat.validate(nb)
code = [c for c in nb.cells if c.cell_type == 'code']
counts = [c.execution_count for c in code]
if any(c is None for c in counts) or counts != sorted(set(counts)):
    raise SystemExit('Run all code cells in order and save A2.ipynb before exporting.')
if any(o.output_type == 'error' for c in code for o in c.outputs):
    raise SystemExit('Preserve the failed notebook, fix errors, rerun and save before exporting.')
last_output = ''.join(o.get('text','') for o in code[-1].outputs)
match = re.search(r'RESULT_DIR: (results/[^\s]+)', last_output)
if not match:
    raise SystemExit('Completed-run marker missing in saved outputs.')
run = (BASE / match.group(1)).resolve()
if not run.is_relative_to(BASE / 'results'):
    raise SystemExit('Invalid results path.')
completed = json.loads((run / 'completed.json').read_text())
if completed['protocol_sha256'] != hashlib.sha256((BASE / 'protocol.json').read_bytes()).hexdigest():
    raise SystemExit('Protocol changed since execution; run the notebook again.')
if completed['data_sha256'] != hashlib.sha256((BASE / 'data/raw/penguins.csv').read_bytes()).hexdigest():
    raise SystemExit('Data changed since execution; investigate.')
abstract = (run / 'ABSTRACT.md').read_text()
next(c for c in nb.cells if c.id == 'abstract').source = abstract
nbformat.write(nb, BASE / 'A2.ipynb')
(BASE / 'ABSTRACT.md').write_text(abstract)
identity = 'Name: ' + nb.metadata.get('authors', [{}])[0].get('name', 'TODO') + '\nStudent ID: ' + nb.metadata.get('student_id', 'TODO')
(BASE / 'SUBMISSION_SUMMARY.md').write_text(abstract.replace('## Abstract','## Submission summary',1) + '\n' + identity + '\n\nRepository URL + commit/tag: TODO\n')
markdown, resources = MarkdownExporter().from_notebook_node(nb, resources={'unique_key': 'A2', 'output_files_dir': 'figures'})
(BASE / 'A2_REPORT.md').write_text(markdown)
for filename, content in resources.get('outputs', {}).items():
    target = BASE / filename
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_bytes(content)
exporter = HTMLExporter(template_name='lab', exclude_input=False, exclude_output=False)
body, _ = exporter.from_notebook_node(nb)
css = '''<style>
@media print {
 @page {size: A4; margin: 12mm;}
 body {font-size: 10pt;}
 pre, code, .highlight pre {white-space: pre-wrap !important; overflow-wrap: anywhere !important;}
 .jp-OutputArea-output, .jp-RenderedHTMLCommon, .jp-OutputArea-child,
 .jp-CodeCell, .jp-Cell-outputWrapper {overflow: visible !important; max-height: none !important;}
 table {font-size: 8pt; width: 100%;}
 td, th {white-space: normal !important; overflow-wrap: anywhere;}
 img, svg {max-width: 100% !important; height: auto;}
 h1, h2, h3 {break-after: avoid;}
}
</style>'''
html = BASE / 'A2.html'
html.write_text(body.replace('</head>', css+'\n</head>'), encoding='utf-8')
print('Abstract refreshed from:', run)
print('HTML with code and saved outputs:', html)
if args.pdf:
    from playwright.sync_api import sync_playwright
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True, args=['--no-sandbox'])
        page = browser.new_page()
        page.route('http://**/*', lambda route: route.abort())
        page.route('https://**/*', lambda route: route.abort())
        page.goto(html.as_uri(), wait_until='load')
        page.evaluate('document.fonts.ready')
        page.pdf(path=str(BASE / 'A2.pdf'), format='A4', print_background=True, prefer_css_page_size=True)
        browser.close()
    print('PDF:', BASE / 'A2.pdf')
else:
    print('Open HTML in a browser and print to PDF, or rerun with --pdf if Chromium is installed.')
