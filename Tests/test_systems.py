def test_1() -> None:
    """
    _summary_ : Test instantiation of Systems class with no landscape file
    """
    # Prepare test data
    from ..SapScript.Utils.systems import Systems

    # Execute test
    _systems = Systems()
    assert isinstance(_systems, Systems)
    assert _systems._landscape_file is None
    assert _systems._available_systems == None
    assert _systems._landscape_xml is None


def test_2() -> None:
    """
    _summary_ : Test instantiation of Systems class with known working landscape file example
    """
    # Prepare test data
    from ..SapScript.Utils.systems import Systems

    # Execute tests
    _systems = Systems(landscape_file="private\landscape.xml")
    assert isinstance(_systems, Systems)
    assert _systems._landscape_file == "landscape.xml"
    assert _systems._available_systems is None
    assert _systems._landscape_xml is None

    # Clean up test data
    import os

    os.remove("landscape.xml")


def test_3() -> None:
    """
    _summary_: Test the load_landscape method of the Systems class without providing a value for landscape_file so default is used.
    """
    # Prepare test data
    from ..SapScript.Utils.systems import Systems
    from pathlib import Path

    _systems = Systems()
    assert isinstance(_systems, Systems)
    assert _systems._landscape_file is None
    assert _systems._available_systems == None
    assert _systems._landscape_xml is None

    # Execute tests
    _systems.load_landscape_file()
    assert isinstance(_systems._landscape_xml, Path)
    assert _systems._landscape_xml.exists()
    assert _systems._landscape_xml.is_file()


def test_4() -> None:
    """
    _summary_: Test the available_systems method of the Systems class with the default landscape file.
    """
    # Prepare test data
    from ..SapScript.Utils.systems import Systems
    from pathlib import Path

    _systems = Systems()
    assert isinstance(_systems, Systems)
    assert _systems._landscape_file is None
    assert _systems._available_systems == None
    assert _systems._landscape_xml is None

    # Execute tests
    _systems.load_landscape_file()
    assert isinstance(_systems._landscape_xml, Path)
    assert _systems._landscape_xml.exists()
    assert _systems._landscape_xml.is_file()
    _available_systems = _systems.available_systems()
    assert isinstance(_available_systems, list)
    print(_available_systems)
