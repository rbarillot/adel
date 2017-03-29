import alinea.adel.data_samples as test_data
from alinea.adel.adel import Adel
import os

def test_instantiate():
    adel = Adel()
    assert len(adel.leaves[0].xydb) == 6
    assert adel.stand.plant_density == 250
    assert adel.convUnit == 0.01
    assert adel.nplants == 1
    assert adel.domain_area == 1. / adel.stand.plant_density
    assert adel.positions[0] == (0, 0, 0)
    return adel

adel = test_instantiate()
g = test_data.adel_two_metamers()


def test_get_axis():
    assert g.nb_scales() == 6
    ms = adel.get_axis(g)
    assert ms.nb_scales() == 4


def test_scene():
    s = adel.scene(g)
    assert len(s) == 6


def test_statistics():
    areas = adel.get_exposed_areas(g)
    assert 'green_area' in areas
    assert 'species' in areas
    assert round(areas['green_area'].values[0],2) == 0.31
    species = g.property('species')
    g.remove_property('species')
    areas = adel.get_exposed_areas(g)
    assert 'species' in areas
    g.add_property('species')
    g.property('species').update(species)
    axstats = adel.axis_statistics(g)
    assert axstats['LAI totale'].round(2).values[0] == 0.02
    pstats = adel.plot_statistics(g, axstats)
    assert pstats['Nbr.axe.tot.m2'][0] == 500


def test_midribs():
    midribs = adel.get_midribs(g)
    midstats = adel.midrib_statistics(g)
    assert midstats['insertion_height'].values[0] == 2


def test_save_and_load():
    fgeom, fg = adel.save(g)
    gg = adel.load()
    assert len(gg) == len(g)
    if os.path.exists(fgeom):
        os.remove(fgeom)
    if os.path.exists(fg):
        os.remove(fg)
