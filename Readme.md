# Code of conduct

### Работа с Git

1. **Основа - [GitLab Flow](https://docs.gitlab.com/ee/topics/gitlab_flow.html#github-flow-as-a-simpler-alternative)**
1. Задачи ставятся в [Gitlab issues](https://gitlab.com/temikmax/org-mephi-2.0/-/issues).
1. [Основная ветка](https://docs.gitlab.com/ee/topics/gitlab_flow.html#github-flow-as-a-simpler-alternative): `master`
1. Пушить напрямую в основную ветку запрещено
1. Все изменения в основную ветку необходимо проводить через [merge request](https://gitlab.com/temikmax/org-mephi-2.0/-/merge_requests)
1. Добавить изменения в основую ветку через merge request может только участник уровня Maintainer
1. Ветки под разработку создаются в [Gitlab issues](https://gitlab.com/temikmax/org-mephi-2.0/-/issues)


# Frontend code of conduct

### Участники команды
1. [Артем Чернышов](https://gitlab.com/ache) - Maintainer
1. [Анита Баландина](https://gitlab.com/anita-balandina) - Developer
1. Марина Петроа - Дизайнер

### Задача считается закрытой, если
1. Написан код и тесты
1. Пройдены тесты на сервере
1. Пройдено *Code Review*
1. Соблюдены требования дизайна и получено подтверждение от дизайнера
1. Закрыт *Merge Request* и изменения добавлены в основную ветку

### Скрипты для сборки
Скрипты необходимо запускать в папке `frontend`
- `yarn/npm install` - устанавливает зависимости node_js
- `yarn/npm debug` - запускает версию для отладки в конфигурации hot module replacement
- `yarn/npm build` - собирает production версию

### Правила именования коммитов
#### Общий стиль
> `тип коммита`: `для какой сущности` `подробности`

Примеры:
> `add: mass email send method to MailSenderService`

> `fix: flaky exception in MailSenderService`

> `test: fix failed unit tests`

#### Язык
Английский. Простое настоящее время (Present Simple).

#### Возможные типы коммитов
- `add` - добавление новой функциональности
- `fix` - исправление бага
- `style` - исправление опечаток и форматирования
- `refactor` - рефакторинг кода
- `ci` - всё, что связано с конфигурацией CI/CD/k8s
- `docs` - всё, что касается документации
- `test` - всё, что связано с тестированием
- `chore` - обычное обслуживание кода


# Backend code of conduct
TODO?
