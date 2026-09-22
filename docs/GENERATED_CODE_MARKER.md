# Hidden Generated-Code Marker

Verse AI Knowledge v21 uses a lightweight provenance marker for generated Markdown.

## Marker

```html
<!-- verse-ai-generated:v21 -->
```

Markdown renderers normally hide HTML comments, so the marker does not clutter the visible response.

It remains visible in raw Markdown and can be detected by tooling.

## Safety Rule

Do **not** use:
- zero-width characters;
- bidirectional-control characters;
- invisible Unicode tags;
- altered identifier characters;
- hidden characters inside Verse source.

Those techniques can make source code confusing or unsafe.

## Placement

When the model returns Verse inside Markdown, place the marker immediately after the final generated-code block:

````markdown
```verse
my_device := class(creative_device):
    ...
```

<!-- verse-ai-generated:v21 -->
````

For multiple generated Verse files in one response, include a marker after each generated file section.

## Optional metadata marker

For tooling, the model may use:

```html
<!-- verse-ai-generated:v21;lang=verse;status=draft -->
```

Do not claim `compiled` unless actual local compile evidence exists.
