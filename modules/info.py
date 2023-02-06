def getHelp():
    commands = [
        {'command': '-help', 'desc': '開啟指令說明。'},
        {'command': '-dice <整數>', 'desc': '生成相應範圍內的隨機數。'},
        {'command': '-fun', 'desc': '從好色龍的網誌隨機回傳一張趣圖。'},
        {'command': '-idiom', 'desc': '隨機回傳一則成語，並附上詳細說明。'},
        {'command': '-idiom <文字>', 'desc': '根據文字內容進行搜尋，回傳一則成語或熟語，並附上詳細說明。'},
        {'command': '-wiki', 'desc': '隨機回傳一則維基百科條目，節錄條目中的第一段摘要。'}
    ]

    return commands