"""Localized, API-free lesson examples and quick lesson settings."""

from __future__ import annotations

import random
import re


SUBJECT_IDS = [
    "mathematics", "algebra", "geometry", "physics", "chemistry", "biology",
    "geography", "history", "uzbek", "russian", "english", "literature",
    "computer_science", "natural_science", "music", "visual_arts",
    "technology", "physical_education", "native_language",
]

SUBJECT_MIN_GRADE = {
    "algebra": 5, "geometry": 5, "physics": 6, "chemistry": 7,
    "biology": 5, "geography": 5, "computer_science": 3,
}

# Ten verified concepts per subject. Five age-aware activity modes expand each
# eligible concept into at least 20 suggestions without network/API calls.
CONCEPTS = {
    "mathematics": [
        ("Сложение и вычитание", "Addition and subtraction", "Qoʻshish va ayirish"),
        ("Таблица умножения", "Multiplication table", "Koʻpaytirish jadvali"),
        ("Деление с остатком", "Division with remainders", "Qoldiqli boʻlish"),
        ("Дроби на примере пиццы", "Fractions using pizza", "Pitsa misolida kasrlar"),
        ("Проценты в повседневной жизни", "Percentages in everyday life", "Kundalik hayotda foizlar"),
        ("Периметр и площадь", "Perimeter and area", "Perimetr va yuza"),
        ("Единицы длины, массы и времени", "Units of length, mass, and time", "Uzunlik, massa va vaqt birliklari"),
        ("Решение текстовых задач", "Solving word problems", "Matnli masalalarni yechish"),
        ("Координатная плоскость", "Coordinate plane", "Koordinata tekisligi"),
        ("Вероятность и среднее арифметическое", "Probability and arithmetic mean", "Ehtimollik va oʻrta arifmetik"),
    ],
    "algebra": [
        ("Числовые выражения", "Numerical expressions", "Sonli ifodalar"),
        ("Отрицательные числа", "Negative numbers", "Manfiy sonlar"),
        ("Пропорции и отношения", "Ratios and proportions", "Nisbat va proporsiyalar"),
        ("Линейные уравнения", "Linear equations", "Chiziqli tenglamalar"),
        ("Системы уравнений", "Systems of equations", "Tenglamalar sistemasi"),
        ("Степени и корни", "Powers and roots", "Darajalar va ildizlar"),
        ("Квадратные уравнения", "Quadratic equations", "Kvadrat tenglamalar"),
        ("Функции и их графики", "Functions and graphs", "Funksiyalar va grafiklar"),
        ("Арифметическая прогрессия", "Arithmetic sequences", "Arifmetik progressiya"),
        ("Алгебра в повседневной жизни", "Algebra in everyday life", "Kundalik hayotda algebra"),
    ],
    "geometry": [
        ("Геометрические фигуры вокруг нас", "Shapes around us", "Atrofimizdagi geometrik shakllar"),
        ("Углы и их виды", "Angles and their types", "Burchaklar va ularning turlari"),
        ("Треугольники", "Triangles", "Uchburchaklar"),
        ("Четырёхугольники", "Quadrilaterals", "Toʻrtburchaklar"),
        ("Окружность и круг", "Circle and circumference", "Aylana va doira"),
        ("Периметр и площадь", "Perimeter and area", "Perimetr va yuza"),
        ("Подобие фигур", "Similarity of shapes", "Shakllarning oʻxshashligi"),
        ("Теорема Пифагора", "Pythagorean theorem", "Pifagor teoremasi"),
        ("Объём геометрических тел", "Volume of solids", "Geometrik jismlar hajmi"),
        ("Координаты и преобразования", "Coordinates and transformations", "Koordinatalar va almashtirishlar"),
    ],
    "physics": [
        ("Скорость, время и расстояние", "Speed, time, and distance", "Tezlik, vaqt va masofa"),
        ("Сила и масса", "Force and mass", "Kuch va massa"),
        ("Сила тяжести", "Gravity", "Ogʻirlik kuchi"),
        ("Давление", "Pressure", "Bosim"),
        ("Работа, мощность и энергия", "Work, power, and energy", "Ish, quvvat va energiya"),
        ("Температура и тепло", "Temperature and heat", "Harorat va issiqlik"),
        ("Электрический ток и цепь", "Electric current and circuits", "Elektr toki va zanjir"),
        ("Свет и отражение", "Light and reflection", "Yorugʻlik va qaytish"),
        ("Звуковые волны", "Sound waves", "Tovush toʻlqinlari"),
        ("Физика в повседневной жизни", "Physics in everyday life", "Kundalik hayotda fizika"),
    ],
    "chemistry": [
        ("Атомы и молекулы", "Atoms and molecules", "Atomlar va molekulalar"),
        ("Химические элементы", "Chemical elements", "Kimyoviy elementlar"),
        ("Периодическая таблица", "Periodic table", "Davriy jadval"),
        ("Химические формулы", "Chemical formulas", "Kimyoviy formulalar"),
        ("Химические реакции", "Chemical reactions", "Kimyoviy reaksiyalar"),
        ("Кислоты, основания и соли", "Acids, bases, and salts", "Kislotalar, asoslar va tuzlar"),
        ("Растворы", "Solutions", "Eritmalar"),
        ("Металлы и неметаллы", "Metals and nonmetals", "Metallar va metallmaslar"),
        ("Вода и её свойства", "Water and its properties", "Suv va uning xossalari"),
        ("Безопасность в лаборатории", "Laboratory safety", "Laboratoriyada xavfsizlik"),
    ],
    "biology": [
        ("Строение клетки", "Cell structure", "Hujayra tuzilishi"),
        ("Органы человека", "Human organs", "Inson organlari"),
        ("Пищеварительная система", "Digestive system", "Ovqat hazm qilish tizimi"),
        ("Дыхательная и кровеносная системы", "Respiratory and circulatory systems", "Nafas olish va qon aylanish tizimlari"),
        ("Здоровое питание", "Healthy nutrition", "Sogʻlom ovqatlanish"),
        ("Фотосинтез", "Photosynthesis", "Fotosintez"),
        ("Строение и размножение растений", "Plant structure and reproduction", "Oʻsimlik tuzilishi va koʻpayishi"),
        ("Экосистемы и пищевые цепи", "Ecosystems and food chains", "Ekotizimlar va oziq zanjirlari"),
        ("Наследственность и генетика", "Heredity and genetics", "Irsiyat va genetika"),
        ("Охрана окружающей среды", "Environmental protection", "Atrof-muhitni muhofaza qilish"),
    ],
    "geography": [
        ("Материки и океаны", "Continents and oceans", "Materiklar va okeanlar"),
        ("Страны и столицы", "Countries and capitals", "Mamlakatlar va poytaxtlar"),
        ("Географическая карта и стороны света", "Maps and compass directions", "Geografik xarita va ufq tomonlari"),
        ("Климатические пояса", "Climate zones", "Iqlim mintaqalari"),
        ("Реки, озёра, горы и равнины", "Rivers, lakes, mountains, and plains", "Daryolar, koʻllar, togʻlar va tekisliklar"),
        ("Природные зоны", "Natural zones", "Tabiiy zonalar"),
        ("География Узбекистана", "Geography of Uzbekistan", "Oʻzbekiston geografiyasi"),
        ("Водные ресурсы Центральной Азии", "Water resources of Central Asia", "Markaziy Osiyoning suv resurslari"),
        ("Изменение климата", "Climate change", "Iqlim oʻzgarishi"),
        ("Экономическая география", "Economic geography", "Iqtisodiy geografiya"),
    ],
    "history": [
        ("Древние цивилизации", "Ancient civilizations", "Qadimgi sivilizatsiyalar"),
        ("Древний Египет, Греция и Рим", "Ancient Egypt, Greece, and Rome", "Qadimgi Misr, Yunoniston va Rim"),
        ("Великий шёлковый путь", "Great Silk Road", "Buyuk Ipak yoʻli"),
        ("История Самарканда", "History of Samarkand", "Samarqand tarixi"),
        ("Амир Темур и государство Тимуридов", "Amir Temur and the Timurid state", "Amir Temur va Temuriylar davlati"),
        ("Мирзо Улугбек", "Mirzo Ulugbek", "Mirzo Ulugʻbek"),
        ("Великие географические открытия", "Age of Exploration", "Buyuk geografik kashfiyotlar"),
        ("Мировые войны", "World Wars", "Jahon urushlari"),
        ("Независимость Узбекистана", "Independence of Uzbekistan", "Oʻzbekiston mustaqilligi"),
        ("Причины и последствия исторических событий", "Causes and effects in history", "Tarixiy voqealarning sabab va oqibatlari"),
    ],
    "uzbek": [
        ("Soʻz turkumlari", "Parts of speech in Uzbek", "Soʻz turkumlari"),
        ("Ot va uning shakllari", "Uzbek nouns and forms", "Ot va uning shakllari"),
        ("Sifat va darajalari", "Uzbek adjectives", "Sifat va darajalari"),
        ("Feʼl zamonlari", "Uzbek verb tenses", "Feʼl zamonlari"),
        ("Gap tuzilishi", "Uzbek sentence structure", "Gap tuzilishi"),
        ("Imlo qoidalari", "Uzbek spelling rules", "Imlo qoidalari"),
        ("Tinish belgilari", "Uzbek punctuation", "Tinish belgilari"),
        ("Matn tuzish va oʻqib tushunish", "Writing and reading comprehension", "Matn tuzish va oʻqib tushunish"),
        ("Ogʻzaki nutq va lugʻat boyligi", "Speaking and vocabulary", "Ogʻzaki nutq va lugʻat boyligi"),
        ("Insho yozish", "Essay writing in Uzbek", "Insho yozish"),
    ],
    "russian": [
        ("Имя существительное", "Nouns in Russian", "Rus tilida ot"),
        ("Имя прилагательное", "Adjectives in Russian", "Rus tilida sifat"),
        ("Глагол и его формы", "Russian verbs and forms", "Rus tilida feʼl shakllari"),
        ("Главные и второстепенные члены предложения", "Sentence parts", "Gapning bosh va ikkinchi darajali boʻlaklari"),
        ("Простое и сложное предложение", "Simple and complex sentences", "Sodda va qoʻshma gap"),
        ("Безударные гласные и приставки", "Russian spelling patterns", "Rus tili imlo qoidalari"),
        ("Корень слова и однокоренные слова", "Word roots and related words", "Soʻz oʻzagi va oʻzakdosh soʻzlar"),
        ("Синонимы и антонимы", "Synonyms and antonyms", "Sinonim va antonimlar"),
        ("Пунктуация в сложном предложении", "Punctuation in complex sentences", "Qoʻshma gaplarda tinish belgilari"),
        ("Подготовка к написанию сочинения", "Preparing to write an essay", "Insho yozishga tayyorgarlik"),
    ],
    "english": [
        ("Introducing Yourself", "Introducing Yourself", "Oʻzini tanishtirish"),
        ("My Family and Home", "My Family and Home", "Mening oilam va uyim"),
        ("My Daily Routine", "My Daily Routine", "Mening kun tartibim"),
        ("Food and Drinks", "Food and Drinks", "Oziq-ovqat va ichimliklar"),
        ("Weather and Seasons", "Weather and Seasons", "Ob-havo va fasllar"),
        ("Shopping and Prices", "Shopping and Prices", "Xaridlar va narxlar"),
        ("Present Simple and Present Continuous", "Present Simple and Present Continuous", "Present Simple va Present Continuous"),
        ("Past Simple and Future Plans", "Past Simple and Future Plans", "Past Simple va kelajak rejalari"),
        ("Comparative and Superlative Adjectives", "Comparative and Superlative Adjectives", "Sifatlarning qiyosiy va orttirma darajasi"),
        ("Travelling and Asking for Directions", "Travelling and Asking for Directions", "Sayohat va yoʻl soʻrash"),
    ],
    "literature": [
        ("Главные герои произведения", "Main characters", "Asarning bosh qahramonlari"),
        ("Характеристика литературного героя", "Character analysis", "Adabiy qahramon tavsifi"),
        ("Тема и основная мысль", "Theme and main idea", "Mavzu va asosiy gʻoya"),
        ("Сюжет и композиция", "Plot and composition", "Syujet va kompozitsiya"),
        ("Басня и её мораль", "Fable and moral", "Masal va uning xulosasi"),
        ("Народные и литературные сказки", "Folk and literary tales", "Xalq va adabiy ertaklar"),
        ("Средства художественной выразительности", "Literary devices", "Badiiy tasvir vositalari"),
        ("Анализ стихотворения", "Poetry analysis", "Sheʼr tahlili"),
        ("Нравственный выбор героя", "A character's moral choice", "Qahramonning axloqiy tanlovi"),
        ("Подготовка к сочинению", "Preparing a literary essay", "Adabiy insho yozishga tayyorgarlik"),
    ],
    "computer_science": [
        ("Устройство компьютера", "Computer components", "Kompyuter qurilmalari"),
        ("Операционная система, файлы и папки", "Operating systems, files, and folders", "Operatsion tizim, fayl va papkalar"),
        ("Безопасность в интернете", "Internet safety", "Internet xavfsizligi"),
        ("Защита персональных данных", "Personal data protection", "Shaxsiy maʼlumotlarni himoya qilish"),
        ("Алгоритмы и блок-схемы", "Algorithms and flowcharts", "Algoritmlar va blok-sxemalar"),
        ("Переменные, условия и циклы", "Variables, conditions, and loops", "Oʻzgaruvchilar, shartlar va takrorlashlar"),
        ("Основы программирования", "Programming basics", "Dasturlash asoslari"),
        ("Компьютерные сети", "Computer networks", "Kompyuter tarmoqlari"),
        ("Искусственный интеллект и робототехника", "AI and robotics", "Sunʼiy intellekt va robototexnika"),
        ("Цифровая грамотность и кибербуллинг", "Digital literacy and cyberbullying", "Raqamli savodxonlik va kiberbulling"),
    ],
}

# Remaining school subjects use carefully localized, subject-aware themes.
GENERIC_CONCEPTS = [
    ("Основные понятия", "Core concepts", "Asosiy tushunchalar"),
    ("История и развитие", "History and development", "Tarix va rivojlanish"),
    ("Инструменты и материалы", "Tools and materials", "Asboblar va materiallar"),
    ("Правила безопасности", "Safety rules", "Xavfsizlik qoidalari"),
    ("Практические навыки", "Practical skills", "Amaliy koʻnikmalar"),
    ("Творческий проект", "Creative project", "Ijodiy loyiha"),
    ("Работа в команде", "Teamwork", "Jamoada ishlash"),
    ("Известные мастера и достижения", "Notable creators and achievements", "Mashhur ijodkorlar va yutuqlar"),
    ("Связь с повседневной жизнью", "Everyday-life connections", "Kundalik hayot bilan bogʻliqlik"),
    ("Итоговая практическая работа", "Final practical task", "Yakuniy amaliy topshiriq"),
]

MODES = {
    "ru": ["Основы", "Простое объяснение", "Практика", "Игровой урок", "Мини-проект"],
    "en": ["Foundations", "Simple explanation", "Practice", "Game-based lesson", "Mini-project"],
    "uz": ["Asoslar", "Sodda tushuntirish", "Amaliyot", "Oʻyinli dars", "Mini-loyiha"],
}

SECTIONS = {
    "ru": ["Основы", "Практика", "Проект"],
    "en": ["Foundations", "Practice", "Project"],
    "uz": ["Asoslar", "Amaliyot", "Loyiha"],
}

QUICK_SETTINGS = [
    ("practice", "Сделать акцент на практике", "Emphasize practice", "Amaliyotga urgʻu berish"),
    ("pairs", "Добавить работу в парах", "Add pair work", "Juftlikda ishlashni qoʻshish"),
    ("group", "Добавить групповое задание", "Add a group task", "Guruh topshirigʻini qoʻshish"),
    ("individual", "Добавить индивидуальное задание", "Add an individual task", "Individual topshiriq qoʻshish"),
    ("games", "Добавить игровые упражнения", "Add game-based exercises", "Oʻyinli mashqlar qoʻshish"),
    ("daily", "Добавить примеры из повседневной жизни", "Add everyday-life examples", "Kundalik hayotdan misollar qoʻshish"),
    ("simple", "Объяснить простыми словами", "Explain in simple language", "Sodda tilda tushuntirish"),
    ("steps", "Добавить пошаговое объяснение", "Add step-by-step explanations", "Bosqichma-bosqich tushuntirish"),
    ("examples", "Добавить больше примеров", "Add more examples", "Koʻproq misollar qoʻshish"),
    ("discussion", "Добавить вопросы для обсуждения", "Add discussion questions", "Muhokama savollarini qoʻshish"),
    ("levels", "Добавить задания разного уровня сложности", "Add differentiated tasks", "Turli darajadagi topshiriqlar qoʻshish"),
    ("strong", "Добавить задание для сильных учеников", "Add an extension for advanced learners", "Kuchli oʻquvchilar uchun topshiriq"),
    ("support", "Добавить поддержку для учеников, которым сложно", "Add support for struggling learners", "Qiynalayotgan oʻquvchilar uchun yordam"),
    ("mini_test", "Добавить мини-тест", "Add a mini-test", "Mini-test qoʻshish"),
    ("answers", "Добавить ответы для учителя", "Add teacher answers", "Oʻqituvchi uchun javoblar"),
    ("homework", "Добавить домашнее задание", "Add homework", "Uy vazifasi qoʻshish"),
    ("experiment", "Добавить практический эксперимент", "Add a practical experiment", "Amaliy tajriba qoʻshish"),
    ("creative", "Добавить творческое задание", "Add a creative task", "Ijodiy topshiriq qoʻshish"),
    ("visuals", "Добавить визуальные материалы", "Add visual materials", "Vizual materiallar qoʻshish"),
    ("rubric", "Добавить критерии оценивания", "Add assessment criteria", "Baholash mezonlarini qoʻshish"),
    ("45min", "Подготовить материал для 45-минутного урока", "Prepare a 45-minute lesson", "45 daqiqalik dars tayyorlash"),
    ("20min", "Подготовить сокращённый материал для 20 минут", "Prepare a 20-minute condensed lesson", "20 daqiqalik qisqa dars tayyorlash"),
    ("no_terms", "Не использовать сложные термины", "Avoid difficult terminology", "Murakkab atamalardan foydalanmaslik"),
    ("uzbekistan", "Использовать местные примеры из Узбекистана", "Use local examples from Uzbekistan", "Oʻzbekistondan mahalliy misollar"),
    ("print", "Сделать материал подходящим для печати", "Make the material print-friendly", "Materialni chop etishga moslashtirish"),
]


def subject_id_from_index(index: int) -> str:
    return SUBJECT_IDS[index]


def _lang_index(lang: str) -> int:
    return {"ru": 0, "en": 1, "uz": 2}.get(lang, 0)


def topic_catalog(subject_id: str, grade: int, lang: str) -> list[dict[str, str]]:
    concepts = CONCEPTS.get(subject_id, GENERIC_CONCEPTS)
    language_index = _lang_index(lang)
    modes = MODES[lang]
    sections = SECTIONS[lang]
    topics = []
    min_grade = SUBJECT_MIN_GRADE.get(subject_id, 1)
    if grade < min_grade:
        return topics
    for concept_index, concept in enumerate(concepts):
        concept_text = concept[language_index]
        # Four modes produce 40 concise, age-adapted options per subject.
        for mode_index, mode in enumerate(modes[:4]):
            topic_id = f"{subject_id}.{concept_index}.{mode_index}.g{grade}.{lang}"
            if lang == "ru":
                text = f"{concept_text}: {mode.lower()} для {grade} класса"
            elif lang == "uz":
                text = f"{concept_text}: {grade}-sinf uchun {mode.lower()}"
            else:
                text = f"{concept_text}: {mode.lower()} for Grade {grade}"
            topics.append({
                "id": topic_id,
                "text": text,
                "section": sections[min(mode_index, 2)],
            })
    return topics


def filter_topics(
    subject_id: str,
    grade: int,
    lang: str,
    search: str = "",
    section: str = "",
) -> list[dict[str, str]]:
    topics = topic_catalog(subject_id, grade, lang)
    query = re.sub(r"\s+", " ", search.strip().casefold())
    if query:
        topics = [topic for topic in topics if query in topic["text"].casefold()]
    if section:
        topics = [topic for topic in topics if topic["section"] == section]
    return topics


def random_topic(subject_id: str, grade: int, lang: str) -> dict[str, str] | None:
    topics = topic_catalog(subject_id, grade, lang)
    return random.choice(topics) if topics else None


def quick_setting_options(lang: str) -> list[tuple[str, str]]:
    index = {"ru": 1, "en": 2, "uz": 3}.get(lang, 1)
    return [(item[0], item[index]) for item in QUICK_SETTINGS]

