#from app.flysight.jump.landing.landing import Landing
#from app.flysight.jump.exit.exit import Exit
import pandas as pd
from flysight.jump.exit.exit import Exit
from flysight.jump.landing.landing import Landing


class Jump(Landing, Exit):
    def __init__(self, name="empty", df=pd.DataFrame()):
        self.name = name
        if not df.empty:
            self.df = df
            super().__init__(self.df)

    def get_df(self):
        return self.df

    def get_name(self):
        return self.name

    def set_name(self, name):
        self.name = name

    def __str__(self):
        return f'{self.name}'
