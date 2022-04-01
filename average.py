import re
from datetime import datetime, timedelta, date
import sys
import os.path

def main(todo_file, done_file, days_back=7):

    dir_file = os.path.split(done_file)
    todo_dir = os.path.dirname(done_file)
    outfilename = os.path.join(todo_dir, "average-report.txt")

    lines = []
    files = [todo_file, done_file]
    for filename in files:
        with open(filename, 'r') as f:
            lines.extend(f.readlines())

    csum = cnum = sum = num = 0
    today_date = datetime.date(datetime.now())
    lastweek = today_date - timedelta(days=days_back)

    for line in lines:
        donematch = re.match(r'x (.*)', line)

        if donematch is not None:
            # a done task
            closed = None
            added = None

            nopri = re.match(r'(\d\d\d\d-\d\d-\d\d) (\d\d\d\d-\d\d-\d\d)', donematch[1])
            if nopri is not None:
                # no prio included
                closed = date.fromisoformat(nopri[1])
                added = date.fromisoformat(nopri[2])
            else:
                # includes prio
                withpri = re.match(r'(\d\d\d\d-\d\d-\d\d) (.*) (\d\d\d\d-\d\d-\d\d)', donematch[1])
                if withpri is not None:
                    closed = date.fromisoformat(withpri[1])
                    added = date.fromisoformat(withpri[3])
                else:
                    print("Not a proper done task")

            if closed is not None and added is not None:
                diff = (closed - added).days
                csum = csum + diff
                cnum = cnum + 1

                if closed == today_date or lastweek < closed < today_date:
                    sum = sum + diff
                    num = num + 1

    caverage = csum / cnum
    average = sum / num

    with open(outfilename, "a") as outfile:
        output = f'''
SUMMARY at {datetime.now():%Y-%m-%d %T}
{cnum} tasks closed in total with average duration {caverage:.2f} days
{num} tasks closed in the last {days_back} days with average duration {average:.2f} days
'''

        print(output)
        outfile.write(output)


if __name__ == "__main__":

    if len(sys.argv) < 3:
        print("Usage: avarage.py [TODO_FILE] [DONE_FILE] <days back>")
        sys.exit(1)

    if os.path.isfile(sys.argv[1]) and os.path.isfile(sys.argv[2]):
        if len(sys.argv) == 4:
            main(sys.argv[1], sys.argv[2], int(sys.argv[3]))
        else:
            # use 7 days as default if not given
            main(sys.argv[1], sys.argv[2])
    else:
        print("Error: %s or %s doesn't exist" % (sys.argv[1], sys.argv[2]))
        sys.exit(1)
