# Опросники об отношениях: бесплатные, открытые, в браузере

**[Пройти сейчас →](https://pairclear.github.io/relationship-questionnaires/?lang=ru)** · [English](README.md) · [Данные (JSON)](data/questionnaires/) · [Навык для Claude](SKILL.md) · [Проверка лицензий валидированных шкал](docs/licence-check.md)

![7 опросников](https://img.shields.io/badge/опросники-7-2ea44f) ![Работает офлайн](https://img.shields.io/badge/офлайн-да-2ea44f) ![Без слежки](https://img.shields.io/badge/слежка-нет-2ea44f) ![RU + EN](https://img.shields.io/badge/lang-RU%20%7C%20EN-blue) ![CC BY 4.0](https://img.shields.io/badge/тексты-CC%20BY%204.0-lightgrey) [![Сделано PairClear](https://img.shields.io/badge/сделано-PairClear-b85c3c)](https://pairclear.com/ru/?utm_source=github&utm_medium=readme&utm_campaign=relationship-questionnaires)

> **Саморефлексия, а не диагностика.** Опросники написаны PairClear и в исследованиях не валидированы. Они смотрят на то, что происходит между двумя людьми, а не на чью-то психику, и не могут сказать, что чувствует партнёр. Если ты боишься партнёра, тебе угрожают или тебя контролируют, или есть мысли навредить себе, звони в экстренную службу (112) или найди бесплатную линию помощи на [findahelpline.com](https://findahelpline.com). В России для женщин, пострадавших от насилия: 8-800-7000-600.

Семь коротких опросников (от 8 до 11 утверждений) с открытыми данными, правилом подсчёта, которое может проверить каждый, и страницей, которая целиком работает в браузере.

## Опросники

| Опросник | О чём | Части | Для печати |
|---|---|---|---|
| Пульс пары | Проверка раз в неделю за 2 минуты | Близость, напряжение | [RU](questionnaires/couple-pulse.ru.md) · [EN](questionnaires/couple-pulse.en.md) |
| Одна ссора или система? | Как проходят ссоры | Повторяющийся круг, эскалация, примирение (+2 вопроса о безопасности) | [RU](questionnaires/conflict-pattern.ru.md) · [EN](questionnaires/conflict-pattern.en.md) |
| Что изменилось в нашем общении | Когда кажется, что партнёр отдаляется | Изменения в общении, сколько это у меня забирает | [RU](questionnaires/contact-changes.ru.md) · [EN](questionnaires/contact-changes.en.md) |
| Кто тянет отношения | Ранняя или неопределённая стадия | Перекос вклада, ясность | [RU](questionnaires/effort-balance.ru.md) · [EN](questionnaires/effort-balance.en.md) |
| Мы вместе или нет? | «Неопределённые отношения» | Ясные сигналы, чего мне стоит неопределённость | [RU](questionnaires/relationship-clarity.ru.md) · [EN](questionnaires/relationship-clarity.en.md) |
| Кто всё помнит | Невидимая нагрузка дома | Моя доля невидимой работы, можем ли мы об этом говорить | [RU](questionnaires/mental-load.ru.md) · [EN](questionnaires/mental-load.en.md) |
| После расставания: где я сейчас | Недели или месяцы спустя | Ещё держусь за прошлое, возвращаюсь к своей жизни | [RU](questionnaires/after-breakup.ru.md) · [EN](questionnaires/after-breakup.en.md) |

## Как считается результат

На каждое утверждение отвечают по одной шкале: 0 Никогда, 1 Редко, 2 Иногда, 3 Часто, 4 Почти всегда. Пункты с пометкой `"rev": true` переворачиваются (4 минус ответ). Каждая часть это среднее её пунктов, от 0 до 4. Ниже 1,5 показывается как «низко», от 1,5 до 2,5 «середина», выше 2,5 «высоко», и к каждому уровню короткий текст о том, что стоит обсудить.

Эти уровни не нормы и не клинические пороги. Данных по этим вопросам ещё никто не собирал, так что «высоко» значит только то, что ты часто отвечал(а) «часто». Два вопроса в опроснике «Одна ссора или система?» о безопасности: они не считаются в баллы, и если на любой ответить «иногда» или чаще, результат сначала покажет, куда обратиться.

## Почему вопросы свои

Мы хотели опубликовать известные валидированные шкалы, переведённые и бесплатные. 26.11.2026 мы проверили восемь (Couples Satisfaction Index, его немецкую версию под CC BY, ECR-R, ECR-RS, Relationship Assessment Scale, M-QoRS, Dyadic Adjustment Scale, опросники Готтмана). Ни у одной условия не разрешают явно всем публиковать, переводить и использовать пункты в коммерческих целях: большинство «бесплатно для исследований», для некоторых нужно разрешение или покупка. Подробно и с источниками: [docs/licence-check.md](docs/licence-check.md).

Поэтому вопросы наши, под CC BY 4.0, и честно помечены как невалидированные. Исследователи могут их валидировать или адаптировать.

## Для разработчиков

- `data/questionnaires/<id>.json`: по файлу на опросник, пункты на EN и RU, части, тексты уровней, вопросы для размышления, ссылки. `data/questionnaires.json` собирает все семь.
- `python3 build.py` проверяет данные (в каждой части не меньше 3 пунктов, у каждого текста оба языка) и заново собирает Markdown, общий файл и `index.html`.
- `index.html` это один файл без зависимостей и без сетевых запросов. Адрес `?q=conflict-pattern&lang=ru` сразу открывает нужный опросник.

## Вопросы

**Можно использовать с клиентами?** Да, как повод для разговора. Не используйте как инструмент оценки: опросники не валидированы.

**Можно заполнить вдвоём с партнёром?** Да, так лучше всего. Заполните по отдельности, сравните по частям и поговорите о самой большой разнице.

**Скажет ли опросник, что партнёр теряет интерес?** Нет, опросник, который заполняешь один, этого не может. «Что изменилось в нашем общении» показывает то, что ты заметил(а), и сколько сил это забирает; остальное это разговор.

**Где хранятся ответы?** Нигде. Страница держит их в памяти и забывает, когда закрываешь вкладку.

## Связанное

- [Тесты PairClear](https://pairclear.com/ru/tests/?utm_source=github&utm_medium=readme&utm_campaign=relationship-questionnaires): [Конфликт или система?](https://pairclear.com/ru/tests/konflikt-ili-sistema/?utm_source=github&utm_medium=readme&utm_campaign=relationship-questionnaires), [Она отдаляется?](https://pairclear.com/ru/tests/ona-otdalyaetsya/?utm_source=github&utm_medium=readme&utm_campaign=relationship-questionnaires), [Он вкладывается или удерживает?](https://pairclear.com/ru/tests/on-vkladyvaetsya-ili-uderzhivaet/?utm_source=github&utm_medium=readme&utm_campaign=relationship-questionnaires), [Твой сценарий после расставания](https://pairclear.com/ru/tests/tvoy-scenariy-posle-rasstavaniya/?utm_source=github&utm_medium=readme&utm_campaign=relationship-questionnaires)
- [Я не психотерапевт](https://github.com/pairclear/not-a-therapist): правила безопасного разговора для ИИ-чатов
- [16 ассоциаций](https://github.com/pairclear/sixteen-associations): упражнение для саморефлексии в браузере

## Как помочь

Переводы приветствуются: добавьте ключ языка рядом с `en` и `ru` в каждом JSON и в `T` в `src/template.html`, затем запустите `python3 build.py`. Пожалуйста, сохраняйте тексты о невалидированности и безопасности.

## Лицензия

Код (`build.py`, `index.html`, `src/`): [MIT](LICENSE). Опросники, тексты и данные: [CC BY 4.0](LICENSE-TEXT.md). Написано с помощью ИИ.
