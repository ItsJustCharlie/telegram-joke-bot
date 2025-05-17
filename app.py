import os  # operating system
import re  # regular expression
from dotenv import load_dotenv
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes
from langchain_groq import ChatGroq
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser

load_dotenv()

os.environ["LANGCHAIN_API_KEY"] = "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"
os.environ["LANGCHAIN_PROJECT"] = "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"
os.environ["LANGCHAIN_TRACING_V2"] = "true"
groq_api_key = "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"

def setup_llm_chain(topic="technology"):
   
    prompt = ChatPromptTemplate.from_messages([
        ("system", "You are a Joking AI. Give me only ONE funny joke on the given topic"),
        ("user", f"generate a joke on the topic: {topic}")
    ])
    
    llm = ChatGroq(
        model="Gemma2-9b-It",
        groq_api_key=groq_api_key
    )
    
    return prompt|llm|StrOutputParser()

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.message:
        await update.message.reply_text("Hi! Mention me with a topic like '@TellMeJokeBot python' to get a joke")

async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.message:
        await update.message.reply_text("Mention me with a topic like '@TellMeJokeBot python', to get some funny jokes")

async def generate_joke(update: Update, context: ContextTypes.DEFAULT_TYPE, topic: str):
    if update.message is None:
        return  # Just skip if no message

    await update.message.reply_text(f"Generating a joke about {topic}")
    joke = setup_llm_chain(topic).invoke({}).strip()
    await update.message.reply_text(joke)

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not update.message:
        return

    msg = update.message.text
    bot_username = context.bot.username

    msg = update.message.text
    bot_username = context.bot.username

    if msg is not None and f'@{bot_username}' in msg:
        match = re.search(f'@{bot_username}\\s+(.*)', msg)
        if match and match.group(1).strip():
            await generate_joke(update, context, match.group(1).strip())
        else:
            await update.message.reply_text("Please specify a topic after mentioning me")

            
def main():
    token = "7919607597:AAFzbLJxKt98ngISnJzlNSxKspRPnKRQAGU"
    app = Application.builder().token(token).build()
    app.add_handler(CommandHandler("start",start))
    app.add_handler(CommandHandler("help", help_command))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    app.run_polling(allowed_updates=Update.ALL_TYPES)
    
if __name__ == "__main__":
    main()