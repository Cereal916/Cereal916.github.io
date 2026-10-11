# slapcraftgames

This project was generated using [Angular CLI](https://github.com/angular/angular-cli) version 22.1.6.

## Development server

To start a local development server, run:

```bash
ng serve
```

Once the server is running, open your browser and navigate to `http://localhost:4200/`. The application will automatically reload whenever you modify any of the source files.

## Code scaffolding

Angular CLI includes powerful code scaffolding tools. To generate a new component, run:

```bash
ng generate component component-name
```

For a complete list of available schematics (such as `components`, `directives`, or `pipes`), run:

```bash
ng generate --help
```

## Building

To build the project run:

```bash
npm run build
```

This will compile your project and store the build artifacts in the `dist/` directory. By default, the production build optimizes your application for performance and speed.

## Running unit tests

To execute unit tests with the [Vitest](https://vitest.dev/) test runner, use the following command:

```bash
ng test
```

## Running end-to-end tests

For end-to-end (e2e) testing, run:

```bash
ng e2e
```

Angular CLI does not come with an end-to-end testing framework by default. You can choose one that suits your needs.

## Deploy

Build and publish the website to its existing GitHub Pages branch and custom domain:

```bash
npm run deploy
```

## House of Pips

- `/hop` is the House of Pips page (demo link, YouTube playlist, screenshots).
- `/hop/wiki` is the player wiki, a lazy-loaded route under `src/app/hop-wiki/`.
- The wiki's sources (Markdown notes, catalogue snapshot and builder) are in `hop-wiki/`; see
  `hop-wiki/README.md`. Rebuild `public/hop/wiki-data/` with `npm run wiki` and never edit the
  generated pages by hand. Wiki changes waiting for the next game release are listed in
  `hop-wiki/CHANGELOG.md`.

## ClipCabinet

- `/clipcabinet/wiki` is the ClipCabinet user wiki, with seven short guides covering
  setup, organization, search and views, playback, export, settings, and FAQ.
- Routes, copy, and styles live in `src/app/clipcabinet-wiki/`. `/clipcabinet`
  redirects to the wiki, and the studio home page links to it.
- `public/clipcabinet/wiki/assets/` contains the approved dark Clip cards icon
  and nine unmodified feature captures of the publisher-owned House of Pips
  sample library. `provenance.json` records their hashes and permitted game ID.
  Keep replacement captures restricted to rights-confirmed games. Timeline
  screenshots use authored demonstration bookmarks, identified in the caption.
- Build with `npm run build` on Node.js 24 or later; run `npm test -- --watch=false`
  before deployment. The build adds HTML entry points for every ClipCabinet guide,
  including its title, description, and canonical URL. Direct links return HTTP 200
  on GitHub Pages, which also keeps the existing `404.html` fallback for other SPA routes.
- `clipcabinet-wiki/build-entrypoints.mjs` reads the same guide metadata as the
  Angular routes. Add new guides there through `clipcabinet-guides.ts`.

## Additional Resources

For more information on using the Angular CLI, including detailed command references, visit the [Angular CLI Overview and Command Reference](https://angular.dev/tools/cli) page.
