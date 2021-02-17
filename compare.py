from csv_diff import load_csv, compare
import json, sys


def parse(text):
    try:
        return json.loads(text)
    except ValueError as e:
        print('invalid json: %s' % e)
        return None # or: raise
    
diff = compare(
    load_csv(open("resources/csv/uk_commodities_2021-02-01.csv"), key="SID"),
    load_csv(open("resources/csv/eu_commodities_2021-02-01.csv"), key="SID")
)
# print(diff)
diff_str = str(diff)
diff_str = diff_str.replace('"', '')
diff_str = diff_str.replace("'", '"')
diff_str = diff_str.replace("\\xa", " ")

parse(diff_str)
# sys.exit()
f = open("resources/compare/differences.json", "w+")
f.write(diff_str)
f.close()
