from threading import Thread
from oratio.Session import Session


class Core:
    def __init__(self, data_gatherers, out_path, session_duration,
                 database_managers, label_manager, num_sessions=-1):
        """

        :param data_gatherers: dictionary for relating collectors to all it's processors,
            and each processor to all it's handlers.
            in the format: {Collector: {Processor: [DataHandler]}}
        :param out_path: path where we want to save the data. str
        :param session_duration: number of seconds for session. float
        :param database_managers: list of DatabaseManagers that creating the database.
        :param label_manager: Label manager object. decide when to pop up question for new label to the user.
        :param num_sessions: how many sessions we want to collect.
            If equals to -1, run infinitely until stopped.
            default: -1
        """

        self.session_duration = session_duration
        self.data_gatherers = data_gatherers
        self.label_manager = label_manager
        self.num_sessions = num_sessions
        self.out_path = out_path
        self.running = False
        self.finished = False

        self.database_managers = database_managers
        for database_manager in self.database_managers:
            database_manager.create_data_holder()
        self.start_session_id = len(self.database_managers[0])

        for processor_handlers_dict in data_gatherers.values():
            for handlers_list in processor_handlers_dict.values():
                for handler in handlers_list:
                    handler.create_data_holder(self.start_session_id)
        self.sessions_passed = self.start_session_id


    def run(self):
        self.running = True
        while self.__keep_running():
            curr_session = Session(self.sessions_passed, self.session_duration, self.data_gatherers, self.out_path)
            curr_session.start_session()
            label = self.label_manager.get_label(curr_session, self.start_session_id)
            curr_session.set_label(label)
            Thread(target=lambda: (
                [session_data_handler.save_session(curr_session) for session_data_handler in self.database_managers]
            )).start()
            self.sessions_passed += 1
        self.running = False
        self.finished = self.sessions_passed == self.num_sessions

    def __keep_running(self):
        if self.num_sessions != -1:
            return self.sessions_passed < self.num_sessions and self.running
        return self.running

    def stop(self):
        self.running = False
