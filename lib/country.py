
# coding: utf-8

# In[2]:


import pandas as pd
import argparse


# In[ ]:


tweet_table=pd.read_csv("../output/withplace_pop.csv")
def get_country(con):
    this_country = tweet_table[tweet_table.place_country==con]
    this_country = this_country.reset_index().iloc[:,1:]
    return this_country


# In[ ]:


if __name__=='__main__':
    parser = argparse.ArgumentParser(description='get country')
    parser.add_argument('country',metavar='S',type= str, help =' desired country ')

    args = parser.parse_args()

    mytable =get_country(args.country)

    mytable.to_csv("../output/country/{}.csv".format(args.country),encoding='utf-8',index=False)
