"""
Starting Template

Once you have learned how to use classes, you can begin your program with this
template.

If Python and Arcade are installed, this example can be run from the command line with:
python -m arcade.examples.starting_template
"""
import arcade
import random
from Criteria import *

SCREEN_WIDTH = 1280
SCREEN_HEIGHT = 720
SCREEN_TITLE = "Triplicate"
DEFAULT_GRAVITY = 3
RESOURCE_PATH = "resources"
levels = []
# ON_KEY_RELEASE apply negative vector on key release.
ON_KEY_RELEASE = True


class ObjectLoader:
    def __init__(self):
        pass

    def load(self, tick):
        pass


class Factory:
    def create(self):
        pass


class FormFactory(Factory):
    def __init__(self, color, val):
        self.color = color
        self.val = val

    def create(self):
        return Form(self.color, self.val)


class PoopFactory(Factory):
    def __init__(self, color, val):
        self.color = color
        self.val = val

    def create(self):
        return Poop(self.color, self.val)


class WeightedObjectLoader(ObjectLoader):
    def __init__(self, tr, factories):
        super().__init__()
        self.factories = factories
        self.tr = tr

    def load(self, tick):
        if tick % self.tr == 0:
            self.t += 1
            x = random.randrange(0, 100)
            for factory in self.factories:
                if x in factory.range:
                    return factory.factory.create()


class RBObjectLoader(ObjectLoader):
    def __init__(self):
        self.Toggle = True

    def load(self, tick):
        if tick % 180 == 0:
            self.Toggle = not self.Toggle
            if self.Toggle:
                return Form((255, 0, 0, 255), "R")
            else:
                return Form((0, 0, 255, 255), "B")


class RGBObjectLoader(ObjectLoader):
    def __init__(self):
        self.t = 0

    def load(self, tick):
        if tick % 180 == 0:
            self.t += 1
            x = self.t % 3
            if x == 0:
                return Form((255, 0, 0, 255), "R")
            elif x == 1:
                return Form((0, 255, 0, 255), "G")
            elif x == 2:
                return Form((0, 0, 255, 255), "B")


class RBPObjectLoader(ObjectLoader):
    def __init__(self):
        self.t = 0

    def load(self, tick):
        if tick % 180 == 0:
            self.t += 1
            x = random.randrange(0, 3)
            if x == 0:
                return Form((255, 0, 0, 255), "R")
            elif x == 1:
                return Poop((0, 255, 0, 255), "G")
            elif x == 2:
                return Form((0, 0, 255, 255), "B")


class RGBPObjectLoader(ObjectLoader):
    def __init__(self,tr):
        self.t = 0
        self.tr = tr

    def load(self, tick):
        if tick % self.tr == 0:
            self.t += 1
            x = random.randrange(0, 4)
            if x == 0:
                return Form((255, 0, 0, 255), "R")
            elif x == 1:
                return Form((0, 255, 0, 255), "G")
            elif x == 2:
                return Form((0, 0, 255, 255), "B")
            elif x == 3:
                return Poop((255, 255, 255, 255), "S")


class Level:
    def __init__(self):
        # You may want many lists. Lists for coins, monsters, etc.
        self.bucket_list = None
        self.object_list = None
        self.object_loader = None
        # This holds the background images. If you don't want changing
        # background images, you can delete this part.
        self.background = None
        self.music = None
        self.tick = 0
        self.selected_bucket = None
        self.score = 0
        self.run = True

    def update(self):
        if self.run:
            self.tick += 1
            if self.object_loader is not None:
                ret = self.object_loader.load(self.tick)
                if ret is not None:
                    ret.reset_pos()
                    self.object_list.append(ret)
            if self.bucket_list is not None:
                for bucket in self.bucket_list:
                    bucket.update()
                    if self.object_list is not None:
                        hit_list = bucket.collides_with_list(self.object_list)
                        for obj in hit_list:
                            if bucket.score(obj):
                                self.score += obj.pass_val
                            else:
                                self.score += obj.fail_val
                            self.object_list.remove(obj)
            if self.object_list is not None:
                for obj in self.object_list:
                    obj.update()
                    if obj.center_y < 5:
                        self.score += obj.miss_val
                        self.object_list.remove(obj)

    def draw(self):
        if self.background is not None:
            arcade.draw_lrwh_rectangle_textured(0, 0,
                                                SCREEN_WIDTH, SCREEN_HEIGHT,
                                                self.background)
        else:
            x = 300
            y = 300
            radius = 200
            arcade.draw_circle_filled(x, y, radius, arcade.color.YELLOW)

            # Draw the right eye
            x = 370
            y = 350
            radius = 20
            arcade.draw_circle_filled(x, y, radius, arcade.color.BLACK)

            # Draw the left eye
            x = 230
            y = 350
            radius = 20
            arcade.draw_circle_filled(x, y, radius, arcade.color.BLACK)

            # Draw the smile
            x = 300
            y = 280
            width = 120
            height = 100
            start_angle = 190
            end_angle = 350
            arcade.draw_arc_outline(x, y, width, height, arcade.color.BLACK,
                                    start_angle, end_angle, 10)
        if self.bucket_list is not None:
            self.bucket_list.draw()
        if self.object_list is not None:
            self.object_list.draw()
        if self.selected_bucket is not None:
            arcade.draw_rectangle_outline(self.bucket_list[self.selected_bucket].center_x,
                                          self.bucket_list[self.selected_bucket].center_y,
                                          self.bucket_list[self.selected_bucket].height * 1.2,
                                          self.bucket_list[self.selected_bucket].width * 1.2,
                                          self.bucket_list[self.selected_bucket].color, (self.tick % 12) + 2, 0)
        arcade.draw_text("Time Left {:d}".format(int((self.length - self.tick) / 60)), (SCREEN_WIDTH / 6) * 4,
                         SCREEN_HEIGHT - (SCREEN_HEIGHT/10), arcade.color.BLACK, 60)
        arcade.draw_text("Score: {}".format(self.score), 0, (SCREEN_HEIGHT / 10)*9,
                         arcade.color.RED, 64)
        if self.tick > self.length:
            arcade.draw_text("GAME OVER", (SCREEN_WIDTH / 5) * 1, (SCREEN_HEIGHT / 6) * 3, arcade.color.BLACK, 128)

    def next_bucket(self):
        # print(self.selected_bucket)
        if self.selected_bucket is None and len(self.bucket_list) > 0:
            self.selected_bucket = 0
        else:
            self.selected_bucket += 1
            if self.selected_bucket >= len(self.bucket_list):
                self.selected_bucket = 0
        # print(self.selected_bucket)
        # Maybe play a sound here?

    def prev_bucket(self):
        # print(self.selected_bucket)
        if self.selected_bucket is None and len(self.bucket_list) > 0:
            self.selected_bucket = len(self.bucket_list) - 1
        else:
            self.selected_bucket -= 1
            if self.selected_bucket < 0:
                self.selected_bucket = len(self.bucket_list) - 1

    def move_bucket(self, x):
        if self.selected_bucket is not None:
            self.bucket_list[self.selected_bucket].v_x += x

    def stop_bucket(self):
        if self.selected_bucket is not None:
            self.bucket_list[self.selected_bucket].v_x = 0

    def stop_all_buckets(self):
        for x in self.bucket_list:
            x.v_x = 0

    def on_key_press(self, key, key_modifiers):
        """
        Called whenever a key on the keyboard is pressed.

        For a full list of keys, see:
        http://arcade.academy/arcade.key.html
        """
        if key == arcade.key.TAB:
            if key_modifiers & arcade.key.MOD_SHIFT:
                self.prev_bucket()
            else:
                self.next_bucket()
        elif key == arcade.key.LEFT or key == arcade.key.A:
            self.move_bucket(-1)
        elif key == arcade.key.RIGHT or key == arcade.key.D:
            self.move_bucket(1)
        elif key == arcade.key.S:
            self.stop_all_buckets()
        elif key == arcade.key.SPACE:
            self.stop_bucket()
        elif key == arcade.key.Q:
            exit(0)

    def on_key_release(self, key, key_modifiers):
        """
        Called whenever the user lets off a previously pressed key.
        """
        if ON_KEY_RELEASE:
            if key == arcade.key.LEFT:
                self.move_bucket(1)
            elif key == arcade.key.RIGHT:
                self.move_bucket(-1)


class Level1(Level):
    def __init__(self):
        super().__init__()
        self.bucket_list = arcade.SpriteList()
        self.bucket_list.append(Bucket((255, 0, 0, 255), [IsFormCriteria(), IsColorCriteria((255, 0, 0))]))
        self.bucket_list.append(Bucket((0, 255, 0, 255), [IsFormCriteria(), IsColorCriteria((0, 255, 0))]))
        self.bucket_list.append(Bucket((0, 0, 255, 255), [IsFormCriteria(), IsColorCriteria((0, 0, 255))]))
        self.bucket_list[0].center_x = SCREEN_WIDTH / 4
        self.bucket_list[1].center_x = (SCREEN_WIDTH / 4) * 2
        self.bucket_list[2].center_x = (SCREEN_WIDTH / 4) * 3

        self.object_loader = RGBObjectLoader()
        self.object_list = arcade.SpriteList()
        self.length = 60 * 120

    def update(self):
        super().update()
        if self.tick > self.length:
            self.run = False

    def draw(self):
        super().draw()


class Level2(Level):
    def __init__(self):
        super().__init__()
        self.bucket_list = arcade.SpriteList()
        self.bucket_list.append(Bucket((255, 0, 255, 255), [IsFormCriteria(), OrCriteria(IsColorCriteria((255, 0, 0)),
                                                                                         IsColorCriteria(
                                                                                             (0, 0, 255)))]))
        self.bucket_list[0].center_x = (SCREEN_WIDTH / 4) * 2

        self.object_loader = RBPObjectLoader()
        self.object_list = arcade.SpriteList()
        self.length = 60 * 120
        self.background = arcade.load_texture("resources/remodeling_an_office_bathroom.jpg")

    def update(self):
        super().update()
        if self.tick > self.length:
            self.run = False

    def draw(self):
        super().draw()


class Level3(Level):
    def __init__(self):
        super().__init__()
        self.bucket_list = arcade.SpriteList()
        self.bucket_list.append(Bucket((255, 0, 0, 255), [IsFormCriteria(), IsColorCriteria((255, 0, 0))]))
        self.bucket_list.append(Bucket((0, 255, 0, 255), [IsFormCriteria(), IsColorCriteria((0, 255, 0))]))
        self.bucket_list.append(Bucket((0, 0, 255, 255), [IsFormCriteria(), IsColorCriteria((0, 0, 255))]))
        self.bucket_list[0].center_x = SCREEN_WIDTH / 5
        self.bucket_list[1].center_x = (SCREEN_WIDTH / 5) * 4
        self.bucket_list[2].center_x = (SCREEN_WIDTH / 5) * 3
        self.bucket_list.append(Bucket((255, 0, 255, 255), [IsFormCriteria(), OrCriteria(IsColorCriteria((255, 0, 0)),
                                                                                         IsColorCriteria(
                                                                                             (0, 0, 255)))]))
        self.bucket_list[3].center_x = (SCREEN_WIDTH / 5) * 2

        self.object_loader = RGBPObjectLoader(60)
        self.object_list = arcade.SpriteList()
        self.length = 60 * 90
        self.background = arcade.load_texture("resources/OfficeSpacePrinterScene.jpg")

    def update(self):
        super().update()
        if self.tick > self.length:
            self.run = False

    def draw(self):
        super().draw()


class Bucket(arcade.Sprite):
    """
    This class represents the coins on our screen. It is a child class of
    the arcade library's "Sprite" class.
    """

    # need a 'criteria'

    def __init__(self, color, criteria):
        super().__init__("resources/trash.png", 1)
        self.criteria = criteria
        self.color = color
        self.center_y = (self.height / 4) * 2
        self.v_x = 0

    def score(self, other):
        for x in self.criteria:
            if not x.check(other):
                return False
        return True

    def update(self):
        self.center_x += self.v_x
        if self.center_x >= SCREEN_WIDTH:
            self.center_x = SCREEN_WIDTH - 1
            self.v_x = 0
        if self.center_x <= 0:
            self.center_x = 1
            self.v_x = 0


class FallingObject(arcade.Sprite):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.gravity = DEFAULT_GRAVITY
        self.pass_val = 100
        self.fail_val = -100
        self.miss_val = -50

    def reset_pos(self):
        # Reset the coin to a random spot above the screen
        self.center_y = random.randrange(SCREEN_HEIGHT + 20,
                                         SCREEN_HEIGHT + 100)
        self.center_x = random.randrange(SCREEN_WIDTH)

    def process_miss(self):
        self.reset_pos()

    def update(self):
        # Move the coin
        self.center_y -= self.gravity

        # See if the coin has fallen off the bottom of the screen.
        # If so, process the miss
        if self.top < 0:
            self.process_miss()


class Poop(FallingObject):
    def __init__(self, color, val):
        super().__init__("resources/poo.png", 0.05)
        self.val = val
        self.color = color
        self.type = "Poop"
        self.gravity = DEFAULT_GRAVITY * 0.5
        self.pass_val = 100
        self.fail_val = -500
        self.miss_val = 50


class Form(FallingObject):
    """
    This class represents the coins on our screen. It is a child class of
    the arcade library's "Sprite" class.
    """

    def __init__(self, color, val):
        super().__init__("resources/form-icon.png", 0.5)
        self.val = val
        self.color = color
        self.type = "Form"
        self.gravity = DEFAULT_GRAVITY


class MyGame(arcade.Window):
    """
    Main application class.

    NOTE: Go ahead and delete the methods you don't need.
    If you do need a method, delete the 'pass' and replace it
    with your own code. Don't leave 'pass' in this program.
    """

    def __init__(self, width, height, title):
        super().__init__(width, height, title)

        arcade.set_background_color(arcade.color.AMAZON)
        self.level = None
        # If you have sprite lists, you should create them here,
        # and set them to None

    def setup(self):
        # Create your sprites and sprite lists here
        self.level = Level1()

    def on_draw(self):
        """
        Render the screen.
        """

        # This command should happen before we start drawing. It will clear
        # the screen to the background color, and erase what we drew last frame.
        arcade.start_render()

        if self.level is not None:
            self.level.draw()
        # Finish drawing and display the result
        # arcade.finish_render()
        # Call draw() on all your sprite lists below

    def on_update(self, delta_time):
        """
        All the logic to move, and the game logic goes here.
        Normally, you'll call update() on the sprite lists that
        need it.
        """
        if self.level is not None:
            self.level.update()

    def on_key_press(self, key, key_modifiers):
        """
        Called whenever a key on the keyboard is pressed.

        For a full list of keys, see:
        http://arcade.academy/arcade.key.html
        """
        if key == arcade.key.Q and key_modifiers & arcade.key.MOD_CTRL:
            exit(0)
        elif key == arcade.key.KEY_1:
            self.level = Level1()
        elif key == arcade.key.KEY_2:
            self.level = Level2()
        elif key == arcade.key.KEY_3:
            self.level = Level3()
        elif self.level is not None:
            self.level.on_key_press(key, key_modifiers)

    def on_key_release(self, key, key_modifiers):
        """
        Called whenever the user lets off a previously pressed key.
        """
        if self.level is not None:
            self.level.on_key_release(key, key_modifiers)

    def on_mouse_motion(self, x, y, delta_x, delta_y):
        """
        Called whenever the mouse moves.
        """
        pass

    def on_mouse_press(self, x, y, button, key_modifiers):
        """
        Called when the user presses a mouse button.
        """
        pass

    def on_mouse_release(self, x, y, button, key_modifiers):
        """
        Called when a user releases a mouse button.
        """
        pass


def main():
    """ Main method """
    game = MyGame(SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE)
    game.setup()
    arcade.run()


if __name__ == "__main__":
    main()
