import google.generativeai as palm
import telebot


TOKEN = 'YOUR_TELEGRAM_BOT_TOKEN'


palm.configure(api_key="YOUR_GENERATIVE_AI_API_KEY")


bot = telebot.TeleBot(TOKEN)


@bot.message_handler(commands=['start', 'help', 'hello'])
def send_welcome(message):
    name = message.from_user.first_name
    bot.reply_to(message, f"Hello {name}! Ask me about anything")


@bot.message_handler(func=lambda message: True)
def handle_search_product(message):
    name = message.from_user.first_name
    msg = message.text
    

    if msg == "":
        bot.reply_to(message, "Sorry, you mustn't write an empty message")
    
    try:
        bot.reply_to(message, f"Please wait a moment, {name}, before sending another message")
        
       
        defaults = {
            'model': 'models/chat-bison-001',
            'temperature': 0.25,
            'candidate_count': 1,
            'top_k': 40,
            'top_p': 0.95,
        }
        
        context = ""
        examples = [
            [
                " ",
            ]
        ]
        
        examples[0].append(str(msg))
        messages = []
        messages.append("NEXT REQUEST")
        
        response = palm.chat(
            **defaults,
            context=context,
            examples=examples,
            messages=messages
        )
        
        print(response.messages)
        print(response.last)
        bot.reply_to(message, response.last)
    
    except Exception as e:
        bot.reply_to(message, str(e))
        bot.reply_to(message, "Sorry, an error occurred while processing your request.")

# старт
if __name__ == "__main__":
    bot.polling()
