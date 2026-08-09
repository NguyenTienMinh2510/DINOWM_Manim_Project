# DINOWM

Du an tao animation Manim minh hoa DINO-WM qua ba phan: Pixel Space, Latent Space va Zero-shot.

## Cau truc

- `assets/`: tai nguyen tinh, layout, hinh anh va audio
- `docs/`: kich ban, phan cong va huong dan setup
- `scenes/`: ma nguon Manim
- `media/`: video/anh render, duoc git ignore

## Cai dat

```bash
python -m venv .venv
.venv\\Scripts\\activate
pip install -r requirements.txt
```

## Chay animation

```bash
manim -pqh scenes/part1_pixel_space.py PixelSpaceScene
manim -pqh scenes/part2_latent_space.py LatentSpaceScene
manim -pqh scenes/part3_zero_shot.py ZeroShotScene
```

Render tung canh cua Part 2 de xem va dieu chinh nhanh:

```bash
manim -pqh scenes/part2_latent_space.py Scene1_DINOv2Encoder
manim -pqh scenes/part2_latent_space.py Scene2_PatchesAndVectors
manim -pqh scenes/part2_latent_space.py Scene3_ViTTransition
manim -pqh scenes/part2_latent_space.py Scene4_MissingDecoder
```
