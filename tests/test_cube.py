from py_espresso.cube import Cube


def test_expand():
    cube = Cube.from_minterm(5, n=5)

    assert cube.to_pattern() == "00101"

    assert cube.expand_var(0).to_pattern() == "-0101"
    assert cube.expand_var(1).to_pattern() == "0-101"
    assert cube.expand_var(2).to_pattern() == "00-01"
    assert cube.expand_var(3).to_pattern() == "001-1"
    assert cube.expand_var(4).to_pattern() == "0010-"


def test_cube_size():
    cube = Cube.from_pattern("--101")

    assert cube.literal_count() == 3
    assert cube.dimension() == 2
    assert cube.size() == 4


def test_cube_contains():
    big = Cube.from_pattern("--101")
    small = Cube.from_pattern("00101")

    assert big.contains(small)
    assert not small.contains(big)


def test_cube_intersects():
    a = Cube.from_pattern("--101")
    b = Cube.from_pattern("00101")
    c = Cube.from_pattern("--100")

    assert a.intersects(b)
    assert not a.intersects(c)


def test_cube_covers_point():
    cube = Cube.from_pattern("---01")

    assert cube.covers_point(1)
    assert cube.covers_point(5)
    assert cube.covers_point(29)

    assert not cube.covers_point(2)
    assert not cube.covers_point(30)
