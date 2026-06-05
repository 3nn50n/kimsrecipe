from flask import Flask, render_template, request
import os
from dotenv import load_dotenv
import google.generativeai as genai

app = Flask(__name__)

load_dotenv()
api_key = os.getenv('GEMINI_API_KEY')
genai.configure(api_key=api_key)
model = genai.GenerativeModel('gemini-3.1-flash-lite')

cuisines=[
    "",
    "Italian",
    "Mexican",
    "Chinese",
    "Indian",
    "Japanese",
    "Thai",
    "French",
    "Mediterranean",
    "American",
    "Greek",
]

dietary_restrictions=[
    "Gluten-Free",
    "Dairy-Free",
    "Vegan",
    "Pescatarian",
    "Nut-Free",
    "Kosher",
    "Halal",
    "Low-Carb",
    "Organic",
    "Locally Sourced",
]

languages = {
    'English': 'en',
    'Spanish': 'es',
    'French': 'fr',
    'German': 'de',
    'Russian': 'ru',
    'Chinese (Simplified)': 'zh-CN',
    'Chinese (Traditional)': 'zh-TW',
    'Japanese':'ja',
    'Korean': 'ko',
    'Italian': 'it',
    'Portuguese': 'pt',
    'Arabic': 'ar',
    'Dutch':'nl',
    'Swedish': 'sv',
    'Turkish': 'tr',
    'Greek': 'el',
    'Hebrew': 'he',
    'Hindi': 'hi',
    'Indonesian': 'id',
    'Thai': 'th',
    'Filipino': 'tl',
    'Vietnamese': 'vi'
# ... potentially more based on actual Whisper support
}

@app.route('/')
def index():
    return render_template('index.html', cuisines=cuisines, dietary_restrictions= dietary_restrictions, languages=languages)

@app.route('/generate_recipe', methods=['POST'])
def generate_recipe():
    ingredients = request.form.getlist('ingredient')
    selected_cuisine = request.form.get('cuisine')
    selected_restrictions = request.form.getlist('restrictions')
    selected_language = request.form.get('language')


    print('selected_ingredient: '+ str(ingredients))
    print('selected_cuisine: ' + selected_cuisine)
    print('selected_restrictions: '+ str(selected_restrictions))
    print('selected_language: '+ selected_language)

    
    # Here you would integrate with the Gemini API to generate a recipe based on the ingredients
    if len(ingredients) != 3:
        return "Kindly provide exactly 3 ingredients."
    
    prompt = f"Do NOT use markdown code blocks.\
                Do NOT wrap the response in ```html.\
                Craft a recipe in HTML in {selected_language}\
                {', '.join(ingredients)}. \
                Ensure the recipe ingredients appear at the top,\
                followed by the step-by-step instructions."
    
    if selected_cuisine:
        prompt+=f"The cuisine should be {selected_cuisine}."


    if selected_restrictions and len(
        selected_restrictions)>0:
        prompt += f"The recipe should have the following restrictions {','.join(selected_restrictions)}."

    try:
        response = model.generate_content(prompt)
        recipe = response.text
    except Exception as e:
        return f"Error generating recipe: {str(e)}"
    return render_template('recipe.html', recipe=recipe)


if __name__ == '__main__':
    app.run(debug=True)