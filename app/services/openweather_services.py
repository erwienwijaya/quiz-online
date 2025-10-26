# services/openweather_services.py
from datetime import datetime, timezone, timedelta
from collections import defaultdict, Counter
from config import Config


class OpenWeatherServices:
    """Business logic for summarizing forecast into 3 days (today, tomorrow, day after tomorrow)."""

    def __init__(self, repository, country_code: str):
        self.repo = repository
        self.country_code = country_code

    def _weekday_id(self, d):
        hari_map = {
            "Monday": "Senin", "Tuesday": "Selasa", "Wednesday": "Rabu",
            "Thursday": "Kamis", "Friday": "Jumat", "Saturday": "Sabtu",
            "Sunday": "Minggu"
        }
        return hari_map.get(d.strftime("%A"), d.strftime("%A"))

    def _avg(self, xs):
        return round(sum(xs) / len(xs), 1) if xs else None

    def get_three_day_forecast(self, city_name: str):
        """Return a ready-to-use structure for UI/API."""
        # 1) Geocode
        geo = self.repo.geocode_city(city_name, self.country_code)

        # 2) Get raw forecast
        data = self.repo.get_5day_3hour_forecast(
            geo["lat"], geo["lon"], units="metric", lang="id")

        # 3) Timezone local from response
        tz_offset_seconds = data.get("city", {}).get("timezone", 0)
        tz_local = timezone(timedelta(seconds=tz_offset_seconds))

        # 4) Grouping by local date
        buckets = defaultdict(list)
        for item in data.get("list", []):
            dt_utc = datetime.fromtimestamp(item["dt"], tz=timezone.utc)
            dt_local = dt_utc.astimezone(tz_local)
            date_key = dt_local.date()
            hour_local = dt_local.hour
            buckets[date_key].append({
                "hour": hour_local,
                "temp": item["main"]["temp"],
                "desc": item["weather"][0]["description"],
                "icon": item["weather"][0]["icon"],
            })

        today_local = datetime.now(tz_local).date()
        three_days = sorted(
            [d for d in buckets.keys() if d >= today_local])[:3]

        results = []
        for d in three_days:
            entries = buckets[d]
            morning_temps, day_temps, night_temps, descs = [], [], [], []

            for e in entries:
                h, t = e["hour"], e["temp"]
                descs.append(e["desc"])
                if h in Config.MORNING_HOURS:
                    morning_temps.append(t)
                elif h in Config.DAY_HOURS:
                    day_temps.append(t)
                elif h in Config.NIGHT_HOURS:
                    night_temps.append(t)

            all_temps = [e["temp"] for e in entries]

            def pick(preferred_bucket):
                pref = self._avg(preferred_bucket)
                if pref is not None:
                    return pref
                return self._avg(all_temps) if all_temps else None

            desc = Counter(descs).most_common(1)[0][0] if descs else ""

            results.append({
                "date": d.isoformat(),
                "weekday": self._weekday_id(d),
                "temps": {
                    "morning": pick(morning_temps),
                    "day": pick(day_temps),
                    "night": pick(night_temps),
                },
                "description": (desc.capitalize() if desc else ""),
            })

        return {"city": geo["name"], "country": self.country_code, "days": results}
