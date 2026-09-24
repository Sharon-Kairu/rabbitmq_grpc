import grpc
import availability_pb2
import availability_pb2_grpc

def get_available_slots(doctor_id):
    channel = grpc.insecure_channel("localhost:50051")
    stub = availability_pb2_grpc.AvailabilityServiceStub(channel)
    request = availability_pb2.DoctorRequest(doctor_id=doctor_id)
    response = stub.GetAvailableSlots(request)
    return list(response.available_slots)