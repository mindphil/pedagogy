My slide presentation for a teaching demo on special right triangles, made using Manim CE.


## Rendering

General format: `manim [quality argument] [python file] [scene name]`

Quality arguments: 
- `-ql -s`/`-ql` for low quality static/video (420p/30fps)
- `-qh -s`/`-qh` for high quality static/video (1080p/60fps) scene
- `-s` saves the last frame as a PNG

For example, to render the title page:
`manim -qh -s demo2.py TitlePage`

## Requirements

- Python <= 3.12
- LaTeX
- Manim CE (use pip for best results)
- NumPy