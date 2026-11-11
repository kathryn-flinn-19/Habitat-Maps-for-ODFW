from pathlib import Path

from fasthtml.common import *

MAP_PATH = Path(__file__).resolve().parent / "figures" / "kit_fox_habitat_map-updated2.png"

app, rt = fast_app()


@app.get("/")
def get():
    return Html(
        Head(Title("ODFW Habitat Maps")),
        Body(
            H1("habitat map"),
            Img(
                src="/map/kit-fox",
                alt="habitat map",
                style="max-width: 50%; height: 50;",
            ),
        ),
    )


@app.get("/map/kit-fox")
def get_kit_fox_map():
    if not MAP_PATH.is_file():
        raise HTTPException(
            status_code=404,
            detail=f"Map has not been generated: {MAP_PATH}",
        )
    return FileResponse(MAP_PATH, media_type="image/png")


serve()