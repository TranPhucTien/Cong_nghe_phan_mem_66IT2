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

css = '''<style>
    h2, body {
        font-size: 12pt;
    }
    h1 {
        font-size: 18pt;
    }
    .eng {
        /* your style */
    }
    .vie {
        /* your style */
    }
</style>\n'''

fileName = '0973108200-MBbank-TranPhucTien'

with open(f"{fileName}.html", "w", encoding="utf-8") as f:
        f.write(css)
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
                name = option.find('td').text
                ans = option.find_all("td")[-1].get_text()
                ansRight = option.find("td", id=re.compile("^rightoption"))
                textAnsRight = ''
                if ansRight is not None:
                    textAnsRight = ansRight.text
                else:
                    textAnsRight = ''

                if (textAnsRight == ans):
                    fullOption += f'<p><b>{name} {ans}</b></p>' + '\n'
                else:
                    fullOption += f'<p>{name} {ans}</p>' + '\n'

            question = f'<h2>{quesNum} {quesText}</h2>'

            resultEng = '<div class="eng">' + question + '\n' + fullOption + '</div>'
            resultVie = '<div class="vie">' + translator.translate(resultEng, src='en', dest='vi').text + '</div>'
            result += resultEng + '\n' + resultVie

    with open(f"{fileName}.html", "a", encoding="utf-8") as f:
        f.write(f"<h1>Chương {chapter}: {chapterTitle.replace('-', ' ')}</h1> \n")
        f.close()

    with open(f"{fileName}.html", "a", encoding="utf-8") as f:
        f.write(result)
        f.write('\n\n\n\n\n')
        f.close()
