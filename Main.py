import arcade
import RPG_Map


def main():
    window: RPG_Map.Map = RPG_Map.Map()
    window.setup()
    arcade.run()


if __name__ == '__main__':
    main()
