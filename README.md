# Study Boost: Telegram-бот для студентов  

**Study Boost** — это инновационный бот для Telegram, который помогает студентам обмениваться учебными материалами, зарабатывать баллы и получать вознаграждения. Бот создан для упрощения взаимодействия между студентами и предоставления доступа к широкому спектру полезной информации.

---

## 📚 Возможности  

### 🔍 **Поиск и публикация материалов**  
- **Обмен материалами**: лекции, лабораторные работы, контрольные, экзамены.  
- **Поиск по ключевым словам**: находите нужный материал за считанные секунды.  
- **Оценивание материалов**: лайки и дизлайки помогают выделить лучшие публикации.  

### 💡 **Советы и мероприятия**  
- **Советы от студентов**: делитесь своими лайфхаками и голосуйте за самые полезные советы.  
- **События и мероприятия**: участвуйте в студенческих активностях через платформу.  

### 🎁 **Система вознаграждений**  
- **Баллы за публикации**: чем больше вы делитесь, тем выше ваш рейтинг.  
- **Топ пользователей**: лидеры рейтинга получают денежные награды.  

### 🔗 **Реферальная программа**  
- Приглашайте друзей в бот и зарабатывайте баллы.  
- Если вы пригласили **10 пользователей**, получите **пожизненную бесплатную подписку**.  

### 💳 **Подписки**  
- Доступ к скачиванию материалов предоставляется через различные виды подписок.  
- Выберите подходящий тариф, чтобы получить максимальную выгоду.  

---

## 🛠️ Структура проекта  

```
├─── NI_assistants
│   └─── sentiment_text.py
├─── commands
│   ├─── commands_admin.py
│   └─── commands_users.py
├─── database
│   ├─── data
│   │   ├─── csv
│   │   ├─── events.db
│   │   ├─── help_suggestions.db        
│   │   ├─── materials.db
│   │   ├─── payments.db
│   │   ├─── subscription_status.db     
│   │   ├─── users.db
│   │   ├─── users_advice.db
│   │   └─── users_rating_history.db    
│   ├─── handlers
│   │   ├─── database_create.py
│   │   └─── database_handler.py        
│   ├─── requests
│   │   ├─── advice.py
│   │   ├─── events.py
│   │   ├─── user_access.py
│   │   └─── user_search.py
│   └─── convert_csv.py
├─── documents
│   ├─── Инструкция к @StudyBoost.pdf   
│   └─── Пользовательское-соглашение.pdf
├─── handlers
│   ├─── commands_handlers
│   │   └─── commands_handlers.py
│   ├─── platform_handlers
│   │   ├─── adviсe_handlers
│   │   │   ├─── add_adviсe.py
│   │   │   ├─── grade_handler.py
│   │   │   └─── view_advice.py
│   │   ├─── events_handlers
│   │   │   ├─── add_events.py
│   │   │   └─── view_events.py
│   │   ├─── material_handlers
│   │   │   ├─── add_material.py
│   │   │   ├─── grade_handlers.py
│   │   │   ├─── search_material_handlers.py
│   │   │   └─── search_materials.py
│   │   ├─── platform_handlers.py
│   │   └─── setting_handlers.py
│   └─── start_hadlers
│       ├─── access_callback.py
│       ├─── deny_access_callback.py
│       ├─── general_handlers.py
│       ├─── hello.py
│       ├─── register_handlers.py
│       └─── sign_in.py
├─── keyboards
│   ├─── admin_keyb.py
│   ├─── advice_keyb.py
│   ├─── cancellation_states.py
│   ├─── events_keyb.py
│   ├─── material_keyb.py
│   ├─── platform_keyb.py
│   └─── registration_keyb.py
├─── states
│   ├─── adviсe_state.py
│   ├─── events_state.py
│   ├─── help_suggestion_state.py
│   ├─── material_state.py
│   ├─── payment_state.py
│   └─── registration_state.py
├─── README.md
├─── bot.py
├─── config.py
├─── download.txt
├─── run.py
```

---

## 🚀 Запуск проекта  

1. Склонируйте репозиторий:  
   ```bash
   git clone 
   cd study-boost
   ```
2. Активируйте виртуальное окружение:  
   ```bash
   venv\Scripts\activate
   ```
3. Запустите бота:  
   ```bash
   python run.py
   ```

---

## 📄 Документация  

- **[Инструкция к боту](documents/Инструкция%20к%20@StudyBoost.pdf)**  
- **[Пользовательское соглашение](documents/Пользовательское-соглашение.pdf)**  