import arcade
import RPG_Map


def main():
    window: RPG_Map.Map2 = RPG_Map.Map2()
    window.setup()
    arcade.run()


if __name__ == '__main__':
    main()
