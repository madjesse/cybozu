import selenium, pyautogui, time, os.path, logging, re
from selenium import webdriver
from selenium.webdriver.common.keys import Keys

# ============================data constants==================================
FACILITY = {
"継続支援コネクトワークス大通東": "connect", 
"就労支援トライズ 大通": "tryze-odori",
"継続支援プラスタ": "plusta", 
"継続支援セコンド": "second",
"就労支援ブリッジ": "bridge",
"就労支援トライズ": "tryze-station",
"継続支援トラビズ": "trbiz"
}

CATEGORY = {
"朝礼": "morning", #date
"議事録": "meeting", #date
"雑談議事録": "submeeting", #date
"体制": "teamwork", #date
"ログ": "logging", #date
"企業見学資料": "corpvisiting", 
"支援会議": "individualplans", 
"ヤフオク": "yahoo", 
"ポスティング": "posting", 
"プチMTG": "MTG", 
"はじめての方へ": "welcome", 
"確認事項": "confirm", 
"info": "info", 
"レポート": "report", 
"連絡事項": "infosharing", 
"ヒヤリ": "happening", 
"苦情相談": "responses", 
"研修": "training", 
"事例検討": "discussions", 
"専門用語解説": "extra", 
"Office": "office", 
"プラスタこどもあーと": "plustaart", 
"カリキュラム": "curriculum", 
"読み物": "reading", 
"odori@トライズ大通": "info",
"(未分類)": "others"
}
DATE_RELEVANT = [
"morning",
"meeting",
"submeeting",
"teamwork",
"logging"
]
