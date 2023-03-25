from api.app.utils.jump.exit.exit import Exit
from api.app.utils.jump.landing.landing import Landing


class Jump(Landing, Exit):
    def __init__(self, df):
        self.df = df
        super().__init__(self.df)

    def get_df(self):
        return self.df

    def __str__(self):
        return f'{self.df}'

