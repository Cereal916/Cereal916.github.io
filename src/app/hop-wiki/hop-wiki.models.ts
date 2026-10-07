// Shapes of the data hop-wiki/build.py writes into public/hop/wiki-data/
// from the Markdown and catalogue snapshot in hop-wiki/ (npm run wiki).

export interface WikiNavPage {
  title: string;
  route: string;
}

export interface WikiNavGroup {
  section: string;
  pages: WikiNavPage[];
}

/** One search entry: title, url (a site route), section, kind and text. */
export interface WikiSearchEntry {
  t: string;
  u: string;
  s: string;
  k: string;
  x: string;
}

export interface WikiManifest {
  site: string;
  version: string;
  nav: WikiNavGroup[];
  search: WikiSearchEntry[];
  pages: string[];
}

export interface WikiTocEntry {
  id: string;
  text: string;
}

export interface WikiPage {
  route: string;
  title: string;
  description: string;
  html: string;
  toc: WikiTocEntry[];
}
