import cv2
import numpy as np
from robot.api import logger
from robot.errors import ExecutionFailed
import os

class Matching(object):

    ROBOT_LIBRARY_VERSION = 1.0

    def find_image(self, template, screenshot, output_path, threshold=0.8):
        self.template_clean = template
        logger.info('Template: ' + template, also_console=True)
        logger.info('Output path: ' + output_path, also_console=True)
        logger.info('Screenshot path: ' + screenshot, also_console=True)
        self.threshold = float(threshold)
        img_rgb = cv2.imread(screenshot)
        img_gray = cv2.cvtColor(img_rgb, cv2.COLOR_BGR2GRAY)
        template = cv2.imread(template, 0)
        w, h = template.shape[::-1]
        res = cv2.matchTemplate(img_gray,template,cv2.TM_CCOEFF_NORMED)
        
        loc = np.where(res >= self.threshold)

        for pt in zip(*loc[::-1]):
            cv2.rectangle(img_rgb, pt, (pt[0] + w, pt[1] + h), (0,0,255), 2)
        
        cv2.imwrite(output_path,img_rgb)
        
        if loc[0] and loc[1]:
            logger.info('Template found.', also_console=True)
        else:
            logger.error('Template %s was not found in the picture!' % self.template_clean)
            raise ExecutionFailed('Template not found')
        
    def find_matches(self, templates, screenshot, output_path, threshold=0.8):
        self.threshold = float(threshold)
        logger.info(str(templates), also_console=True)
        for i, template in enumerate(templates):
            self.output_path = output_path + '/output_' + str(i) + '.png'
            self.find_image(template, screenshot, self.output_path, self.threshold)
