def colors(df):
    color="tomato"
    return [f'background-color:{color}']*len(df)
def colors2(df):
    color="yellow"
    return [f'background-color:{color}']*len(df)
def colors3(df):
    color="black"
    return [f'background-color:{color}']*len(df)
def colors4(df):
    color="brown"
    return [f'background-color:{color}']*len(df)
def colors5(df):
    color="brown"
    return [f'background-color:{color}']*len(df)
def dcolor(df):
    return [f'background-color:green']*len(df) if df.status else [f'background-color:red']*len(df)
