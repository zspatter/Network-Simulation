import network_simulator.Organ as o
import network_simulator.OrganList as ol


def test__init__():
    organ_list = ol.OrganList()
    assert len(organ_list.organ_list) is 0


def test_add_organ():
    organ_list = ol.OrganList()
    organ = o.Organ(o.Organ.PANCREAS, o.Organ.O_NEG, 1)
    organ_list.add_organ(organ)
    assert len(organ_list.organ_list) is 1
    assert organ in organ_list.organ_list
    organ_list.add_organ(organ)
    assert len(organ_list.organ_list) is 1
    assert organ in organ_list.organ_list


def test_remove_organ():
    organ_list = ol.OrganList()
    organ = o.Organ(o.Organ.PANCREAS, o.Organ.O_NEG, 1, organ_list)
    organ_list.remove_organ(organ)
    assert len(organ_list.organ_list) is 0
    assert organ not in organ_list.organ_list
    organ1 = o.Organ(o.Organ.PANCREAS, o.Organ.O_NEG, 1, organ_list)
    organ_list.remove_organ(organ)
    assert len(organ_list.organ_list) is 1
    assert organ1 in organ_list.organ_list
    organ_list.remove_organ(organ1)
    assert len(organ_list.organ_list) is 0
    assert organ1 not in organ_list.organ_list


def test_empty_list():
    organ_list = ol.OrganList()
    organ = o.Organ(o.Organ.PANCREAS, o.Organ.O_NEG, 1, organ_list)
    organ = o.Organ(o.Organ.PANCREAS, o.Organ.O_NEG, 1, organ_list)
    organ = o.Organ(o.Organ.PANCREAS, o.Organ.O_NEG, 1, organ_list)
    assert len(organ_list.organ_list) is 3
    organ_list.empty_list()
    assert len(organ_list.organ_list) is 0
