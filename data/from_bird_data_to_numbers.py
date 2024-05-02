#mcandrew

import numpy as np
import pandas as pd

from epiweeks import Week
from datetime import datetime, timedelta

if __name__ == "__main__":

    d = pd.read_csv("./HPAI Detections in Wild Birds.csv")
    d["day"] = [ datetime.strptime(x,"%m/%d/%Y").strftime("%Y-%m-%d")  for x in d["Date Detected"].values]

    from_day_to_week = {"day": d.day.unique()}
    weeks = [ Week.fromdate(datetime.strptime(day,"%Y-%m-%d")).cdcformat()  for day in from_day_to_week["day"]  ]
    from_day_to_week["week"] = weeks
    from_day_to_week = pd.DataFrame(from_day_to_week)
    
    def count(x):
        num_birds = len(x)
        num_juris = len(x.County.unique())
        return pd.Series({"num_birds": num_birds, "num_juris":num_juris})

    groups = d.groupby(["day"]).apply( count ).reset_index()
    groups = groups.merge( from_day_to_week, on = ["day"] )

    #--aggregate to epidemic week level
    def addup(x):
        return pd.Series({ "num_birds":x.num_birds.sum(), "num_juris":x.num_juris.sum()})
    week_level = groups.groupby(["week"]).apply(addup).reset_index()
    week_level["elapsed_weeks"] = np.arange(len(week_level))

    week_level.to_csv("./weekly_incdient_wild_birds_aphis.csv",index=False)
