import streamlit as st
import openai
import json
from openai import OpenAIError, RateLimitError, AuthenticationError
from dotenv import load_dotenv
import os
load_dotenv()
openai_api_key = os.getenv("OPENAI_API_KEY")
# Перевірка, що ключ дійсно завантажився
if not openai_api_key:
    raise ValueError("Не знайдено OPENAI_API_KEY у .env файлі!")

# --- Завантаження курсів ---
with open('courses.json', encoding='utf-8') as f:
    courses = json.load(f)

# --- Категорії та підкатегорії ---
categories = {
    "IT": ["AI", "Програмування", "Кібербезпека", "Тестування", "Web-розробка"],
    "Гуманітарні": ["Суспільні науки", "Розвиток мислення", "Вивчення мови", "Психологія"],
    "Бізнес": ["Фінанси", "Підприємництво", "Аналітика", "Маркетинг", "Менеджмент"],
    "Соціальні": ["Громадське суспільство", "Ментальне здоровʼя та безпека", "Подолання впливу війни"],
    "Освітні": ["Для освітян", "Підготовка до ЗНО/МНТ", "Інклюзивна освіта"],
    "Громадська/публічна сфера": ["Держслужба", "Військова служба", "Комунікації у сфері публічного управління"],
    "Творчі": ["Дизайн", "Музика", "Фото/відео виробництво"]
}

# --- Відповіді до питань ---
answers = {
    "goal": ["Нові знання", "Професійне зростання", "Перекваліфікація"],
    "field": list(categories.keys()),
    "basic_knowledge": ["Починаю з нуля", "Маю базові знання"],
    "level": ["Початковий", "Середній", "Просунутий"],
    "material_format": ["Відеолекції з викладачем", "Самостійне читання тексту", "Змішаний формат (відео + текст)", "Немає значення"],
    "time_per_week": ["до 2 годин", "2-5 годин", "понад 5 годин", "ще не знаю"],
    "course_duration": ["короткі курси (1–2 тижні)", "середньої тривалості (3–6 тижнів)", "довготривалі програми (2+ місяці)", "немає значення"],
    "teaching_approach": ["Більше теорії, пояснень і концептів", "Переважно практика та завдання", "Збалансований підхід", "Все одно"],
    "certificate": ["Так", "Ні", "Неважливо"],
    "paid_courses": ["Так", "Ні"]
}

# --- Сесійний стан ---
if "step" not in st.session_state:
    st.session_state.step = 0
if "data" not in st.session_state:
    st.session_state.data = {}

# --- Кнопка скидання ---
if st.button("🔄 Почати спочатку"):
    st.session_state.step = 0
    st.session_state.data = {}
    st.rerun()

# --- Вивід повідомлень ---
def show_user_message(msg):
    st.markdown(
        f'<div style="text-align: right; background-color:#DCF8C6; padding:8px; '
        f'border-radius:10px; margin:5px 0;">{msg}</div>',
        unsafe_allow_html=True
    )

def show_bot_message(msg):
    st.markdown(
        f'<div style="text-align: left; background-color:#F1F0F0; padding:8px; '
        f'border-radius:10px; margin:5px 0;">{msg}</div>',
        unsafe_allow_html=True
    )

# --- UI ---
st.title("🎓 Підбір онлайн-курсів")

# 0-й КРОК: Мета
if st.session_state.step == 0:
    show_bot_message ("Вітаю! Я допоможу правильно обрати онлайн-курс серед сотень варіантів на платформі Prometheus. Будь ласка, дайте відповіді на запитання. Завдяки отриманій інформації я запропоную ті курси, які найкраще вам підійдуть. ")
    show_bot_message(" Яка ваша мета навчання?")
    goal = st.radio("Оберіть мету:", answers["goal"])
    if st.button("Далі"):
        st.session_state.data['goal'] = goal
        st.session_state.step += 1
        st.rerun()

# 1-й КРОК: Сфера / Категорія
elif st.session_state.step == 1:
    show_user_message(f"Моя мета: {st.session_state.data.get('goal', '')}")
    show_bot_message("У якій сфері ви хочете навчатися?")
    category = st.radio("Оберіть сферу:", answers["field"])
    if st.button("Далі"):
        st.session_state.data['category'] = category
        st.session_state.step += 1
        st.rerun()

# 2-й КРОК: Базові знання
elif st.session_state.step == 2:
    show_user_message(f"Сфера: {st.session_state.data.get('category', '')}")
    show_bot_message("Чи маєте базові знання з цієї теми, чи бажаєте почати з нуля?")
    basic_knowledge = st.radio("Оберіть:", answers["basic_knowledge"])
    if st.button("Далі"):
        st.session_state.data['basic_knowledge'] = basic_knowledge
        st.session_state.step += 1
        st.rerun()

# 3-й КРОК: Рівень складності
elif st.session_state.step == 3:
    show_user_message(f"Базові знання: {st.session_state.data.get('basic_knowledge','')}")
    show_bot_message("Який рівень складності вам підходить?")
    level = st.radio("Оберіть рівень:", answers["level"])
    if st.button("Далі"):
        st.session_state.data['level'] = level
        st.session_state.step += 1
        st.rerun()

# 4-й КРОК: Формат подачі
elif st.session_state.step == 4:
    show_user_message(f"Рівень: {st.session_state.data.get('level','')}")
    show_bot_message("Який формат подачі матеріалу вам більше підходить?")
    material_format = st.radio("Оберіть формат:", answers["material_format"])
    if st.button("Далі"):
        st.session_state.data['material_format'] = material_format
        st.session_state.step += 1
        st.rerun()

# 5-й КРОК: Час на навчання
elif st.session_state.step == 5:
    show_user_message(f"Формат: {st.session_state.data.get('material_format','')}")
    show_bot_message("Скільки часу ви готові приділяти навчанню щотижня?")
    time_per_week = st.radio("Оберіть час:", answers["time_per_week"])
    if st.button("Далі"):
        st.session_state.data['time_per_week'] = time_per_week
        st.session_state.step += 1
        st.rerun()

# 6-й КРОК: Тривалість курсу
elif st.session_state.step == 6:
    show_user_message(f"Час на навчання: {st.session_state.data.get('time_per_week','')}")
    show_bot_message("Яка тривалість курсу вам ближча?")
    course_duration = st.radio("Оберіть тривалість:", answers["course_duration"])
    if st.button("Далі"):
        st.session_state.data['course_duration'] = course_duration
        st.session_state.step += 1
        st.rerun()

# 7-й КРОК: Підхід до викладання
elif st.session_state.step == 7:
    show_user_message(f"Тривалість: {st.session_state.data.get('course_duration','')}")
    show_bot_message("Який підхід до викладання вам буде зручніший?")
    teaching_approach = st.radio("Оберіть підхід:", answers["teaching_approach"])
    if st.button("Далі"):
        st.session_state.data['teaching_approach'] = teaching_approach
        st.session_state.step += 1
        st.rerun()

# 8-й КРОК: Сертифікат
elif st.session_state.step == 8:
    show_user_message(f"Підхід: {st.session_state.data.get('teaching_approach','')}")
    show_bot_message("Чи важливий для вас сертифікат по завершенню курсу?")
    certificate = st.radio("Оберіть:", answers["certificate"])
    if st.button("Далі"):
        st.session_state.data['certificate'] = certificate
        st.session_state.step += 1
        st.rerun()

# 9-й КРОК: Платні курси
elif st.session_state.step == 9:
    show_user_message(f"Сертифікат: {st.session_state.data.get('certificate','')}")
    show_bot_message("Чи можна вам пропонувати платні курси?")
    paid_courses = st.radio("Оберіть:", answers["paid_courses"])
    if st.button("Далі"):
        st.session_state.data['paid_courses'] = paid_courses
        st.session_state.step += 1
        st.rerun()



# … (попередні кроки залишаються без змін)

elif st.session_state.step == 10:
    # Перевірка, що категорія вже зібрана
    if 'category' not in st.session_state.data:
        st.error("⚠️ Трапилася помилка: спочатку потрібно обрати категорію.")
        st.stop()

    show_user_message(f"Платні курси: {st.session_state.data.get('paid_courses','')}")
    show_bot_message("Для більш точної відповіді, оберіть цікаві вам теми (можна кілька):")
    subcats = categories.get(st.session_state.data['category'], [])
    selected_subcats = st.multiselect("Оберіть підкатегорії:", options=subcats)

    # Єдина кнопка “Показати курси” (з унікальним key)
    show_courses_btn = st.button("Показати курси", key="show_courses")
    if show_courses_btn:
        if not selected_subcats:
            st.warning("Будь ласка, оберіть хоча б одну підкатегорію.")
            st.stop()
        # Зберігаємо вибрані підкатегорії та позначаємо, що пошук виконано
        st.session_state.data['subcategory'] = selected_subcats
        st.session_state.data['search_done'] = True
        st.session_state.data['gpt_requested'] = False
        st.rerun()

    # Якщо пошук ще не було виконано — просто виходимо, чекаємо натискання
    if not st.session_state.data.get('search_done', False):
        st.stop()

    # --------------------------------------
    # Далі: ми в стані search_done == True
    # Відображаємо обрані підкатегорії і виконуємо пошук курсів
    # --------------------------------------
    show_user_message(f"Обрані підкатегорії: {', '.join(st.session_state.data['subcategory'])}")
    show_bot_message("🔎 Шукаємо курси за вашими критеріями...")

    # Виконуємо фільтрацію курсів (гнучка логіка, ігноруємо відсутні поля)
    results = []
    for c in courses:
        # 1) Фільтр за категорією (обов’язково)
        if c.get('category') != st.session_state.data['category']:
            continue

        # 2) Рівень (якщо у курсі є поле 'level')
        course_levels = c.get('level')
        if course_levels:
            if isinstance(course_levels, str):
                course_levels = [course_levels]
            if st.session_state.data['level'] not in course_levels:
                continue

        # 3) Платність (якщо є поле 'price')
        course_price = c.get('price')
        if course_price:
            if st.session_state.data['paid_courses'] == "Ні" and course_price != "Безкоштовні":
                continue

        # 4) Сертифікат (якщо є поле 'certificate')
        course_cert = c.get('certificate')
        cert_req = st.session_state.data['certificate']
        if cert_req != "Неважливо" and course_cert:
            if course_cert != cert_req:
                continue

        # 5) Підкатегорії (якщо є поле 'subcategory')
        course_subcats = c.get('subcategory')
        if course_subcats:
            if isinstance(course_subcats, str):
                course_subcats = [course_subcats]
            if not any(sub in course_subcats for sub in st.session_state.data['subcategory']):
                continue

        # 6) Мета (якщо є поле 'goal')
        course_goals = c.get('goal')
        if course_goals:
            if isinstance(course_goals, str):
                course_goals = [course_goals]
            if st.session_state.data['goal'] not in course_goals:
                continue

        course_duration = c.get('duration')
        if course_duration == "Короткі курси (1-2 тижні)":
        # 1-2 тижні = 7-14 днів
            filtered_courses = [c for c in filtered_courses if 7 <= c["duration"] <= 14]

        elif course_duration == "Довгі курси (понад 2 тижні)":
             filtered_courses = [c for c in filtered_courses if c["duration"] > 14]

        elif course_duration == "Швидкі курси (до 5 днів)":
            filtered_courses = [c for c in filtered_courses if c["duration"] <= 5]

        # Якщо курс пройшов усі перевірки — додаємо до результатів
        results.append(c)

    if not results:
        st.warning("😔 На жаль, курсів за вашими критеріями не знайдено.")
        st.stop()

    # Виведення перших 5 знайдених курсів
    for idx, course in enumerate(results[:5], 1):
        st.markdown(f"**{idx}. [{course['title']}]({course['url']})**")
        st.write(course['description'])
        lvls = course.get('level') or []
        if isinstance(lvls, str):
            lvls = [lvls]
        st.write(f"Рівень: {', '.join(lvls)} | Ціна: {course.get('price','Невідомо')} | Сертифікат: {course.get('certificate','Немає')}")

    # Тепер викликаємо GPT лише коли натиснули відповідну кнопку  
    if not st.session_state.data.get('gpt_requested', False):
        if st.button("🧠 Пояснити від GPT", key="explain_gpt"):
            st.session_state.data['gpt_requested'] = True

            # Формуємо prompt із перших трьох курсів для GPT
            prompt = (
                f"Користувач шукає курси для мети '{st.session_state.data['goal']}', "
                f"рівень '{st.session_state.data['level']}', "
                f"категорія '{st.session_state.data['category']}', "
                f"підкатегорії: {', '.join(st.session_state.data['subcategory'])}.\n"
                f"Ось знайдені курси:\n"
            )
            for c in results[:3]:
                prompt += f"- {c['title']}: {c['description']}\n"
            prompt += "Поясни, чому ці курси можуть бути корисні користувачу."

            try:
                response = openai.chat.completions.create(
                    model="gpt-4o",
                    messages=[{"role": "user", "content": prompt}],
                    max_tokens=300
                )
               
                gpt_text = response.choices[0].message.content

                st.session_state.data['gpt_response'] = gpt_text

            except RateLimitError:
             st.session_state.data['gpt_response'] = (
             "На жаль, пояснення GPT зараз недоступне через обмеження квоти. "
             "Спробуйте пізніше."
                    )
            except AuthenticationError:
             st.session_state.data['gpt_response'] = (
            "Помилка автентифікації: переконайтеся, що ваш API-ключ дійсний."
                    )
            except Exception as e:
             st.session_state.data['gpt_response'] = (
        f"Сталася невідома помилка при зверненні до GPT: {e}"
                    )

            st.rerun()
        else:
            st.stop()

    # Якщо ми вже сюди дійшли — 'gpt_requested' == True, тому виводимо відповідь від GPT:
    show_bot_message("Ось пояснення від GPT:")
    st.markdown(st.session_state.data.get('gpt_response', "Відповідь відсутня."))
  
  



