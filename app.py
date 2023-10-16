from fastapi import FastAPI, Depends, HTTPException
from fastapi.responses import FileResponse
from enum import Enum
from pyIslam.praytimes import PrayerConf, Prayer, LIST_FAJR_ISHA_METHODS
from datetime import date, datetime
import pytz
from pathlib import Path

app = FastAPI(
    title="Adhan API",
    description="API to check if its adhan time",
    version="0.0.1",
    docs_url="/docs",
)
base_path = Path("/code")


@app.get("/")
async def index():
    return FileResponse(base_path / Path("public/index.html"))
    

@app.get("/assets/{file_name:path}")
async def assets(file_name: str):
    final_path = base_path / Path("public/assets/" + file_name)
    # make sure resolved final_path is under base_path
    if str(final_path).startswith(str(base_path)):
        return FileResponse(final_path)
    else:
        return HTTPException(status_code=404)


def is_close(a, b, threshold=1):
    dt_a = datetime.combine(date.today(), a)
    dt_b = datetime.combine(date.today(), b)
    diff = dt_a - dt_b
    diff_minutes = abs(diff.total_seconds()) / 60
    return diff_minutes <= threshold


class PrayerName(str, Enum):
    fajr = "fajr"
    dohr = "dohr"
    asr = "asr"
    maghreb = "maghreb"
    ishaa = "ishaa"


class Methods(str, Enum):
    one = 1
    two = 2
    three = 3
    four = 4
    five = 5
    six = 6
    seven = 7
    eight = 8
    nine = 9


Methods.__doc__ = "".join(
    [
        ("- " + str(item.id) + ": " + ", ".join(item.organizations) + "\n")
        for item in LIST_FAJR_ISHA_METHODS
    ]
)


class AsrModel(str, Enum):
    """
    - Jomhor (Shafii, Maliki & Hambali)
    - Hanafi
    """

    jomhor = "jomhor"
    hanafi = "hanafi"


asr_fiqh_map = {AsrModel.jomhor: 1, AsrModel.hanafi: 2}

Timezone = Enum("Timezone", {t: t for t in pytz.all_timezones})


def get_pt(
    timezone: Timezone,
    longitude: float,
    latitude: float,
    fajr_isha_method: Methods = Methods.one,
    asr_fiqh: AsrModel = AsrModel.jomhor,
) -> Prayer:
    # TODO: use Google Zone API to get the daylight savings offset
    # curl "https://maps.googleapis.com/maps/api/timezone/json?location={longitude},-{latitude}&timestamp={utc_now}&key=YOUR_API_KEY"
    # {
    #    "dstOffset" : 0,
    #    "rawOffset" : 0,
    #    "status" : "OK",
    #    "timeZoneId" : "Europe/London",
    #    "timeZoneName" : "Greenwich Mean Time"
    # }
    # now = datetime.now(pytz.timezone(timezone.value))
    # hours = now.utcoffset().total_seconds() / 60 / 60

    # Use the timezone object to localize the current time
    tz = pytz.timezone(timezone.value)
    localized_now = tz.localize(datetime.now())

    # Calculate the offset, taking DST into account
    hours = localized_now.utcoffset().total_seconds() / 3600
    # TODO: validate the longitude and latitude
    prayer_conf = PrayerConf(
        longitude,
        latitude,
        hours,
        int(fajr_isha_method.value),
        asr_fiqh_map[asr_fiqh],
    )
    return Prayer(prayer_conf, date.today())


def is_prayer_time_close(
    timezone: Timezone,
    name: PrayerName = None,
    prayer: Prayer = Depends(get_pt),
    threshold: float = 1,
):
    now = datetime.now(pytz.timezone(timezone.value)).time()
    if name:
        return is_close(now, getattr(prayer, f"{name}_time")(), threshold)
    return any(
        is_close(now, getattr(prayer, f"{name}_time")(), threshold)
        for name in PrayerName
    )


@app.get("/is_adhan_time")
def is_adhan_time(
    is_prayer_time_close: bool = Depends(is_prayer_time_close),
) -> bool:
    """return true if the its adhan time else false"""
    return is_prayer_time_close


@app.get("/show_adhan_times")
def show_adhan_times(
    prayer: Prayer = Depends(get_pt),
) -> dict:
    """Call this API to see at what times the adhan will be triggered"""
    return {name: getattr(prayer, name + "_time")() for name in PrayerName}
