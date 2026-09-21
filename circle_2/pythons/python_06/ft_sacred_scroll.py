import alchemy.elements
import alchemy


def main():
    print("=== Sacred Scroll Mastery ===\n")

    print("Testing direct module access:")
    print("alchemy.elements.create_fire(): ", end="")
    print(alchemy.elements.create_fire())

    print("alchemy.elements.create_water(): ", end="")
    print(alchemy.elements.create_water())

    print("alchemy.elements.create_earth(): ", end="")
    print(alchemy.elements.create_earth())

    print("alchemy.elements.create_air(): ", end="")
    print(alchemy.elements.create_air())

    print()

    print("\nTesting package-level access (controlled by __init__.py):")
    print("alchemy.create_fire(): ", end="")
    try:
        print(alchemy.create_fire())
    except  AttributeError:
        print("AttributeError - not exposed")

    print("alchemy.create_water(): ", end="")
    try:
        print(alchemy.create_water())
    except AttributeError:
        print("AttributeError - not exposed")

    print("alchemy.create_earth(): ", end="")
    try:
        print(alchemy.create_earth())
    except AttributeError:
        print("AttributeError - not exposed")

    print("alchemy.create_air(): ", end="")
    try:
        print(alchemy.create_air())
    except AttributeError:
        print("AttributeError - not exposed")


    print("\nPackage metadata:")
    print("Version: ",alchemy.__version__)
    print("Author: ", alchemy.__author__)


main()
