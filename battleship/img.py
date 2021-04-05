from svglib.svglib import svg2rlg
from reportlab.graphics import renderPM
from typing import List, Union, Optional
import xml.etree.ElementTree as ET
from io import StringIO
import main as battleship

SVG_SIZE = 45
SVG = {
    "m": """<g id="miss"> <path style="fill:#ffffff;stroke-width:0.26797" d="m 182.90537,151.43753 a 80,80 0 0 1 -80,80 80,80 0 0 1 -79.999997,-80 80,80 0 0 1 79.999997,-79.999999 80,80 0 0 1 80,79.999999 z" /> </g>""",
    "h": """<g><path id="path12" style="fill:#d40000;stroke-width:0.26797" d="m 182.90537,151.43753 a 80,80 0 0 1 -80,80 80,80 0 0 1 -79.999997,-80 80,80 0 0 1 79.999997,-79.999999 80,80 0 0 1 80,79.999999 z" /></g>"""
}
# The svgs

def _svg(viewBox: int, size: Optional[int] = None) -> ET.Element:
    """A helper function only used internally by the engine, creates an svg and minimizes redundant code.
    Copied from chess.svg module

    Arguments:
        viewbox: int - the size of the viewbox, more info at https://css-tricks.com/scale-svg/
        size: Optional[int] - the width and height of the svg, does not affect the scale
    """
    svg = ET.Element("svg", {
        "xmlns": "http://www.w3.org/2000/svg",
        "version": "1.1",
        "xmlns:xlink": "http://www.w3.org/1999/xlink",
        "viewBox": f"0 0 {viewBox:d} {viewBox:d}",
        "width": f"{viewBox:d}",
        "height": f"{viewBox:d}"
    })

    if size is not None:
        svg.set("width", str(size))
        svg.set("height", str(size))
    
    return svg

# # def svg(tile: "battleship.Tile", size: Optional[int] = None, withTag: bool = True):
# #     """Returns the svg for a tile.

# #     Arguments:
# #         tile: battleship.Tile - The tile to get the svg of.
# #         size: Optional[int] - The size of the svg
# #         withTag: bool - Whether the svg should be wrapped in an svg tag. Defaults to true.
# #     """
# #     svgs = SVG_TILES
# #     el = ET.fromstring(svgs[tile.symbol.lower()])
# #     if withTag:
# #         svg = _svg(SVG_SIZE, size)
# #         svg.append(el)
# #     else:
# #         svg = el
# #     return ET.tostring(svg).decode("utf-8")
# #     #return ET.ElementTree(svg)

# def png(tile: "battleship.Tile", size: Optional[int]=None):
#     """Returns the png for a tile.

#     Arguments:
#         tile: battleship.Tile - The tile to get the png of.
#         size: Optional[int] - The size of the png
#     """
#     return renderPM.drawToString(svg2rlg(StringIO(svg(tile, size=size))))

def board(board: battleship.Board, *,
          size: Optional[int]=SVG_SIZE,
          withTag: Optional[bool]=True,
          style: Optional[str] = None) -> str:
    """Returns the board as an svg.

    Arguments:
        board: battleship.Board - The tile to get the svg of.
        size: Optional[int] - The size of the svg
    """
    if style:
        ET.SubElement(svg, "style").text = style

    svg = _svg(9 * SVG_SIZE, size)
    defs = ET.SubElement(svg, "defs")
    if board:
        for player in battleship.PLAYERS:
            for piece_type in battleship.TILE_TYPES:
                defs.append(ET.fromstring(SVG[battleship.Tile(piece_type, player).symbol]))

    # svgs = SVG_TILES(size)
    # svg = _svg(SVG_SIZE, size*9)
    # for x, y in enumerate(board):
    #     for tile in y:
    #         svg.append(ET.fromstring(svgs[tile.symbol.lower()]))
    # return ET.tostring(svg).decode("utf-8")

if __name__ == "__main__":
    from main import Tile, Board
    # open("board.svg", "w").write(board(Board()))
    open("board.svg", "w").write(board(Board([[Tile.from_symbol('h'), Tile.from_symbol('h'), Tile.from_symbol('h'), Tile.from_symbol('h'), Tile.from_symbol('w'), Tile.from_symbol('w'), Tile.from_symbol('w'), Tile.from_symbol('w'), Tile.from_symbol('w'), Tile.from_symbol('w')], [Tile.from_symbol('w'), Tile.from_symbol('w'), Tile.from_symbol('w'), Tile.from_symbol('w'), Tile.from_symbol('w'), Tile.from_symbol('w'), Tile.from_symbol('w'), Tile.from_symbol('w'), Tile.from_symbol('w'), Tile.from_symbol('w')], [Tile.from_symbol('w'), Tile.from_symbol('w'), Tile.from_symbol('w'), Tile.from_symbol('w'), Tile.from_symbol('w'), Tile.from_symbol('w'), Tile.from_symbol('w'), Tile.from_symbol('w'), Tile.from_symbol('w'), Tile.from_symbol('w')], [Tile.from_symbol('w'), Tile.from_symbol('w'), Tile.from_symbol('w'), Tile.from_symbol('w'), Tile.from_symbol('w'), Tile.from_symbol('w'), Tile.from_symbol('w'), Tile.from_symbol('w'), Tile.from_symbol('w'), Tile.from_symbol('w')], [Tile.from_symbol('w'), Tile.from_symbol('w'), Tile.from_symbol('w'), Tile.from_symbol('w'), Tile.from_symbol('w'), Tile.from_symbol('w'), Tile.from_symbol('w'), Tile.from_symbol('w'), Tile.from_symbol('w'), Tile.from_symbol('w')], [Tile.from_symbol('w'), Tile.from_symbol('w'), Tile.from_symbol('w'), Tile.from_symbol('w'), Tile.from_symbol('w'), Tile.from_symbol('w'), Tile.from_symbol('w'), Tile.from_symbol('w'), Tile.from_symbol('w'), Tile.from_symbol('w')], [Tile.from_symbol('w'), Tile.from_symbol('w'), Tile.from_symbol('w'), Tile.from_symbol('w'), Tile.from_symbol('w'), Tile.from_symbol('w'), Tile.from_symbol('w'), Tile.from_symbol('w'), Tile.from_symbol('w'), Tile.from_symbol('w')], [Tile.from_symbol('w'), Tile.from_symbol('w'), Tile.from_symbol('w'), Tile.from_symbol('w'), Tile.from_symbol('w'), Tile.from_symbol('w'), Tile.from_symbol('w'), Tile.from_symbol('w'), Tile.from_symbol('w'), Tile.from_symbol('w')], [Tile.from_symbol('w'), Tile.from_symbol('w'), Tile.from_symbol('w'), Tile.from_symbol('w'), Tile.from_symbol('w'), Tile.from_symbol('w'), Tile.from_symbol('w'), Tile.from_symbol('w'), Tile.from_symbol('w'), Tile.from_symbol('w')], [Tile.from_symbol('w'), Tile.from_symbol('w'), Tile.from_symbol('w'), Tile.from_symbol('w'), Tile.from_symbol('w'), Tile.from_symbol('w'), Tile.from_symbol('w'), Tile.from_symbol('w'), Tile.from_symbol('w'), Tile.from_symbol('h')]])))
