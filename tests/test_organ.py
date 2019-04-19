import network_simulator.Organ as o
from network_simulator.CompatibilityMarkers import OrganType, BloodTypeLetter, BloodTypePolarity


def test_move_organ():
    test_organ = o.Organ(organ_type=OrganType.Heart.value, blood_type='NA', location=1)

    # tests initial values
    assert test_organ.current_location is 1
    assert test_organ.origin_location is 1
    assert test_organ.viability is 60
    assert test_organ.path == [test_organ.origin_location]

    # tests altered values are as expected
    test_organ.move_organ(2, 20, ([1, 2, 3], 'weight'))
    assert test_organ.current_location is 2
    assert test_organ.origin_location is 1
    assert test_organ.viability is 40
    assert test_organ.path == [1, 2, 3]

    # tests whether moving cost can be greater than current viability
    test_organ.move_organ(3, 100, ([3, 2, 1], 'weight'))
    assert test_organ.current_location is 2
    assert test_organ.origin_location is 1
    assert test_organ.viability is 40
    assert test_organ.path == [1, 2, 3]


def test_get_viability():
    assert o.Organ.get_viability(OrganType.Heart.value) == 60
    assert o.Organ.get_viability(OrganType.Kidney.value) == 300
    assert o.Organ.get_viability(OrganType.Liver.value) == 120
    assert o.Organ.get_viability(OrganType.Lungs.value) == 60
    assert o.Organ.get_viability(OrganType.Pancreas.value) == 120
    assert o.Organ.get_viability(OrganType.Intestines.value) == 80
