import cv2
import numpy as np
from robot.api import logger
from robot.errors import ExecutionFailed
import os

class Matching(object):

    ROBOT_LIBRARY_VERSION = 1.0
    ROBOT_LIBRARY_SCOPE = 'TEST CASE'
    
    def __init__(self):
        self.error = False
    
    def find_image(self, template, screenshot, output_path, threshold=0.8):     # Matching only one template
        self.template_clean = template      # Keep initial template value for logging. We don't have to change template value in the code, but I was lazy
        
        # Logging info for debugging purposes
        logger.info('Template: ' + template, also_console=True)
        logger.info('Output path: ' + output_path, also_console=True)
        logger.info('Screenshot path: ' + screenshot, also_console=True)
        
        self.threshold = float(threshold)       # Robot sends always parameters as string so don't forget to always retype them if you need something different!
        
        # Checking if template is present. Almost original copy paste.
        img_rgb = cv2.imread(screenshot)
        img_gray = cv2.cvtColor(img_rgb, cv2.COLOR_BGR2GRAY)
        template = cv2.imread(template, 0)
        w, h = template.shape[::-1]
        res = cv2.matchTemplate(img_gray,template,cv2.TM_CCOEFF_NORMED)
        
        loc = np.where(res >= self.threshold)
        
        # Getting locations of objects
        for pt in zip(*loc[::-1]):
            cv2.rectangle(img_rgb, pt, (pt[0] + w, pt[1] + h), (0,0,255), 2)
        
        cv2.imwrite(output_path,img_rgb)        # Drawing rectangles with match to file.   
        
        # Condition for failing or passing test. If loc is empty than no match was found on the page
        if loc[0].any() and loc[1].any():
            logger.info('Template found.', also_console=True)
        else:
            self.error = True
            logger.error('Template %s was not found in the picture!' % self.template_clean)
               
    def find_matches(self, templates, screenshot, output_path, threshold=0.8):      #Matching multiple templates
        self.threshold = float(threshold)
        logger.info(str(templates), also_console=True)      # Logging path to all templates for debugging purposes.
        
        # Going through all templates and finding them on page.
        for i, template in enumerate(templates):
            self.output_path = output_path + '/output_' + str(i) + '.png'
            self.find_image(template, screenshot, self.output_path, self.threshold)
            
    def check_fail(self):
        if self.error==True:
            raise ExecutionFailed('There were errors in execution!')