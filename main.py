#!/usr/bin/python

#          _          _            _            _             _          _         _            _
#         /\ \       /\ \         /\ \         /\ \          /\ \       /\ \      / /\         /\ \
#         \ \ \     /  \ \       /  \ \       /  \ \         \_\ \      \ \ \    / /  \       /  \ \
#         /\ \_\   / /\ \ \     / /\ \ \     / /\ \ \        /\__ \     /\ \_\  / / /\ \__   / /\ \ \
#        / /\/_/  / / /\ \_\   / / /\ \_\   / / /\ \_\      / /_ \ \   / /\/_/ / / /\ \___\ / / /\ \_\
#       / / /    / /_/_ \/_/  / /_/_ \/_/  / /_/_ \/_/     / / /\ \ \ / / /    \ \ \ \/___// / /_/ / /
#      / / /    / /____/\    / /____/\    / /____/\       / / /  \/_// / /      \ \ \     / / /__\/ /
#     / / /    / /\____\/   / /\____\/   / /\____\/      / / /      / / /   _    \ \ \   / / /_____/
# ___/ / /__  / / /______  / / /______  / / /______     / / /   ___/ / /__ /_/\__/ / /  / / /
#/\__\/_/___\/ / /_______\/ / /_______\/ / /_______\   /_/ /   /\__\/_/___\\ \/___/ /  / / /
#\/_________/\/__________/\/__________/\/__________/   \_\/    \/_________/ \_____\/   \/_/

import wolframalpha
from imdbpie import Imdb

from flask import Flask, request, redirect, render_template

def listify(texts):
    '''A method parsing the text from the wolfram alpha pod for the specific question.

    Args:
      texts:
        The text response from the wolfram alpha pod

    Returns:
      A list with the movie titles
    '''

    items = texts.split('\n') #When you see a new line, cut it there and list it
    del items[0]        #delete the first (header) row

    #Cut every row on the '|' and keep only the second item of the row
    items = [item.split('|')[1].strip() for item in items]
    return items    #Return the list

def imdbit(title):
    '''A method using imdb API to search by movie titles.

    Args:
      title:
        The title of the movie

    Returns:
      The imdb id of the movie (www.imdb.com/title/theiddddd/)
    '''

    imdb = Imdb()   #Start imdb

    movie = imdb.search_for_title(title) #do the search
    m = dict(movie[0])  #save the most relevant movie in a dictionary
    return m.get('imdb_id') #return the id


def wolframquery(year):
    '''A method using Wolfram Alpha API to get the best selling movies
       for a specified year.

    Args:
      year:
        The year for which we want to find the best selling movies

    Returns:
      A list containing the best selling movie titles or nothing
    '''

    app_id = 'U4PYLU-P42925A34P'    # API KEY (needed for wolfram)
    client = wolframalpha.Client(app_id)    #Creating the cliend
    query = 'Best selling movies of ' + year    #Forming the question
    print(query)    #let's see what we are asking
    res = client.query(query)   #ask

    if len(res.pods) > 0:       #Do we have an answer?
        texts = ''     #If we do, Initialise texts
        im_res = {}     #and results dictionary
        pod = res.pods[1]   #get the most relevant
        if pod.text:        #Do we have text?
            movies = listify(pod.text) #if yes create a list with the results
            for movie in movies:        #for every movie
                im_res[movie] = imdbit(movie)     #get the id and save it
            return im_res  #return it
        else:           #if we do not have text, we don't have an answer
            texts = 'I have no answer for that.'
            texts = texts.encode('ascii', 'ignore')
            print(texts)
    else:       #We don't have an answer
        print('Sorry, I am not sure.')


app = Flask(__name__)


@app.route('/')
def index():
    '''Shows a page with instructions of how to use this.
    '''

    return render_template('index.html')


@app.route('/', methods=['POST'])
def year_form_post():
    '''The form to submit the year.
    '''

    text = request.form['text']
    return redirect('/year/' + text, code=302)


@app.route('/year/<year>')
def showforyear(year):
    '''Shows a list of the best selling movies for the year in question.

    Args:
      year:
        The year for which we want the best selling movies.
    '''

    results = wolframquery(year)
    return render_template('base.html', movies=results, year=year)


if __name__ == '__main__':
    app.run(debug=True)
