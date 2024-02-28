from django.test import TestCase
from .models import Payment
import time
import unittest


class PaymentModelTest(TestCase):
    def test_payment_creation(self):
        payment = Payment.objects.create(
            amount=50.0, status=Payment.Status.PENDING)
        self.assertEqual(payment.amount, 50.0)
        self.assertEqual(payment.status, Payment.Status.PENDING)
        self.assertIsNotNone(payment.created_at)
        self.assertIsNotNone(payment.updated_at)

    @unittest.expectedFailure
    def test_create_payment_with_invalid_status(self):
        with self.assertRaises(ValueError, msg="Invalid status should raise a ValueError"):
            Payment.objects.create(amount=60.0, status='invalid_status')

    def test_create_payment_with_invalid_status(self):
        with self.assertRaises(ValueError, msg="Invalid status should raise a ValueError"):
            print("Attempting to create a payment with status: invalid_status")
            Payment.objects.create(amount=50.0, status="invalid_status")
            print("This should not be printed if ValueError is raised")

    def test_payment_status_choices(self):
        # Check if creating a payment with valid status does not raise ValueError
        valid_status_payment = Payment.objects.create(
            amount=30.0, status=Payment.Status.PENDING)
        self.assertEqual(valid_status_payment.status, Payment.Status.PENDING)

        # Check if creating a payment with an invalid status raises ValueError
        with self.assertRaises(ValueError, msg="Invalid status should raise a ValueError"):
            print("Attempting to create a payment with status: invalid_status")
            Payment.objects.create(amount=40.0, status="invalid_status")
            print("This should not be printed if ValueError is raised")

    def test_payment_timestamps(self):
        payment = Payment.objects.create(
            amount=40.0, status=Payment.Status.PENDING)
        initial_created_at = payment.created_at
        initial_updated_at = payment.updated_at

        # Simulate an update with a small delay
        time.sleep(1)
        payment.status = Payment.Status.COMPLETED
        payment.save()

        # Refresh the instance to get the updated values from the database
        payment.refresh_from_db()

        # Check if updated_at is changed but created_at remains the same
        self.assertEqual(payment.created_at, initial_created_at)
        self.assertGreater(payment.updated_at, initial_updated_at,
                           msg="updated_at should be greater than initial_updated_at")
