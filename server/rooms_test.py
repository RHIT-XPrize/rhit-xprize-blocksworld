from rooms import RoomsTracker
import threading

class TestRoomsTracker:
    class MockSIOApp:
        def __init__(self):
            self.enter_room_calls = {}

        def enter_room(self, _, room_name):
            if not room_name in self.enter_room_calls:
                self.enter_room_calls[room_name] = 0

            self.enter_room_calls[room_name] += 1

    def setup_method(self):
        self.sio_app = self.MockSIOApp()
        self.rooms_tracker = RoomsTracker(self.sio_app)

    def test_first_add_to_room(self):
        self.rooms_tracker.add_to_room(123)

        assert self.sio_app.enter_room_calls == {"Room0": 1}

    def test_two_additions(self):
        self.rooms_tracker.add_to_room(123)
        self.rooms_tracker.add_to_room(5)

        assert self.sio_app.enter_room_calls == {"Room0": 2}

    def test_stress_additions(self):
        class RoomAdder(threading.Thread):
            def __init__(self, count, seed, room_tracker):
                self.count = count
                self.seed = seed
                self.room_tracker = room_tracker
                super(RoomAdder, self).__init__()

            def run(self):
                for i in range(0, self.count):
                    self.room_tracker.add_to_room(2*i + self.seed)
                    self.room_tracker.add_to_room(2*i + 1 + self.seed)

        expected_calls = {}
        for i in range(0, 100):
            expected_calls["Room" + str(i)] = 2

        t1 = RoomAdder(25, 0, self.rooms_tracker)
        t2 = RoomAdder(25, 25, self.rooms_tracker)
        t3 = RoomAdder(25, 50, self.rooms_tracker)
        t4 = RoomAdder(25, 75, self.rooms_tracker)

        t1.start()
        t2.start()
        t3.start()
        t4.start()

        t1.join()
        t2.join()
        t3.join()
        t4.join()

        assert self.sio_app.enter_room_calls == expected_calls