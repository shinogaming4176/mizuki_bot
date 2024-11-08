import os
import telebot
import requests
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()

BOT_TOKEN = os.getenv("BOT_TOKEN")
OPEN_AI_KEY = os.getenv("OPEN_AI_KEY")

client = OpenAI(api_key=OPEN_AI_KEY)
bot = telebot.TeleBot(BOT_TOKEN)

# Handle the /jokes command - Sends a joke
@bot.message_handler(commands=["jokes"])
def send_jokes(message):
    bot.send_message(message.chat.id, "Here is a joke for you:")    

    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": "You are a stand-up comedian"},
            {"role": "user", "content": "tell me a joke about IT guys"},
        ],
    )
    bot.send_message(message.chat.id, response.choices[0].message.content, parse_mode="Markdown")

# Handle the /mizu5 command - Sends an image related to Mizu5
@bot.message_handler(commands=["mizu5pic"])
def send_photos(message):
    # Send only the image (no text message)
    image_url = "https://preview.redd.it/what-is-everyones-last-predictions-for-mizu5-before-the-v0-jz5twlmhq1ud1.jpeg?auto=webp&s=ad66ca321b88b6ead1ab3c945fe8f24707cc321f"
    
    # Send the image using the URL
    bot.send_photo(message.chat.id, image_url)

@bot.message_handler(commands=["homura"])
def send_gif(message):
    # GIF URL
    gif_url = "https://tenor.com/view/madoka-magica-homura-shooting-herself-gif-11935785"
    
    # Send the GIF using the URL
    bot.send_animation(message.chat.id, gif_url)

@bot.message_handler(commands=["mizu5gif"])
def send_gif(message):
    # GIF URL
    gif_url = "https://tenor.com/view/mizu5-mizuki-pjsk-project-sekai-mizuki-akiyama-gif-13622273774150727491"
    
    # Send the GIF using the URL
    bot.send_animation(message.chat.id, gif_url)





@bot.message_handler(commands=["start", "hello"])
def send_welcome(message):
    bot.send_message(message.chat.id, "☆*: .｡. o(≧▽≦)o .｡.:*☆")

@bot.message_handler(commands=["chelsea"])
def send_chelsea(message):
    bot.send_message(message.chat.id, "Chelsea is the best team in the world")

@bot.message_handler(commands=["wiki"])
def send_wiki(message):
    import bs4
    from langchain_openai import ChatOpenAI
    from langchain_community.document_loaders import WikipediaLoader
    from langchain_chroma import Chroma
    from langchain_core.output_parsers import StrOutputParser
    from langchain_core.runnables import RunnablePassthrough
    from langchain_openai import OpenAIEmbeddings
    from langchain_text_splitters import RecursiveCharacterTextSplitter

    bot.send_message(message.chat.id, "Fetching wiki information...")
    try:
        wiki = message.text.split(" ", 1)[1]
    except IndexError:
        bot.send_message(message.chat.id, "Please provide a topic after the command.")
        return

    llm = ChatOpenAI(model="gpt-4o-mini")
    docs = WikipediaLoader(query=wiki, load_max_docs=2).load()
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
    splits = text_splitter.split_documents(docs)
    vectorstore = Chroma.from_documents(documents=splits, embedding=OpenAIEmbeddings())

    retriever = vectorstore.as_retriever()
    prompt = hub.pull("rlm/rag-prompt")

    rag_chain = (
        {"context": retriever | format_docs, "question": RunnablePassthrough()}
        | prompt
        | llm
        | StrOutputParser()
    )

    results = rag_chain.invoke(wiki)
    bot.send_message(message.chat.id, results, parse_mode="Markdown")

@bot.message_handler(func=lambda msg: True)
def echo_all(message):
    bot.reply_to(message, message.text)

bot.infinity_polling()
