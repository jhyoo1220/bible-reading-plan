import sys
from reading_plan import ReadingPlan
from sql_connector import SQLConnector
from epub_html import EpubHTML


READING_PLAN_FILE = "./data/reading_plan.txt"

BIBLE_DB_PATH_PREFIX = "./data/dbs"
BIBLE_TYPE_TO_DB = {
    "kor_new_trans": "Korean_NewTrans.db",
    "kor_revised": "Korean_Revised.db",
}


if __name__ == '__main__':
    bible_type = sys.argv[1]
    ebook_path = sys.argv[2]
    verse_repr_str = sys.argv[3].lower()
    verse_repr = True if verse_repr_str == "true" else False

    # 1. Read plans from reading plan file
    reading_plans = []
    reading_day = 1
    with open(READING_PLAN_FILE, "r") as f:
        curr_reading_plan = None

        for line in f.readlines():
            if ReadingPlan.is_reading_plan(line):
                if curr_reading_plan is not None:
                    reading_plans.append(curr_reading_plan)

                curr_reading_plan = ReadingPlan(reading_day)
                reading_day += 1

            elif curr_reading_plan is not None:
                curr_reading_plan.add_reading(line)

        if curr_reading_plan is not None:
            reading_plans.append(curr_reading_plan)

    # 2. Read texts from bible database
    bible_db_path = f"{BIBLE_DB_PATH_PREFIX}/{BIBLE_TYPE_TO_DB[bible_type]}"
    bible_connector = SQLConnector(bible_db_path)
    for idx_plan in range(len(reading_plans)):
        print(f"Reading text from database for Day {reading_plans[idx_plan].reading_day} ...")

        for idx_readings in range(len(reading_plans[idx_plan].readings)):
            curr_text_list = bible_connector.read_text_list(reading_plans[idx_plan].readings[idx_readings])
            reading_plans[idx_plan].readings[idx_readings].update_text_list(curr_text_list)

    bible_connector.close_connection()

    # 3. Make epub files
    for reading_plan in reading_plans:
        reading_html_text = EpubHTML.generate_html(reading_plan, verse_repr)
        html_file_path = f"{ebook_path}/readings_{reading_plan.reading_day:03}.html"
        with open(html_file_path, "w", encoding="utf-8") as f:
            print(reading_html_text, file=f)
