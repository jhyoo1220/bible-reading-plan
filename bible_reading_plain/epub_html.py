from reading_plan import ReadingPlan


class EpubHTML(object):
    @staticmethod
    def _generate_html_head(title: str) -> str:
        return f"""
<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.1//EN" "http://www.w3.org/TR/xhtml11/DTD/xhtml11.dtd">
<html xmlns="http://www.w3.org/1999/xhtml">
<head>

<title>
{title}
</title>

<meta http-equiv="Content-Type" content="text/html; charset=UTF-8" />
<link rel="stylesheet" href="style.css" type="text/css" />
</head>

"""

    @staticmethod
    def _generate_bible_head(head_type: str, value: str) -> str:
        head_type_to_size = {
            "date": 1,
            "reading_list": 2,
            "chapter": 3,
            "verse": 4,
        }
        font_size = head_type_to_size[head_type]

        return f"\n<h{font_size}>{value}</h{font_size}>\n"

    @staticmethod
    def _generate_text(text: str) -> str:
        return f"<p>{text}<p>\n"

    @classmethod
    def generate_html(cls, reading_plan: ReadingPlan, verse_repr: bool) -> str:
        content = cls._generate_html_head(reading_plan.get_reading_day_str())
        content += "<body>\n"
        content += cls._generate_bible_head("date", reading_plan.get_reading_day_str())

        for reading in reading_plan.readings:
            content += cls._generate_bible_head("reading_list", reading.get_reading_list())

            last_chapter = 0
            for curr_text in reading.text_list:
                chapter = curr_text["chapter"]

                if reading.has_multiple_chapters() and chapter != last_chapter:
                    content += cls._generate_bible_head("chapter", reading.get_book_with_chapter(chapter))
                    last_chapter = chapter

                if curr_text["type"] == 1:
                    if curr_text["divided_verse"] <= 1 and verse_repr:
                        content += cls._generate_text(f"""{str(curr_text["verse"])}. {curr_text["text"]}""")
                    else:
                        content += cls._generate_text(curr_text["text"])

                else:
                    content += cls._generate_bible_head("verse", curr_text["text"])

        content += "\n</body>\n</html>"

        return content
