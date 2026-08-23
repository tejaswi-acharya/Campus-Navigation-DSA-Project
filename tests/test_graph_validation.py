from graph import validate_configuration


def test_validate_configuration_detects_invalid_vertices():
    errors = validate_configuration({"A": (0, 0)}, [("A", "Z", 5)])
    assert any("Vertex 'Z'" in error for error in errors)


def test_validate_configuration_detects_duplicate_edges():
    errors = validate_configuration(
        {"A": (0, 0), "B": (1, 1)},
        [("A", "B", 5), ("B", "A", 5)],
    )
    assert any("Duplicate edge" in error for error in errors)
