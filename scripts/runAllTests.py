import sys
import os
import importlib
from TeamIsntThisFun.drivers.driverDefault import driverDefaultFunc

# Full script plan:
#   Read file (populate array) -> Parse file -> Sent to driver, calls functions from parse
#   -> Output to report function -> Html

def main():
    readFiles()

def readFiles():
    """Reads in the lines from the test case specification file, passes them to parse, passes parsed list to driver specified
    by the test case specification file, and then calls the report function to handle building and displaying the results of
    the test in an HTML page."""
    rootDir = '../testCases/'
    testCaseLines = 8

    ## readFiles() will build the String contents2 with test case data to be later displayed on an HTML page
    contents2 = '''<table border="1" style="width:100%"> 
            <tr> 
            <td>Test #</td>
                <td>Req. Tested</td>
                <td>Component Tested</td> 
                <td>Method Tested</td>
                <td>Test Inputs</td>
                <td>Expected Outcome</td>
                <td>Actual Outcome</td>
                <td width="10%">Outcome</td>
            </tr>'''
    
    for filename in sorted(os.listdir(rootDir)):
        infoLines = [0] * testCaseLines
        N = testCaseLines
        f = open("../testCases/" + filename)
        for i in range(N):
            line = f.next().strip()
            infoLines[i] = line
            # print line
        infoList = parseFiles(infoLines)
        output = driverDefaultFunc(infoList)
        try:
            output = str(output)
        except:
            pass
        contents2 = report(infoList, contents2, output)
        f.close()
        
    ## Predefined header for HTML report
    contents1 = '''<!DOCTYPE html PUBLIC "-//W3C//DTD HTML 4.01 Transitional//EN">
                    <html>
                    <head>
                      <meta content="text/html; charset=ISO-8859-1"http-equiv="content-type">
                      <title>Isn't This Fun?</title>
                    </head>
                    <body>
                        <h1>Beets Automated Test Suite</h1></br></br>'''

    ## Predefined footer for HTML report
    contents3 = '''</table></body></html>'''
        
    ## Build HTML page and generate it in a browser window
    browseLocal(contents1 + contents2 + contents3)

def parseFiles(inLineArray):
    """Parse the list of lines from the test case specification file to put these lines in the correct format."""
    # 1. test number or ID
    # 2. requirement being tested
    # 3. component being tested
    # 4. method being tested
    # 5. test input(s) including command-line argument(s)
    # 6. expected outcome(s)
    # 7. driver name
    # 8. input type

    paren = '('
    comm = '#'
    quote = '"'
    defaultDriver = "driverDefault"
    inputList = []


    componentName = inLineArray[2]

    head, mid, tail = inLineArray[3].partition(paren)
    funcName = head

    inputType = inLineArray[7]

    if '#' in inLineArray[4]:
        head, mid, tail = inLineArray[4].partition(comm)
    else:
        head = inLineArray[4]

    splitInputs = head.split(',')
    for i in range(len(splitInputs)):
        if (inputType == "string"):
            try:
                inputList.append(head.strip())
            except:
                inputList.append(inLineArray[4])
        elif (inputType == "int"):
            try:
                inputList.append(int(head.strip()))
            except:
                inputList.append(inLineArray[4])
        elif (inputType == "float"):
            try:
                inputList.append(float(head.strip()))
            except:
                inputList.append(inLineArray[4])
        else:
            inputList.append(inLineArray[4])

    if '#' in inLineArray[5]:
        head, mid, tail = inLineArray[5].partition(comm)
    else:
        head = inLineArray[5]
    
    try:
        expectedVal = head.replace(quote, "")
        expectedVal = expectedVal.strip()
    except:
        print(head)
        expectedVal = ["Test"]

    try:
        driverName = inLineArray[6]
    except:
        driverName = defaultDriver


    returnVal = [inLineArray[0], inLineArray[1], componentName, funcName, inputList, expectedVal, driverName]
    return returnVal


def compare(oracle, actualOutput):
    """Test whether the expected value from the test case specification file equals the actual output from the function."""
    if oracle == actualOutput:
        return '''<font color='green'>Pass</font>'''
    else:
        return '''<font color='red'>Fail</font>'''
    
         
    
def strToFile(text, filename):
    """Write a file with the given name and the given text."""
    output = open(filename, "w")
    output.write(text)
    output.close()
    
def browseLocal(webpageText, filename='tempBrowseLocal.html'):
    '''Start your webbrowser on a local file containing the text
    with given filename.'''
    import webbrowser, os.path
    strToFile(webpageText, filename)
    webbrowser.open("file:///" + os.path.abspath(filename))  # elaborated for Mac
    
def report(returnVal, contents2, outputVal):
    """ Write results of test to HTML file """
    
    contents2 = contents2 + '''<tr> 
                    <td>''' + str(returnVal[0]) + '''</td>
                    <td>''' + str(returnVal[1]) + '''</td>
                    <td>''' + str(returnVal[2]) + '''</td> 
                    <td>''' + str(returnVal[3]) + '''</td>
                    <td>''' + str(returnVal[4]) + '''</td>
                    <td>''' + str(returnVal[5]) + '''</td>
                    <td>''' + str(outputVal) + '''</td>
                    <td>''' + str(compare(returnVal[5], outputVal)) + '''</td>
                </tr>'''
    return contents2

if __name__ == "__main__":
    """Call main if the module is run and not if imported."""
    main()