#!/usr/bin/env node

import fs from 'node:fs';
import path from 'node:path';
import { pathToFileURL } from 'node:url';

const htmlPath = process.argv[2];
const dependencyRoot = process.env.MERMAID_VALIDATOR_DEPS;

if (!htmlPath) {
  console.error('Usage: validate_mermaid_html.mjs <html-file>');
  process.exit(2);
}

if (!dependencyRoot) {
  console.error('MERMAID_VALIDATOR_DEPS is not set. Run validate_mermaid_html.sh instead.');
  process.exit(2);
}

if (!fs.existsSync(htmlPath)) {
  console.error(`HTML file not found: ${htmlPath}`);
  process.exit(2);
}

const html = fs.readFileSync(htmlPath, 'utf8');
const { JSDOM } = await import(
  pathToFileURL(path.join(dependencyRoot, 'node_modules/jsdom/lib/api.js'))
);
const parsedHtml = new JSDOM(html, { includeNodeLocations: true });
const elements = [...parsedHtml.window.document.querySelectorAll('.mermaid')];

if (elements.length === 0) {
  console.error(`No .mermaid elements found in ${htmlPath}`);
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

for (const [index, element] of elements.entries()) {
  const code = element.textContent.trim();
  const location = parsedHtml.nodeLocation(element);
  const sourceLine = location?.startLine ?? '?';

  if (!code || /^<!--(?:.|\n)*-->$/.test(code)) {
    console.error(`Diagram ${index + 1} (HTML line ${sourceLine}) is empty or still contains a placeholder.`);
    failures += 1;
    continue;
  }

  try {
    await mermaid.parse(code);
    console.log(`Diagram ${index + 1} (HTML line ${sourceLine}): valid`);
  } catch (error) {
    failures += 1;
    const message = error instanceof Error ? error.message : String(error);
    const mermaidLine = message.match(/Parse error on line (\d+)/)?.[1];
    console.error(`Diagram ${index + 1} (HTML line ${sourceLine}): INVALID`);
    if (mermaidLine && Number.isInteger(sourceLine)) {
      console.error(`Approximate Mermaid source location: HTML line ${sourceLine + Number(mermaidLine)}`);
    }
    console.error(message);
  }
}

if (failures > 0) {
  console.error(`\n${failures} Mermaid diagram(s) failed validation.`);
  process.exit(1);
}

console.log(`\nAll ${elements.length} Mermaid diagram(s) passed validation.`);
