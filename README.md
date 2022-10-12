# AMS CS App
#### App for Computer Science classes 2022-2023 and beyond
- Students can post projects, videos, photos
- Forums allow students to ask questions and mark each other's solutions as 'helpful'

#### Completed:
- Deployed on Heroku!

#### Next steps:
- Need to delete all unused profile pictures from AWS S3 buckets - consider separating profile and
  creating a 'profile pics' model - this way you can associate pics with users, and delete all
  unused photos from db and AWS
- Add 'description' to forum topic model. then be able to display a short description of the prompt on the
  forum-questions-list.html template 
- Update permissions for superusers - should be able to post and ask questions without
  joining a class
- Removed student access if not currently enrolled in class - Do not remove projects!