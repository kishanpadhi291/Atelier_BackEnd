from django.db import models
from user.models import User
# Create your models here.
class ChatMessage(models.Model):
    sender = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name="sender")
    receiver = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name="receiver")
    message = models.CharField(max_length=10000000000)
    date = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['date']
        verbose_name_plural = "Message"

    def __str__(self):
        return f"{self.sender} - {self.receiver}"

    # @property
    # def sender_profile(self):
    #     sender_profile = User.objects.get(user=self.sender)
    #     return sender_profile
    #
    # @property
    # def receiver_profile(self):
    #     receiver_profile = User.objects.get(user=self.receiver)
    #     return receiver_profile