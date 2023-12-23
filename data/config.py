from aiogram.utils.markdown import hbold, hitalic, hcode, hunderline
from string import Template

price_list = ["35 USDT", "70 USDT", " 100USDT"]

pic = "https://img.freepik.com/premium-vector/business-candle-stick-graph-chart-of-stock-market_41981-401.jpg?size=626&ext=jpg"

dostup_text = Template(f"""ЦЕНА: {hbold('$price')}

{hitalic('После истечения выбранного периода вы будете удалены из канала.')}
{hitalic('Чтобы снова зайти необходимо будет произвести оплату повторно.')}

{hunderline('Для того чтобы вы были допущены в канал нажмите на кнопку под этим сообщением и следуйте инструкциям.')}
""")


oplata_text = f"""{hbold('Оплата:')} {hcode('TH9n968wHMRjAqHMKguMsHHKJqYmQsXjQU')}
{hbold('Сеть:')} TRC-20

{hunderline('Для того чтобы вы были допущены в канал нажмите на кнопку под этим сообщением и следуйте инструкциям.')}
{hunderline('В противном случае вы не будете допущены в канал!')}"""
