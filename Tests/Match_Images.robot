*** Settings ***
Library    ../Libraries/Matching.py
Library    SeleniumLibrary
Library    OperatingSystem    
Test Teardown    Close Browser
Test Setup   Open Browser    https://demo.mahara.org/    chrome  



*** Test Cases ***
Match
    ${screenshot}=    Normalize Path    ${CURDIR}/../Outputs/Mahara.png  
    ${output}=    Normalize Path    ${CURDIR}/../Outputs/ 
    ${images}=    Normalize Path    ${CURDIR}/../Resources/Image_Matching/  
    @{templates}=    Set Variable   ${images}/image1.png    ${images}/image2.png    ${images}/image3.png   
    Capture Page Screenshot    ${screenshot}    
    Find Matches    ${templates}    ${screenshot}    ${output}    0.8    
    Check Fail 
