from telegram import Update
from telegram.ext import Updater, CommandHandler, CallbackContext

# Хранилище задач в памяти
tasks = []

# Команда для добавления новой задачи
def add_task(update: Update, context: CallbackContext) -> None:
    task_description = ' '.join(context.args)
    if task_description:
        tasks.append({'description': task_description, 'done': False})
        update.message.reply_text(f"Задача добавлена: {task_description}")
    else:
        update.message.reply_text("Пожалуйста, укажите описание задачи.")

# Команда для просмотра списка задач
def list_tasks(update: Update, context: CallbackContext) -> None:
    if not tasks:
        update.message.reply_text("Задачи отсутствуют.")
    else:
        task_list = [f"{idx + 1}. {'[x]' if task['done'] else '[ ]'} {task['description']}" for idx, task in enumerate(tasks)]
        update.message.reply_text("\n".join(task_list))

# Команда для отметки задачи как выполненной
def mark_done(update: Update, context: CallbackContext) -> None:
    try:
        task_number = int(context.args[0]) - 1
        if 0 <= task_number < len(tasks):
            tasks[task_number]['done'] = True
            update.message.reply_text(f"Задача {task_number + 1} отмечена как выполненная.")
        else:
            update.message.reply_text("Неверный номер задачи.")
    except (IndexError, ValueError):
        update.message.reply_text("Пожалуйста, укажите корректный номер задачи.")

def main():
    # Замените 'YOUR_BOT_TOKEN_HERE' на ваш реальный токен бота
    updater = Updater('7448196994:AAHlbICu1T5O8kD7Yn0-5quKPnfnKY5BU5s', use_context=True)
    
    dp = updater.dispatcher

    dp.add_handler(CommandHandler("add", add_task))
    dp.add_handler(CommandHandler("list", list_tasks))
    dp.add_handler(CommandHandler("done", mark_done))

    updater.start_polling()
    updater.idle()

if name == 'main':
    main()
