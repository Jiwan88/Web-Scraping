import scrapy
from UniversityScraper.items import UniversityItem
import logging, re, traceback

class DundeeSpider(scrapy.Spider):
    name = 'old_dundee'
    allowed_domains = ['www.dundee.ac.uk']
    start_urls = ['https://www.dundee.ac.uk/undergraduate/courses', "https://www.dundee.ac.uk/postgraduate/courses", 'https://www.dundee.ac.uk/guides/english-language-requirements']

    def parse(self, response):
        if 'undergraduate' in response.url:
            yield scrapy.Request(response.url, callback=self.parse_undergrad)

        if 'postgraduate' in response.url:
            yield scrapy.Request(response.url, callback=self.parse_postgrad)


    def parse_undergrad(self, response):
        courses = response.css(".filterable-list a::attr(href)").extract()   
        logging.warn("DuneSpider; Scraping Started...; url= %s",response.url)
        courses_length = len(courses)

        for course in range(courses_length):
            courses[course] = "https://www.dundee.ac.uk" + courses[course]

        logging.warn("DuneSpider; Scraping Courses Started....; url= %s",response.url)
        for course_url in courses:
            yield scrapy.Request(course_url, callback=self.parse_course)


        courses_entry_req = courses.copy()
        courses_fee = courses.copy()
        courses_subject = courses.copy()
        courses_careers = courses.copy()

        for course in range(courses_length):
            courses_entry_req[course] = courses[course] + "/entry-requirements"
            courses_fee[course] = courses[course] + "/fees-and-funding"
            courses_subject[course] = courses[course] + "/teaching-and-assessment"
            courses_careers[course] = courses[course] + "/careers"

        for course_url in courses_entry_req:
             yield scrapy.Request(course_url, callback=self.parse_course_entry_req)

        for course_url in courses_fee:
             yield scrapy.Request(course_url, callback=self.parse_course_fee)

        for course_url in courses_subject:
             yield scrapy.Request(course_url, callback=self.parse_course_subject)

        for course_url in courses_careers:
             yield scrapy.Request(course_url, callback=self.parse_course_careers)


    def parse_postgrad(self, response):
        courses = response.css(".filterable-list a::attr(href)").extract() 
        logging.warn("DuneSpider; Scraping Started...; url= %s",response.url)
        courses_length = len(courses)

        for course in range(courses_length):
            courses[course] = "https://www.dundee.ac.uk" + courses[course]

        logging.warn("DuneSpider; Scraping Courses Started....; url= %s",response.url)
        for course_url in courses:
            yield scrapy.Request(course_url, callback=self.parse_course)

        courses_entry_req = courses.copy()
        courses_fee = courses.copy()
        courses_subject = courses.copy()
        courses_careers = courses.copy()

        for course in range(courses_length):
            courses_entry_req[course] = courses[course] + "/entry-requirements"
            courses_fee[course] = courses[course] + "/fees-and-funding"
            courses_subject[course] = courses[course] + "/teaching-and-assessment"
            courses_careers[course] = courses[course] + "/careers"

        for course_url in courses_entry_req:
             yield scrapy.Request(course_url, callback=self.parse_course_entry_req)

        for course_url in courses_fee:
             yield scrapy.Request(course_url, callback=self.parse_course_fee)

        for course_url in courses_subject:
             yield scrapy.Request(course_url, callback=self.parse_course_subject)

        for course_url in courses_careers:
             yield scrapy.Request(course_url, callback=self.parse_course_careers)


    def parse_course(self, response):
        try:
            item = UniversityItem()
            #1 course name
            course_name = response.css(".hero__title::text").extract_first()
            item['course_name'] = course_name

            #2 category
            category = response.css(".hero__group_name a::text").extract_first()
            item['category'] = category

            #4 Course Website
            course_website = response.url
            item['course_website'] = course_website

            if 'undergraduate' in response.url:
                 #5 duration
                duration = response.css(".program__overview-item:nth-child(3) strong::text").extract()
                item['duration'] = duration
                #7 study_mode
                study_mode = response.css(".program__overview-item:nth-child(4) strong::text").extract()
                item['study_mode'] = study_mode
                #8 degree_level
                item['degree_level'] = 'Undergraduate'
                #11 intake month
                intake_month = response.css("#course-entry-dates p").css("::text").extract()
                item['intake_month'] = intake_month[0].split()[0]
                #14 city
                city = response.css(".program__overview-item:nth-child(5) strong").css("::text").extract()
                item['city'] = city
        
            else:
                duration = response.css(".program__overview-item:nth-child(2) strong::text").extract()
                item['duration'] = duration
                study_mode = response.css(".program__overview-item:nth-child(3) strong").css("::text").extract()
                item['degree_level'] = 'Postgraduate'
                intake_month = response.css(".program__overview-item:nth-child(1) strong").css("::text").extract()
                item['intake_month'] = intake_month[0].split()[0]
                city = response.css(".program__overview-item:nth-child(4) strong").css("::text").extract()
                item['city'] = 'city'

            #6 duration_term
            time = duration[0].split()
            try:
                if int(time[0]) <= 12 and time[1] == 'months':
                    item['duration'] = 'months'
                elif int(time[0]) == 1:
                    item['duration'] = 'year'
                elif int(time[0]) >= 12 and time[1] == 'months':
                    item['duration'] = 'years'
                else:
                    item['duration'] = 'years'
            
            except ValueError:
                    item['duration'] = 'years'

            
            #8 Degree level

            #9 Monthly Intake
            
            #10 Intake Day
            
            #11 Intake Month
                
            #12 Apply Day
            # apply_day = None

            #13 Apply Month
            # apply_month = None

            #14 City
            #15 Domestic Only
            # domestic_only = None
            #50 Course Description
            course_description = response.css(".wysiwyg p::text").extract()
            item['course_description'] = course_description

            yield item

        except Exception as e:
            logging.error("SampleSpider; msg=Crawling Failed > %s;url= %s",str(e),response.url)
            logging.error("SampleSpider; msg=Crawling Failed;url= %s;Error=%s",response.url,traceback.format_exc())


    def parse_course_fee(self, response):
        try:
            item = UniversityItem()

            #16 International Fee
            international_fee = response.css("#international-fees::text").extract()
            item['international_fee'] = international_fee

            #17 Domestic Fee
            domestic_fee = response.css("#scottish-fees::text").extract()
            item['domestic_fee'] = domestic_fee

            #18 Fee Term
            item['fee_term'] = 'Year'

            #19 Fee Year
            item['fee_year'] = '2020'

            #20 Currency
            item['currency'] = "Pound Sterling"

            #21 Study Load
            # study_load = None

            yield  item
        except Exception as e:
            logging.error("SampleSpider; msg=Crawling Failed > %s;url= %s",str(e),response.url)
            logging.error("SampleSpider; msg=Crawling Failed;url= %s;Error=%s",response.url,traceback.format_exc())


    def parse_course_entry_req(self, response):
        try:
            item = UniversityItem()
            #22 IELTS Listening
            ielts_listening = response.css(".scores__score:nth-child(3) strong").css("::text").extract()
            item['ielts_listening'] = ielts_listening            

            #23 IELTS Speaking
            ielts_speaking = response.css(".scores__score:nth-child(4) strong").css("::text").extract()
            item['ielts_speaking'] = ielts_speaking

            #24 IELTS Writing
            ielts_writing = response.css(".scores__score:nth-child(5) strong").css("::text").extract()
            item['ielts_writing'] = ielts_writing

            #25 IELTS Reading
            ielts_reading = response.css(".scores__score:nth-child(2) strong").css("::text").extract()
            item['ielts_reading'] = ielts_reading

            #26 IELTS Overall
            ielts_overall = response.css(".scores__score:nth-child(1) strong").css("::text").extract()
            item['ielts_overall'] = ielts_overall

            ''' PTE and TOEFL data is common for all fields'''

            #27 PTE Listening
            item['pte_listening'] = 56

            #28 PTE Speaking
            item['pte_speaking'] = 56

            #29 PTE Writing
            item['pte_writing'] = 56

            #30 PTE Reading
            item['pte_reading'] = 56

            #31 PTE Overall
            item['pte_overall'] = 62

            #32 TOEFL Listening
            item['toefl_listening'] = 21

            #33 TOEFL Speaking
            item['toefl_speaking'] = 20

            #34 TOEFL Writing
            item['toefl_writing'] = 23

            #35 TOEFL Reading
            item['toefl_reading'] = 20

            #36 TOEFL Overall
            item['toefl_overall'] = 88

            #37 English Test
            item['english_test'] = 6.5

            #38 Reading
            item['reading'] = 5.5

            #39 Listening
            item['listening'] = 5.5

            #40 Speaking
            item['speaking'] = 5.5

            #41 Writing
            item['writing'] = 6.0

            #42 Overall
            item['overall'] = 6.5

            #43 Academic Level
            # item['academic_level'] = None

            #44 Academic Score
            # academic_score = None

            #45 Score Type
            # score_type = None
            
            #46 Academic Country
            # academic_country = None

            #47 Other Test
            # other_test = None

            #48 Score
            # score = None

            #49 Other Requirements
            # other_requirements = None

            yield item
        except Exception as e:
            logging.error("SampleSpider; msg=Crawling Failed > %s;url= %s",str(e),response.url)
            logging.error("SampleSpider; msg=Crawling Failed;url= %s;Error=%s",response.url,traceback.format_exc())


            
    def parse_course_subject(self, response):
        try:
            item =UniversityItem()
            #51 Course Structure
            if 'undergraduate' in response.url:
                course_structure = response.xpath('//h2[@class="accordion__heading"]/button/span[@class="accordion__button-title"]/text()').extract()
                item['course_structure'] = course_structure
            else:
                if len(response.xpath('//h2[@class="accordion__heading"]/button/span[@class="accordion__button-title"]/text()').extract()) == 0:
                    course_structure = response.css(".wysiwyg a::text").extract()
                else:
                    course_structure = response.xpath('//h2[@class="accordion__heading"]/button/span[@class="accordion__button-title"]/text()').extract()
                item['course_structure'] = course_structure


            yield item
        except Exception as e:
            logging.error("SampleSpider; msg=Crawling Failed > %s;url= %s",str(e),response.url)
            logging.error("SampleSpider; msg=Crawling Failed;url= %s;Error=%s",response.url,traceback.format_exc())
            
            
    def parse_course_careers(self, response):
        try:
            item = UniversityItem()
            #52 Career
            career = response.css(".wysiwyg p::text").extract()
            item['career'] = career

            #53 Scholarship
            # scholarship = None
            yield item
        
        except Exception as e:
            logging.error("SampleSpider; msg=Crawling Failed > %s;url= %s",str(e),response.url)
            logging.error("SampleSpider; msg=Crawling Failed;url= %s;Error=%s",response.url,traceback.format_exc())


    # def parse_pte_toefl(self, response):
    ''' This data is all given in one single page, so i just manually added  https://www.dundee.ac.uk/guides/english-language-requirements .
    also storing in dictionary and meta tag can also be used to get the dict key value'''




