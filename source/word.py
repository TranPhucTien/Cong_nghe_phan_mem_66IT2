import requests
import re
from googletrans import Translator
from bs4 import BeautifulSoup
import os

directory = "word"

if not os.path.exists(directory):
    os.mkdir(directory)

translator = Translator()

LIST_Link = [
    'https://compsciedu.com/mcq-questions/Software-Engineering/Basics',
    'https://compsciedu.com/mcq-questions/Software-Engineering/Software-Life-Cycle-Models',
    'https://compsciedu.com/mcq-questions/Software-Engineering/Software-Testing',
    'https://compsciedu.com/mcq-questions/Software-Engineering/Software-Management',
    'https://compsciedu.com/mcq-questions/Software-Engineering/Requirements-Modeling'
]

css = '''<style>
    h2, body {
        font-size: 12pt;
    }
    h1 {
        font-size: 18pt;
        text-align: center;
    }
    .eng h2 {
        color: #3c78d8;
    }
    .vie h2 {
        /* your style */
    }
</style>\n'''

fileName = 'Nhom-7-CNPM'

with open(f"{fileName}.html", "w", encoding="utf-8") as f:
        
        f.close()

for i, link in enumerate(LIST_Link):
    chapter = i + 1
    chapterTitle = link.split('/')[-1]
    beginPage = 1
    endPage = 5
    result = ''

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
            for option in listOption:
                nameOption = option.find('td').text
                ansOption = option.find_all("td")[-1].get_text()
                ansRight = option.find("td", id=re.compile("^rightoption"))
                textAnsRight = ''
                if ansRight is not None:
                    textAnsRight = ansRight.text
                else:
                    textAnsRight = ''

                if (textAnsRight == ansOption):
                    fullOption += f'<p><b>{nameOption} {ansOption}</b></p>' + '\n'
                else:
                    fullOption += f'<p>{nameOption} {ansOption}</p>' + '\n'

            question = f'<h2>{quesNum} {quesText}</h2>'

            resultEng =  question + '\n' + fullOption
            resultVie = translator.translate(resultEng, src='en', dest='vi').text
            result += f'<div class="eng">{resultEng}</div> \n <div class="vie">{resultVie}</div>\n'

    path = f"../{directory}/{fileName}.html"
    with open(path, "a", encoding="utf-8") as f:
        f.write(f"<h1>Chương {chapter}: {chapterTitle.replace('-', ' ')}</h1> \n")
        f.write(result)
        f.write('\n\n\n\n\n')
        f.close()
