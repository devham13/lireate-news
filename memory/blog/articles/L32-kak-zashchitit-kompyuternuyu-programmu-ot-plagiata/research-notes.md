# Research notes — L32 «Как защитить компьютерную программу от плагиата: регистрация, договоры и досудебка»

**topic_id:** L32  
**site:** lireate (рубрика «Программа ЭВМ», `lireate_category_id=19`)  
**slug:** kak-zashchitit-kompyuternuyu-programmu-ot-plagiata  
**article_mode:** B (checklist / how-to)  
**search_intent:** checklist  
**target_service:** reg-po / защита ПО  
**research_date:** 2026-11-04  
**disclaimer:** Нормы ГК РФ, регламенты Роспатента и судебная практика проверены на 04.11.2026. Материал не заменяет индивидуальную юридическую консультацию.

**Угол (карточка):** десктоп, SaaS, исходники; ст. 1261, депонирование в Роспатенте, NDA, претензия. **Не дублировать L20** (мобильное приложение: ПО vs ТЗ, сторы, классы МКТУ).

---

## Яндекс Вордстат

**⚠️ WORDSTAT AUTH WARNING:** namespace `user-mcp-kv` (инструмент `wordstat_get_top_requests`) в среде Cloud Agent не подключён. Точные показы в месяц **не получены**; объёмы спроса в текст статьи не включать.

При появлении MCP обновить токен: https://oauth.yandex.ru/authorize?response_type=token&client_id=c654b948515a4a07a4c89648a0831d40

**Внутренний сигнал спроса (Метрика lireate, не для публикации):** кластер SEO от 02.11.2026 (`blog-topics.md`, `metrika_visits`).

**Экспертная семантика (без объёмов, для writer):**

| Фраза | Роль |
|-------|------|
| как защитить компьютерную программу от плагиата | primary_query |
| незаконное использование программы для эвм | secondary |
| доказательства копирования кода | secondary |
| депонирование исходного кода роспатент | LSI |
| претензия нарушение прав на программу | LSI |
| NDA исходный код разработчик | LSI |
| ст 1261 гк программа для эвм | LSI |
| регистрация программы для эвм пошлина | LSI |
| git история коммитов авторское право | LSI |
| SaaS защита кода от копирования | LSI |
| лицензионное соглашение EULA | LSI |
| компенсация ст 1301 программа | LSI |

**Критично для SEO:** в выдаче смешиваются «защита научной работы от плагиата», «контент сайта» и «пиратство лицензий». В lead и H1 — **именно программа для ЭВМ (код)**, не текстовый антиплагиат и не только пиратство Windows/Office.

---

## 1. SERP-обзор (WebSearch + research-serp.json, ноябрь 2026)

**Паттерн:** повторяются материалы Тинькофф Журнала / bashukchichkanov.com («пять способов»), обзоры gpg.ru, Habr 741374 (ПО и БД), юрфирмы про регистрацию. Сильнее всего по **досудебке и доказательствам** — [Habr 1042622](https://habr.com/ru/articles/1042622/), [nevskylaw.ru — претензия](https://nevskylaw.ru/knowledge/pretenziya-za-narushenie-isklyuchitelnyh-prav-na-po/), [Habr 1033846 — миф регистрации](https://habr.com/ru/articles/1033846/), [aglegal на Habr 1072018](https://habr.com/ru/companies/aglegal/articles/1072018/). Официальный контур: [ст. 1261](https://www.consultant.ru/document/cons_doc_LAW_64629/ce1359ed5b9bd99896d7a496c7887e7c223a2cbc/), [ст. 1262](https://www.consultant.ru/document/cons_doc_LAW_64629/d0887a7ca3da6c85fbbce19815b9b1ead5e67687/), [услуга Роспатента](https://rospatent.gov.ru/ru/stateservices/gosudarstvennaya-registraciya-programmy-dlya-elektronnyh-vychislitelnyh-mashin-ili-bazy-dannyh-i-vydacha-svidetelstv-o-gosudarstvennoy-registracii-programmy-dlya-elektronnyh-vychislitelnyh-mashin-ili-bazy-dannyh-ih-dublikatov).

**Пробел Lireate:** единый **чек-лист для владельца десктоп/SaaS-продукта**: что охраняет ст. 1261 → как фиксировать версии (git + депонирование без иллюзий) → договоры и NDA → как отличить копирование кода от «повторили функционал» → претензия по ст. 1252.1 / 1301 → когда ссылаться на L20 (мобилка) и на материал Lireate про правовые методы.

| # | URL | Тип | Сильные стороны | Слабые / пробелы | Не копировать |
|---|-----|-----|-----------------|------------------|---------------|
| 1 | [bashukchichkanov — 5 способов](https://www.bashukchichkanov.com/press/pyat-sposobov-zashchitit-kompyuternuyu-programmu-ot-plagiata-v-materiale-tinkoff-zhurnala/) | Обзор | Популярные меры | Без чек-листа досудебки | Структуру 1:1 |
| 2 | [gpg.ru — можно ли защитить](https://gpg.ru/magazine/itproducts/mozhno-li-zashchitit-kompyuternuyu-programmu-ot-plagiata.html) | Журнал | Базовые способы | Старый контекст | — |
| 3 | [Habr 741374 — ПО и БД](https://habr.com/ru/articles/741374/) | Гайд | Правовые способы | Не SaaS-чек-лист | — |
| 4 | [Habr 1033846 — миф регистрации](https://habr.com/ru/articles/1033846/) | Аналитика | СИП/ВС, git, пределы депонирования | Длинный нarrative | — |
| 5 | [Habr 1042622 — алгоритм при копировании](https://habr.com/ru/articles/1042622/) | Workflow | Идеи vs код, превентивные меры | Фокус «сайт/приложение» | Путать с L20 целиком |
| 6 | [nevskylaw — претензия](https://nevskylaw.ru/knowledge/pretenziya-za-narushenie-isklyuchitelnyh-prav-na-po/) | Гайд | 4 элемента претензии, сравнение, 1252.1 | Не про регистрацию пакета | — |
| 7 | [saenko-group — реестр и плагиат](https://saenko-group.ru/press-center/articles/zashhita-programmnogo-obespecheniya-ot-plagiata-pri-pomoshhi-yurista/) | Бюро | Акцент на исходный код | Упрощения про «только код» | — |
| 8 | [brandr — регистрация 2026](https://brandr.legal/ru/regystraczyya-avtorskogo-prava-na-komp/) | Бюро | Актуальный год | Коммерческий тон | — |
| 9 | [copytrust — регистрация](https://www.copytrust.ru/articles/registratsiya-prav-na-programmi-i-programmnoe-obespechenie) | Бюро | Пакет документов | — | — |
| 10 | [Консультант — незаконное использование ПО](https://www.consultant.ru/law/podborki/otvetstvennost_za_nezakonnoe_ispolzovanie_programmnogo_obespecheniya/) | Подборка | НПА | Не how-to | — |

**Intent (checklist):** основатель продукта (десктоп, on-prem, SaaS) хочет **до и после инцидента** понять: нужна ли регистрация в Роспатенте, как закрыть права у команды, что положить в NDA, как доказать копирование **кода**, когда писать претензию и какую компенсацию заявлять.

---

## 2. Антиканнибализация (материалы Lireate)

| Материал | Фокус | Как отстроить L32 |
|----------|-------|-------------------|
| **L20** — `/registraciya_mobilnogo_prilozheniya_programma_dlya_evm_ili_tovarnyy_znak` | Мобильное приложение: **ПО vs ТЗ**, сторы, классы 9/42/35 | L32 — **защита от плагиата кода**; одна отсылка «для мобилки и знака — L20» |
| `/zaschita_kompyuternoy_programmyi_i_bazyi_dannyix_pravovyie_metodyi` | Общие правовые методы ПО и БД | L32 — **практический чек-лист** + досудебка; не переписывать обзор |
| L11 — договор с дизайнером | UI/графика | L32 — NDA и права на **исходный код** у dev/подрядчиков |
| Habr 1042622 | Сайт + приложение + код | L32 явно про **ПО для ЭВМ**, не про копирование вёрстки сайта |

---

## 3. Таблица фактов (только с URL)

| Факт | Источник | Дата | Можно в текст |
|------|----------|------|---------------|
| Программа для ЭВМ охраняется как литературное произведение; объект — данные и команды в объективной форме, **исходный и объектный код**, подготовительные материалы, аудиовизуальные отображения (ст. 1261 ГК РФ) | [ст. 1261](https://www.consultant.ru/document/cons_doc_LAW_64629/ce1359ed5b9bd99896d7a496c7887e7c223a2cbc/) | ред. 2026 | да |
| С **01.01.2027** в ст. 1261 расширяется формулировка «Программы для ЭВМ» (ФЗ от 04.08.2026 № 296-ФЗ: устройства с автоматизированной обработкой на основе алгоритмов) | [ред. 04.08.2026](https://www.consultant.ru/document/cons_doc_LAW_76298/fc7e51e494a7e398d91682078caaf15de336c87a/) | 08.2026 | да (кратко, «с 2027») |
| Авторское право **возникает при создании**; регистрация для возникновения/защиты **не обязательна** (п. 4 ст. 1259 ГК РФ) | [ст. 1259](https://www.consultant.ru/document/cons_doc_LAW_64629/) | 2026 | да |
| **Не охраняются** идеи, концепции, принципы, методы, процессы, системы, способы решения задачи (п. 5 ст. 1259 ГК РФ) — повтор функционала при **своём коде** часто **не** нарушение | [Habr 1042622](https://habr.com/ru/articles/1042622/); [ст. 1259](https://www.consultant.ru/document/cons_doc_LAW_64629/) | 2026 | да |
| Государственная регистрация программы для ЭВМ **добровольна** (ст. 1262 ГК РФ); заявка — **одна программа**; формальная проверка документов, **без** экспертизы новизны/уникальности | [ст. 1262](https://www.consultant.ru/document/cons_doc_LAW_64629/d0887a7ca3da6c85fbbce19815b9b1ead5e67687/); [Habr 1033846](https://habr.com/ru/articles/1033846/) | 2026 | да |
| Сведения реестра считаются достоверными, **пока не доказано иное** (п. 6 ст. 1262 ГК РФ) — не отменяет спора об **реальном** авторстве | [ст. 1262](https://www.consultant.ru/document/cons_doc_LAW_64629/d0887a7ca3da6c85fbbce19815b9b1ead5e67687/); [Habr 1033846](https://habr.com/ru/articles/1033846/) | 2026 | да |
| Пошлина за регистрацию программы для ЭВМ — **5 000 ₽** (страница услуги Роспатента) | [rospatent.gov.ru](https://rospatent.gov.ru/ru/stateservices/gosudarstvennaya-registraciya-programmy-dlya-elektronnyh-vychislitelnyh-mashin-ili-bazy-dannyh-i-vydacha-svidetelstv-o-gosudarstvennoy-registracii-programmy-dlya-elektronnyh-vychislitelnyh-mashin-ili-bazy-dannyh-ih-dublikatov) | 2026 | да |
| Срок госуслуги по регистрации ПО — **62 рабочих дня** с даты приёма заявки | [rospatent.gov.ru](https://rospatent.gov.ru/ru/stateservices/gosudarstvennaya-registraciya-programmy-dlya-elektronnyh-vychislitelnyh-mashin-ili-bazy-dannyh-i-vydacha-svidetelstv-o-gosudarstvennoy-registracii-programmy-dlya-elektronnyh-vychislitelnyh-mashin-ili-bazy-dannyh-ih-dublikatov) | 2026 | да |
| Депонируемые материалы: исходный текст (полный или фрагменты) **в объёме, достаточном для идентификации** (п. 27 Правил по приказу № 211); лимит «70 страниц» — **устаревший** регламент | [приказ № 211 / п. 27](https://www.consultant.ru/document/cons_doc_LAW_201372/94378eca2a396e597d77fd93061fe54b609a5c25/); [Habr 305854](https://habr.com/ru/articles/305854/) | 2016+ | да |
| При подаче на бумаге код (кроме реферата) — **PDF/A** на машиночитаемом носителе; объём на носителе **не регламентирован**, но на практике эксперт ориентируется на проверку порядка **~50 страниц** (FAQ Роспатента) | [rospatent.gov.ru FAQ](https://rospatent.gov.ru/ru/stateservices/gosudarstvennaya-registraciya-programmy-dlya-elektronnyh-vychislitelnyh-mashin-ili-bazy-dannyh-i-vydacha-svidetelstv-o-gosudarstvennoy-registracii-programmy-dlya-elektronnyh-vychislitelnyh-mashin-ili-bazy-dannyh-ih-dublikatov) | 2026 | да*** |
| Роспатент **не проверяет** уникальность кода; регистрация = депонирование экземпляра на дату (позиция ВС по делу № А40-46622/2019; СИП № А60-46975/2016 — регистрация **не** единственное доказательство права) | [Habr 1033846](https://habr.com/ru/articles/1033846/) | 2020–2026 | да* |
| Для доказывания авторства суды учитывают **git-историю**, переписку, ТЗ, трекеры задач; нотариальный осмотр репозитория усиливает доказательства | [Habr 1033846](https://habr.com/ru/articles/1033846/); [nris.ru](https://nris.ru/baza-znanij/blog/kak-zashitit-ishodnyj-kod-chto-nuzhno-sdelat-razrabotchiku-do-vyhoda-produkta-na-rynok/) | 2026 | да |
| SaaS: ограничивать доступ к репозиториям, отзывать права подрядчикам, фиксировать выгрузки; NDA/конфиденциальность — отдельно или в договоре с подрядчиком | [nris.ru](https://nris.ru/baza-znanij/blog/kak-zashitit-ishodnyj-kod-chto-nuzhno-sdelat-razrabotchiku-do-vyhoda-produkta-na-rynok/) | 2026 | да |
| Без **отчуждения** исключительного права в договоре с разработчиком правообладатель может **не** иметь полномочий защищать код | [Habr 1042622](https://habr.com/ru/articles/1042622/); [advolaw.ru — кому код](https://advolaw.ru/articles/komu-prinadlezhit-kod) | 2026 | да |
| В спорах о коде нужно доказать **факт копирования**, а не только схожесть или одинаковый результат | [advolaw.ru](https://advolaw.ru/articles/komu-prinadlezhit-kod); [nevskylaw — скопировали код](https://nevskylaw.ru/knowledge/skopirovali-nash-programmnyy-kod-konkurent/) | 2026 | да |
| Претензия по ПО: объект + цепочка прав + способ использования + доказательства; **процент совпадения** без методики не заменяет юридический вывод | [nevskylaw.ru — претензия](https://nevskylaw.ru/knowledge/pretenziya-za-narushenie-isklyuchitelnyh-prav-na-po/) | 2026 | да |
| До иска об **убытках/коменсации** в арбитраже между юрлицами/ИП — **претензионный порядок** (п. 5.1 ст. 1252 ГК РФ); иск после отказа или **30 дней** без ответа (если договором не иной срок) | [nevskylaw.ru — претензия](https://nevskylaw.ru/knowledge/pretenziya-za-narushenie-isklyuchitelnyh-prav-na-po/); [ст. 1252](https://www.consultant.ru/document/cons_doc_LAW_64629/) | 2026 | да |
| Компенсация за нарушение исключительного права на произведение (в т.ч. программу): **10 000–10 000 000 ₽** либо 2× стоимость контрафактных экземпляров либо 2× стоимость права использования (ст. 1301 ГК РФ) | [ст. 1301](https://www.consultant.ru/document/cons_doc_LAW_64629/c2f79b53ce582e92680379e2ebd23eeb9fb7855a/) | ред. 2026 | да |
| Регистрация в реестре Минцифры — **отдельная** цель; часто мотивирует депонирование в Роспатенте, но **не заменяет** договоры и доказательную базу | [Habr 1003964](https://habr.com/ru/articles/1003964/); [dvitex.ru](https://www.dvitex.ru/poleznoe/biznes/intellektualnaya-sobstvennost/kak-zaregistrirovat-programmu-dlya-evm/) | 2026 | да*** |
| Патент на программу возможен только для **технического решения** с новизной; не заменяет охрану **текста кода** по авторскому праву | [dvitex.ru](https://www.dvitex.ru/poleznoe/biznes/intellektualnaya-sobstvennost/kak-zaregistrirovat-programmu-dlya-evm/) | 2026 | да*** |

\* Ссылки на судебные акты — через вторичный источник Habr с указанием номеров дел; в статье предпочтительно [Консультант / sudact] при наличии.  
\*\*\* Уточняющий контекст; не выдавать за обязательную норму без оговорки «на практике / по регламенту».

---

## 4. action_outline (writer)

1. **Развести объекты:** что защищает ст. 1261 (код, подготовительные материалы) vs что **не** защищает (идея, алгоритм «в голове», UI без отдельной охраны) — примеры десктоп/SaaS.
2. **Превентивный блок:** git + версии релизов; договоры с сотрудниками/фрилансом (отчуждение прав); NDA и режим доступа к репозиторию; лицензия/EULA для дистрибуции.
3. **Депонирование в Роспатенте:** добровольность, пакет (заявление, реферат, фрагмент кода), **5 000 ₽**, **62 раб. дня**; честно — формальная экспертиза, пределы свидетельства (ссылка Habr 1033846).
4. **Альтернативы/дополнения:** нотариат, коммерческое депонирование, переписка и ТЗ — **в связке**, не вместо договоров.
5. **Инцидент:** зафиксировать чужое использование (скриншоты, hash, выгрузка, экспертное сравнение фрагментов); не опираться только на «похожий интерфейс».
6. **Претензия:** 4 элемента (объект, цепочка прав, действие нарушителя, расчёт); обязательность для арбитража по компенсации (1252.1); срок ответа **30 дней**; варианты по ст. 1301.
7. **Дальше:** иск / обеспечительные меры — кратко, без дублирования отдельной статьи про суд.
8. **Отсылка L20:** мобильное приложение + товарный знак + сторы — **не этот чек-лист**; внутренняя ссылка на L20.
9. **Финальный чек-лист** «до релиза / после обнаружения копии» + CTA reg-po / консультация Lireate.

**reader_outcome:** читатель собирает **пакет защиты десктоп/SaaS-программы от копирования кода**: понимает роль ст. 1261, когда имеет смысл депонирование, как закрыть права у команды, как отличить плагиат кода от клонирования идеи и как оформить **претензию** до суда.

**utility_verdict:** PASS

---

## 5. Риски для GEO QA / writer

- Не обещать «100% защиту от плагиата» регистрацией в Роспатенте.
- Не смешивать с **антиплагиатом текстов** (dissertatsia.ru и т.п. из SERP).
- Не уходить в **L20** (МКТУ, App Store) длиннее одного блока-отсылки.
- Цифры компенсации — только **ст. 1301** в актуальной редакции (верхняя граница 10 млн ₽ в Consultant на 2026).
- ПДн в заявке Роспатента — согласие субъектов; ссылки на политику Lireate только канон `/politika_konfidencialnosti` и `/private_data` при упоминании форм.
