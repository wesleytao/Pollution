
# coding: utf-8

# In[1]:


import pickle
import pandas as pd
from tqdm import tqdm_notebook,tqdm
import datetime
import re
import argparse


# In[ ]:


pollution = ["air #pollution", "空气污染", "#airpollution", "वायु प्रदुषण", "la pollution de l'air", "la #pollution",
            "air #pollution", "l'air #pollution", "वायु प्रदुषण",'air quality','smog','embouteillage',"#वायु प्रदुषण","वायु #प्रदूषण"]
climate_change=['changement climatique','#changementclimatique']

forest_file = ["forest fire", "forest fires"]
water_flood = ["water poisoning", "water contamination","flood flash", 'flood water', "flood warning"]
earthquake  = ["earthquake"]
oil_spill =     ["oil spill", "pipeline spill", "tarsands spill", "tankers spill", "fossilfuel spill", "petroleum spill"]
toxic_mildew = ["acid rain", "toxic rain", "mildew home", "mildew infested", "mildew basement", "mildew removal",
                "mildew growth", "mildew inspection", "mold flood", "mildew flood"]
bug = ["adelgid", "aphid", "beetle", "earwig", "insect", "locust", "louse", "moth", "psyllid", "termites",
              "termite bites", "bug bites", "bugs bites","bed bugs","bug","bugs"]
allergy  = """allergy
allergins
pollen
dander
allergy + cough
allergies + cough
pollen + cough
dander + cough
dust + cough
allergy + sneeze
allergies + sneeze
pollen + sneeze
dander + sneeze
dust + sneeze
allergy + asthma
allergies + asthma
pollen + asthma
dander + asthma
dust + asthma
allergy + respiratory
allergies + respiratory
pollen + respiratory
dander + respiratory
dust + respiratory
allergy + lung
allergies + lung
pollen + lung
dander + lung
dust + lung""".split("\n")
allergy = [word.replace("+", "") for word in allergy]
allergy = [word.replace("  ", " ") for word in allergy]
dust = ["dust"]
pollution_re          = re.compile(r'('+'|'.join(pollution)+')',  re.IGNORECASE)
climate_change_re  = re.compile(r'('+'|'.join(climate_change)+')',  re.IGNORECASE)
forest_file_re     = re.compile(r'('+'|'.join(forest_file)+')',  re.IGNORECASE)
water_flood_re     = re.compile(r'('+'|'.join(water_flood)+')',  re.IGNORECASE)
earthquake_re      = re.compile(r'('+'|'.join(earthquake )+')',  re.IGNORECASE)
oil_spill_re       = re.compile(r'('+'|'.join(oil_spill)+')',  re.IGNORECASE)
bug_re             = re.compile(r'('+'|'.join(bug)+')',  re.IGNORECASE)
allergy_re         = re.compile(r'('+'|'.join(allergy)+')',  re.IGNORECASE)
dust_re            = re.compile(r'('+'|'.join(dust)+')',  re.IGNORECASE)
toxic_mildew_re    = re.compile(r'('+'|'.join(toxic_mildew)+')',  re.IGNORECASE)


# In[ ]:


def get_full_text(tweet):
    try:
        return(tweet["extended_tweet"]["full_text"])
    except:
        return(tweet["text"])


# In[ ]:


def get_unified(df):
    value_column=['followers_count','statuses_count','listed_count','favourites_count','pollution', 'climate_change', 'forest_file', 'water_flood',
       'earthquake', 'oil_spill', 'bug', 'allergy', 'dust', 'toxic_mildew']
    other_column=set(userprofile.columns) - set(value_column)
    # for non value column we only select one
    part_a = df.loc[df.id.drop_duplicates().index]  # index
    part_a.drop(columns=value_column,inplace=True)
    # for value column we select the max
    part_b=df.groupby(['id'])[value_column].max()
    part_b.reset_index(inplace=True)
    # combine both part
    assert(part_a.shape[0]==part_b.shape[0])
    mydf=part_a.merge(part_b,on=['id'])
    return mydf


# In[ ]:


if __name__== "__main__":
    parser = argparse.ArgumentParser(description='get user profile')
    parser.add_argument('path',metavar='I',type= str, help ='input json path output/**.p ')
    parser.add_argument('savename',metavar='S',type=str,help='saved name for file')
    args = parser.parse_args()
    print("loading file...")
    with open(args.path,mode='br') as f:
        placejson=pickle.load(f,encoding='utf-8')
    print("file loaded")
    userattribute = [attribute for attribute in set(placejson[0]['user'])]

    userprofile=pd.DataFrame()
    for attribute in tqdm(userattribute):
        userprofile[attribute] = list(map(lambda thistweet: thistweet['user'][attribute] if attribute in thistweet['user'].keys() else None,placejson))

    userprofile['text']=list(map(lambda tweet: get_full_text(tweet), placejson))


    print("going to get tweet feature for each user")
    with tqdm(total =100) as pbar:
        userprofile['pollution'] = list(map(lambda tweet: True if pollution_re.search(tweet) else False,userprofile.text))
        pbar.update(10)
        userprofile['climate_change'] = list(map(lambda tweet: True if climate_change_re.search(tweet) else False,userprofile.text))
        pbar.update(10)
        userprofile['forest_file'] = list(map(lambda tweet: True if forest_file_re.search(tweet) else False,userprofile.text))
        pbar.update(10)
        userprofile['water_flood'] = list(map(lambda tweet: True if water_flood_re.search(tweet) else False,userprofile.text))
        pbar.update(10)
        userprofile['earthquake'] = list(map(lambda tweet: True if earthquake_re.search(tweet) else False,userprofile.text))
        pbar.update(10)
        userprofile['oil_spill'] = list(map(lambda tweet: True if oil_spill_re.search(tweet) else False,userprofile.text))
        pbar.update(10)
        userprofile['bug'] = list(map(lambda tweet: True if bug_re.search(tweet) else False,userprofile.text))
        pbar.update(10)
        userprofile['allergy'] = list(map(lambda tweet: True if allergy_re.search(tweet) else False,userprofile.text))
        pbar.update(10)
        userprofile['dust'] = list(map(lambda tweet: True if dust_re.search(tweet) else False,userprofile.text))
        pbar.update(10)
        userprofile['toxic_mildew'] = list(map(lambda tweet: True if toxic_mildew_re.search(tweet) else False,userprofile.text))
        pbar.update(10)


    userprofile.drop(columns=['id_str'],inplace=True)
    userprofile.drop_duplicates(inplace=True)
    datetime.datetime.strptime('Tue May 05 15:58:46 +0000 2009','%a %b %d %H:%M:%S %z %Y')
    userprofile['created_at']=list(map(lambda time: datetime.datetime.strptime(time,'%a %b %d %H:%M:%S %z %Y'),userprofile.created_at))

    userprofile_clean=get_unified(userprofile)
    userprofile_clean.to_csv("../output/{}.csv".format(args.savename),index=False)


# In[78]:
