def getHelp():
    commands = [
        {'command': '-help', 'desc': '開啟指令說明。'},
        {'command': '-dice', 'desc': '輸入 `-dice <數字>` 即可生成相應範圍內的隨機數。'},
        {'command': '-meme', 'desc': '從好色龍的網誌隨機回傳一張趣圖。'},
        {'command': '-idiom', 'desc': '隨機回傳一則成語，並附上注音、釋義及典故。'},
        {'command': '-wiki', 'desc': '隨機回傳一則維基百科條目，節錄條目中的第一段摘要。'}
    ]

    return commands