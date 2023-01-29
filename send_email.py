def send_mail(df, date, TO, name):
    FROM = '770787047@qq.com'
    my_key = '' # 在qq 邮箱里设置
    ret = True
    try:
        header = """<head>
        <meta charset="utf-8">
        <style>
        .customers
        {
            font-family:"Trebuchet MS", Arial, Helvetica, sans-serif;
            width:100%;
            border-collapse:collapse;
        }
        .customers td, .customers th
        {
            font-size:1em;
            border:1px solid #98bf21;
            padding:3px 7px 2px 7px;
        }
        .customers th
        {
            font-size:1.1em;
            text-align:left;
            padding-top:5px;
            padding-bottom:4px;
            background-color:#A7C942;
            color:#ffffff;
        }
        .customers tr.alt td
        {
            color:#000000;
            background-color:#EAF2D3;
        }
        </style>
        </head>"""

        body = '<html>' + header + '<body>' \
               + '<pr/>' \
               + df.to_html().replace('<table border="1" class="dataframe">',
                                            "<table class='customers'>").replace("<tr>", "<tr class='alt'>") \
               + '<br/>' \
               + '</body></html>'

        outer = MIMEMultipart()
        outer['From'] = formataddr(["陈浩", FROM])
        outer['To'] = formataddr([name, TO])
        outer['Subject'] = "%s 策略1 top 50股票池如下" % (date)

        inner = MIMEMultipart('alternative')
        part1 = MIMEText(body, 'html')
        inner.attach(part1)
        outer.attach(inner)

        server = smtplib.SMTP_SSL("smtp.qq.com", 465)
        server.login(FROM, my_key)
        server.sendmail(FROM, [TO, ], outer.as_string())
        server.quit()
    except Exception:
        ret = False
    return ret

pred_date = sorted(list(pd.read_csv('processed_data.csv')['Date'].unique()))[-1]
df = pd.read_csv('result/' + pred_date + '.csv')
TO = "770787047@qq.com"
name = "chenhao"
