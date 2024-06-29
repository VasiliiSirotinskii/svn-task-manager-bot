import os
from telegram import Update, ForceReply
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackContext

# Получение токена бота из переменной окружения
TOKEN = os.getenv("BOT_TOKEN")

updater = Updater(TOKEN, use_context=True)
dispatcher = updater.dispatcher

# Список задач
tasks = []

def start(update: Update, context: CallbackContext) -> None:
    update.message.reply_text('Hi! Use /add <task>, /list, /done <task_number> to manage your tasks.')

def add(update: Update, context: CallbackContext) -> None:
    task = ' '.join(context.args)
    tasks.append({'task': task, 'done': False})
    update.message.reply_text(f'Task added: {task}')

def list_tasks(update: Update, context: CallbackContext) -> None:
    if not tasks:
        update.message.reply_text('No tasks yet.')
        return
    message = ''
    for i, task in enumerate(tasks):
        status = '✓' if task['done'] else '✗'
        message += f"{i + 1}. {task['task']} [{status}]\n"
    update.message.reply_text(message)

def done(update: Update, context: CallbackContext) -> None:
    try:
        task_number = int(context.args[0]) - 1
        if 0 <= task_number < len(tasks):
            tasks[task_number]['done'] = True
            update.message.reply_text(f'Task {task_number + 1} marked as done.')
        else:
            update.message.reply_text('Invalid task number.')
    except (ValueError, IndexError):
        update.message.reply_text('Usage: /done <task_number>')

# Регистрируем команды
dispatcher.add_handler(CommandHandler("start", start))
dispatcher.add_handler(CommandHandler("add", add))
dispatcher.add_handler(CommandHandler("list", list_tasks))
dispatcher.add_handler(CommandHandler("done", done))

# Запускаем бота
updater.start_polling()
updater.idle()
