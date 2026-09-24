import graphene
from graphene_django import DjangoObjectType
from models import Doctor, Booking
from grpc_client import get_available_slots
from tasks import send_booking_confirmation


class DoctorType(DjangoObjectType):
    class Meta:
        model = Doctor
        fields = ("id", "name", "specialty")


class BookingType(DjangoObjectType):
    class Meta:
        model = Booking
        fields = ("id", "doctor", "patient_name", "slot_time", "status", "created_at")


class Query(graphene.ObjectType):
    doctors = graphene.List(DoctorType)
    available_slots = graphene.List(graphene.String, doctor_id=graphene.Int(required=True))

    def resolve_doctors(root, info):
        return Doctor.objects.all()

    def resolve_available_slots(root, info, doctor_id):
        # This is the GraphQL layer calling out to the gRPC microservice
        return get_available_slots(doctor_id)


class CreateBooking(graphene.Mutation):
    class Arguments:
        doctor_id = graphene.Int(required=True)
        patient_name = graphene.String(required=True)
        slot_time = graphene.String(required=True)

    booking = graphene.Field(BookingType)

    def mutate(root, info, doctor_id, patient_name, slot_time):
        doctor = Doctor.objects.get(id=doctor_id)
        booking = Booking.objects.create(
            doctor=doctor,
            patient_name=patient_name,
            slot_time=slot_time,
            status="pending",
        )
        # Push the confirmation task to RabbitMQ via Celery instead of doing it here directly
        send_booking_confirmation.delay(booking.id)
        return CreateBooking(booking=booking)


class Mutation(graphene.ObjectType):
    create_booking = CreateBooking.Field()


schema = graphene.Schema(query=Query, mutation=Mutation)