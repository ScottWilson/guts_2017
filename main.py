"""
This sample demonstrates a simple skill built with the Amazon Alexa Skills Kit.
The Intent Schema, Custom Slots, and Sample Utterances for this skill, as well
as testing instructions are located at http://amzn.to/1LzFrj6

For additional samples, visit the Alexa Skills Kit Getting Started guide at
http://amzn.to/1LGWsLG
"""

from __future__ import print_function
import random

# --------------- Helpers that build all of the responses ----------------------

def build_speechlet_response(title, output, reprompt_text, should_end_session):
    return {
        'outputSpeech': {
            'type': 'PlainText',
            'text': output
        },
        'card': {
            'type': 'Simple',
            'title': "SessionSpeechlet - " + title,
            'content': "SessionSpeechlet - " + output
        },
        'reprompt': {
            'outputSpeech': {
                'type': 'PlainText',
                'text': reprompt_text
            }
        },
        'shouldEndSession': should_end_session
    }


def build_response(session_attributes, speechlet_response):
    return {
        'version': '1.0',
        'sessionAttributes': session_attributes,
        'response': speechlet_response
    }


# --------------- Functions that control the skill's behavior ------------------

def get_welcome_response():
    """ If we wanted to initialize the session to have some attributes we could
    add those here
    """

    session_attributes = {}
    card_title = "Welcome"
    speech_output = "Welcome to our Alexa Skills kit. Please ask to start the maths quiz. " \
    # If the user either does not reply to the welcome message or says something
    # that is not understood, they will be prompted again with this text.
    reprompt_text = "Please ask me quiz you."
    should_end_session = False
    return build_response(session_attributes, build_speechlet_response(
        card_title, speech_output, reprompt_text, should_end_session))


def handle_session_end_request():
    card_title = "Session Ended"
    speech_output = "Thank you for trying our Alexa Skills Kit! "
    # Setting this to true ends the session and exits the skill.
    should_end_session = True
    return build_response({}, build_speechlet_response(
        card_title, speech_output, None, should_end_session))


def maths_query(intent, session):
    session_attributes = session['attributes']

    if "chosenDifficulty" not in session_attributes:
        session_attributes["chosenDifficulty"] = 'medium'

    
    #set difficulty boundaries
    if session_attributes["chosenDifficulty"] == 'medium':
        random_int1 = random.randint(1, 20)
        random_int2 = random.randint(1, 10)
        random_int3 = random.randint(0, 2)
        potential_operators = [" plus "," minus "," times "]

        chosenOperator = potential_operators[random_int3]
        if chosenOperator == " plus ":
            if random_int2 < 0:
                chosenOperator = " minus "
            answer = random_int1 + random_int2
        elif chosenOperator == " minus ":
            if random_int2 < 0:
                chosenOperator = " plus "
            answer = random_int1 - random_int2
        elif chosenOperator == " times ":
            answer = (random_int1*random_int2)

    elif session_attributes["chosenDifficulty"] == 'hard':
        random_int1 = random.randint(10, 30)
        random_int2 = random.randint(-30, 30)
        chosenOperator = " times "
        answer = random_int1 * random_int2

    else:
        random_int1 = random.randint(1, 10)
        random_int2 = random.randint(1, 10)
        potential_operators = [" plus ", " minus "]
        functionDecider = random.randint(0, 1)
        chosenOperator = potential_operators[functionDecider]
        if chosenOperator == " plus ":
            answer = random_int1 + random_int2
        elif chosenOperator == " minus ":
            answer = random_int1 - random_int2


    if random_int2 < 0 and chosenOperator != " times ":
        speech_output = "What is " + str(random_int1) + " " + chosenOperator + " " + str(-1 * random_int2) + "?"
    else:
        speech_output = "What is " + str(random_int1) + " " + chosenOperator + " " + str(random_int2) + "?"


    if answer < 0:
        session_attributes['answer'] = "Minus " + str(-1*answer)
    else:
        session_attributes['answer'] = str(answer)

    reprompt_text = "howdy"
    should_end_session = False

    # Setting reprompt_text to None signifies that we do not want to reprompt
    # the user. If the user does not respond or says something that is not
    # understood, the session will end.
    return build_response(session_attributes, build_speechlet_response(
        intent['name'], speech_output, reprompt_text, should_end_session))

def get_answer(intent, session):

    session_attributes = session['attributes']
    if "answer" in session_attributes:
        speech_output = "The answer is: " + session_attributes["answer"]
    else:
        speech_output = "You have not answered any questions yet. Please ask for a question."
    reprompt_text = "howdy"
    should_end_session = False
    return build_response(session_attributes, build_speechlet_response(
        intent['name'], speech_output, reprompt_text, should_end_session))

#Method for setting difficulty of all Qs
def set_difficulty(intent, session):
    session_attributes = session['attributes']
    should_end_session = False
    selected_difficulty = intent['slots']['Difficulty']['value']
    session_attributes['chosenDifficulty'] = selected_difficulty
    speech_output = "Your selected difficulty is " + selected_difficulty
    #todo: validate input
    """else:
        speech_output = "This is not a valid difficulty. Your difficulty is " + session_attributes['chosenDifficulty']"""

    reprompt_text = "howdy pardner"

    return build_response(session_attributes, build_speechlet_response(
            intent['name'], speech_output, reprompt_text, should_end_session))


# --------------- Events ------------------

def on_session_started(session_started_request, session):
    """ Called when the session starts """

    print("on_session_started requestId=" + session_started_request['requestId']
          + ", sessionId=" + session['sessionId'])


def on_launch(launch_request, session):
    """ Called when the user launches the skill without specifying what they
    want
    """

    print("on_launch requestId=" + launch_request['requestId'] +
          ", sessionId=" + session['sessionId'])
    # Dispatch to your skill's launch
    return get_welcome_response()


def on_intent(intent_request, session):
    """ Called when the user specifies an intent for this skill """

    print("on_intent requestId=" + intent_request['requestId'] +
          ", sessionId=" + session['sessionId'])

    intent = intent_request['intent']
    intent_name = intent_request['intent']['name']

    # Dispatch to your skill's intent handlers
    if intent_name == "MathsQuestionIntent":
        #start maths game
        return maths_query(intent, session)
    elif intent_name == "GetAnswerToPreviousQuestionIntent":
        return get_answer(intent, session)
    elif intent_name == "SetDifficultyIntent":
        return set_difficulty(intent, session)
    elif intent_name == "AMAZON.CancelIntent" or intent_name == "AMAZON.StopIntent":
        return handle_session_end_request()
    else:
        raise ValueError("Invalid intent")


def on_session_ended(session_ended_request, session):
    """ Called when the user ends the session.

    Is not called when the skill returns should_end_session=true
    """
    print("on_session_ended requestId=" + session_ended_request['requestId'] +
          ", sessionId=" + session['sessionId'])
    # add cleanup logic here


# --------------- Main handler ------------------

def lambda_handler(event, context):
    """ Route the incoming request based on type (LaunchRequest, IntentRequest,
    etc.) The JSON body of the request is provided in the event parameter.
    """
    print("event.session.application.applicationId=" +
          event['session']['application']['applicationId'])

    """
    Uncomment this if statement and populate with your skill's application ID to
    prevent someone else from configuring a skill that sends requests to this
    function.
    """

    if event['session']['new']:
        on_session_started({'requestId': event['request']['requestId']},
                           event['session'])

    if event['request']['type'] == "LaunchRequest":
        return on_launch(event['request'], event['session'])
    elif event['request']['type'] == "IntentRequest":
        return on_intent(event['request'], event['session'])
    elif event['request']['type'] == "SessionEndedRequest":
        return on_session_ended(event['request'], event['session'])
