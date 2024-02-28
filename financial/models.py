from django.db import models


class Payment(models.Model):
    # Define choices for the 'status' field
    class Status(models.TextChoices):
        PENDING = 'pending', 'Pending'
        COMPLETED = 'completed', 'Completed'
        FAILED = 'failed', 'Failed'

    # Fields for the Payment model
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    status = models.CharField(
        max_length=20, choices=Status.choices, default=Status.PENDING)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    # Override the save method to check for valid 'status' values
    def save(self, *args, **kwargs):
        # Check if the 'status' value is valid
        if self.status not in [self.Status.PENDING, self.Status.COMPLETED]:
            raise ValueError("Invalid payment status")
        print(f"Saving payment with status: {self.status}")
        super().save(*args, **kwargs)

    # Define a human-readable string representation of the Payment instance
    def __str__(self):
        return f"Payment - Amount: {self.amount}, Status: {self.status}"
