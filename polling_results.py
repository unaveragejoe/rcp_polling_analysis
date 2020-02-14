import pandas as pd
import numpy as np

class polling_results():
    def __init__(self, rcp_url):
        self.rcp_url = rcp_url
    
        self.df = pd.read_html(self.rcp_url)[2]
        
        # Cleaning column names
        self.df.columns = [col.lower().strip() for col in self.df.columns]
        
        self.df['sample_num'] = self.df['sample'].apply(lambda x: self.convert_sample_to_int(x))
        self.df['voters_cleaned'] = self.df['sample'].apply(lambda x: x[-3:].strip().lower())
        
        self.modify_data()
            
    def convert_sample_to_int(self, row):
        try:
            return int(row[:-3].strip())
        except:
            return 0
        
    def modify_data(self):
        # Dropping the first row which is usually an average of x number of polls
        # Also creating columns to separate sample size from sample type
        self.df = self.df.drop([0], axis=0)
        
        # Creating an index column that is easily accessable later         
        self.df = self.df.reset_index()
        
        self.df['biden'] = pd.to_numeric(self.df['biden'], errors='coerce')
        self.df['sanders'] = pd.to_numeric(self.df['sanders'], errors='coerce')
        self.df['warren'] = pd.to_numeric(self.df['warren'], errors='coerce')
        self.df['buttigieg'] = pd.to_numeric(self.df['buttigieg'], errors='coerce')
                
    def filter_data(self):

        # Excludes polls with sample sizes above a lower threshold below an upper threshold
        condition_lower = self.df['sample_num'] >= self.sample_lower_thresh
        condition_upper = self.df['sample_num'] <= self.sample_upper_thresh
        self.df = self.df[condition_lower & condition_upper]
        
        # Filter polls where likely voters ('lv'), registered voters ('rv'), or all voters ('all')
        if self.voter_type == 'rv':
            self.df = self.df[self.df['voters_cleaned'] == 'rv']
        elif self.voter_type == 'lv':
            self.df = self.df[self.df['voters_cleaned'] == 'lv']
        
    def weighted_avg(self, num_polls_to_include=5, voter_type='all', polls_to_exclude=[], sample_upper_thresh=10000000, sample_lower_thresh=0):
        self.voter_type = voter_type
        self.polls_to_exclude = polls_to_exclude
        self.sample_upper_thresh = sample_upper_thresh
        self.sample_lower_thresh = sample_lower_thresh
        
        self.filter_data()

        # Filter the n most recent polls
        
        self.num_polls_to_include = num_polls_to_include
        self.df_w = self.df.copy().iloc[:self.num_polls_to_include]

        self.df_w['biden_ppl'] = (self.df_w['biden']) / 100 * self.df_w['sample_num']
        self.df_w['sanders_ppl'] = (self.df_w['sanders']) / 100 * self.df_w['sample_num']
        self.df_w['warren_ppl'] = (self.df_w['warren']) / 100 * self.df_w['sample_num']
        self.df_w['butti_ppl'] = (self.df_w['buttigieg']) / 100 * self.df_w['sample_num']
        self.df_w = self.df_w[~self.df_w['poll'].isin(self.polls_to_exclude)]

        saved_result = (self.df_w[['biden_ppl', 'sanders_ppl', 'warren_ppl', 'butti_ppl']].sum() / 
                       self.df_w['sample_num'].sum())
        
        self.df_w = self.df.copy().iloc[:self.num_polls_to_include]

        return saved_result
    
    def unweighted_avg(self, num_polls_to_include=5, voter_type='all', polls_to_exclude=[], sample_upper_thresh=10000000, sample_lower_thresh=0):
        
        self.voter_type = voter_type
        self.polls_to_exclude = polls_to_exclude
        self.sample_upper_thresh = sample_upper_thresh
        self.sample_lower_thresh = sample_lower_thresh
        
        self.filter_data()
        
        # Filter the n most recent polls
        self.num_polls_to_include = num_polls_to_include
        self.df_uw = self.df.copy().iloc[:self.num_polls_to_include]
        self.df_uw = self.df_uw[~self.df_uw['poll'].isin(self.polls_to_exclude)]
        
        saved_result = self.df_uw[['biden', 'sanders', 'warren', 'buttigieg']].mean() / 100
    
        self.df_uw = self.df.copy().iloc[:self.num_polls_to_include]

        return saved_result
