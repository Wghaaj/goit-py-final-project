# goit-py-final-project
# Personal Assistant (first draft)

### 1. Початок роботи
- клонуйте репозиторій
- Створіть віртуальне середовище:
``` bash
python3 -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements.txt
python main.py
```

Для Windows PowerShell замість перших двох команд використовуйте py -m venv .venv та .\.venv\Scripts\Activate.ps1.

### 2. Створення нової гілки
Кожен працює у власній feature-гілці. Наприклад, feature/contacts.
```bash
git status
git switch main
git pull --ff-only origin main
git switch -c feature/contacts
```
Не створюйте гілку зі старої версії main та не працюйте безпосередньо в main.

### 3. Збереження та відправлення змін
``` bash
    git status #якщо захочете перевірити гілку
    git diff  #якщо захочете подивитися змінені файли 
```

``` bash
git add .
git commit -m "description"
git push origin HEAD
```

### 4. Перед кожним початком роботи в існуючій гілці

Перейдіть у свою гілку та збережіть попередні зміни (якщо є):

```bash
git switch feature/contacts
git add .
git commit -m "Describe changes"
git push origin HEAD
```

Отримайте актуальні зміни з GitHub та main:

```bash
git pull --ff-only origin <branch>
git fetch origin
git merge origin/main
```

У разі виникнення конфліктів зверніться до Team Lead.

### 5. Pull Request (PR)
1. Перевірте, що програма запускається та ваш функціонал працює.
2. Зробіть commit та push усіх необхідних змін у свою гілку.
3. На GitHub відкрийте Pull requests → New pull request.
4. Оберіть base: main, compare: свою feature-гілку.
5. Напишіть коротку назву, опис змін та як їх перевірити.
6. Створіть PR та запросіть review.

Якщо потрібні виправлення, внесіть їх у ту саму гілку, зробіть commit та push. PR оновиться автоматично. Новий PR створювати не потрібно.

Після погодження Team Lead виконує merge. Лише тоді зміни потрапляють у main.

### 6. Після merge
```bash
git switch main
git pull --ff-only origin main
```
Для нової задачі створіть нову feature-гілку з актуальної main.

### 7. Якщо виник merge conflict
Не використовуйте force push або reset --hard. Повідомте Team Lead, якщо не впевнені у виправленні. Якщо конфлікт виник під час git merge origin/main, відкрийте конфліктні файли, узгодьте правильний код, приберіть маркери конфлікту, додайте виправлені файли через git add, виконайте git commit та git push. Якщо потрібно скасувати саме незавершений merge, використайте git merge --abort.

### 8. Правила команди
- Заборонено push безпосередньо в main та самостійний merge PR.
- Перед початком роботи синхронізуйте свою гілку з main; наприкінці сеансу робіть commit і push.
- Не редагуйте чужі файли без попереднього узгодження.
- Пишіть зрозумілі повідомлення комітів
- Дотримуйтеся PEP 8, перевіряйте некоректне введення та збереження даних.
- Нові сторонні бібліотеки узгоджуйте з командою та додавайте до requirements.txt.

### 9. Корисні команди
```bash
git status	#Поточна гілка та стан файлів
git branch -a	#Список гілок
git diff	#Незастейджені зміни
git diff --cached	#Зміни для наступного коміту
git log --oneline -5	#Останні п'ять комітів
git fetch origin	#Отримати інформацію про віддалені гілки
```