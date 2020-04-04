from pathlib import Path

import pytest


data_dir = Path(__file__).parent.resolve() / "fixtures/datasets"


@pytest.fixture(scope="session")
def naturalearth_lowres():
    return data_dir / "ne_110m_admin_0_countries/ne_110m_admin_0_countries.shp"


@pytest.fixture(scope="session")
def naturalearth_modres():
    return data_dir / "ne_10m_admin_0_countries/ne_10m_admin_0_countries.shp"


@pytest.fixture(scope="session")
def naturalearth_lowres1():
    return (
        data_dir
        / "ne_110m_admin_1_states_provinces/ne_110m_admin_1_states_provinces.shp"
    )


@pytest.fixture(scope="session")
def naturalearth_modres1():
    return (
        data_dir / "ne_10m_admin_1_states_provinces/ne_10m_admin_1_states_provinces.shp"
    )