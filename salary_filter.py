import requests
from bs4 import BeautifulSoup
import re


class SalarySearcher():


    def __init__(self):
        self.get_country_digit()
        self.get_income_range()
        self.relate_country_digit_to_link()
        self.find_all_jobs_in_link()
        self.filter_jobs_by_income_range()
        self.extract_job_title_and_salary()
        self.sort_jobs_by_salary()
        self.print_job_list_with_index()

    def get_country_digit(self):
        valid_options = ["1", "2", "3"]
        get_option_text = "\nChoose the country to search:\n" \
                          "1 - Germany\n" \
                          "2 - Switzerland\n" \
                          "3 - Austria\n\n" \
                          "User Input: "
        country_digit = input(get_option_text)
        while country_digit not in valid_options:
            print("Invalid input. Please enter a digit from 1 to 3.")
            country_digit = input(get_option_text)
        self.country_digit = country_digit

    def get_income_range(self):
        text_min = "\n----------\n" \
                   "Enter the minimal salary (EUR): \n\n" \
                   "User Input: "
        text_max = "\n----------\n" \
                   "Enter the maximal salary (EUR): \n\n" \
                   "User Input: "

        self.min_salary = int(self.get_income_range_input(text_min))
        self.max_salary = int(self.get_income_range_input(text_max))

    def get_income_range_input(self, input_message):
        validation_error_message = "The salary may only contain numbers"
        inputed_value = input(input_message)
        while not re.match(r"^[0-9]*$", inputed_value):
            print(validation_error_message)
            inputed_value = input(input_message)
        return inputed_value

    def relate_country_digit_to_link(self):
        DICTIONARY_DIGIT_COUNTRY = {
            '1' : "https://www.lohnanalyse.de/at/loehne.html",
            '2' : "https://www.lohnanalyse.de/ch/loehne.html",
            '3' :  "https://www.lohnanalyse.de/de/loehne.html"
        }
        self.link = DICTIONARY_DIGIT_COUNTRY[self.country_digit]

    def find_all_jobs_in_link(self):
        print("\n\nSearching for jobs...\n")
        response = requests.get(self.link)
        soup = BeautifulSoup(response.text, 'html.parser')
        self.jobs = soup.find_all(class_='job col odd')

    def get_job_title(self, job):
        job_name = job.find(class_='job-title').get_text().replace("\n","").replace("\t","")
        return job_name

    def get_job_salary(self, job):
        job_salary = job.find(class_='job-salary').get_text().split(",")[0].replace(".", "")
        return job_salary

    def filter_jobs_by_income_range(self):
        self.filtered_jobs_by_income = [
            job for job in self.jobs if self.min_salary < int(self.get_job_salary(job)) < self.max_salary
        ]

    def extract_job_title_and_salary(self):
        self.job_title_and_salary = [
            [self.get_job_title(job), self.get_job_salary(job)] for job in self.filtered_jobs_by_income
        ]

    def sort_jobs_by_salary(self):
        self.job_title_and_salary.sort(key=lambda x: int(x[1]), reverse=True)

    def print_job_list_with_index(self):
        print("\n----------\n"
              "Jobs Found:\n\n")
        for index, job in enumerate(self.job_title_and_salary, start=1):
            job_title = job[0]
            job_salary = job[1]
            print(f"{index}) {job_title} - {job_salary},00 EUR")
        print("")


s = SalarySearcher()