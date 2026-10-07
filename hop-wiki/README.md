# House of Pips player wiki

The wiki at `/hop/wiki` is built from the sources in this folder into
`public/hop/wiki-data/` (one JSON file per page plus `manifest.json`), which
the Angular code in `src/app/hop-wiki/` renders. Never edit
`public/hop/wiki-data/pages/` or `manifest.json` by hand; edit the sources and
rebuild.

## Layout

- `catalogue.json`: a snapshot of the game's catalogues (perks, supplies,
  skills, modes, rarities, achievements, Bone Boxes and their numbers). When the
  game changes a catalogue entry, update it here.
- `content/pages/*.md`: the hand-written pages. Front matter sets `title`,
  `section` (a sidebar section), `order`, `description`, and optionally
  `hidden: true`, which keeps a page's source and checks but leaves it out of
  the sidebar, search and site data.
- `private/` (gitignored and never pushed, because this repository is public):
  the hidden Spoilers page and the catalogue entries only it uses. The build
  uses them when the folder is present and works without it. Keep a backup of
  this folder somewhere private; git does not track it.
- `content/catalogue/*.md`: one `## <id>` section of notes per perk, supply
  and skill, plus the intro for each list page.
- `content/screenshots.tsv`: the screenshots pages may show, with captions.
- `public/hop/wiki-data/img/`: every picture (catalogue icons and cards under
  their folders, screenshots under `screens/`). Add a new picture here.
- `build.py`: the builder (Python 3 standard library only).
- `CHANGELOG.md`: wiki changes waiting for the next game release.

## Writing pages

Markdown headings, lists, tables, links and emphasis work as usual. The wiki
also understands:

- References: `{{perk:<id>}}`, `{{supply:<id>}}`, `{{skill:<id>}}`,
  `{{page:<slug>}}`, `{{mode:<id>}}`, `{{rarity:<id>}}`, `{{branch:<id>}}`,
  `{{version}}`.
- A screenshot: `{{shot:<key>}}` on its own line.
- Generated tables and lists on their own line, such as `{{modes-table}}`,
  `{{perk-prices}}`, `{{rival-levels}}` and `{{achievements}}`.
- Boxes: `:::note`, `:::tip`, `:::warning`, `:::example` and
  `:::spoiler <summary>`, each closed by `:::`.

The build fails if a perk, supply or skill has no notes, if notes name an entry
the catalogue does not have, if a link or picture does not resolve, if a page
links to a hidden page, or if player text mentions source paths, telemetry,
anti-cheat, how Rival decides its moves, or spoiler material outside the
spoiler page. Never describe Rival's decision-making, late-game secrets, the
story's ending or how the game is developed.

## Build and preview

```bash
npm run wiki
```

Then preview with the **Serve House of Pips Wiki** run configuration, which
rebuilds the wiki, starts the dev server and opens `/hop/wiki`; stopping it
stops the server. Without IntelliJ, run `npm run wiki:serve` and open
`http://localhost:4200/hop/wiki`.

The build also writes a Steam Community guide draft of the perk list to
`hop-wiki/.build/steam/perks-guide.bbcode.txt` (gitignored).

## Releasing wiki changes

Every change to the wiki gets a line under `## Unreleased` in `CHANGELOG.md`.
When the game's next release is prepared, the game repository's agent
instructions announce the unreleased wiki changes (`WIKI RELEASE REQUIRED:`),
set `game.version` in `catalogue.json` to the release version and move the
entries under that version. After the game release ships, commit this
repository and deploy it with the **Deploy Slapcraft** configuration.
