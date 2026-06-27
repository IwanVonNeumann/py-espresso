def test_expand():
    cube = Cube.from_minterm(5, 5)
    assert cube.expand_var(0).to_pattern() == "-0101"
    assert cube.expand_var(1).to_pattern() == "0-101"
