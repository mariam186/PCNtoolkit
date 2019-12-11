#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Jul 25 17:01:24 2019

@author: seykia
"""

from __future__ import print_function
from __future__ import division

import os
import sys
import numpy as np
import pickle

try:  # run as a package if installed
    from nispat.normative_model.normbase import NormBase
    from nispat.hbr import HBR 
except ImportError:
    pass

    path = os.path.abspath(os.path.dirname(__file__))
    if path not in sys.path:
        sys.path.append(path)
    del path

    from hbr import HBR
    from norm_base import NormBase

class NormHBR(NormBase):
    """ Classical GPR-based normative modelling approach
    """

    def __init__(self, X, y=None, configparam=None):
        self.configparam = configparam
        
        with open(configparam, 'rb') as handle:
             configs = pickle.load(handle)
        
        self.type = configs['model_type']
        
        if 'batch_effects_train' in configs:
            batch_effects_train = configs['batch_effects_train']
        else:
            batch_effects_train = np.zeros([X.shape[0],2])
            
        self.configs = dict()
        
        if 'model_type' in configs:
            self.configs['type'] = configs['model_type']
        else:
            self.configs['type'] = 'linear'
        
        if 'random_intercept' in configs:
            self.configs['random_intercept'] = configs['random_intercept']
        else:
            self.configs['random_intercept'] = True
        
        if 'random_slope' in configs:
            self.configs['random_slope'] = configs['random_slope']
        else:
            self.configs['random_slope'] = True
            
        if 'random_noise' in configs:
            self.configs['random_noise'] = configs['random_noise']
        else:
            self.configs['random_noise'] = True
                
        if 'hetero_noise' in configs:
            self.configs['hetero_noise'] = configs['hetero_noise']
        else:
            self.configs['hetero_noise'] = False
        
        if y is not None:
            self.hbr = HBR(np.squeeze(X), 
                           np.squeeze(batch_effects_train[:, 0]), 
                           np.squeeze(batch_effects_train[:, 1]), 
                           np.squeeze(y), self.configs)
        
    @property
    def n_params(self):
        return 1
    
    @property
    def neg_log_lik(self):
        return -1
    
    def estimate(self, X, y=None):
        self.hbr.estimate()
        return None
        
    def predict(self, Xs, X=None, Y=None, theta=None): 
        with open(self.configparam, 'rb') as handle:
             configparam = pickle.load(handle)
             
        batch_effects_test = configparam['batch_effects_test']
        if 'prediction' in configparam:
            pred_type = configparam['prediction']
        else:
            pred_type = 'single'
            
        yhat, s2 = self.hbr.predict(np.squeeze(Xs), 
                                    np.squeeze(batch_effects_test[:, 0]), 
                                    np.squeeze(batch_effects_test[:, 1]), pred = pred_type)
        

        return yhat, s2