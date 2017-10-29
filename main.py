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
    speech_output = "Welcome to our Alexa Skills kit. Please ask to start a quiz (either maths or shapes). " \
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


def maths_query(session):
    session_attributes = session['attributes']

    # set difficulty boundaries
    if session_attributes["chosenDifficulty"] == 'medium':
        random_int1 = random.randint(1, 20)
        random_int2 = random.randint(1, 10)
        random_int3 = random.randint(0, 2)
        potential_operators = [" plus ", " minus ", " times "]

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
            answer = (random_int1 * random_int2)

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
        question_string = "What is " + str(random_int1) + " " + chosenOperator + " " + str(-1 * random_int2) + "?"
    else:
        question_string = "What is " + str(random_int1) + " " + chosenOperator + " " + str(random_int2) + "?"

    """if answer < 0:
        answer_string = "Minus " + str(-1 * answer)
    else:
        answer_string = str(answer)"""
    answer_string = str(answer)

    return question_string, answer_string


def get_answer(intent, session):
    session_attributes = session['attributes']

    if 'quizStarted' in session_attributes and not session_attributes['quizStarted']:
        speech_output = "Please start a quiz. You can do this by saying start a maths quiz or start a shapes quiz"
        should_end_session = False
        reprompt_text = "Please start a quiz. You can do this by saying start a maths quiz or start a shapes quiz"
        return build_response(session_attributes, build_speechlet_response(
            intent['name'], speech_output, reprompt_text, should_end_session))

    if "current_answer" in session_attributes:
        speech_output = "The answer is: " + session_attributes["current_answer"]
        reprompt_text = "The answer is: " + session_attributes["current_answer"]
    else:
        speech_output = "You have not answered any questions yet. Please ask for a question."
        reprompt_text = "You have not answered any questions yet. Please ask for a question."

    should_end_session = False
    return build_response(session_attributes, build_speechlet_response(
        intent['name'], speech_output, reprompt_text, should_end_session))

def letter_checker_query(session):
    possible_words = ['elephant', 'apple', 'animal', 'orange', 'penguin', 'carrot', 'moon', 'computer',
                      'chair', 'dog', 'bat', 'light', 'bottle', 'table', 'box']


    random_int = random.randint(0, 14)
    chosen_word = possible_words[random_int]

    question_text = 'Which letter does the word ' + chosen_word + ' start with?'
    answer_text = chosen_word[0]
    return question_text, answer_text



# Method for setting difficulty of all Qs
def set_difficulty(intent, session):
    session_attributes = session['attributes']
    should_end_session = False
    selected_difficulty = intent['slots']['Difficulty']['value']
    session_attributes['chosenDifficulty'] = selected_difficulty
    speech_output = "Your selected difficulty is " + selected_difficulty
    # todo: validate input
    """else:
        speech_output = "This is not a valid difficulty. Your difficulty is " + session_attributes['chosenDifficulty']"""

    reprompt_text = "howdy pardner"

    return build_response(session_attributes, build_speechlet_response(
        intent['name'], speech_output, reprompt_text, should_end_session))

    # used for building quizzes initially, next question is navigate to the next one



def next_question(intent, session):
    # get counter and other relevant info for the question

    session_attributes = session['attributes']
    if 'quizStarted' not in session_attributes or not session_attributes['quizStarted']:
        speech_output = "Please start a quiz. You can do this by saying start a maths quiz or start a shapes quiz"
        should_end_session = False
        reprompt_text = "Please start a quiz. You can do this by saying start a maths quiz or start a shapes quiz"
        return build_response(session_attributes, build_speechlet_response(
            intent['name'], speech_output, reprompt_text, should_end_session))

    main_counter = session_attributes['question_counter']
    #quit out at end of quiz
    if main_counter == session_attributes["number_of_questions"]:
        speech_output = "That's the end of the quiz! Thanks for playing!"
        reprompt_text = "That's the end of the quiz! Thanks for playing!"
        should_end_session = True
        session['quizStarted'] = False
        return build_response(session_attributes, build_speechlet_response(
        intent['name'], speech_output, reprompt_text, should_end_session))


    session_attributes['current_question'] = session_attributes['question_list'][main_counter]
    session_attributes['current_answer'] = session_attributes['answer_list'][main_counter]

    speech_output = session_attributes['current_question']
    reprompt_text = "The question is " + session_attributes['current_question']
    should_end_session = False

    session_attributes['question_counter'] += 1
    return build_response(session_attributes, build_speechlet_response(
        intent['name'], speech_output, reprompt_text, should_end_session))



def start_quiz(intent, session, type_of_quiz):
    # todo: get input validation for the commands that are valid at this point
    session['attributes'] = {}
    session['attributes']['quizStarted'] = True
    session['attributes']["number_of_questions"] = 10
    session['attributes']["chosenDifficulty"] = 'medium'
    question_list = [""] * session['attributes']["number_of_questions"]
    answer_list = [""] * session['attributes']["number_of_questions"]
    i = 0

    if type_of_quiz == "shapes":
        while i < session['attributes']["number_of_questions"]:
            question_list[i], answer_list[i] = shape_query(session)
            i = i + 1
        # add lists to session attributes and initialise a counter
        speech_output = "Welcome to the shapes Quiz! Please say 'next' to get onto your first question"
    elif type_of_quiz == "maths":
        speech_output = "Welcome to the maths Quiz! Please say 'next' to get onto your first question"
        while i < session['attributes']["number_of_questions"]:
            question_list[i], answer_list[i] = maths_query(session)
            i = i + 1
    elif type_of_quiz == "letters":
        speech_output = "Welcome to the letters Quiz! Please say 'next' to get onto your first question"
        while i < session['attributes']["number_of_questions"]:
            question_list[i], answer_list[i] = letter_checker_query(session)
            i = i + 1
    elif type_of_quiz == 'noises':
        speech_output = "Welcome to the noises Quiz! Please say 'next' to get onto your first question"
        while i < session['attributes']["number_of_questions"]:
            question_list[i], answer_list[i] = animal_noises_query(session)
            i = i + 1

    # add lists to session attributes and initialise a counter
    session['attributes']['question_list'], session['attributes']['answer_list'] = question_list, answer_list
    session['attributes']['question_counter'] = 0


    reprompt_text = "Please say 'next' to get onto your first question"
    should_end_session = False

    return build_response(session['attributes'], build_speechlet_response(
        intent['name'], speech_output, reprompt_text, should_end_session))

#questions for shape quiz
def shape_query(session):
    shapeList = ['a circle','a triangle','a square','a rectangle','a diamond','a pentagon','a hexagon','a heptagon',
                 'an octagon', 'a rhombus','a parallelogram','a kite','a eclipse','a five pointed star']
    shape_sides = ['one', 'three', 'four', 'four', 'four', 'five', 'six', 'seven', 'eight', 'four', 'four', 'four',
                   'one', 'ten']

    random_int = random.randint(0, 13)
    chosen_shape = shapeList[random_int]
    chosen_answer = shape_sides[random_int]

    question_text = "How many sides does " + chosen_shape + " have?"
    answer_text = chosen_answer
    return question_text, answer_text


def animal_noises_query(session):
    animal_list = ["cow", "sheep", 'chicken', 'dog', 'cat', 'rooster', 'duck', 'pig', 'horse', 'donkey']
    animal_noises = ['moo', 'baa', 'cluck', 'bark', 'cat', 'cock-a-doodle-doo', 'quack', 'oink', 'hee-haw']

    random_int = random.randint(0, 9)
    chosen_animal = animal_list[random_int]
    chosen_noise = animal_noises[random_int]

    answer_text = chosen_noise
    question_text = "What noise does a " + chosen_animal + " make?"
    return question_text, answer_text


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
    if intent_name == "GetAnswerToPreviousQuestionIntent":
        return get_answer(intent, session)
    elif intent_name == "MakeMathsQuizIntent":
        return start_quiz(intent, session, "maths")
    elif intent_name == "MoveOntoNextQuestion":
        return next_question(intent, session)
    elif intent_name == "MakeShapesQuizIntent":
        return start_quiz(intent, session, "shapes")
    elif intent_name == "MakeLettersQuizIntent":
        return start_quiz(intent, session, "letters")
    elif intent_name == "MakeNoisesQuizIntent":
        return start_quiz(intent, session, 'noises')
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
