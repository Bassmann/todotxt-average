import re
from datetime import datetime, timedelta, date
import sys
import os.path


def main(done_file):

    dir_file = os.path.split(done_file)
    todo_dir = os.path.dirname(done_file)
    outfilename = os.path.join(todo_dir, "average-report.txt")

    with open(done_file, "r") as f:
        lines = f.readlines()

    csum = cnum = sum = num = 0
    today_date = datetime.date(datetime.now())
    lastweek = today_date - timedelta(days=7)

    for line in lines:
        matches = re.split(r"\s", line)

        added = date.fromisoformat(matches[2])
        closed = date.fromisoformat(matches[1])

        diff = (closed - added).days
        csum = csum + diff
        cnum = cnum + 1

        if closed == today_date or lastweek < closed < today_date:
            sum = sum + diff
            num = num + 1

    caverage = csum / cnum
    average = sum / num

    with open(outfilename, "a") as outfile:
        outfile.write("SUMMARY at {0}\n".format(str(datetime.now())[:16]))
        outfile.write(
            "{0} tasks closed in total with average duration {1}\n".format(
                cnum, "{:.2f}".format(caverage)
            )
        )
        outfile.write(
            "{0} tasks closed in the last 7 days with average duration {1}\n".format(
                num, "{:.2f}".format(average)
            )
        )


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: collect-average.py [DONE_FILE]")
        sys.exit(1)

    if os.path.isfile(sys.argv[1]):
        main(sys.argv[1])
    else:
        print("Error: %s doesn't exist" % (sys.argv[1]))
        sys.exit(1)
