from fastapi import FastAPI, Depends
from enum import Enum
from pyIslam.praytimes import PrayerConf, Prayer, LIST_FAJR_ISHA_METHODS
from datetime import date, datetime
import pytz

app = FastAPI()


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
    timezone: Timezone = "EST",
    longitude: float = -81.374417,
    latitude: float = 19.290800,
    fajr_isha_method: Methods = Methods.one,
    asr_fiqh: AsrModel = AsrModel.jomhor,
) -> Prayer:
    now = datetime.now(pytz.timezone(timezone.value))
    hours = now.utcoffset().total_seconds() / 60 / 60
    prayer_conf = PrayerConf(
        longitude,
        latitude,
        hours,
        int(fajr_isha_method.value),
        asr_fiqh_map[asr_fiqh],
    )
    return Prayer(prayer_conf, date.today())


def is_prayer_time_close(
    timezone: Timezone = "EST",
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
