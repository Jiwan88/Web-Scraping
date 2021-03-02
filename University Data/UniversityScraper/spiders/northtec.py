import scrapy
from ..items import  UniversityItem
import logging, re, traceback


class NorthtecSpider(scrapy.Spider):
    name = 'northtec'
    allowed_domains = ['www.northtec.ac.nz']
    start_urls = ['https://www.northtec.ac.nz/programmes/']

    def parse(self, response):
        category = response.xpath("//div[@class='span3 tablet6 mobile4 inline-block']/div[@class='col-inner']/a/@href").extract()
        category_length = len(category)
        for category_url in range(category_length):
            category[category_url] =  'https://www.northtec.ac.nz' + category[category_url]

        single_page_category = ['https://www.northtec.ac.nz/programmes/civil-engineering/new-zealand-diploma-in-engineering-civil', 'https://www.northtec.ac.nz/programmes/architectural-technology/new-zealand-diploma-in-architectural-technology', 'https://www.northtec.ac.nz/programmes/mechanical-engineering/new-zealand-certificate-in-mechanical-engineering-level-3', ]

        for category_url in category:
            if category_url not in single_page_category:
                yield scrapy.Request(category_url, callback=self.parse_category)
        
        for category_url in single_page_category:
            yield scrapy.Request(category_url, callback=self.parse_course)


    def parse_category(self, response):
        courses = response.xpath("//div[@class='col-inner']/div[@class='list-item']/a/@href").extract()
        for course in courses:
            yield scrapy.Request('https://www.northtec.ac.nz' + course, callback=self.parse_course)


    def parse_course(self, response):
        try:
            item = UniversityItem()
            #1 CourseName
            course_name = response.css("h1::text").extract()
            item['course_name'] = course_name

            #2 Category
            if 'Engineering' in course_name:
                item['category'] = 'Engineering'
            else:
                category = response.css(".CMSBreadCrumbsLink::text").extract()
                item['category'] = category[2]

            #4 Course Website
            course_website = response.url

            #5 Duration
            duration = response.css(".icon-svg-duration+ .text-with-icon__content p").css("::text").extract()
            item['duration'] = duration
            
            #6 Duration Term
            if 'weeks' in duration:
                item['duration_term'] = 'weeks'
            elif 'year' in duration:
                item['duration'] = 'year' 

            #7 Study Mode
            study_mode = response.css(".icon-svg-calendar+ .text-with-icon__content").css("::text").extract()
            if 'Online (eCampus):' in study_mode:
                item['study_mode'] = "Online"
            else:
                item['study_mode'] = "OnCampus"
            
            #11 Intake Month
            intake_month = response.css(".icon-svg-calendar+ .text-with-icon__content p").css("::text").extract()
            item['intake_month'] = intake_month
 
            #14 City
            city = response.css(".ribbon::text").extract()
            item['city'] = city

            #15 Domestic Only
            #16 International Fee
            fee = response.css(".icon-svg-pig+ .text-with-icon__content").css("::text").extract()
            
            try:
                # degree_level
                degree_level = response.css(".text-with-icon:nth-child(1)").css("::text").extract()
                if '3' in degree_level or '3' in response.url:
                    item['degree_level'] = 'CERTIFICATE'
                elif '4' in degree_level:
                    item['degree_level'] = 'CERTIFICATE' 
                elif '5' in degree_level:
                    item['degree_level'] = 'DIPLOMA'
                elif '6' in degree_level:
                    item['degree_level'] = 'DIPLOMA'
                elif '7' in degree_level:
                    item['degree_level'] = 'BACHELOR'
                else:
                    item['degree_level'] = 'CERTIFICATE'

                #17 Domestic Fee
                if "Fees Free" in fee:
                    item['domestic_fee'] = 'Fee Free'
                if 'Programme not open to international students' in fee:
                    item['international_fee'] = 'Programme not open to international students'
                    item['domestic_only'] = True
                else:
                    fee_list = []
                    for i in fee:
                        fee_list.append(re.findall(r'\d+,\d{3}', i))
                    fee_list = [x for x in fee_list if x]
                    if len(fee_list) == 2:
                        item['domestic_fee'] = fee_list[0]
                        item['international_fee'] = fee_list[1]
                        item['domestic_only'] = False

                #18 Fee Term
                if (item['domestic_fee'] == 'Fee Free') and (item['international_fee'] == 'Programme not open to international students'):
                    item['fee_term'] = None 
                else:
                    item['fee_term'] = '1 Year'

            except Exception as e:
                logging.error("NorthSpider; msg=Crawling Failed > %s;url= %s",str(e),response.url)
                logging.error("NorthSpider; msg=Crawling Failed;url= %s;Error=%s",response.url,traceback.format_exc())

            #19 Fee Year
            item['fee_year'] = 2021
            #20 Currency
            item['currency'] = 'NZD'

            #21 Study Load # i found Full time/ Part time
            study_load1 = response.css(".text-with-icon:nth-child(1)").css("::text").extract()
            study_load2 = response.css(".text-with-icon:nth-child(2)").css("::text").extract()
            if 'Full time/Part time' in study_load1 or 'Full time/Part time' in study_load2:
                item['study_load'] = 'Full time/Part time'
            elif 'Part time' in study_load1 or 'Part time' in study_load2:
                item['study_load'] = 'Part time'
            elif 'Full time' in study_load1 or 'Full time' in study_load2:
                item['study_load'] = 'Full time'
            
            # SO MAY THINGS TO DO FROM THIS COURSE DESCRIPTION WHOLE PARAGRAPH
            course_info = response.css(".course-description").css("::text").extract()
            try: 
                if "Admission information\xa0" in course_info:
                    ielts = course_info.index("Admission information\xa0")
                elif "Admission information" in course_info:
                    ielts = course_info.index("Admission information")
                elif 'Entry requirements' in course_info:
                    ielts = course_info.index("Entry requirements")
                ielts_p = ' '.join(course_info[ielts:ielts+ 100]) 
                
                ielts_score = re.findall(r'\s[5-8]{1}\.?5?', ielts_p)
                # ielts_score = [x for x in ielts_score if x]

                #22 IELTS Listening
                item['ielts_listening'] = ielts_score[0]

                #23 IELTS Speaking
                item['ielts_speaking'] = ielts_score[0]

                #24 IELTS Writing
                item['ielts_writing'] = ielts_score[0]

                #25 IELTS Reading
                item['ielts_reading'] = ielts_score[0]

                #26 IELTS Overall
                item['ielts_overall'] = ielts_score[0]
                
                #49 Other Requirements
                item['other_requirements'] = ielts_p
            except Exception as e:
                logging.error("NorthSpider; msg=Crawling Failed > %s;url= %s",str(e),response.url)
                logging.error("NorthSpider; msg=Crawling Failed;url= %s;Error=%s",response.url,traceback.format_exc())
        
            #50 Course Description
            try:
                course_description1 = response.css("h3+ p").css("::text").extract()
                course_description2 = response.css(".course-description > p:nth-child(2)").css("::text").extract()
                course_description = course_description1[1:] + course_description2
                item['course_description'] = course_description
            except Exception as e:
                logging.error("NorthSpider; msg=Crawling Failed > %s;url= %s",str(e),response.url)
                logging.error("NorthSpider; msg=Crawling Failed;url= %s;Error=%s",response.url,traceback.format_exc())

            #51 Course Structure
            try:
                course_structure = response.css(".text-left").css("::text").extract()  # this applies to most of the pages with int text-list
                item['course_structure'] = course_structure

                #52 Career
                if 'Study and Career Pathways' in course_info:
                    career_p = course_info.index('Study and Career Pathways')
                if 'Career opportunities and pathways' in course_info:
                    career_p = course_info.index('Career opportunities and pathways')

                career  = ' '.join(course_info[career_p: career_p+200])
                item['career'] = career                

            except Exception as e:
                logging.error("NorthSpider; msg=Crawling Failed > %s;url= %s",str(e),response.url)
                logging.error("NorthSpider; msg=Crawling Failed;url= %s;Error=%s",response.url,traceback.format_exc())
            
            #54 language
            item['language'] = 'English'  # some maori subject can be maori language

            yield  item
        except Exception as e:
            logging.error("NorthSpider; msg=Crawling Failed > %s;url= %s",str(e),response.url)
            logging.error("NorthSpider; msg=Crawling Failed;url= %s;Error=%s",response.url,traceback.format_exc())

            
