from django.test import TestCase
from django.contrib.auth.models import User
from classroom.models import SchoolYear,Classroom,Project,ProjectTopic

# test for the creation of a new school year
class CreateNewSchoolYearTest(TestCase):
    def setUp(self):
        # creating a new school year
        SchoolYear.objects.create(year='2021-2022')
    
    def test(self):
        # fetching the newly created school year
        school_year = SchoolYear.objects.get(year='2021-2022')
        # testing the title of the newly created school year
        self.assertEqual(school_year.__str__(),'2021-2022')

# test for the creation of new classrooms
class CreateNewClassroomTest(TestCase):
    def setUp(self):
        # creating a new school year and 3 new classrooms
        school_year = SchoolYear.objects.create(year='2021-2022')
        Classroom.objects.create(title='Class 1',school_year=school_year,join_code='abc123')
        Classroom.objects.create(title='Class 2',school_year=school_year,join_code='abc123')
        Classroom.objects.create(title='Class 3',school_year=school_year,join_code='abc123')
        
    def test(self):
        # fetching the newly created classrooms and school year
        classroom1 = Classroom.objects.get(title='Class 1')
        classroom2 = Classroom.objects.get(title='Class 2')
        classroom3 = Classroom.objects.get(title='Class 3')
        school_year = SchoolYear.objects.get(year='2021-2022')
        # creating a list of all classes in the newly created school year
        classes = school_year.classrooms.all()
        # testing the length of the list 'classes'
        self.assertEqual(len(classes),3)
        # testing the title and school year of each newly created classroom object
        self.assertEqual(classroom1.__str__(),'Class 1 - 2021-2022')
        self.assertEqual(classroom2.__str__(),'Class 2 - 2021-2022')
        self.assertEqual(classroom3.__str__(),'Class 3 - 2021-2022')

# test for the creation of new projects
class CreateNewProjectTest(TestCase):
    def setUp(self):
        # creating a new user and two new projects associated with that user
        user1 = User.objects.create_user(username='NewUser1',email='newuser@gmail.com')
        school_year = SchoolYear.objects.create(year='2021-2022')
        classroom = Classroom.objects.create(title='Class 1',school_year=school_year,join_code='abc123')
        topic = ProjectTopic.objects.create(title = 'Topic 1',classroom=classroom)
        Project.objects.create(user=user1,project_topic=topic,title='Project 1',description='This is my first project!')
        Project.objects.create(user=user1,project_topic=topic,title='Project 2',description='This is my first project!')
    
    def test(self):
        # fetching the newly creatd user and their projects
        user1 = User.objects.get(username='NewUser1')
        project1 = Project.objects.get(user=user1,title='Project 1')
        project2 = Project.objects.get(user=user1,title='Project 2')
        # testing the titles of each newly created project
        self.assertEqual(project1.title,'Project 1')
        self.assertEqual(project2.title,'Project 2')
        # testing that both projects were created by the same user
        self.assertEqual(project1.user,user1)
        self.assertEqual(project2.user,user1)
        # creating a list of all projects created by user1
        projects = user1.projects.all()
        # verifying the length of the list 'projects'
        self.assertEqual(len(projects),2)