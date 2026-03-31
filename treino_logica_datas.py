#Função para validação de ano, correção para 4 digitos em caso de digitação de 2, validação de período (aceito min/máx de 5 anos)
def val_year():
    current_year=datetime.now().year
    while True:
        try:
            year=int(input(f"Ano: "))
            corrected=False
            if year <100:
                year=year+2000
                corrected=True
            if year < current_year-5 or year > current_year+5:
                print(f"Período inválido.. Período permitido:5 anos")
                continue
            if corrected:
                print(f"Correção realizada para {year}")
            return year
        except ValueError:
            print(f"Informe um valor válido")

#Função para identificar ano bissexto
def leap_year(year):
    if (year%4==0 and year%100!=0) or year%400==0:
        return True
    else:
        return False

#Função para validação do mês
def val_month():
    while True:
        try:
            month=int(input(f"Mês: "))
            if month <1 or month >12:
                print(f"Mês inválido")
            else:
                return month
        except ValueError:
            print(f"Informe um valor válido!")

#Função para validação de dia, com dicionário de quantos dias tem cada mês e validação do ano bissexto
def val_day(month,year):
    days_of_month={
        1: 31,
        2: 28,
        3: 31,
        4: 30,
        5: 31,
        6: 30,
        7: 31,
        8: 31,
        9: 30,
        10: 31,
        11: 30,
        12: 31
    }
    while True:
        try:
            day=int(input(f"Dia: "))
            limit = days_of_month[month]
            if month==2 and leap_year(year):
                limit=29
            if day <1 or day >limit:
                print(f"Dia inválido. Este mês tem {limit} dias")
                continue
            return day
        except ValueError:
            print(f"Informe um valor válido!")