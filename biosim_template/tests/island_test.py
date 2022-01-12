from biosim import island_map
from biosim import landscapes
islandmap = """\
    WWW
    WLW
    WWW"""

map = island_map.Map(islandmap)
wat = landscapes.Water
low = landscapes.LowLand


def test_create_map():
    assert isinstance(map.creating_island(), dict)
