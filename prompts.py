"""Bilingual prompt templates for material generation and quality checks."""


def _extra_instructions(additional: str, output_lang: str) -> str:
    if not additional.strip():
        return ""
    labels = {
        "ru": "Дополнительные указания учителя:",
        "uz": "O'qituvchining qo'shimcha ko'rsatmalari:",
        "en": "Additional teacher instructions:",
    }
    label = labels[output_lang]
    return f"\n\n{label}\n{additional.strip()}"


def build_lesson_plan_prompt(
    subject: str,
    grade: int,
    topic: str,
    output_lang: str,
    additional: str = "",
) -> str:
    extra = _extra_instructions(additional, output_lang)
    if output_lang == "uz":
        return f"""MUHIM: Javobning barcha qismlarini faqat o'zbek tilida, lotin yozuvida yozing. Rus tilidan foydalanmang.

Siz O'zbekiston maktab ta'limi bo'yicha tajribali metodistsiz.

Quyidagi parametrlar asosida batafsil dars rejasini tuzing:
- Fan: {subject}
- Sinf: {grade}
- Mavzu: {topic}{extra}

Dars rejasi tuzilishi:
1. **Dars maqsadlari** — ta'limiy, rivojlantiruvchi va tarbiyaviy
2. **Dars turi** — aralash, yangi bilim beruvchi, mustahkamlovchi va hokazo
3. **Jihozlar va materiallar**
4. **Darsning borishi** — har bir bosqich va uning vaqtini ko'rsating:
   - Tashkiliy qism (2–3 daqiqa)
   - Uy vazifasini tekshirish (5–7 daqiqa)
   - Avvalgi bilimlarni faollashtirish (5 daqiqa)
   - Yangi mavzuni o'rganish (15–20 daqiqa)
   - Mustahkamlash (8–10 daqiqa)
   - Yakun va refleksiya (3–5 daqiqa)
   - Uy vazifasi (2 daqiqa)
5. **Metodik tavsiyalar**

Har bir bosqichda o'qituvchi va o'quvchilarning aniq faoliyatini yozing.
{grade}-sinf o'quvchilarining yosh xususiyatlarini hisobga oling.
Faol ta'lim usullaridan foydalaning.

Faqat o'zbek tilida javob bering."""

    if output_lang == "en":
        return f"""IMPORTANT: Write every part of the response in English only.

You are an experienced curriculum specialist for schools in Uzbekistan.

Create a detailed lesson plan using these parameters:
- Subject: {subject}
- Grade: {grade}
- Topic: {topic}{extra}

Lesson-plan structure:
1. **Lesson objectives** — educational, developmental, and character-building
2. **Lesson type** — combined, introduction of new material, consolidation, etc.
3. **Equipment and materials**
4. **Lesson procedure** — show the time for every stage:
   - Organization and readiness (2–3 minutes)
   - Homework review (5–7 minutes)
   - Activation of prior knowledge (5 minutes)
   - Learning new material (15–20 minutes)
   - Consolidation (8–10 minutes)
   - Summary and reflection (3–5 minutes)
   - Homework assignment (2 minutes)
5. **Methodological recommendations**

Describe specific teacher and student actions for every stage.
Account for the age characteristics of Grade {grade} students.
Use active-learning methods.

Respond in English only."""

    return f"""Ты — опытный методист школьного образования Узбекистана.

Составь подробный план урока по следующим параметрам:
- Предмет: {subject}
- Класс: {grade}
- Тема: {topic}{extra}

Структура плана урока:
1. **Цели урока** — образовательные, развивающие, воспитательные
2. **Тип урока** — комбинированный, изучение нового, закрепление и т.д.
3. **Оборудование и материалы**
4. **Ход урока** — по этапам с указанием времени:
   - Организационный момент (2–3 мин)
   - Проверка домашнего задания (5–7 мин)
   - Актуализация знаний (5 мин)
   - Изучение нового материала (15–20 мин)
   - Закрепление (8–10 мин)
   - Подведение итогов, рефлексия (3–5 мин)
   - Домашнее задание (2 мин)
5. **Методические рекомендации**

Каждый этап должен содержать конкретные действия учителя и учеников.
Учитывай возрастные особенности учащихся {grade}-го класса.
Используй активные методы обучения.

Отвечай только на русском языке."""


def build_exercises_prompt(
    subject: str,
    grade: int,
    topic: str,
    output_lang: str,
    additional: str = "",
) -> str:
    extra = _extra_instructions(additional, output_lang)
    if output_lang == "uz":
        return f"""MUHIM: Javobning barcha qismlarini faqat o'zbek tilida, lotin yozuvida yozing. Rus tilidan foydalanmang.

Siz O'zbekiston maktabida ishlaydigan tajribali amaliyotchi o'qituvchisiz.

Turli darajadagi topshiriqlar to'plamini yarating:
- Fan: {subject}
- Sinf: {grade}
- Mavzu: {topic}{extra}

Topshiriqlarga qo'yiladigan talablar:
1. **1-daraja — Bilish va tushunish** (3–4 ta topshiriq)
   Faktlar, ta'riflar va formulalarni esga tushirishga oid sodda topshiriqlar.

2. **2-daraja — Qo'llash** (3–4 ta topshiriq)
   Bilimlarni odatiy vaziyatlarda qo'llashga oid topshiriqlar.

3. **3-daraja — Tahlil va ijodkorlik** (2–3 ta topshiriq)
   Tahlil, taqqoslash va ijodiy yechim talab qiladigan murakkab topshiriqlar.

4. **Qo'shimcha yulduzchali topshiriq**
   Bitta olimpiada yoki noodatiy topshiriq.

Har bir topshiriq uchun quyidagilarni ko'rsating:
- Topshiriq sharti
- Kutiladigan javob yoki baholash mezoni
- Taxminiy bajarish vaqti

Topshiriqlar O'zbekistonning {grade}-sinf maktab dasturiga mos bo'lsin.
Faqat o'zbek tilida javob bering."""

    if output_lang == "en":
        return f"""IMPORTANT: Write every part of the response in English only.

You are an experienced classroom teacher in a school in Uzbekistan.

Create a differentiated set of exercises:
- Subject: {subject}
- Grade: {grade}
- Topic: {topic}{extra}

Exercise requirements:
1. **Level 1 — Knowledge and understanding** (3–4 exercises)
   Simple recall of facts, definitions, and formulas.
2. **Level 2 — Application** (3–4 exercises)
   Apply knowledge in standard situations.
3. **Level 3 — Analysis and creativity** (2–3 exercises)
   More challenging analysis, comparison, and creative problems.
4. **Extension challenge**
   One olympiad-style or non-standard exercise.

For every exercise, provide its wording, expected answer or assessment criteria, and estimated completion time.
The exercises must align with Uzbekistan's Grade {grade} school curriculum.
Respond in English only."""

    return f"""Ты — опытный учитель-практик в школе Узбекистана.

Создай набор разноуровневых заданий:
- Предмет: {subject}
- Класс: {grade}
- Тема: {topic}{extra}

Требования к заданиям:
1. **Уровень 1 — Знание и понимание** (3–4 задания)
   Простые задания на воспроизведение фактов, определений, формул.
2. **Уровень 2 — Применение** (3–4 задания)
   Задания на применение знаний в стандартных ситуациях.
3. **Уровень 3 — Анализ и творчество** (2–3 задания)
   Задания повышенной сложности: анализ, сравнение, творческие задачи.
4. **Дополнительное задание со звёздочкой**
   Одно олимпиадное или нестандартное задание.

Для каждого задания укажи формулировку, ожидаемый ответ или критерии оценки и примерное время выполнения.
Задания должны соответствовать школьной программе Узбекистана для {grade}-го класса.
Отвечай только на русском языке."""


def build_test_prompt(
    subject: str,
    grade: int,
    topic: str,
    output_lang: str,
    additional: str = "",
) -> str:
    extra = _extra_instructions(additional, output_lang)
    if output_lang == "uz":
        return f"""MUHIM: Javobning barcha qismlarini faqat o'zbek tilida, lotin yozuvida yozing. Rus tilidan foydalanmang.

Siz O'zbekiston maktablarida bilimni baholash bo'yicha metodistsiz.

Javoblari bilan test yarating:
- Fan: {subject}
- Sinf: {grade}
- Mavzu: {topic}{extra}

Test tuzilishi:
1. **A qism — Javob variantli test savollari** (10 ta savol)
   - To'rtta javob varianti: A, B, C, D
   - Faqat bitta to'g'ri javob
   - Savollar soddadan murakkabga qarab joylashtirilsin

2. **B qism — Qisqa javobli savollar** (5 ta savol)
   - Bo'sh joyni to'ldirish, ta'rif berish yoki formula yozish

3. **C qism — Batafsil javob** (2 ta savol)
   - Batafsil yechim talab qiladigan masala yoki savollar

Oxirida quyidagilarni keltiring:
- **Javoblar kaliti** — A va B qismlar uchun
- **Baholash mezonlari** — C qism uchun
- **Baholash shkalasi** — a'lo / yaxshi / qoniqarli / qoniqarsiz

Test O'zbekistonning {grade}-sinf dasturiga mos bo'lsin.
Faqat o'zbek tilida javob bering."""

    if output_lang == "en":
        return f"""IMPORTANT: Write every part of the response in English only.

You are an assessment specialist for schools in Uzbekistan.

Create a test with answers:
- Subject: {subject}
- Grade: {grade}
- Topic: {topic}{extra}

Test structure:
1. **Part A — Multiple-choice questions** (10 questions)
   - Four options: A, B, C, D
   - Exactly one correct answer
   - Order questions from easier to more challenging
2. **Part B — Short-answer questions** (5 questions)
   - Fill a blank, provide a definition, or write a formula
3. **Part C — Extended responses** (2 questions)
   - Problems or questions requiring a developed solution

At the end, include an answer key for Parts A and B, assessment criteria for Part C, and a grading scale.
The test must align with Uzbekistan's Grade {grade} curriculum.
Respond in English only."""

    return f"""Ты — методист по оценке знаний в школах Узбекистана.

Создай тест с ответами:
- Предмет: {subject}
- Класс: {grade}
- Тема: {topic}{extra}

Структура теста:
1. **Часть A — Тестовые вопросы с вариантами ответа** (10 вопросов)
   - 4 варианта ответа (A, B, C, D), один правильный ответ
   - Вопросы от простых к сложным
2. **Часть B — Вопросы с кратким ответом** (5 вопросов)
   - Заполнить пропуск, дать определение или написать формулу
3. **Часть C — Развёрнутый ответ** (2 вопроса)
   - Задачи или вопросы, требующие развёрнутого решения

В конце приведи ключ ответов для частей A и B, критерии оценивания для части C и шкалу оценок.
Тест должен соответствовать программе Узбекистана для {grade}-го класса.
Отвечай только на русском языке."""


def build_quality_check_prompt(
    check_type: str,
    subject: str,
    grade: int,
    topic: str,
    material: str,
    output_lang: str,
) -> str:
    if output_lang == "uz":
        roles = {
            "curriculum": "Siz O'zbekiston davlat ta'lim dasturi bo'yicha ekspertsiz.",
            "difficulty": "Siz yosh pedagogikasi bo'yicha pedagog-psixologsiz.",
            "clarity": "Siz o'quv materiallarining aniqligi bo'yicha muharrirsiz.",
        }
        criteria = {
            "curriculum": f"""1. Mazmun {grade}-sinf dasturiga mosmi?
2. Faktik xatolar mavjudmi?
3. Mavzuning asosiy tushunchalari qamrab olinganmi?""",
            "difficulty": f"""1. Murakkablik {grade}-sinf o'quvchilarining yoshiga mosmi?
2. Juda murakkab yoki haddan tashqari sodda qismlar bormi?
3. Soddadan murakkabga o'tish izchilmi?""",
            "clarity": f"""1. Ifodalar {grade}-sinf o'quvchilari uchun tushunarlimi?
2. Topshiriqlarda noaniqlik yoki ikki xil talqin mavjudmi?
3. Tuzilish va ketma-ketlik mantiqiymi?""",
        }
        return f"""MUHIM: Javobni faqat o'zbek tilida, lotin yozuvida yozing. Rus tilidan foydalanmang.

{roles[check_type]}

Quyidagi o'quv materialini tekshiring:
- Fan: {subject}
- Sinf: {grade}
- Mavzu: {topic}

Tekshiriladigan material:
---
{material[:3000]}
---

Baholash mezonlari:
{criteria[check_type]}

Javobni aynan shu shaklda yozing:
**Baho:** [Mos / Qisman mos / Takomillashtirish kerak]
**Izoh:** [aniq fikr yoki tavsiya berilgan 1–2 ta gap]

Faqat o'zbek tilida javob bering."""

    if output_lang == "en":
        roles = {
            "curriculum": "You are an expert on Uzbekistan's national school curriculum.",
            "difficulty": "You are an educational psychologist specializing in age-appropriate instruction.",
            "clarity": "You are an editor specializing in clear educational materials.",
        }
        criteria = {
            "curriculum": f"""1. Does the content align with the Grade {grade} curriculum?
2. Are there any factual errors?
3. Are the topic's key concepts covered?""",
            "difficulty": f"""1. Is the difficulty appropriate for Grade {grade} students?
2. Are any elements too difficult or too simple?
3. Is there a clear progression from simple to complex?""",
            "clarity": f"""1. Is the wording clear for Grade {grade} students?
2. Are any exercises ambiguous?
3. Are the structure and sequence logical?""",
        }
        return f"""IMPORTANT: Write the response in English only.

{roles[check_type]}

Review this educational material:
- Subject: {subject}
- Grade: {grade}
- Topic: {topic}

Material to review:
---
{material[:3000]}
---

Assessment criteria:
{criteria[check_type]}

Use exactly this response format:
**Rating:** [Meets expectations / Partially meets expectations / Needs improvement]
**Comment:** [1–2 sentences with a specific finding or recommendation]

Respond in English only."""

    roles = {
        "curriculum": "Ты — эксперт по школьной программе Узбекистана.",
        "difficulty": "Ты — педагог-психолог, специалист по возрастной педагогике.",
        "clarity": "Ты — редактор учебных материалов, специалист по ясности текста.",
    }
    criteria = {
        "curriculum": f"""1. Соответствует ли содержание программе для {grade}-го класса?
2. Нет ли фактических ошибок?
3. Охвачены ли ключевые понятия темы?""",
        "difficulty": f"""1. Соответствует ли сложность возрасту учащихся {grade}-го класса?
2. Нет ли слишком сложных или слишком простых элементов?
3. Выдержана ли последовательность от простого к сложному?""",
        "clarity": f"""1. Понятны ли формулировки для учеников {grade}-го класса?
2. Нет ли двусмысленностей в заданиях?
3. Логична ли структура и последовательность?""",
    }
    return f"""{roles[check_type]}

Проверь следующий учебный материал:
- Предмет: {subject}
- Класс: {grade}
- Тема: {topic}

Материал для проверки:
---
{material[:3000]}
---

Критерии оценки:
{criteria[check_type]}

Ответь строго в формате:
**Оценка:** [Соответствует / Частично соответствует / Требует доработки]
**Комментарий:** [1–2 предложения с конкретным замечанием или подтверждением]

Отвечай только на русском языке."""
