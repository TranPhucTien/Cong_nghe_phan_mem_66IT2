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
        <td>Question - max 120 characters</td>
        <td>Answer 1 - max 75 characters</td>
        <td>Answer 2 - max 75 characters</td>
        <td>Answer 3 - max 75 characters</td>
        <td>Answer 4 - max 75 characters</td>
        <td>Time limit (sec) – 5, 10, 20, 30, 60, 90, 120, or 240 secs</td>
        <td>Correct answer(s) - choose at least one</td>
    </tr>\n'''

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

                row += f'<td>{ans[:70]}</td>'

                if (textAnsRight == ans):
                    ansNum = index + 1

            row += f'<td>{timeLimit}</td>'
            row += f'<td>{ansNum}</td>'

            question = f'<td>{quesNum} {quesText[:115]}</td>'
            resultEng = f'<tr>{question} {row}</tr>'
            # resultVie = translator.translate(resultEng, src='en', dest='vi').text
            result += resultEng
    
    result += '</table>'

    with open(f"kahoot1/{chapter}.{chapterTitle}.html", "w", encoding="utf-8") as f:
        f.write(styles)
        f.write(f"<h1>Chương {chapter}: {chapterTitle.replace('-', ' ')}</h1> \n")
        f.write(result)
        f.write('\n\n\n\n\n')
        f.close()
