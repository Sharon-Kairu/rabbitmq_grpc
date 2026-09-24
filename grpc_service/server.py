from concurrent import futures
import grpc
import availability_pb2
import availability_pb2_grpc

# Hardcoded availability data, keyed by doctor_id — simulates a real scheduling engine
FAKE_AVAILABILITY = {
    1: ["09:00", "10:30", "14:00"],
    2: ["11:00", "13:00", "15:30"],
    3: ["09:30", "12:00", "16:00"],
}

class AvailabilityService(availability_pb2_grpc.AvailabilityServiceServicer):
    def GetAvailableSlots(self, request, context):
        slots = FAKE_AVAILABILITY.get(request.doctor_id, [])
        return availability_pb2.SlotsResponse(available_slots=slots)

def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=4))
    availability_pb2_grpc.add_AvailabilityServiceServicer_to_server(AvailabilityService(), server)
    server.add_insecure_port("[::]:50051")
    server.start()
    print("gRPC Availability Service running on port 50051...")
    server.wait_for_termination()

if __name__ == "__main__":
    serve()