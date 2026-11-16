from dataclasses import dataclass
from collections import defaultdict
import re


@dataclass(frozen=True, slots=True)
class LogEntry:
    timestamp: str
    level: str
    service: str
    message: str


Pattern = (
    r"^(?P<timestamp>\S+) \[(?P<level>\w+)\] (?P<service>[\w-]+): (?P<message>.+)$"
)


def parse_log_line(line: str) -> LogEntry | None:
    match = re.match(Pattern, line)
    if not match:
        return None

    return LogEntry(**match.groupdict())


def filter_logs_by_level(logs: list[LogEntry], level: str) -> list[LogEntry] | None:
    filter_logs = [log for log in logs if log.level.upper() == level.upper()]
    return filter_logs


def calculate_error_rates(logs: list[LogEntry]) -> dict[str, float]:
    total_counts = defaultdict(int)
    error_counts = defaultdict(int)

    for log in logs:
        total_counts[log.service] += 1
        if log.level.upper() in ("ERROR", "CRITICAL"):
            error_counts[log.service] += 1

    rates = {}
    for service, total in total_counts.items():
        rates[service] = error_counts[service] / total
    return rates


if __name__ == "__main__":
    sample_logs = [
        LogEntry("10:00Z", "INFO", "auth-service", "Login ok"),
        LogEntry("10:01Z", "ERROR", "auth-service", "DB timeout"),
        LogEntry("10:02Z", "ERROR", "payment-service", "Gateway 504"),
    ]

    # Test filtering
    errors = filter_logs_by_level(sample_logs, "error")
    print("Filtered errors count:", len(errors))
    for err in errors:
        print(" ->", err)

    # Test error rate calculation:
    rates = calculate_error_rates(sample_logs)
    print("Calculated error rates:", rates)

errors = filter_logs_by_level(sample_logs, "error")
print("Filtered errors count:", len(errors))
for err in errors:
    print(" ->", err)
