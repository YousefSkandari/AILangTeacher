import openai
import requests
import json
import re

# Step 1: Set up OpenAI API credentials
OPENAI_API_KEY = "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"
openai.api_key = OPENAI_API_KEY

def generate_lesson(prompt, language):
    response = openai.Completion.create(
        engine="text-davinci-003",
        prompt=prompt,
        max_tokens=1000,
        n=1,
        stop=None,
        temperature=0.7,
    )

    lesson = response.choices[0].text.strip()
    return lesson

def assess_performance(prompt):
    response = openai.Completion.create(
        engine="text-davinci-003",
        prompt=prompt,
        max_tokens=1000,
        n=1,
        stop=None,
        temperature=0.7,
    )

    assessment = response.choices[0].text.strip()
    return assessment

def ask_questions(questions):
    user_answers = []

    for question in questions:
        if not question.strip():  # Skip empty lines
            continue

        question_parts = question.split('|')
        for part in question_parts:
            print(part)
        
        answer = input("Your answer: ")
        user_answers.append(answer)
        print()

    return user_answers

def conduct_lesson_steps(lesson_steps, language, skill):
    print(f"Conducting the {skill} lesson...")
    step_count = 1

    for step in lesson_steps:
        step_prompt = f"Generate content for the following {language} {skill} lesson step:\n\n{step}"
        step_content = generate_lesson(step_prompt, language)
        print(f"Step {step_count}:")
        print(step_content)
        input("Press Enter to move to the next step.")
        step_count += 1

    print("Now that you have completed the lesson, let's test your understanding.")
    test_prompt = f"Generate multiple-choice questions related to the {language} {skill} lesson steps. Each question should start on a new line, have a clear format for easy interaction with input functions, and separate the question and multiple-choice options with a '|' symbol."
    test_questions = generate_lesson(test_prompt, language)
    test_question_list = test_questions.split('\n')
    test_answers = ask_questions(test_question_list)

    performance_prompt = f"Assess the user's performance in the {language} {skill} test based on their answers: {test_answers}. Then, suggest a new, more difficult lesson."
    assessment = assess_performance(performance_prompt)
    print(assessment)

def conduct_step(step, language, skill):
    step_content = re.sub(r"^(Step \d+:)", "", step).strip()  # Remove the step title
    prompt = f"Conduct this step of a {skill} lesson for learning {language} online for an individual: {step_content}"
    
    response = openai.Completion.create(
        engine="text-davinci-003",
        prompt=prompt,
        max_tokens=1000,
        n=1,
        stop=None,
        temperature=0.7,
    )

    lesson_output = response.choices[0].text.strip()
    return lesson_output

def main():
    print("Welcome to Language Learning with OpenAI!")
    language = input("Please enter the language you want to learn: ")

    # Initial test to assess user's current understanding
    print("Before we begin, let's assess your current understanding of the language.")
    input("Press Enter to start the initial test.")
    initial_test_prompt = f"Create an initial test with multiple-choice questions to evaluate the student's current understanding of {language}. Each question should start on a new line, have a clear format for easy interaction with input functions, and separate the question and multiple-choice options with a '|' symbol the questions must test the user on their abilities in the chosen language rather than general knowledge questions."
    initial_test = generate_lesson(initial_test_prompt, language)
    print("Initial Test:")
    initial_test_questions = initial_test.split('\n')
    initial_test_answers = ask_questions(initial_test_questions)
    print("Please complete the initial test.")
    print("Your Assessment Results Are Ready.")

    initial_test_performance_prompt = f"Assess the user's performance in the initial {language} test and suggest a starting lesson."
    initial_assessment = assess_performance(initial_test_performance_prompt)
    print(initial_assessment)

    learning_skills = ['reading', 'speaking']
    lesson_count = 1

    for skill in learning_skills:
        print(f"Generating your {skill} lesson in {language}...")

        prompt = f"Conduct a step-by-step lesson for an individual learning to {skill} in {language} online, based on the user's performance in the initial test. The lesson should have examples and information to help the user learn at their skill lever, tailored for self-learning Do not give me an outline of a lesson, Make sure it is learning material they do no have access to outside learning resources so create your own."

        lesson = generate_lesson(prompt, language)
        print(f"Lesson {lesson_count} - {skill.capitalize()} Lesson:")
        print(lesson)

        # Extract the steps from the lesson
        steps_start = lesson.find("Steps:") + len("Steps:")
        steps_end = lesson.find("Conclusion:")
        lesson_steps = lesson[steps_start:steps_end].strip().split('\n')[1:]

        # Conduct the lesson steps
        conduct_lesson_steps(lesson_steps, language, skill)

        lesson_count += 1
        for step in lesson_steps:
            step_output = conduct_step(step, language, skill)
            print(step_output)

        # User completes the lesson and takes a test
        print("Please complete the lesson and take the test.")
        input("Press Enter when you are ready for the assessment.")

        performance_prompt = f"Assess the user's performance in the {language} {skill} test and suggest a new lesson."
        assessment = assess_performance(performance_prompt)
        print(assessment)

        lesson_count += 1

if __name__ == "__main__":
    main()
