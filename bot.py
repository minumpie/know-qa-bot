import logging
import json
import random
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes
from config import BOT_TOKEN

# Настройка логов
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO,
    filename='logs/bot.log',
    encoding='utf-8'
)

# Загрузка вопросов с проверкой
def load_questions():
    try:
        with open('questions.json', 'r', encoding='utf-8') as f:
            data = json.load(f)

        valid_data = [q for q in data if "question" in q and "answer" in q]

        if not valid_data:
            raise ValueError("No valid questions found in questions.json")

        logging.info(f"Loaded {len(valid_data)} questions from questions.json")
        return valid_data

    except FileNotFoundError:
        logging.error("questions.json not found")
        return []
    except json.JSONDecodeError:
        logging.error("Invalid JSON format in questions.json")
        return []
    except Exception as e:
        logging.error(f"Unexpected error while loading questions: {e}")
        return []

QUESTIONS = load_questions()
used_questions = set()

# Команда /start
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "Привет! 🐇 Я KnowQA.\n"
        "Отправь /question, чтобы получить случайный вопрос по тестированию.\n"
        "Используй /help, чтобы узнать список команд."
    )
    logging.info(f"User {update.effective_chat.id} started the bot")

# Команда /help
async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "📜 Доступные команды:\n"
        "/start — приветствие\n"
        "/help — список команд\n"
        "/question — случайный вопрос по тестированию"
    )
    logging.info(f"User {update.effective_chat.id} requested /help")

# Команда /question
async def question(update: Update, context: ContextTypes.DEFAULT_TYPE):
    global used_questions

    if not QUESTIONS:
        await update.message.reply_text("❌ Ошибка: база вопросов пуста или повреждена.")
        logging.error("No questions available — /question aborted")
        return

    # Сброс, если все вопросы уже использованы
    if len(used_questions) == len(QUESTIONS):
        used_questions.clear()
        logging.info("All questions have been shown, restarting the cycle")

    # Получение случайного вопроса, который ещё не использовался
    available_indices = [i for i in range(len(QUESTIONS)) if i not in used_questions]
    index = random.choice(available_indices)
    used_questions.add(index)

    q = QUESTIONS[index]['question']
    a = QUESTIONS[index]['answer']

    try:
        text = f"❓ *Вопрос:*\n{q}\n\n✅ *Ответ:*\n{a}"
        await update.message.reply_markdown(text)
        logging.info(f"Sent question #{index + 1}")
    except Exception as e:
        logging.error(f"Failed to send question: {e}")

# Запуск бота
def main():
    app = ApplicationBuilder().token(BOT_TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("help", help_command))
    app.add_handler(CommandHandler("question", question))
    logging.info("Bot started")
    app.run_polling()

if __name__ == '__main__':
    main()
