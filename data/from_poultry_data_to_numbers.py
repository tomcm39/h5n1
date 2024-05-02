#mcandrew

import numpy as np
import pandas as pd

from epiweeks import Week
from datetime import datetime, timedelta

if __name__ == "__main__":

    d = pd.read_csv("./A Table by Confirmation Date.csv",sep="\t",encoding="utf-16")
    d = d.replace(np.nan,0)

    control_area_cols = [x for x in d.columns if "Control Area" in x]
    d = d.replace(',','', regex=True)

    d = d.iloc[1:]

    for col in control_area_cols:
        d[col] = d[col].astype(float)
    
    d["birds_affected"] = d.loc[:,control_area_cols].sum(1)
    d["date"]           = [ datetime.strptime(x,"%d-%b-%y").strftime("%Y-%m-%d") for x in d.iloc[:,0]]

    d = d[ ["date","birds_affected"] ]

    from_day_to_week = {"date": d.date.unique()}
    weeks = [ Week.fromdate(datetime.strptime(date,"%Y-%m-%d")).cdcformat()  for date in from_day_to_week["date"]  ]
    from_day_to_week["week"] = weeks
    from_day_to_week         = pd.DataFrame(from_day_to_week)

    d = d.merge( from_day_to_week, on = ["date"] )
 
    #--aggregate to epidemic week level
    def addup(x):
        return pd.Series({ "birds_affected": x.birds_affected.sum() })
    week_level = d.groupby(["week"]).apply(addup).reset_index()
    week_level["elapsed_weeks"] = np.arange(len(week_level))

    week_level.to_csv("./weekly_incident_poultry_aphis.csv",index=False)
    week_level.to_csv("./arxiv/weekly_incident_poultry_aphis__{:s}.csv".format(datetime.today().strftime("%Y-%m-%d")),index=False)
