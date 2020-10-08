


class Person(object):

    def __init__(self, name=None, connected=[], timestep=0, status=0):
        self.name = name
        self.connected = connected # ["Amy", "Bob"]
        self.timestep = timestep
        self.status = status # [0: Healthy; >1: Susceptible; 1: Infected; -1: Recovered; None: Death]
        self.last_status = 0

    def set_name(self, name):
        self.name = name

    def get_name(self):
        return self.name

    def get_status_name(self):
        if self.status is None:
            return "Died"
        elif self.status == 0:
            return "Healthy"
        elif self.status == -1:
            return "Recovered"
        elif self.status == 1:
            return "Infected"
        else:
            return "Susceptible"

    def get_timestep(self):
        return self.timestep

    def update_timestep(self, status):
        self.timestep += 1
        self.last_status = self.status
        self.status = status

    def is_updated(self, timestep):
        return self.timestep == timestep

    def get_connected(self):
        return self.connected

    def delete_connected(self, person_name):
        if person_name in self.connected:
            self.connected.remove(person_name)
        return

    def set_status(self, status):
        self.status = status

    def get_status(self):
        return self.status

    def get_last_status(self):
        return self.last_status

    def add_connected(self, connected):
        if type(connected) is list:
            self.connected.extend(connected)
        else:
            self.connected.append(connected)
        self.connected = list(set(self.connected))
