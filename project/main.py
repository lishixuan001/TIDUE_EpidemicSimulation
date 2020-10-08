import os, sys, copy, uuid
from person import Person
from utils import *
from pdb import set_trace as st
import pandas as pd
import matplotlib.pyplot as plt



class Main():

    def __init__(self):
        self.basedir = "./"
        self.netfile_dir = os.path.join(self.basedir, "net_files")
        self.timestep = 0
        self.net = dict()
        self.simulation_data = list()
        self.simulation_stat = dict()
        self.simulation_code = str(uuid.uuid4().hex)
        self.simulation_record = dict()

    def set_params(self, trans_rate, recov_rate, death_rate, suspe_time, int_code):
        self.trans_rate = trans_rate
        self.recov_rate = recov_rate
        self.death_rate = death_rate
        self.suspe_time = suspe_time
        self.int_code = int_code

    def simulation_mode(self, netfile_name, trans_rate, recov_rate, death_rate, suspe_time, int_code):
        self.savedir_init()
        self.load_net(netfile_name)
        self.set_params(trans_rate, recov_rate, death_rate, suspe_time, int_code)
        self.collect_simulation_data()
        self.show_relationship()
        for _ in range(self.int_code):
            self.update()
            self.collect_simulation_data()
        self.save_simulation_data(save=True)
        self.show_overall_stats(display=True)
        return

    def interactive_mode(self):
        self.savedir_init()
        program_exit = False
        while not program_exit:
            self.show_menu()
            command_line = self.get_input("Please Select From Menu By Inputing Index Number:")
            command_line = command_line.split()
            if len(command_line) <= 0:
                continue
            elif not len(command_line) == 1 and command_line[0].isdigit():
                self.show_warning("Please Input Menu Index (E.g: 1)")
                continue
            else:
                command = command_line[0].strip()
                assert command.isnumeric()
                if command == "0":
                    program_exit = True
                    continue
                elif command == "1":
                    # Load Network
                    netfile_name = self.get_input("Please Input Name of Network:")
                    success = self.load_net(netfile_name, do_quit=False)
                    if success:
                        print("Load Succeeded!")
                    continue

                elif command == "2":
                    # Set Rates
                    rate_index = self.get_input("Please Input Name of The Rate You Want To Set \n\
                                               (1) trans_rate\n\
                                               (2) recov_rate\n\
                                               (3) death_rate\n\
                                               (4) suspe_time\n\
                                               (0) BACK TO MENU")
                    rate_name_dict = {"1":"trans_rate", "2":"recov_rate", "3":"death_rate", "4":"suspe_time"}
                    if rate_index == "0":
                        continue
                    elif rate_index in ["1", "2", "3"]:
                        rate_num = self.get_input("Please Input The Rate Numerics Your Want To Set To [E.g: 0.3]: ")
                        try:
                            rate_num = float(rate_num)
                            if not (rate_num >= 0 and rate_num <= 1):
                                self.show_warning(f"Parameter [trans_rate/recov_rate/death_rate] Must Be Float Within [0, 1] Field")
                                continue
                            else:
                                self.__dict__[rate_name_dict[rate_index]] = rate_num
                                continue
                        except:
                            self.show_warning("Parameter [trans_rate/recov_rate/death_rate] Must Be Float Within [0, 1] Field")
                            continue
                    elif rate_index == "4":
                        rate_num = self.get_input("Please Input The Rate Numerics Your Want To Set To [E.g: 0.3]: ")
                        if not rate_num.isdigit():
                            self.show_warning("Parameter [suspe_time] Must Be An Non-Negative Integer")
                            continue
                        else:
                            if int(rate_num) < 0:
                                self.show_warning("Parameter [suspe_time] Must Be An Non-Negative Integer")
                                continue
                            else:
                                self.__dict__[rate_name_dict[rate_index]] = int(rate_num)
                                continue
                    else:
                        self.show_warning("Index Not In Menu")
                        continue


                elif command == "3":
                    # Node Operations (Find, Insert, Delete)
                    operation_name = self.get_input("Please Input The Type Of Operation You Would Like To Perform:\n\
                                                    (1) find\n\
                                                    (2) insert\n\
                                                    (3) delete\n\
                                                    (0) BACK TO MENU")
                    if operation_name == "0":
                        continue
                    elif operation_name == "1":
                        person_name = self.get_input("Please Input The Person Name You Want To Check:")
                        if person_name not in self.net:
                            self.show_warning("Person Not Found In Network")
                            continue
                        else:
                            self.show_person_record(person_name)
                            continue
                    elif operation_name == "2":
                        person_name = self.get_input("Please Input The Person Name You Want To Insert:")
                        if person_name in self.net:
                            self.show_warning("Person Already Exists In Network")
                            continue
                        else:
                            std_person = Person()
                            self.net[person_name] = copy.deepcopy(std_person)
                            self.net[person_name].set_name(person_name)
                            print(f"Person [{person_name}] Inserted In Network Successfully!")
                            continue
                    elif operation_name == "3":
                        person_name = self.get_input("Please Input The Person Name You Want To Delete:")
                        if person_name not in self.net:
                            self.show_warning("Person Not Found In Network")
                            continue
                        else:
                            connected_people = self.net[person_name].get_connected()
                            del self.net[person_name]
                            for neibor_name in connected_people:
                                self.net[neibor_name].delete_connected(person_name)
                            continue
                    else:
                        self.show_warning("Index Not In Menu")
                        continue

                elif command == "4":
                    # Edge Operations (Add, Remove)
                    operation_name = self.get_input("Please Input The Type Of Operation You Would Like To Perform:\n\
                                                    (1) add\n\
                                                    (2) remove\n\
                                                    (0) BACK TO MENU")
                    if operation_name == "0":
                        continue
                    elif operation_name == "1":
                        names = self.get_input("Please Input Two Person Names You Would Like To Connect, Seperated By Comma (E.g: Alice, Bob):")
                        names = [name.strip() for name in names.split(",")]
                        if not len(names) == 2:
                            self.show_warning("Input Format Not Correct. Please Input Two Person Names You Would Like To Connect, Seperated By Comma (E.g: Alice, Bob)")
                            continue
                        else:
                            name1, name2 = names
                            if name1 not in self.net:
                                self.show_warning(f"Person [{name1}] Not Found In Network")
                                continue
                            elif name2 not in self.net:
                                self.show_warning(f"Person [{name2}] Not Found In Network")
                                continue
                            else:
                                self.net[name1].add_connected(name2)
                                self.net[name2].add_connected(name1)
                                continue
                    elif operation_name == "2":
                        names = self.get_input("Please Input Two Person Names You Would Like To Disconnect, Seperated By Comma (E.g: Alice, Bob):")
                        names = [name.strip() for name in names.split(",")]
                        if not len(names) == 2:
                            self.show_warning("Input Format Not Correct. Please Input Two Person Names You Would Like To Disconnect, Seperated By Comma (E.g: Alice, Bob)")
                            continue
                        else:
                            name1, name2 = names
                            if name1 not in self.net:
                                self.show_warning(f"Person [{name1}] Not Found In Network")
                                continue
                            elif name2 not in self.net:
                                self.show_warning(f"Person [{name2}] Not Found In Network")
                                continue
                            else:
                                self.net[name1].delete_connected(name2)
                                self.net[name2].delete_connected(name1)
                                continue
                    else:
                        self.show_warning("Index Not In Menu")
                        continue

                elif command == "5":
                    # New Infection
                    person_name = self.get_input("Please Input The Person Name You Want To Newly Infect: ")
                    if person_name not in self.net:
                        self.show_warning(f"Person [{person_name}] Not Found In Network")
                        continue
                    else:
                        if not hasattr(self, "suspe_time"):
                            self.show_warning("Parameter [suspe_time] Has Not Been Set Yet")
                            continue
                        else:
                            self.net[person_name].set_status(1+self.suspe_time)
                            continue

                elif command == "6":
                    # Display Network
                    if not self.check_if_has_network():
                        self.show_warning("Network Is Empty Now")
                        continue
                    else:
                        self.show_relationship()
                        continue

                elif command == "7":
                    # Display Statistics
                    if not self.check_if_has_network():
                        self.show_warning("Network Is Empty Now")
                        continue
                    else:
                        self.show_overall_stats(display=True)
                        continue

                elif command == "8":
                    # Update (Run A Timestep)
                    rates = ["trans_rate", "recov_rate", "death_rate", "suspe_time"]
                    has_all_rates = True
                    for rate in rates:
                        if not hasattr(self, rate):
                            self.show_warning(f"Rate [{rate}] Is Not Set Yet")
                            has_all_rates = False
                            break
                    if has_all_rates:
                        if not self.check_if_has_network():
                            self.show_warning("Network Is Empty")
                            continue
                        else:
                            self.update()
                            continue
                    else:
                        continue

                elif command == "9":
                    # (9) Save Metwork
                    if not self.check_if_has_network():
                        self.show_warning("Network Is Empty")
                        continue
                    else:
                        file_name = self.get_input("Please Input The Name Of Network You Want To Save:")
                        if os.path.exists(os.path.join(self.netfile_dir, file_name + ".txt")):
                            self.show_warning("Network File Name Already Exists")
                            continue
                        else:
                            with open(os.path.join(self.netfile_dir, file_name + ".txt"), "w") as file:
                                # Health Status
                                line = ""
                                for person_name in self.net:
                                    if self.net[person_name].get_status() != 0:
                                        line = ",".join([line, f"{person_name} {self.net[person_name].get_status()}"])
                                if line.startswith(","):
                                    line = line[1:]
                                file.write(line + "\n")
                                # Relationship
                                lines = list()
                                for person_name in self.net:
                                    for neibor_name in self.net[person_name].get_connected():
                                        lines.append(f"{person_name}:{neibor_name}\n")
                                file.writelines(lines)

                else:
                    self.show_warning("Index Not In Menu")
                    continue


    def show_menu(self):
        print("============================================")
        print("(1) Load Network")
        print("(2) Set Rates")
        print("(3) Node Operations (Find, Insert, Delete)")
        print("(4) Edge Operations (Add, Remove)")
        print("(5) New Infection")
        print("(6) Display Network")
        print("(7) Display Statistics")
        print("(8) Update (Run A Timestep)")
        print("(9) Save Metwork")
        print("(0) Exit")

    def get_input(self, msg):
        return input(f"\n{msg}\n--> ").strip()

    def show_warning(self, msg):
        print(f"\n********************\n## WARNING: {msg}\n********************\n")

    def check_if_has_network(self):
        return len(self.net) > 0

    def check_if_has_params(self):
        return hasattr(self, 'trans_rate') and hasattr(self, 'recov_rate') and hasattr(self, 'death_rate') and hasattr(self, 'suspe_time')

    def raise_command_input_error(self):
        print("Please Leave Command Following The Guideline")

    def show_person_record(self, person_name):
        assert person_name in self.net
        person = self.net[person_name]
        print("============================================")
        print("Person [{}] is in timestep [{}] and health status [{}]".format(person_name,
                                                                              person.get_timestep(),
                                                                              person.get_status_name()))

    def show_relationship(self):
        print("============================================")
        max_name_length = len(max(list(self.net.keys()), key=lambda x: len(x)))
        max_neibor_length = len(str(max([self.net[person_name] for person_name in self.net], key=lambda x: len(x.get_connected())).get_connected()))
        for person_name in self.net:
            person = self.net[person_name]
            print("[{}] has connected people {}".format(person.get_name().center(max_name_length, " "),
                                                                  str(person.get_connected()).ljust(max_neibor_length, " ")))

    def savedir_init(self, foldername="simulation"):
        self.simulation_dir = os.path.join(self.basedir, foldername)
        if not os.path.exists(self.simulation_dir):
            os.mkdir(self.simulation_dir)

    def collect_simulation_data(self):
        categories = self.show_overall_stats(display=False) # Dictionary -> key: "Healthy"; value: ["Amy", "Bob"]
        environ_dataline = [len(categories[category]) / len(categories.values()) for category in categories]
        environ_dataline.extend([self.trans_rate, self.death_rate, self.recov_rate, self.suspe_time])
        for person_name in self.net:
            person = self.net[person_name]
            dataline = [self.timestep, person.get_name(), person.get_status_name()]
            dataline.extend(environ_dataline)
            self.simulation_data.append(dataline)
            if person_name not in self.simulation_record:
                self.simulation_record[person_name] = list()
            self.simulation_record[person_name].append(person.get_status_name())
        for category in categories:
            if category not in self.simulation_stat:
                self.simulation_stat[category] = list()
            self.simulation_stat[category].append(len(categories[category]))

    def save_simulation_data(self, save=True, columns=["Timestep", "Name", "Status", \
                                                       "HeathyPercentage", "RecoveredPercentage", \
                                                       "DeathPercentage", "InfectedPercentage",
                                                       "SusceptiblePercentage",
                                                       "TransRate", "DeathRate", "RecovRate", "SuspeTime"]):
        if save:
            dateframe = pd.DataFrame(data=self.simulation_data, columns=columns)
            dateframe.to_csv(os.path.join(self.simulation_dir, self.simulation_code + ".csv"), index=False)
            self.create_simulation_graph(save=True)
        else:
            self.create_simulation_graph(save=False)

    def show_simulation_record(self):
        print("============================================")
        max_name_length = len(max(list(self.net.keys()), key=lambda x: len(x)))
        for person_name in self.simulation_record:
            print("[{}]: {}".format(person_name.center(max_name_length, " "),
                                    " -> ".join(self.simulation_record[person_name])))

    def create_simulation_graph(self, save=False):
        x_axis = list(range(self.timestep + 1))
        for category in self.simulation_stat:
            y_axis = self.simulation_stat[category]
            plt.plot(x_axis, y_axis, label=category)
        plt.xlabel('Time Steps')
        plt.ylabel('Population')
        plt.title('Record of Population in All Health Status Over Time Steps')
        plt.legend()
        if save:
            plt.savefig(os.path.join(self.simulation_dir, self.simulation_code + ".png"))
        else:
            plt.show()


    def show_overall_stats(self, display=False):
        categories = dict(
            Healthy=[],
            Recovered=[],
            Died=[],
            Infected=[],
            Susceptible=[]
        )
        for person_name in self.net:
            person = self.net[person_name]
            categories[person.get_status_name()].append(person.get_name())

        if display:
            # Display Overall Statistics
            print("============================================")
            max_category_length = len(max([category for category in categories], key=lambda x: len(x)))
            for category in categories:
                percentage = round(len(categories[category]) / len(self.net) * 100, 2)
                print("[{}] people are [{}] of the population; their names are {}".format(category.center(max_category_length, " "),
                                                                                          (str(percentage) + "%").center(6, " "),
                                                                                          categories[category]))
        return categories

    def show_stats(self):
        print("============================================")
        print("TimeStep: [{}]".format(self.timestep))
        for person_name in self.net:
            person = self.net[person_name]
            print([person.get_name(), person.get_status_name()])

    def update(self):
        """
        Simulate over 1 time step
        """
        self.timestep += 1
        # st()
        for person_name in self.net:
            person = self.net[person_name]
            # If the person has not been updated, update
            if not person.is_updated(self.timestep):
                # Check if Death
                if person.status is None:
                    self.net[person_name].update_timestep(status=None)
                    continue
                # If the person is infected already, test death rate and recover rate
                if person.status is not None and person.status > 0:
                    # Test Death First
                    result = get_result(self.death_rate, self.recov_rate)[0]
                    if result == 1:
                        # Death
                        self.net[person_name].update_timestep(status=None)
                    elif result == 0:
                        # Recover
                        self.net[person_name].update_timestep(status=-1)
                    else:
                        # If is suspectable
                        if person.status > 1:
                            self.net[person_name].update_timestep(status=person.status-1)
                        else:
                            assert person.status == 1
                            self.net[person_name].update_timestep(status=person.status)
                else:
                    assert person.status == 0 or person.status == -1
                    infected_neibors = list()
                    # Collect related persons' last status
                    for neibor_name in person.get_connected():
                        neibor = self.net[neibor_name]
                        if neibor.is_updated(self.timestep):
                            neibor_status = neibor.get_last_status()
                        else:
                            neibor_status = neibor.get_status()
                        if neibor_status is not None and neibor_status > 0:
                                infected_neibors.append(neibor_name)

                    infected_neibors = list(set(infected_neibors))
                    result = if_success(rate=pow(1-self.trans_rate, len(infected_neibors))) # Test If Person Can *NOT* be Infected
                    if result[0]:
                        # Then the person is not infected
                        self.net[person_name].update_timestep(status=person.status)
                    else:
                        self.net[person_name].update_timestep(status=1+self.suspe_time)

    def load_net(self, netfile_name, do_quit=True):
        """
        Generate self.net which is a Dictionary
        """
        std_person = Person()
        file_dir = os.path.join(self.netfile_dir, netfile_name + ".txt")
        if not os.path.exists(file_dir):
            self.show_warning("Net File Does Not Exist")
            if do_quit:
                exit()
            return False
        with open(file_dir, "r") as file:
            lines = file.readlines()
            if len(lines) == 0:
                self.show_warning("You Are Loading An Empty Net File")
                if do_quit:
                    exit()
                return False
            else:
                # Collect Person Status
                persons = lines[0].strip().replace('\n', '').split(",")
                for person_info in persons:
                    person_name, person_status = person_info.strip().split()
                    if person_name not in self.net:
                        self.net[person_name] = copy.deepcopy(std_person)
                        self.net[person_name].set_name(person_name)
                    if person_status.strip() == "None":
                        self.net[person_name].status = None
                    else:
                        self.net[person_name].status = int(person_status)

                # Collect Relationship
                for line in lines[1:]:
                    line = line.strip().replace('\n', '')
                    name1, name2 = line.split(":")
                    if name1 not in self.net:
                        self.net[name1] = copy.deepcopy(std_person)
                        self.net[name1].set_name(name1)
                    if name2 not in self.net:
                        self.net[name2] = copy.deepcopy(std_person)
                        self.net[name2].set_name(name2)
                    self.net[name1].add_connected(name2)
                    self.net[name2].add_connected(name1)
        return True



if __name__ == "__main__":
    args = sys.argv
    if len(args) == 1:
        # Output Usage Information
        print("Do 'python main.py -s netfile trans_rate recov_rate death_rate int_code' for simulation mode and \
              'python main.py -i' for interactive mode")
        exit()
    elif len(args) == 2:
        flag = args[1]
        if "-i" in flag:
            operator = Main()
            operator.interactive_mode()
        else:
            print("Do 'python main.py -s netfile trans_rate recov_rate death_rate int_code' for simulation mode and \
                  'python main.py -i' for interactive mode")
            exit()
    else:
        flag, params = args[1], args[2:]
        if (len(flag) != 0 and not ("-s" in flag)) or len(args) != 8 :
            print("Do 'python main.py -s netfile trans_rate recov_rate death_rate int_code' for simulation mode and \
                  'python main.py -i' for interactive mode")
            exit()
        else:
            netfile, trans_rate, recov_rate, death_rate, suspe_time, int_code = params
            try:
                trans_rate = float(trans_rate)
                recov_rate = float(recov_rate)
                death_rate = float(death_rate)
                suspe_time = int(suspe_time)
                int_code = int(int_code)
            except Exception as e:
                print("# WARNING: paramters not numeric or does not make sense")
                exit()
            operator = Main()
            operator.simulation_mode(netfile, trans_rate, recov_rate, death_rate, suspe_time, int_code)
