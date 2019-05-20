from traffic.data import airports


def test_getter() -> None:
    airport = airports["LHR"]
    assert airport is not None
    assert airport.icao == "EGLL"
    assert airport.iata == "LHR"
    assert airport.country == "United Kingdom"
    assert airport.name == "London Heathrow Airport"
    lat, lon = airport.latlon
    assert max(abs(lat - 51.471626), abs(lon + 0.467081)) < 1e-2


def test_search() -> None:
    assert airports.search("denmark").data.icao.str.startswith("EK").all()
    assert airports.search("ITALY").data.icao.str.startswith("LI").all()


def test_runway_list() -> None:
    airport = airports["TLS"]
    assert airport is not None
    rwy_list = set(t.name for t in airport.runways.list)
    assert rwy_list == {"14L", "14R", "32L", "32R"}


def test_runway_bearing() -> None:
    for apt_name in ["EHAM", "EDDF", "LFPG", "KLAX", "KSFO", "RJTT"]:
        airport = airports[apt_name]
        assert airport is not None
        for runway in airport.runways.list:
            delta = abs(int(runway.name[:2]) * 10 - runway.bearing)
            if delta > 180:
                delta = 360 - delta
            # It can be as big as 25 degrees with parallel runways!
            assert delta < 25, f"Error with airport {apt_name} {runway.name}"
