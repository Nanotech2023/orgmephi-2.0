# Code of conduct

[[_TOC_]]

### Условные обозначения
- [Gitlab issues](https://gitlab.com/temikmax/org-mephi-2.0/-/issues): `Issues`, `Issue`
- [Merge Request](https://gitlab.com/temikmax/org-mephi-2.0/-/merge_requests): `MR`
- Code Review: `CR`
- Основная ветка: `master`
- Основная ветка разработки (frontend): `frontend`
- Основная ветка разработки (develop-backend): `backend`
- Сервер `staging`: виртуальная машина/окружение, предназначенное для хостинга создаваемого веб-приложения

### Сервер разработки
???

### Правила работы с Git

1. **Основа - [GitLab Flow](https://docs.gitlab.com/ee/topics/gitlab_flow.html#production-branch-with-gitlab-flow)**
1. `Issue` ставятся в `Issues`
1. Фиксированные ветки:
    - `master`
    - `frontend`
    - `backend`
1. Пушить напрямую в `master` запрещено
1. Все изменения в `master` можно добавить только через `MR` из веток `frontend` и `backend`
    * Название `Merge {{ source_branch }} to master {{ текущая_дата }}`
    * Закрыть `MR` можно только с согласованием `Maintainer` от команды `frontend` и `Maintainer` от команды `backend`
1. Все изменения в API взаимодействия между `frontend` и `backend` должны проходить двойное согласование между `Maintainer` от команды `frontend` и `Maintainer` от команды `backend`
1. В качестве исключения, создать `MR` можно напрямую в ветку `master`, только если изменения в коде касаются конфигруации CI/CD или регламентов разработки

### Правила взаисодействия со статусом задач
1. `Issue` в статусе `status: stuck`, если что-то блокирует азадчу: дизайн, API или реализованный backend. Это необходимо отобразить с соответвующими labels
1. `Issue` в статусе `status: open`, если она готова к реализации и все необходимые блокирующие элементы, включая дизайн, API, или backend разрешены
1. `Issue` в статусе `status: in progress`, если она в процессе реализации. Реализация `Issue` включает в себя:
    - Написание код
    - Написание тестов
    - Проходение тестов в системе CI
1. `Issue` в статусе `status: on review`, если она реализована и требуется `CR`. В процессе необходимо:
    - Получить подтверждение, что функционал отвечает требованиям ТЗ и API
    - Получить подтверждение, что соблюдены требования дизайна и получено подтверждение от дизайнера
1. `Issue` в статусе `status: done`, если она реализована, одобрено `CR` и код добавлен в соотствующую ветку разработки. В том числе:
    - Пройдено `CR`
    - Добавляемый функционал отвечает требованиям ТЗ и API
    - Соблюдены требования дизайна и получено подтверждение от дизайнера
    - Закрыт `MR` и изменения добавлены в соответствующую ветку разработки: `frontend` или `backend`
1. `Issue` считается закрытой
    - Код из соответствующей ветки разработки (`frontend` или `backend`) добавлен в ветку `master`
    - ? Изменения опубликованы на сервере `staging`? -- требуется информация о сервере `staging`

### Правила со взаисодействия со статусом MR
1. `MR` не может иметь label `status:`
1. Если `Issue`, соотвествующий `MR` находится в статусе `status: in progress`, то имя `MR` должно следовать шаблону `Draft: Resolve "Имя_задачи"`
1. Если `Issue`, соотвествующий `MR` находится в статусе `status: in review`, то имя `MR` должно следовать шаблону `Resolve "Имя_задачи"`
1. Если `Issue`, соотвествующий `MR` находится в статусе `status: done`, то имя `MR` должно следовать шаблону `Resolve "Имя_задачи"`, а `MR` сам должен быть в состоянии `merged`


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
1. Пушить напрямую в ветку `frontend` запрещено
1. Все изменения в `frontend` можно добавить только через `MR`
1. Каждая `Issue` реализуется в отдельной рабочей ветке
1. Рабочие ветки создаются в `Issues` путём создания `MR` в `frontend`
    * Название `Resolve "Название задачи"`
    * Закрыть `MR` можно только с согласованием `Maintainer` или `Developer` от команды `frontend`
    * При согласовании `MR` следует руководствоваться [Инженерными практиками Google для Code Review](https://tproger.ru/translations/code-review-a-la-google/)
1. При появлении изменений в `master` необходимо в срочном порядке создать `MR` из `master` в `frontend`
    * Название `Merge master to frontend {{ текущая_дата }}`
    * Закрыть `MR` можно только с согласованием `Maintainer` от команды `frontend`
    * Конфликты необходимо разрешать в пользу ветки `master`

### Инструменты разработки
- [JetBrains WebStorm 2021.1](https://www.jetbrains.com/webstorm/)
    - Code style находится в файле `.idea/codeStyles/Project.xml`
- [Node.js 14 LTS](https://nodejs.org/en/)
- [yarn 1.22.5](https://classic.yarnpkg.com/en/docs/install/)

### Скрипты для сборки
- `yarn --cwd frontend install` - устанавливает зависимости Node.js в папку `frontend/node_modules`
- `yarn --cwd frontend debug` - запускает версию для отладки в конфигурации *hot module replacement* по адресу `http://localhost:4200`
    - Необходимо установить зависимости Node.js 
- `yarn --cwd frontend build` - собирает production версию в папку `frontend/dist`
    - Необходимо установить зависимости Node.js
- `yarn --cwd frontend production` - запускает production версию из папку `frontend/dist` по адресу `http://localhost:3000`
    - Необходимо установить зависимости Node.js и собрать production версию




# Backend code of conduct
### Участники команды
1. [Святослав Дмитриев](https://gitlab.com/sodmitriev) - Maintainer
1. [Михаил Григорьев](https://gitlab.com/grigorevmp) - Developer
1. [Марат Хисамутдинов](https://gitlab.com/marat.ai) - Developer