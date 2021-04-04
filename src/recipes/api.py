from flask import Flask, render_template, request

import requests
app = Flask(__name__)

url = "https://spoonacular-recipe-food-nutrition-v1.p.rapidapi.com/"

headers = {
  'x-rapidapi-host': "spoonacular-recipe-food-nutrition-v1.p.rapidapi.com",
  'x-rapidapi-key': "f301e3ac05msh916feb095e3e809p1ee0f9jsnbda8c8a6fb2e",
  }

find = "recipes/findByIngredients"
randomFind = "recipes/random"

@app.route('/')
def search_page():
  return render_template('recipe_search.html')

if __name__ == '__main__':
  app.run()

@app.route('/recipes')
def get_recipes():
  if (str(request.args['ingridients']).strip() != ""):
      # List recipes if ingredients are found
      querystring = {"number":"9","ranking":"1","ignorePantry":"false","ingredients":request.args['ingridients']}
      response = requests.request("GET", url + find, headers=headers, params=querystring).json()
      return render_template('recipes_results.html', recipes=response)
  else:
      # Random recipes
      querystring = {"number":"9"}
      response = requests.request("GET", url + randomFind, headers=headers, params=querystring).json()
      print(response)
      return render_template('recipes_results.html', recipes=response['recipes'])
      