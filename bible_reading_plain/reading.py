import re


def chapter_verse(chapter: int, verse: int) -> dict:
    return {
        "chapter": chapter,
        "verse": verse,
    }

def book_name(korean: str, db: str):
    return {
        "korean": korean,
        "db": db,
    }


BOOK_NAMES = {
    "GENESIS": book_name("창세기", "Genesis"),
    "EXODUS": book_name("출애굽기", "Exodus"),
    "LEVITICUS": book_name("레위기", "Leviticus"),
    "NUMBERS": book_name("민수기", "Numbers"),
    "DEUTERONOMY": book_name("신명기", "Deuteronomy"),
    "JOSHUA": book_name("여호수아", "Joshua"),
    "JUDGES": book_name("사사기", "Judges"),
    "RUTH": book_name("룻기", "Ruth"),
    "1 SAMUEL": book_name("사무엘상", "FirstSamuel"),
    "2 SAMUEL": book_name("사무엘하", "SecondSamuel"),
    "1 KINGS": book_name("열왕기상", "FirstKings"),
    "2 KINGS": book_name("열왕기하", "SecondKings"),
    "1 CHRONICLES": book_name("역대상", "FirstChronicles"),
    "2 CHRONICLES": book_name("역대하", "SecondChronicles"),
    "EZRA": book_name("에스라", "Ezra"),
    "NEHEMIAH": book_name("느헤미야", "Nehemiah"),
    "ESTHER": book_name("에스더", "Esther"),
    "JOB": book_name("욥기", "Job"),
    "PSALM": book_name("시편", "Psalms"),
    "PROVERBS": book_name("잠언", "Proverbs"),
    "ECCLESIASTES": book_name("전도서", "Ecclesiastes"),
    "SONG": book_name("아가", "SongOfSongs"),
    "ISAIAH": book_name("이사야", "Isaiah"),
    "JEREMIAH": book_name("예레미야", "Jeremiah"),
    "LAMENTATIONS": book_name("예레미야애가", "Lamentations"),
    "EZEKIEL": book_name("에스겔", "Ezekiel"),
    "DANIEL": book_name("다니엘", "Daniel"),
    "HOSEA": book_name("호세아", "Hosea"),
    "JOEL": book_name("요엘", "Joel"),
    "AMOS": book_name("아모스", "Amos"),
    "OBADIAH": book_name("오바댜", "Obadiah"),
    "JONAH": book_name("요나", "Jonah"),
    "MICAH": book_name("미가", "Micah"),
    "NAHUM": book_name("나훔", "Nahum"),
    "HABAKKUK": book_name("하박국", "Habakkuk"),
    "ZEPHANIAH": book_name("스바냐", "Zephaniah"),
    "HAGGAI": book_name("학개", "Haggai"),
    "ZECHARIAH": book_name("스가랴", "Zechariah"),
    "MALACHI": book_name("말라기", "Malachi"),
    "MATTHEW": book_name("마태복음", "Matthew"),
    "MARK": book_name("마가복음", "Mark"),
    "LUKE": book_name("누가복음", "Luke"),
    "JOHN": book_name("요한복음", "John"),
    "ACTS": book_name("사도행전", "Acts"),
    "ROMANS": book_name("로마서", "Romans"),
    "1 CORINTHIANS": book_name("고린도전서", "FirstCorinthians"),
    "2 CORINTHIANS": book_name("고린도후서", "SecondCorinthians"),
    "GALATIANS": book_name("갈라디아서", "Galatians"),
    "EPHESIANS": book_name("에베소서", "Ephesians"),
    "PHILIPPIANS": book_name("빌립보서", "Philippians"),
    "COLOSSIANS": book_name("골로새서", "Colossians"),
    "1 THESSALONIANS": book_name("데살로니가전서", "FirstThessalonians"),
    "2 THESSALONIANS": book_name("데살로니가후서", "SecondThessalonians"),
    "1 TIMOTHY": book_name("디모데전서", "FirstTimothy"),
    "2 TIMOTHY": book_name("디모데후서", "SecondTimothy"),
    "TITUS": book_name("디도서", "Titus"),
    "PHILEMON": book_name("빌레몬서", "Philemon"),
    "HEBREWS": book_name("히브리서", "Hebrews"),
    "JAMES": book_name("야고보서", "James"),
    "1 PETER": book_name("베드로전서", "FirstPeter"),
    "2 PETER": book_name("베드로후서", "SecondPeter"),
    "1 JOHN": book_name("요한일서", "FirstJohn"),
    "2 JOHN": book_name("요한이서", "SecondJohn"),
    "3 JOHN": book_name("요한삼서", "ThirdJohn"),
    "JUDE": book_name("유다서", "Jude"),
    "REVELATION": book_name("요한계시록", "Revelation"),
}


class Reading(object):
    def __init__(self, line: str):
        splitted = line.strip().split(" ")

        book = splitted[0]
        if len(splitted) == 3:
            book += " " + splitted[1]

        self._book_db = BOOK_NAMES[book]["db"]
        self._book_korean = BOOK_NAMES[book]["korean"]

        self._reading_list = splitted[-1]
        num_colons = self._reading_list.count(":")
        num_hyphens = self._reading_list.count("-")

        # GENESIS 1:1-3:24, PSALM 4-6
        if (num_colons == 0 or num_colons == 2) and num_hyphens == 1:
            range_splitted = self._reading_list.split("-")
            self._from = self.parse_chapter_verse(range_splitted[0])
            self._to = self.parse_chapter_verse(range_splitted[1])

        # PSALM 90, GENESIS 11:32
        elif (num_colons == 0 or num_colons == 1) and num_hyphens == 0:
            self._from = self.parse_chapter_verse(self._reading_list)
            self._to = self._from

        # GENESIS 11:1-26
        elif num_colons == 1 and num_hyphens == 1:
            self._from, self._to = self.parse_chapter_verse_range(self._reading_list)

        # Something is wrong!
        else:
            print(f"Cannot parse {self._reading_list} from {line}")

        self.text_list = None

    @staticmethod
    def parse_chapter_verse(line: str) -> dict:
        splitted = line.split(":")
        if len(splitted) >= 2:
            return chapter_verse(int(splitted[0]), int(splitted[1]))

        return chapter_verse(int(splitted[0]), None)

    @staticmethod
    def parse_chapter_verse_range(line: str) -> (dict, dict):
        splitted = line.split("-")

        from_part = Reading.parse_chapter_verse(splitted[0])
        to_part = chapter_verse(from_part["chapter"], int(splitted[1]))

        return from_part, to_part

    @staticmethod
    def is_reading(line: str) -> bool:
        return len(line.strip()) > 0

    def get_db_params(self) -> dict:
        return {
            "book": self._book_db,
            "chapters": ", ".join(str(x) for x in range(self._from["chapter"], self._to["chapter"] + 1)),
        }

    def is_target(self, chapter: int, verse: int) -> bool:
        if chapter < self._from["chapter"] or self._to["chapter"] < chapter:
            return False

        if not self.has_multiple_chapters():
            return self._from["verse"] is None or (self._from["verse"] <= verse and verse <= self._to["verse"])

        elif self._from["chapter"] == chapter:
            return self._from["verse"] is None or self._from["verse"] <= verse

        elif self._to["chapter"] == chapter:
            return self._to["verse"] is None or self._to["verse"] >= verse

        return True

    def update_text_list(self, text_list: list):
        self.text_list = text_list

    def has_multiple_chapters(self) -> bool:
        return self._from["chapter"] != self._to["chapter"]

    def get_reading_list(self) -> str:
        return f"{self._book_korean} {self._reading_list}"

    def get_book_with_chapter(self, chapter: int) -> str:
        return f"{self._book_korean} {str(chapter)}장"
