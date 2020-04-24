import arcade

"""
Drawing an example happy face

If Python and Arcade are installed, this example can be run from the command line with:
python -m arcade.examples.happy_face
"""

import arcade


def draw_road(cx,cy,sx,sy,offset):
    # Clear screen and start render process
    zx = (cx - (sx/2))
    zy = (cy - (sy/2))
    line_height = 64
    margin_x = 32
    lane_width = (128 + margin_x)
    arcade.draw_rectangle_filled(cx, cy, sx, sy, arcade.color.BATTLESHIP_GREY)
    num_lines = (sy / line_height) / 4
    num_lanes = (sx / lane_width)
    j = 0
    while j < num_lanes:
        j += 1
        i = 0
        y_pos = offset
        while i < num_lines:
            arcade.draw_rectangle_filled(zx+(j*lane_width),zy+offset+(i*line_height*4), (margin_x/2), line_height, arcade.color.WHITE_SMOKE)
            i += 1


# Set constants for the screen size
SCREEN_WIDTH = 1280
SCREEN_HEIGHT = 720
SCREEN_TITLE = "Happy Face Example"
size_x = SCREEN_WIDTH
size_y = SCREEN_HEIGHT
# Open the window. Set the window title and dimensions
arcade.open_window(SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE)
# Set the background color
arcade.set_background_color(arcade.color.WHITE)

arcade.start_render()
draw_road((SCREEN_WIDTH/2), SCREEN_HEIGHT/2, (160 * 6) - 8, SCREEN_HEIGHT*0.75, 0)
arcade.finish_render()

# Keep the window open until the user hits the 'close' button
arcade.run()
