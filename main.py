#!/usr/bin/python

import wolframalpha

def wolframquery(year):
    # API KEY
    app_id = 'U4PYLU-P42925A34P'
    client = wolframalpha.Client(app_id)    #Creating the cliend
    query = 'Best selling movies of ' + year    #Forming the question
    print(query)    #let's see what we are asking
    res = client.query(query)   #ask

    if len(res.pods) > 0:       #Do we have an answer?
        texts = ''     #If we do, Initialise texts
        im_res = {}     #and results dictionary
        pod = res.pods[1]   #get the most relevant
        if pod.text:        #Do we have text?
            print(pod.text) #if yes print it
        else:           #if we do not have text, we don't have an answer
            texts = 'I have no answer for that.'
            texts = texts.encode('ascii', 'ignore')
            print(texts)
    else:       #We don't have an answer
        print('Sorry, I am not sure.')

wolframquery('2012')
