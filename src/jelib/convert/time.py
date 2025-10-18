from datetime import datetime
from zoneinfo import ZoneInfo

def convert_timezone(dt: datetime, from_tz: str | None, to_tz: str) -> datetime:
    if dt.tzinfo is None:
        dt = dt.replace(tzinfo=ZoneInfo(from_tz))
    return dt.astimezone(ZoneInfo(to_tz))


def main():
    now = datetime.now()

    il_now = convert_timezone(now, "America/New_York", "Asia/Jerusalem")

    il_formatted = il_now.strftime("%I:%M:%S %p")
    print(il_formatted)


if __name__ == "__main__":
    main()