import openai
import json
from flask import Flask, render_template, request
from dotenv import dotenv_values

config = dotenv_values('.env')
openai.api_key = config["OPENAI_API_KEY"]

app = Flask(__name__, 
            template_folder='templates',
            static_url_path='',
            static_folder='static',
            )

def get_colors_fake(msg):
  return [
        "#000000",
        "#3F4C6B",
        "#5C258D",
        "#FFFEFF",
        "#E9F5FF",
        "#BDEDFD",
        "#B4CFEC",
        "#D2D9E3",
        "#FFFFFF"
      ];


def get_colors(msg):
    prompt = f"""
    You are a color palette generating assistant that responds to text prompts for color palettes
    Your should generate color palettes that fit the theme, mood, or instructions in the prompt.
    The palettes should be between 2 and 8 colors.

    Q: Convert the following verbal description of a color palette into a list of colors: The Mediterranean Sea
    A: ["#006699", "#66CCCC", "#F0E68C", "#008000", "#F08080"]

    Q: Convert the following verbal description of a color palette into a list of colors: sage, nature, earth
    A: ["#EDF1D6", "#9DC08B", "#609966", "#40513B"]


    Desired Format: a JSON array of hexadecimal color codes

    Q: Convert the following verbal description of a color palette into a list of colors: {msg} 
    A:
    """

    response = openai.Completion.create(
        prompt=prompt,
        model="text-davinci-003",
        max_tokens=200,
    )

    colors = json.loads(response["choices"][0]["text"])
    return colors

@app.route("/palette", methods=["POST"])
def prompt_to_palette():
  param_query = request.form.get("query")
  
  colors = get_colors(param_query)
  # colors = get_colors_fake(param_query)
  
  return {"colors": colors}

def simple_openai_call():
  try:
    response = openai.Completion.create(
      model="text-davinci-003",
      prompt="Give me a knock knock word"
    )
    return response["choices"][0]["text"]
  except (
    openai.error.InvalidRequestError, 
    openai.error.RateLimitError
    ) as e:
    print(e)
    return str(e)   

@app.route("/")
def index():
  return render_template("index.html")

if __name__ == "__main__":
  app.run(debug=True)