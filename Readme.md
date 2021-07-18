# Code of conduct

[[_TOC_]]

### Правила работы с Git

1. **Основа - [GitLab Flow](https://docs.gitlab.com/ee/topics/gitlab_flow.html#production-branch-with-gitlab-flow)**
1. Задачи ставятся в [Gitlab issues](https://gitlab.com/temikmax/org-mephi-2.0/-/issues).
1. Фиксированные ветки:
    1. Основная ветка: `master`
    1. Ветка разработки frontend: `frontend`
    1. Ветка разработки backend: `backend`
1. Пушить напрямую в основную ветку запрещено
1. Все изменения в основную ветку можно добавить только через [merge request](https://gitlab.com/temikmax/org-mephi-2.0/-/merge_requests) из веток `frontend` и `backend`
   * Закрыть merge request можно только с согласованием `Owner`, `Maintainer` от команды `frontend` и `Maintainer` от команды `backend`

### Правила закрытия задач
Задача считается закрытой, если
1. Написан код и тесты
1. Пройдены тесты на сервере
1. Пройдено *Code Review*
1. Добавляемый функционал отвечает требованиям ТЗ и API
1. Соблюдены требования дизайна и получено подтверждение от дизайнера
1. Закрыт *Merge Request* и изменения добавлены в соответствующую ветку разработки

### Правила именования коммитов
#### Общий стиль
> `тип коммита`: `для какой сущности` `подробности`

Примеры:
> `add: mass email send method to MailSenderService`

> `fix: flaky exception in MailSenderService`

> `test: fix failed unit tests`

#### Язык
Английский. Простое настоящее время (Present Simple).

#### Типы коммитов
- `add` - добавление новой функциональности
- `fix` - исправление бага
- `style` - исправление опечаток и форматирования
- `refactor` - рефакторинг кода
- `ci` - всё, что связано с конфигурацией CI/CD/k8s
- `docs` - всё, что касается документации
- `test` - всё, что связано с тестированием
- `chore` - обычное обслуживание кода




# Frontend code of conduct

### Участники команды
1. [Артем Чернышов](https://gitlab.com/ache) - Maintainer
1. [Анита Баландина](https://gitlab.com/anita-balandina) - Developer
1. Марина Петрова - Дизайнер

### Правила работы с Git
1. Пушить напрямую в ветку разработки frontend запрещено
1. Каждая задача реализуется в отдельной рабочей ветке
1. Рабочие ветки создаются в [Gitlab issues](https://gitlab.com/temikmax/org-mephi-2.0/-/issues) путём создания [merge request](https://gitlab.com/temikmax/org-mephi-2.0/-/merge_requests) в **ветку разработки frontend** 
1. Все изменения в ветку разработки frontend можно добавить только через [merge request](https://gitlab.com/temikmax/org-mephi-2.0/-/merge_requests)
    * Закрыть merge request можно только с согласованием `Maintainer` от команды `frontend`

### Инструменты разработки
- [JetBrains WebStorm 2021.1](https://www.jetbrains.com/webstorm/)
- [Node.js 14 LTS](https://nodejs.org/en/)
- [yarn 1.22.5](https://classic.yarnpkg.com/en/docs/install/)

### Скрипты для сборки
- `yarn --cwd frontend install` - устанавливает зависимости Node.js в папку `frontend/node_modules`
- `yarn --cwd frontend debug` - запускает версию для отладки в конфигурации *hot module replacement* по адресу `http://localhost:4200`
    - Необходимо установить зависимости Node.js 
- `yarn --cwd frontend build` - собирает production версию в папку `frontend/dist`
    - Необходимо установить зависимости Node.js




# Backend code of conduct
### Участники команды
1. [Святослав Дмитриев](https://gitlab.com/sodmitriev) - Maintainer
1. [Михаил Григорьев](https://gitlab.com/grigorevmp) - Developer
1. [Марат Хисамутдинов](https://gitlab.com/marat.ai) - Developer