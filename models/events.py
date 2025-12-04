# Importing Python's logging method
# Will use as a second option incase database is down
import logging
# Importing custom Logger class
from models.logger import Logger

class EventLogger:
    """
    Singleton class
    used for managing and recording logs
    """
    _instance = None

    # Creating new instance of the class
    def __new__(cls):
        if cls._instance is None: #If no instance
            cls._instance = super(EventLogger, cls).__new__(cls)#Creating new instance
            cls._instance.logger = None
        return cls._instance #return same instance

    @classmethod
    def init_logger(self, logger=None):
        temp_logger = Logger()
        if temp_logger.is_init():
            self.logger = temp_logger
            print('Database Logging Initialised')
        else:
            # If no logger given then use file logging instead
            logging.basicConfig(filename="../log_file.txt", format="%(asctime)s - %(levelname)s - %(message)s")
            print('Creating File Logging')

    # Methods for logging

    # REGISTRATION:
    # Method for logging registration
    def log_registration(self, action, user_id, details, ip_address):
        try:
            if self.logger:
                self.logger.log(action,user_id,details, ip_address)
            else:
                logging.info(f"Action: {action} [user: {user_id}] - {details}")
            print("Logged registration")
        except Exception as e:
            print("Unable to log successful registration")

    # Method for logging unsuccessfull registration
    def log_unsuccessful_registration(self, action, user_id, details, ip_address):
        try:
            if self.logger:
                self.logger.log(action,user_id,details, ip_address)
            else:
                logging.warning(f"Action: {action} [user: {user_id}] - {details}")
            print("Logged unsuccessful registration")
        except Exception as e:
            print("Unable to log registration issue")

    # LOGIN
    # Method for logging login
    def log_login(self, action, user_id, details, ip_address):
        try:
            if self.logger:
                self.logger.log(action,user_id,details, ip_address)
            else:
                logging.info(f"Action: {action} [user: {user_id}] - {details}")
            print("Logged login")
        except Exception as e:
            print("Unable to log login")


    # Method for logging unsuccessfull login
    def log_unsuccessful_login(self, action, user_id, details, ip_address):
        try:
            if self.logger:
                self.logger.log(action,user_id,details, ip_address)
            else:
                logging.warning(f"Action: {action} [user: {user_id}] - {details}")
            print("Logged login issue")
        except Exception as e:
            print("Unable to log login error")

    # SEARCH
    # Method for logging search
    def log_search(self, action, user_id, details, ip_address):
        try:
            if self.logger:
                self.logger.log(action,user_id,details, ip_address)
            else:
                logging.info(f"Action: {action} [user: {user_id}] - {details}")
            print("Logged search")
        except Exception as e:
            print("Unable to log search")


    # HOME LINKS
    # Method for logging open links
    def log_home_link(self, action, user_id, details, ip_address):
        try:
            if self.logger:
                self.logger.log(action,user_id,details, ip_address)
            else:
                logging.info(f"Action: {action} [user: {user_id}] - {details}")
            print("Logged opened link")
        except Exception as e:
            print("Unable to log link opening")

    # BLOG CREATION
    # Method for Blog Creation.
    def log_blog_creation(self, action, user_id, details, ip_address):
        try:
            if self.logger:
                self.logger.log(action,user_id,details, ip_address)
            else:
                logging.info(f"Action: {action} [user: {user_id}] - {details}")
            print("Logged blog creation")
        except Exception as e:
            print("Unable to log blog creation")

    # BLOG DISPLAY
    # Method for registering blog was displayed
    def log_blog_displayed(self, action, user_id, details, ip_address):
        try:
            if self.logger:
                self.logger.log(action,user_id,details, ip_address)
            else:
                logging.info(f"Action: {action} [user: {user_id}] - {details}")
            print("Logged blog displayed")
        except Exception as e:
            print("Unable to log blog display")

    # BLOG DELETION
    # Method for showing blog was deleted
    def log_blog_deleted(self, action, user_id, details, ip_address):
        try:
            if self.logger:
                self.logger.log(action,user_id,details, ip_address)
            else:
                logging.info(f"Action: {action} [user: {user_id}] - {details}")
            print("Logged blog deleted")
        except Exception as e:
            print("Unable to log blog deletion")