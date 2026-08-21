import { readFile, writeFile } from 'node:fs/promises';

const [input = 'chapter-14-bibliography.html', output = 'data/procurement-source.json'] = process.argv.slice(2);
const html = await readFile(input, 'utf8');
const plain = value => value.replace(/<[^>]*>/g, ' ').replace(/&amp;/g, '&').replace(/\s+/g, ' ').trim();
const category = text => /jstor|database|academic search|project muse/i.test(text) ? 'database' : /library|archive|collection/i.test(text) ? 'library' : /rights|licen[cs]|film|video|audio|image/i.test(text) ? 'rights' : /subscription|membership|stream/i.test(text) ? 'subscription' : 'books';
const entries = [...html.matchAll(/<(li|p)[^>]*>([\s\S]*?)<\/\1>/gi)].map((match, index) => {
  const fragment = match[2];
  const link = fragment.match(/href=["']([^"']+)["']/i)?.[1] || null;
  const text = plain(fragment);
  const isbn = text.match(/(?:ISBN(?:-1[03])?\s*:?\s*)([0-9Xx -]{10,17})/i)?.[1]?.replace(/[- ]/g, '') || null;
  const type = category(text);
  return { id: `source-${index + 1}`, title: text.slice(0, 240), url: link, isbn, category: type, group: type, priority: 99, price: null, accessNote: type === 'rights' ? 'Contact for rights quote' : type === 'database' ? 'Institutional access may be required' : type === 'library' ? 'Check public, school, or academic library access' : 'No verified current price' };
}).filter(item => item.title);
await writeFile(output, JSON.stringify({ generatedAt: new Date().toISOString(), sourceGuide: input, sources: entries }, null, 2) + '\n');
console.log(`Wrote ${entries.length} procurement sources to ${output}`);
