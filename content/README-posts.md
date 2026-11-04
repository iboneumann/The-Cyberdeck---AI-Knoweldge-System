# Hugo Content Package: Cyberdeck Development Ghost

Drop-in content for a Hugo site. Everything is plain Markdown with YAML front matter,
plus one optional stylesheet and a site-config excerpt.

## What is inside

```
hugo-content/
  README.md                         this file
  hugo.toml.example                 site-config excerpt to merge
  archetypes/cyberdeck.md           front-matter template for new docs pages
  assets/css/cyberdeck.css          optional phosphor styling (scoped)
  content/
    posts/
      cyberdeck-development-ghost.md      long-form blog post
      deepseek-harness-on-ubuntu.md       practical setup post
    docs/
      _index.md
      cyberdeck-terminal/
        _index.md
        installation.md
        commands.md
        architecture.md
        source-code.md
        troubleshooting.md
```

## Install

From the root of your Hugo site:

```bash
cp -r hugo-content/content/* content/
cp -r hugo-content/assets/* assets/
cp -r hugo-content/archetypes/* archetypes/
```

Then merge the relevant blocks from `hugo-content/hugo.toml.example` into your
`hugo.toml` (or `config/_default/hugo.toml`).

Enable the stylesheet in your theme. For most themes, add to
`layouts/partials/extend_head.html`:

```html
{{ with resources.Get "css/cyberdeck.css" }}
  <link rel="stylesheet" href="{{ .RelPermalink }}">
{{ end }}
```

If your theme does not support `extend_head.html`, add the same block to
`layouts/_default/baseof.html` inside `<head>`.

## Theme compatibility

Written for any theme that supports a `docs` section. Tested against:

- **PaperMod** — set `mainSections = ["posts", "docs"]` in `hugo.toml`
- **Ananke** — docs pages appear under their section automatically
- **Book** — native fit; docs pages get sidebar navigation for free
- **Docsy** — native fit
- **Blowfish** — requires `[params] mainSections`

The posts use only standard Markdown: headings, fenced code, tables, blockquotes,
and task lists. No shortcodes are required, so nothing breaks on a minimal theme.

## Optional: enable the styling

`assets/css/cyberdeck.css` scopes every rule under `.cyberdeck` so it cannot leak
into your existing design. To use it, wrap the parts you want styled:

```markdown
<div class="cyberdeck">

Your content here.

</div>
```

Or apply it only to the source-code page by adding the class in that page's front
matter and wrapping the body.

## Front matter notes

Every page carries:

```yaml
title: "..."
date: 2026-11-04
draft: false
weight: 10          # docs ordering only
tags: [...]
categories: [...]
summary: "..."
```

Set `draft: true` on anything you want to stage before publishing. Hugo will not
build drafts unless you pass `--buildDrafts`.

## Verify before publishing

```bash
hugo --gc --minify
hugo server --buildDrafts --navigateToChanged
```

Check that the code blocks render with syntax highlighting. If they do not, your
theme needs `[markup.highlight]` enabled — see the config excerpt.

## Licence

The prose is yours to adapt. The code samples are MIT, matching DeepSeek Harness.
