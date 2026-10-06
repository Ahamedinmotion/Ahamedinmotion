# The motion system

Six self-contained SVGs bring the profile's engineering diagrams to life.
They retain the supplied 42 Abu Dhabi palette, VG5000 lettering and window
framing. All diagrams are illustrations, not live telemetry or measured results.

| Panel | Motion | Loop |
| --- | --- | --- |
| Hero | Map drift, exploded isometric layers, packets and build/test/iterate stages | 4.8–28 seconds |
| Firasah | Evidence travelling through a graph; briefing lines composing | 5–6 seconds |
| Himaya | Three aligned conceptual waveforms and an event scan | 7 seconds |
| FlyBrain | Circuit activity and expanding intervention waves | 6 seconds |
| Robotics | Six curriculum ranks highlighted in order | 9 seconds |
| Footer | Directional conversation arrow | 3 seconds |

Names, explanations and claims stay still. Every loop is a CSS animation inside
its SVG. There is no browser JavaScript, external font request, tracking,
automated workflow or third-party rendering service.

## Rebuild the artwork

Use Python 3 and a virtual environment:

```sh
python3 -m venv .venv
. .venv/bin/activate
pip install -r tools/requirements.txt
python tools/build_motion.py
```

The generator writes six `assets/*-motion.svg` files and their six static companions. The bundled, unmodified
VG5000 font retains its SIL Open Font License in `tools/fonts/OFL.txt`.

## Reduced motion

Motion rules are enclosed in `@media (prefers-reduced-motion: no-preference)`.
Visitors requesting reduced motion receive separate static SVGs through README picture sources; the internal CSS condition provides an additional fallback.
[The static edition](STATIC.md) also provides a manual way to view the profile
without animation.

The implementation follows the browser constraints documented in
[MDN's SVG image guide](https://developer.mozilla.org/en-US/docs/Web/SVG/Guides/SVG_as_an_image)
and the [reduced-motion media feature](https://developer.mozilla.org/en-US/docs/Web/CSS/Reference/At-rules/@media/prefers-reduced-motion).
