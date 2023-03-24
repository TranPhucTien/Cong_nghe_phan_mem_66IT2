import requests
import re
from googletrans import Translator
from bs4 import BeautifulSoup

translator = Translator()

LIST_Link = [
    'https://compsciedu.com/mcq-questions/Software-Engineering/Basics',
    'https://compsciedu.com/mcq-questions/Software-Engineering/Software-Life-Cycle-Models',
    'https://compsciedu.com/mcq-questions/Software-Engineering/Software-Testing',
    'https://compsciedu.com/mcq-questions/Software-Engineering/Software-Management',
    'https://compsciedu.com/mcq-questions/Software-Engineering/Requirements-Modeling'
]

styles = '''<style>
    h1 {
        user-select: none;
    }
</style>
'''

for i, link in enumerate(LIST_Link):
    chapter = i + 1
    chapterTitle = link.split('/')[-1]
    beginPage = 1
    endPage = 5
    timeLimit = 30
    result = '''<table>
    <tr>
        <td>Question Text</td>
        <td>Question Type</td>
        <td>Option 1</td>
        <td>Option 2</td>
        <td>Option 3</td>
        <td>Option 4</td>
        <td>Option 5</td>
        <td>Correct Answer</td>
        <td>Time in seconds</td>
        <td>Image Link</td>
    </tr>
    <tr>
        <td>Text of the question (required)</td>
        <td>Multiple Choice</td>
        <td>Text for option 1 (required)</td>
        <td>Text for option 2 (required)</td>
        <td>Text for option 3 (optional)</td>
        <td>Text for option 4 (optional)</td>
        <td>Text for option 5 (optional)</td>
        <td>Integer (1-5 for the correct option)</td>
        <td>Time in seconds (optional, default value is 30)</td>
        <td>Link of the image (optional)</td>
    </tr>
    '''

    print(chapterTitle)

    for x in range(beginPage, endPage + 1):
        print(f'------------------------------ {x}/{endPage} --------------------------')
        url = f"{link}/{x}"
        response = requests.get(url)

        soup = BeautifulSoup(response.content, "html.parser")

        tableList = soup.find_all('div', attrs={'class': 'quescontainer'})

        for table in tableList:
            tableQue = table.find('table', attrs={'class': 'table-striped'})
            quesNum = tableQue.find('span').text
            quesText = tableQue.find('span', attrs={'class': 'questionpre'}).text
            listOption = tableQue.find_all('tr', attrs={'style': 'vertical-align:bottom;line-height:40px;overflow:hidden;'})
            
            fullOption = ''
            row = ''
            ansNum = 0
            for index, option in enumerate(listOption):
                ans = option.find_all("td")[-1].get_text()
                ansRight = option.find("td", id=re.compile("^rightoption"))
                textAnsRight = ''

                if ansRight is not None:
                    textAnsRight = ansRight.text
                else:
                    textAnsRight = ''

                row += f'<td>{ans}</td>'

                if (textAnsRight == ans):
                    ansNum = index + 1

            row += '<td></td>'
            row += f'<td>{ansNum}</td>'
            row += f'<td>{timeLimit}</td>'

            question = f'<td>{quesNum} {quesText}</td>'
            resultEng = f'<tr>{question}\n<td>Multiple Choice</td>\n{row}\n</tr>'
            result += resultEng
    
    result += '</table>'

    with open(f"./quizizz/{chapter}.{chapterTitle}.html", "w", encoding="utf-8") as f:
        f.write(f"{styles}<h1>Chương {chapter}: {chapterTitle.replace('-', ' ')}</h1> \n")
        f.write(result)
        f.write('\n\n\n\n\n')
        f.close()
