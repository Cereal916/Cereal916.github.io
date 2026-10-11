import { mkdir, readFile, writeFile } from 'node:fs/promises';
import { fileURLToPath } from 'node:url';
import { WIKI_GUIDES, WIKI_ROOT } from '../src/app/clipcabinet-wiki/clipcabinet-guides.ts';

// GitHub Pages needs a real HTML entry for each known route to return HTTP 200.
const output = new URL('../dist/slapcraftgames/browser/', import.meta.url);
const template = await readFile(new URL('index.html', output), 'utf8');
const escape = (value) =>
  value
    .replaceAll('&', '&amp;')
    .replaceAll('"', '&quot;')
    .replaceAll('<', '&lt;')
    .replaceAll('>', '&gt;');
if (!/<title>[^<]*<\/title>/.test(template) || !/<base href="[^"]*"\s*\/?>/.test(template)) {
  throw new Error('The built index is missing its title or base URL.');
}
const entries = WIKI_GUIDES.map((guide) => ({
  guide,
  path: WIKI_ROOT + (guide.slug ? '/' + guide.slug : ''),
}));
entries.push({ guide: WIKI_GUIDES[0], path: '/clipcabinet' });
for (const { guide, path } of entries) {
  const canonical =
    'https://www.slapcraftgames.com' + WIKI_ROOT + (guide.slug ? '/' + guide.slug : '');
  const html = template
    .replace(
      /<title>[^<]*<\/title>/,
      '<title>' + escape(guide.label + ' | ClipCabinet Wiki | Slapcraft Games') + '</title>',
    )
    .replace(/<base href="[^"]*"\s*\/?>/, '<base href="/">')
    .replace(
      '</head>',
      '<meta name="description" content="' +
        escape(guide.summary) +
        '"><link rel="canonical" href="' +
        canonical +
        '"></head>',
    );
  const directory = new URL(path.slice(1) + '/', output);
  await mkdir(directory, { recursive: true });
  await writeFile(new URL('index.html', directory), html);
}
console.log(
  'Prepared ' + entries.length + ' ClipCabinet HTML entry points in ' + fileURLToPath(output),
);
