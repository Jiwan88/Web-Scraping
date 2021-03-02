import scrapy
from ..items import UniversityItem
import logging, traceback


class SherbrookeSpider(scrapy.Spider):
    name = 'sherbrooke'
    allowed_domains = ['www.usherbrooke.ca']
    start_urls = ['https://www.usherbrooke.ca/admission/programmes/?currentPage=1&']
    page_number = 2

    def parse(self, response):
        courses =  response.xpath('//*[@id="c38915"]/div/div[2]/div[2]/a/@href').extract()
        
        for course_url in courses:
            yield scrapy.Request(course_url, callback=self.parse_course)
        
        next_page = 'https://www.usherbrooke.ca/admission/programmes/?currentPage=' + str(SherbrookeSpider.page_number) + '&'

        if SherbrookeSpider.page_number <= 27:
            SherbrookeSpider.page_number += 1
            yield response.follow(next_page, callback=self.parse)

    
    def parse_course(self, response):
        try:
            item = UniversityItem()
            course_name = response.css("#main h1::text").extract() 
            item['course_name'] = course_name
            #2 Category
            category =  response.css(".pap-uniteAdministrativeApprobation::text").extract()
            item['category'] = category

            #4 Course Website
            item['course_website'] = response.url
            
            #8 Degree Level
            degree_level = response.css("dl:nth-child(1) dd:nth-child(6)").css("::text").extract()
            if 'Automne' or 'Hiver' or 'Ã‰tÃ©' in degree_level:
                item['degree_level'] = None
            else: 
                item['degree_level'] = degree_level

            #11 Intake Month
            intake_month1 = response.css("dd:nth-child(8)::text").extract()
            intake_month2 = response.css("dl:nth-child(1) dd:nth-child(6)").css("::text").extract()
            if ("Automne" in intake_month1) or ('Hiver' in intake_month1) or ('Été' in intake_month1) or ('Automne, Hiver') in intake_month1 or ('Automne, Hiver, Étér') in intake_month1 or ('Automne, Hiver, Été' in intake_month1):
                item['intake_month'] = intake_month1
            if ("Automne" in intake_month2) or ('Hiver' in intake_month2) or ('Été' in intake_month2) or ('Automne, Hiver') in intake_month2 or ('Automne, Hiver, Étér') in intake_month2 or ('Automne, Hiver, Été' in intake_month2):
                item['intake_month'] = intake_month2
              
            #14 City
            city1 = response.css("dl+ dl dd:nth-child(6)::text").extract()
            city2 = response.css("dl+ dl dd:nth-child(4)::text").extract()
            if 'Campus principal de Sherbrooke' in city1 or 'Campus de la santé Sherbrooke' in city1 or 'Campus de Longueuil' in city1:
                item['city'] = city1
            elif 'Campus principal de Sherbrooke' in city1 or 'Campus de la santé Sherbrooke' in city1 or 'Campus de Longueuil' in city2:
                item['city'] = city2
            elif 'Formation Ã  distance - Campus principal' in city1:
                item['city'] = city1
            else:
                item['city'] = 'Campus principal de Sherbrooke'


            #15 Domestic Only, hard need to see if the earth icon is available or not on the search page
            domestic_only1 = response.css(".lineSeparator p::text").extract() 
            domestic_only2 = response.css(".gapSeparator::text").extract()
            if 'Ouvert aux étudiants internationaux en régime régulier' in domestic_only1 or 'Ouvert aux étudiants internationaux en régime régulier' in domestic_only2:
                item['domestic_only'] = False
            else:
                item['domestic_only'] = True

            # #16 International Fee
            if item['domestic_only'] is True:
                item['international_fee'] = None
            else:
                item['international_fee'] = '9375 - 10425'

            # #17 Domestic Fee
            item['domestic_fee'] = '4485'  # https://www.usherbrooke.ca/admission/couts-et-aide-financiere/frais-de-scolarite/etudiant-canadien-hors-quebec/#c34539-1

            #18 Fee Term
            item['fee_term'] = 'Year'

            #19 Fee Year
            item['fee_year'] = '2020'

            #20 Currency
            item['currency'] = 'CAD'

            # language
            if item['domestic_only'] is False:
                item['language'] = 'English, French'
            else:
                item['language'] = 'French'

            #21 Study Load
            study_load = response.css("dl+ dl dd:nth-child(4)::text").extract()
            study_load2 = response.css("dl+ dl dd:nth-child(2)::text").extract()
            if 'Temps complet, Temps partiel' in study_load:
                item['study_load'] = 'Both'
            elif 'Temps complet' in study_load:
                item['study_load'] = 'Full-time'
            elif 'Temps partiel' in study_load:
                item['study_load'] = 'Part-time'
            elif 'Temps complet, Temps partiel' in study_load2:
                item['study_load'] = 'Both'
            elif 'Temps complet' in study_load2:
                item['study_load'] = 'Full-time'
            elif 'Temps partiel' in study_load2:
                item['study_load'] = 'Part-time'

            # https://www.usherbrooke.ca/admission/programme/203/baccalaureat-en-administration-des-affaires/
            # I only found the data of ielts and english on this page admission and requirements, so i filled these values 

            
            if item['domestic_only'] is False:
                #22 IELTS Listening
                item['ielts_listening'] = 7

                # #23 IELTS Speaking
                item['ielts_speaking'] = 7

                # #24 IELTS Writing
                item['ielts_writing'] = 7

                # #25 IELTS Reading
                item['ielts_reading'] = 7

                # #26 IELTS Overall
                item['ielts_overall'] = 7

                # #32 TOEFL Listening
                item['toefl_listening'] = 100

                # #33 TOEFL Speaking
                item['toefl_speaking'] = 100

                # #34 TOEFL Writing
                item['toefl_writing'] = 100

                # #35 TOEFL Reading
                item['toefl_reading'] = 100

                # #36 TOEFL Overall
                item['toefl_overall'] = 100

            #49 Other Requirements
            item['other_requirements']  = 'French language Compulsory'

            #50 Course Description
            course_description = response.css(".tab-content strong , strong+ p").css("::text").extract()
            item['course_description'] = course_description

            #51 Course Structure
            course_structure = response.css(".ap-pop::text").extract()
            item['course_structure'] = course_structure

            #52 Career
            career = response.css("ul:nth-child(13) li::text").extract()
            item['career'] = career

            yield item

        except Exception as e:
            logging.error("SherbrookeSpider; msg=Crawling Failed > %s;url= %s",str(e),response.url)
            logging.error("SherbrookeSpider; msg=Crawling Failed;url= %s;Error=%s",response.url,traceback.format_exc())


                    




