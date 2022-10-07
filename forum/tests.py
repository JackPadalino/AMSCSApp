""" 
from django.test import TestCase
from django.contrib.auth.models import User
from classroom.models import SchoolYear,Classroom
from .models import (
    Forum,
    ForumTopic,
    Question,
    Answer,
    AnswerNotification
    )

from users.models import (
    Profile
    )

# test for the creation of a forum
class CreateNewForumTest(TestCase):
    def setUp(self):
        # creating a new school year and two new classes
        school_year = SchoolYear.objects.create(year=2022)
        classroom1 = Classroom.objects.create(title='Class 1',school_year=school_year,join_code='abc123')
        # creating new forum objects
        #Forum.objects.create(title='Forum 1',classroom=classroom1)
        #Forum.objects.create(title='Forum 2',classroom=classroom2)
    
    def test(self):
        # fetching the newly created classes and their related forums
        classroom1 = Classroom.objects.get(title='Class 1')
        forum1 = Forum.objects.get(title='Projects')
        forum2 = Forum.objects.get(title='Class Discussions')
        # verifying that the names of the forums correspond to the names of their related classes
        self.assertEqual(forum1.classroom.title,'Class 1')
        self.assertEqual(forum2.classroom.title,'Class 1')

# test for the creating of a topic
class CreateNewTopicTest(TestCase):
    def setUp(self):
        # creating a new school year, classroom, forum, and 3 forum topics
        school_year = SchoolYear.objects.create(year=2022)
        classroom = Classroom.objects.create(title='Class 1',school_year=school_year,join_code='abc123')
        forum = Forum.objects.create(title='Forum 1',classroom=classroom)
        ForumTopic.objects.create(title='Topic 1',forum=forum)
        ForumTopic.objects.create(title='Topic 2',forum=forum)
        ForumTopic.objects.create(title='Topic 3',forum=forum)
    
    def test(self):
        # fetching the 3 new topics, the newly created classroom, and the forum related to the classroom
        forum_topic1 = ForumTopic.objects.get(title='Topic 1')
        forum_topic2 = ForumTopic.objects.get(title='Topic 2')
        forum_topic3 = ForumTopic.objects.get(title='Topic 3')
        classroom = Classroom.objects.get(title='Class 1')   
        forum = Forum.objects.get(title='Forum 1')
        # creating a list of all topics in the new forum
        forum_topics = forum.forum_topics.all()
        # testing the length of the list 'topics'
        self.assertEqual(len(forum_topics),3)
        # testing that each topic has the correct title
        self.assertEqual(forum_topic1.title,'Topic 1')
        self.assertEqual(forum_topic2.title,'Topic 2')
        self.assertEqual(forum_topic3.title,'Topic 3')

# testing for the creation of several questions by a user
class CreateNewUserQuestionTest(TestCase):
    def setUp(self):
        # creating a new user, school year, classroom, forum, topic, 3 new questions
        user = User.objects.create_user(username='NewUser',email='newuser@gmail.com',password='newest_user!',first_name='Snerd',last_name='Snerdyson')
        school_year = SchoolYear.objects.create(year=2022)
        classroom = Classroom.objects.create(title='Class 1',school_year=school_year,join_code='abc123')
        forum = Forum.objects.create(title='Forum 1',classroom=classroom)
        forum_topic = ForumTopic.objects.create(title='New Topic',forum=forum)
        Question.objects.create(author=user,forum=forum,forum_topic=forum_topic,title='Question 1',content='This is my first question!',project_link='')
        Question.objects.create(author=user,forum=forum,forum_topic=forum_topic,title='Question 2',content='This is my second question!',project_link='')
        Question.objects.create(author=user,forum=forum,forum_topic=forum_topic,title='Question 3',content='This is my third question!',project_link='')
    
    def test(self):
        # fetching the newly created user and the 3 new questions
        user = User.objects.get(username='NewUser')
        question1 = Question.objects.get(title='Question 1')
        question2 = Question.objects.get(title='Question 2')
        question3 = Question.objects.get(title='Question 3')
        # creating a list of all questions by the new user
        questions = user.questions.all()
        # testing the length of the list 'questions'
        self.assertEqual(len(questions),3)
        # testing that the new user is the author of each new question
        for question in questions:
            self.assertEqual(question.author,user)
        # testing the title and author of each question
        self.assertEqual(f'{question1.title} - {question1.author.first_name} {question1.author.last_name}','Question 1 - Snerd Snerdyson')
        self.assertEqual(f'{question2.title} - {question2.author.first_name} {question2.author.last_name}','Question 2 - Snerd Snerdyson')
        self.assertEqual(f'{question3.title} - {question2.author.first_name} {question3.author.last_name}','Question 3 - Snerd Snerdyson')

# testing the creation of new answers
class CreateNewAnswerTest(TestCase):
    def setUp(self):
        # creating three new users, a new school year, a new classroom, a new forum, 3 questions, and six new answers
        # 2 answers per newly created question. 2 answers per newly created user
        user1 = User.objects.create_user(username='NewUser1',email='newuser@gmail.com',password='newest_user!',first_name='Snerd',last_name='Snerdyson')
        user2 = User.objects.create_user(username='NewUser2',email='newuser@gmail.com',password='newest_user!',first_name='Snerd',last_name='Snerdyson')
        user3 = User.objects.create_user(username='NewUser3',email='newuser@gmail.com',password='newest_user!',first_name='Snerd',last_name='Snerdyson')
        school_year = SchoolYear.objects.create(year=2022)
        classroom = Classroom.objects.create(title='Class 1',school_year=school_year,join_code='abc123')
        forum = Forum.objects.create(title='Forum 1',classroom=classroom)
        forum_topic = ForumTopic.objects.create(title='New Topic',forum=forum)
        question1 = Question.objects.create(author=user1,forum=forum,forum_topic=forum_topic,title='Question 1',content='This is my first question!',project_link='')
        question2 = Question.objects.create(author=user2,forum=forum,forum_topic=forum_topic,title='Question 2',content='This is my first question!',project_link='')
        question3 = Question.objects.create(author=user3,forum=forum,forum_topic=forum_topic,title='Question 3',content='This is my first question!',project_link='')
        Answer.objects.create(author=user2,forum=forum,forum_topic=forum_topic,question=question1,content='Here is my answer!')
        Answer.objects.create(author=user3,forum=forum,forum_topic=forum_topic,question=question1,content='Here is my answer!')
        Answer.objects.create(author=user1,forum=forum,forum_topic=forum_topic,question=question2,content='Here is my answer!')
        Answer.objects.create(author=user3,forum=forum,forum_topic=forum_topic,question=question2,content='Here is my answer!')
        Answer.objects.create(author=user1,forum=forum,forum_topic=forum_topic,question=question3,content='Here is my answer!')
        Answer.objects.create(author=user2,forum=forum,forum_topic=forum_topic,question=question3,content='Here is my answer!')
    
    def test(self):
        # fetching the newly creatd user objects, the new classroom, the forum, the 3 questions, and the 6 new answers
        user1 = User.objects.get(username='NewUser1')
        user2 = User.objects.get(username='NewUser2')
        user3 = User.objects.get(username='NewUser3')
        classroom = Classroom.objects.get(title='Class 1')
        forum = Forum.objects.get(title='Forum 1')
        question1 = Question.objects.get(title='Question 1')
        question2 = Question.objects.get(title='Question 2')
        question3 = Question.objects.get(title='Question 3')
        answer1 = Answer.objects.get(author=user2,question=question1)
        answer2 = Answer.objects.get(author=user3,question=question1)
        answer3 = Answer.objects.get(author=user1,question=question2)
        answer4 = Answer.objects.get(author=user3,question=question2)
        answer5 = Answer.objects.get(author=user1,question=question3)
        answer6 = Answer.objects.get(author=user2,question=question3)
        # creating a list of all answers in the new forum
        answers = forum.answers.all()
        # testing the length of the list 'answers'
        self.assertEqual(len(answers),6)
        # creating a list of answers for each question
        question1answers = question1.answers.all()
        question2answers = question2.answers.all()
        question3answers = question3.answers.all()
        # testing the length of each question's answers list
        self.assertEqual(len(question1answers),2)
        self.assertEqual(len(question2answers),2)
        self.assertEqual(len(question3answers),2)
        # testing the author of each answer
        self.assertEqual(answer1.author,user2)
        self.assertEqual(answer2.author,user3)
        self.assertEqual(answer3.author,user1)
        self.assertEqual(answer4.author,user3)
        self.assertEqual(answer5.author,user1)
        self.assertEqual(answer6.author,user2)
        # creating a list of answers for each user
        user1answers = user1.answers.all()
        user2answers = user2.answers.all()
        user3answers = user3.answers.all()
        # testing the length of each user's list of answers
        self.assertEqual(len(user1answers),2)
        self.assertEqual(len(user2answers),2)
        self.assertEqual(len(user3answers),2)
        # testing that each answer is associated with the correct question
        self.assertEqual(answer1.question,question1)
        self.assertEqual(answer2.question,question1)
        self.assertEqual(answer3.question,question2)
        self.assertEqual(answer4.question,question2)
        self.assertEqual(answer5.question,question3)
        self.assertEqual(answer6.question,question3)

# test for the creation of answer notifications when a user's question is answered
class CreateNewAnswerNotificationTest(TestCase):
    def setUp(self):
        # creating three new users, a new school year, a new classroom, a new forum, 2 questions, and two new answers
        # 1 answers per newly created question
        user1 = User.objects.create_user(username='NewUser1',email='newuser@gmail.com',password='newest_user!',first_name='Snerd',last_name='Snerdyson')
        user2 = User.objects.create_user(username='NewUser2',email='newuser@gmail.com',password='newest_user!',first_name='Snerd',last_name='Snerdyson')
        school_year = SchoolYear.objects.create(year=2022)
        classroom = Classroom.objects.create(title='Class 1',school_year=school_year,join_code='abc123')
        forum = Forum.objects.create(title='Forum 1',classroom=classroom)
        forum_topic = ForumTopic.objects.create(title='New Topic',forum=forum)
        question1 = Question.objects.create(author=user1,forum=forum,forum_topic=forum_topic,title='Question 1',content='This is my first question!',project_link='')
        question2 = Question.objects.create(author=user1,forum=forum,forum_topic=forum_topic,title='Question 2',content='This is my first question!',project_link='')
        answer1=Answer.objects.create(author=user2,forum=forum,forum_topic=forum_topic,question=question1,content='Here is my answer!')
        answer2=Answer.objects.create(author=user2,forum=forum,forum_topic=forum_topic,question=question2,content='Here is my answer!')
        #AnswerNotification.objects.create(answer=answer1,notified_user=question1.author)
        #AnswerNotification.objects.create(answer=answer2,notified_user=question2.author)
    
    def test(self):
        # fetching the newly created user 1, their questions, and the answer notifications created when
        # their questions were answerered by user 2
        user1 = User.objects.get(username='NewUser1')
        user2 = User.objects.get(username='NewUser2')
        question1 = Question.objects.get(title='Question 1')
        question2 = Question.objects.get(title='Question 2')
        answer1 = Answer.objects.get(question=question1)
        answer2 = Answer.objects.get(question=question2)
        notification1 = AnswerNotification.objects.get(answer=answer1)
        notification2 = AnswerNotification.objects.get(answer=answer2)
        # testing that each answer notification has the correct corresponding answer
        self.assertEqual(notification1.answer,answer1)
        self.assertEqual(notification2.answer,answer2)
        # testing that each notification points to the correct user who asked the question
        self.assertEqual(notification1.notified_user,user1)
        self.assertEqual(notification2.notified_user,user1)
        # testing that each notification points to the correct user who answered the question
        self.assertEqual(notification1.answer.author,user2)
        self.assertEqual(notification2.answer.author,user2)
        # creating a list of notifications for a user
        user1_notifications = user1.answer_notifications.all()
        # testing the length of user notifications
        self.assertEqual(len(user1_notifications),2)


 """