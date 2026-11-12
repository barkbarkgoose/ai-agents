#!/usr/bin/env node

import fs from 'node:fs';
import path from 'node:path';
import { pathToFileURL } from 'node:url';

const guidePath = process.argv[2];
const dependencyRoot = process.env.MERMAID_VALIDATOR_DEPS;

if (!guidePath) {
  console.error('Usage: validate_mermaid.mjs <guide.md|guide.html>');
  process.exit(2);
}

if (!dependencyRoot) {
  console.error('MERMAID_VALIDATOR_DEPS is not set. Run validate_mermaid.sh instead.');
  process.exit(2);
}

if (!fs.existsSync(guidePath)) {
  console.error(`File not found: ${guidePath}`);
  process.exit(2);
}

const source = fs.readFileSync(guidePath, 'utf8');
const { JSDOM } = await import(
  pathToFileURL(path.join(dependencyRoot, 'node_modules/jsdom/lib/api.js'))
);

// Each diagram as { code, line }: the first line of its source in the file.
let diagrams;
const kind = /\.(md|markdown)$/i.test(guidePath) ? 'Markdown' : 'HTML';
if (kind === 'Markdown') {
  diagrams = [...source.matchAll(/^```mermaid[^\n]*\n([\s\S]*?)^```/gm)].map((match) => ({
    code: match[1].trim(),
    line: source.slice(0, match.index).split('\n').length + 1
  }));
} else {
  const parsedHtml = new JSDOM(source, { includeNodeLocations: true });
  diagrams = [...parsedHtml.window.document.querySelectorAll('.mermaid')].map((element) => ({
    code: element.textContent.trim(),
    line: parsedHtml.nodeLocation(element)?.startLine ?? '?'
  }));
}

if (diagrams.length === 0) {
  console.error(`No Mermaid diagrams found in ${guidePath}`);
  process.exit(1);
}

// Mermaid's parser expects a small browser-like DOM even though this is a
// syntax-only check. Set the globals before importing Mermaid.
const dom = new JSDOM('<!doctype html><html><body></body></html>');
globalThis.window = dom.window;
globalThis.document = dom.window.document;

for (const name of ['DOMParser', 'Node', 'HTMLElement', 'SVGElement', 'XMLSerializer']) {
  if (!(name in globalThis) && name in dom.window) {
    globalThis[name] = dom.window[name];
  }
}

const mermaidModule = await import(
  pathToFileURL(path.join(dependencyRoot, 'node_modules/mermaid/dist/mermaid.esm.min.mjs'))
);
const mermaid = mermaidModule.default;

mermaid.initialize({
  startOnLoad: false,
  securityLevel: 'loose'
});

let failures = 0;

for (const [index, { code, line: sourceLine }] of diagrams.entries()) {
  if (!code || /^<!--(?:.|\n)*-->$/.test(code)) {
    console.error(`Diagram ${index + 1} (${kind} line ${sourceLine}) is empty or still contains a placeholder.`);
    failures += 1;
    continue;
  }

  try {
    await mermaid.parse(code);
    console.log(`Diagram ${index + 1} (${kind} line ${sourceLine}): valid`);
  } catch (error) {
    failures += 1;
    const message = error instanceof Error ? error.message : String(error);
    const mermaidLine = message.match(/Parse error on line (\d+)/)?.[1];
    console.error(`Diagram ${index + 1} (${kind} line ${sourceLine}): INVALID`);
    if (mermaidLine && Number.isInteger(sourceLine)) {
      // Markdown's line is the diagram's first line; HTML's is the line of the opening tag.
      const offset = kind === 'Markdown' ? -1 : 0;
      console.error(`Approximate Mermaid source location: ${kind} line ${sourceLine + Number(mermaidLine) + offset}`);
    }
    console.error(message);
  }
}

if (failures > 0) {
  console.error(`\n${failures} Mermaid diagram(s) failed validation.`);
  process.exit(1);
}

console.log(`\nAll ${diagrams.length} Mermaid diagram(s) passed validation.`);
