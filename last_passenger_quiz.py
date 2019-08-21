from random import randint


class Passenger:
    def __init__(self, ticket_seat):
        self.ticket_seat = ticket_seat
        self.taken_seat = None

    def take_seat(self, seat=None):
        self.taken_seat = seat if seat else self.ticket_seat


class Plain:
    FREE_SEAT, BUSY_SEAT = ('free', 'busy')

    def __init__(self, seats_number):
        self.seats = {i: Plain.FREE_SEAT for i in range(1, seats_number + 1)}

    def _free_all_seats(self):
        for seat in self.seats:
            self.seats[seat] = Plain.FREE_SEAT

    def _change_seat_status(self, seat):
        self.seats[seat] = Plain.BUSY_SEAT

    def _define_random_seat(self):
        return randint(1, len(self.seats))

    def _choose_free_random_seat(self):
        random_seat = self._define_random_seat()
        if self.seats[random_seat] == Plain.FREE_SEAT:
            return random_seat
        return self._choose_free_random_seat()

    def _board_passenger(self, passenger):
        if passenger.ticket_seat == 1:
            taken_seat = self._define_random_seat()
            self._change_seat_status(taken_seat)
            passenger.take_seat(taken_seat)
            return

        if self.seats[passenger.ticket_seat] == Plain.FREE_SEAT:
            self._change_seat_status(passenger.ticket_seat)
            passenger.take_seat()
        else:
            random_seat = self._choose_free_random_seat()
            self._change_seat_status(random_seat)
            passenger.take_seat(random_seat)

    def board(self, passengers):
        for passenger in passengers:
            self._board_passenger(passenger)

    def free_plain(self):
        self._free_all_seats()


class Airport:
    def __init__(self, flights, tickets):
        self.flights = flights
        self.tickets = tickets
        self.last_passenger_on_his_seat_count = 0

    def notice_last_pasenger(self, last_passenger):
        if last_passenger.taken_seat == last_passenger.ticket_seat:
            self.last_passenger_on_his_seat_count += 1

    def calc_probability(self):
        if self.last_passenger_on_his_seat_count == 0:
            return 0
        return (self.last_passenger_on_his_seat_count / self.flights)*100

    def start_work(self):
        plain = Plain(self.tickets)
        for _ in range(self.flights):
            passengers_queue = [
                Passenger(ticket)
                for ticket in range(1, self.tickets + 1)
            ]
            plain.board(passengers_queue)
            self.notice_last_pasenger(
                passengers_queue[len(passengers_queue) - 1])
            plain.free_plain()


def input_handler(input_text, default_value):
    try:
        input_result = int(input(input_text))
        return input_result
    except:
        return default_value


if __name__ == '__main__':
    FLIGHTS, TICKETS = (100, 100)
    flights = input_handler('Number of flights:\n', default_value=FLIGHTS)
    passengers = input_handler(
        'Number of passengers in one flight:\n', default_value=TICKETS)

    print('{0} flights with {1} passengers in each'.format(
        flights, passengers))

    airport = Airport(flights, passengers)
    airport.start_work()
    probability = airport.calc_probability()
    print('Probability that last passenger takes his seat is {0}% for {1} flights'.format(
        probability, flights))
