from django.db import models
from django.contrib.auth.models import User
from django.utils.timezone import now

#Questions
class QuestionData(models.Model):
	ANSWER_CHOICES=(
		("A", ("A")),
		("B", ("B")),
		("C", ("C")),
		("D", ("D")),
		)
	id_no=models.CharField(max_length=1000,primary_key=True)
	question=models.TextField()
	optionA=models.TextField()
	optionB=models.TextField()
	optionC=models.TextField()
	optionD=models.TextField()
	correct_choice=models.CharField(choices=ANSWER_CHOICES, max_length=10, null=False)


#Time Interval Of Quiz
class Time(models.Model):
	start_time = models.DateTimeField(max_length=100, blank=False, default=now)
	end_time = models.DateTimeField(max_length=100, blank=False, default=now)

	def __str__(self):
		return str(self.end_time)

		
#Scored Card + Solved
class SolvedQ(models.Model):
	id_no=models.ForeignKey(User, on_delete=models.CASCADE)
	q_id=models.ForeignKey(QuestionData, on_delete=models.CASCADE)
	check=models.BooleanField(default=False)
	