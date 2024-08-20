from django.db import models


# Define choices for the request status
class RequestStatus(models.TextChoices):
    NOT_STARTED = "Not Started"
    IN_PROGRESS = "In Progress"
    COMPLETE = "Complete"


# Define the User model
class User(models.Model):
    telegram_id = models.BigIntegerField(unique=True, db_index=True)
    request_status = models.CharField(
        max_length=50,
        choices=RequestStatus.choices,
        default=RequestStatus.NOT_STARTED
    )

    def __str__(self):
        return f"User {self.telegram_id}"


# Define the Form model
class Form(models.Model):
    user = models.ForeignKey(User, related_name="forms", on_delete=models.CASCADE)
    full_name = models.CharField(max_length=255)
    email_address = models.EmailField()
    phone_number = models.CharField(max_length=15)

    def __str__(self):
        return f"Form {self.id} for user {self.user.telegram_id}"
