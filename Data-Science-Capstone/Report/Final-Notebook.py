{
 "metadata": {
  "language_info": {
   "codemirror_mode": {
    "name": "ipython",
    "version": 3
   },
   "file_extension": ".py",
   "mimetype": "text/x-python",
   "name": "python",
   "nbconvert_exporter": "python",
   "pygments_lexer": "ipython3",
   "version": "3.7.1-final"
  },
  "orig_nbformat": 2,
  "kernelspec": {
   "name": "Python 3.7.1 64-bit ('base': conda)",
   "display_name": "Python 3.7.1 64-bit ('base': conda)",
   "metadata": {
    "interpreter": {
     "hash": "540b8b5107148be1bb809aadf5ddc82ec8ca277383f3dc745d8ed3d4f9450841"
    }
   }
  }
 },
 "nbformat": 4,
 "nbformat_minor": 2,
 "cells": [
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": [
    "## Data For Report\n",
    "The data that we have chosen to zero in on are going to be those that would directly impact the severity of a collision. The lat/long of a collision has no correlation to the severity of the accident, so, for the purposes of our analysis, we can drop it as part of the model. As a part of the preparation, we need to sift through the data in order to see what aspects are truly relevant.  \n",
    "\n",
    "We will create a correlation matrix using all of the data that we have, to see if there is a baseline of correlation from one variable to the next. The goal will be to first identify which items have high correlation to severity. Then, the next aspect is to see if there is redundant data. We don't need two independent variables that are highly correlated to both be part of the calculation for severity, since it will bias the model.  \n",
    "\n",
    "I already notice that with my data description, I am focusing too much on the cleaning aspect. Invariably, the cleaning is directly tied to the understanding of the data therein, so I will continue to conduct any and all cleaning in this file, and will draw conclusions about which data I will retain and which data I will drop. The information will be contained on the top of this document, here, and will be contained below, at the end of the cleaning process. The final step will include outputting the cleaned data as a csv for further use in a different file.  \n",
    "\n",
    "I will note my logic for dropping columns if I feel I need further justification. Given that 'SEVERITYDESC' has 100% correlation to 'SEVERITYCODE', I will drop this column, since it is a perfect, and hindsight based predictor of severity, and removes any predictability power from the model entirely."
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 4,
   "metadata": {},
   "outputs": [],
   "source": [
    "import pandas as pd\n",
    "import numpy as np\n",
    "\n",
    "collision_data = pd.read_csv(\"Data-Collisions.csv\")"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 5,
   "metadata": {},
   "outputs": [
    {
     "output_type": "execute_result",
     "data": {
      "text/plain": [
       "        SEVERITYCODE              X              Y       OBJECTID  \\\n",
       "count  194673.000000  189339.000000  189339.000000  194673.000000   \n",
       "mean        1.298901    -122.330518      47.619543  108479.364930   \n",
       "std         0.457778       0.029976       0.056157   62649.722558   \n",
       "min         1.000000    -122.419091      47.495573       1.000000   \n",
       "25%         1.000000    -122.348673      47.575956   54267.000000   \n",
       "50%         1.000000    -122.330224      47.615369  106912.000000   \n",
       "75%         2.000000    -122.311937      47.663664  162272.000000   \n",
       "max         2.000000    -122.238949      47.734142  219547.000000   \n",
       "\n",
       "              INCKEY      COLDETKEY         INTKEY  SEVERITYCODE.1  \\\n",
       "count  194673.000000  194673.000000   65070.000000   194673.000000   \n",
       "mean   141091.456350  141298.811381   37558.450576        1.298901   \n",
       "std     86634.402737   86986.542110   51745.990273        0.457778   \n",
       "min      1001.000000    1001.000000   23807.000000        1.000000   \n",
       "25%     70383.000000   70383.000000   28667.000000        1.000000   \n",
       "50%    123363.000000  123363.000000   29973.000000        1.000000   \n",
       "75%    203319.000000  203459.000000   33973.000000        2.000000   \n",
       "max    331454.000000  332954.000000  757580.000000        2.000000   \n",
       "\n",
       "         PERSONCOUNT       PEDCOUNT    PEDCYLCOUNT       VEHCOUNT  \\\n",
       "count  194673.000000  194673.000000  194673.000000  194673.000000   \n",
       "mean        2.444427       0.037139       0.028391       1.920780   \n",
       "std         1.345929       0.198150       0.167413       0.631047   \n",
       "min         0.000000       0.000000       0.000000       0.000000   \n",
       "25%         2.000000       0.000000       0.000000       2.000000   \n",
       "50%         2.000000       0.000000       0.000000       2.000000   \n",
       "75%         3.000000       0.000000       0.000000       2.000000   \n",
       "max        81.000000       6.000000       2.000000      12.000000   \n",
       "\n",
       "        SDOT_COLCODE    SDOTCOLNUM     SEGLANEKEY  CROSSWALKKEY  \n",
       "count  194673.000000  1.149360e+05  194673.000000  1.946730e+05  \n",
       "mean       13.867768  7.972521e+06     269.401114  9.782452e+03  \n",
       "std         6.868755  2.553533e+06    3315.776055  7.226926e+04  \n",
       "min         0.000000  1.007024e+06       0.000000  0.000000e+00  \n",
       "25%        11.000000  6.040015e+06       0.000000  0.000000e+00  \n",
       "50%        13.000000  8.023022e+06       0.000000  0.000000e+00  \n",
       "75%        14.000000  1.015501e+07       0.000000  0.000000e+00  \n",
       "max        69.000000  1.307202e+07  525241.000000  5.239700e+06  "
      ],
      "text/html": "<div>\n<style scoped>\n    .dataframe tbody tr th:only-of-type {\n        vertical-align: middle;\n    }\n\n    .dataframe tbody tr th {\n        vertical-align: top;\n    }\n\n    .dataframe thead th {\n        text-align: right;\n    }\n</style>\n<table border=\"1\" class=\"dataframe\">\n  <thead>\n    <tr style=\"text-align: right;\">\n      <th></th>\n      <th>SEVERITYCODE</th>\n      <th>X</th>\n      <th>Y</th>\n      <th>OBJECTID</th>\n      <th>INCKEY</th>\n      <th>COLDETKEY</th>\n      <th>INTKEY</th>\n      <th>SEVERITYCODE.1</th>\n      <th>PERSONCOUNT</th>\n      <th>PEDCOUNT</th>\n      <th>PEDCYLCOUNT</th>\n      <th>VEHCOUNT</th>\n      <th>SDOT_COLCODE</th>\n      <th>SDOTCOLNUM</th>\n      <th>SEGLANEKEY</th>\n      <th>CROSSWALKKEY</th>\n    </tr>\n  </thead>\n  <tbody>\n    <tr>\n      <td>count</td>\n      <td>194673.000000</td>\n      <td>189339.000000</td>\n      <td>189339.000000</td>\n      <td>194673.000000</td>\n      <td>194673.000000</td>\n      <td>194673.000000</td>\n      <td>65070.000000</td>\n      <td>194673.000000</td>\n      <td>194673.000000</td>\n      <td>194673.000000</td>\n      <td>194673.000000</td>\n      <td>194673.000000</td>\n      <td>194673.000000</td>\n      <td>1.149360e+05</td>\n      <td>194673.000000</td>\n      <td>1.946730e+05</td>\n    </tr>\n    <tr>\n      <td>mean</td>\n      <td>1.298901</td>\n      <td>-122.330518</td>\n      <td>47.619543</td>\n      <td>108479.364930</td>\n      <td>141091.456350</td>\n      <td>141298.811381</td>\n      <td>37558.450576</td>\n      <td>1.298901</td>\n      <td>2.444427</td>\n      <td>0.037139</td>\n      <td>0.028391</td>\n      <td>1.920780</td>\n      <td>13.867768</td>\n      <td>7.972521e+06</td>\n      <td>269.401114</td>\n      <td>9.782452e+03</td>\n    </tr>\n    <tr>\n      <td>std</td>\n      <td>0.457778</td>\n      <td>0.029976</td>\n      <td>0.056157</td>\n      <td>62649.722558</td>\n      <td>86634.402737</td>\n      <td>86986.542110</td>\n      <td>51745.990273</td>\n      <td>0.457778</td>\n      <td>1.345929</td>\n      <td>0.198150</td>\n      <td>0.167413</td>\n      <td>0.631047</td>\n      <td>6.868755</td>\n      <td>2.553533e+06</td>\n      <td>3315.776055</td>\n      <td>7.226926e+04</td>\n    </tr>\n    <tr>\n      <td>min</td>\n      <td>1.000000</td>\n      <td>-122.419091</td>\n      <td>47.495573</td>\n      <td>1.000000</td>\n      <td>1001.000000</td>\n      <td>1001.000000</td>\n      <td>23807.000000</td>\n      <td>1.000000</td>\n      <td>0.000000</td>\n      <td>0.000000</td>\n      <td>0.000000</td>\n      <td>0.000000</td>\n      <td>0.000000</td>\n      <td>1.007024e+06</td>\n      <td>0.000000</td>\n      <td>0.000000e+00</td>\n    </tr>\n    <tr>\n      <td>25%</td>\n      <td>1.000000</td>\n      <td>-122.348673</td>\n      <td>47.575956</td>\n      <td>54267.000000</td>\n      <td>70383.000000</td>\n      <td>70383.000000</td>\n      <td>28667.000000</td>\n      <td>1.000000</td>\n      <td>2.000000</td>\n      <td>0.000000</td>\n      <td>0.000000</td>\n      <td>2.000000</td>\n      <td>11.000000</td>\n      <td>6.040015e+06</td>\n      <td>0.000000</td>\n      <td>0.000000e+00</td>\n    </tr>\n    <tr>\n      <td>50%</td>\n      <td>1.000000</td>\n      <td>-122.330224</td>\n      <td>47.615369</td>\n      <td>106912.000000</td>\n      <td>123363.000000</td>\n      <td>123363.000000</td>\n      <td>29973.000000</td>\n      <td>1.000000</td>\n      <td>2.000000</td>\n      <td>0.000000</td>\n      <td>0.000000</td>\n      <td>2.000000</td>\n      <td>13.000000</td>\n      <td>8.023022e+06</td>\n      <td>0.000000</td>\n      <td>0.000000e+00</td>\n    </tr>\n    <tr>\n      <td>75%</td>\n      <td>2.000000</td>\n      <td>-122.311937</td>\n      <td>47.663664</td>\n      <td>162272.000000</td>\n      <td>203319.000000</td>\n      <td>203459.000000</td>\n      <td>33973.000000</td>\n      <td>2.000000</td>\n      <td>3.000000</td>\n      <td>0.000000</td>\n      <td>0.000000</td>\n      <td>2.000000</td>\n      <td>14.000000</td>\n      <td>1.015501e+07</td>\n      <td>0.000000</td>\n      <td>0.000000e+00</td>\n    </tr>\n    <tr>\n      <td>max</td>\n      <td>2.000000</td>\n      <td>-122.238949</td>\n      <td>47.734142</td>\n      <td>219547.000000</td>\n      <td>331454.000000</td>\n      <td>332954.000000</td>\n      <td>757580.000000</td>\n      <td>2.000000</td>\n      <td>81.000000</td>\n      <td>6.000000</td>\n      <td>2.000000</td>\n      <td>12.000000</td>\n      <td>69.000000</td>\n      <td>1.307202e+07</td>\n      <td>525241.000000</td>\n      <td>5.239700e+06</td>\n    </tr>\n  </tbody>\n</table>\n</div>"
     },
     "metadata": {},
     "execution_count": 5
    }
   ],
   "source": [
    "collision_data.describe()"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 6,
   "metadata": {},
   "outputs": [
    {
     "output_type": "execute_result",
     "data": {
      "text/plain": [
       "(194673, 38)"
      ]
     },
     "metadata": {},
     "execution_count": 6
    }
   ],
   "source": [
    "collision_data.shape"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 7,
   "metadata": {},
   "outputs": [],
   "source": [
    "collision_data.drop(collision_data[collision_data.EXCEPTRSNCODE == 'NEI'].index, inplace=True)\n",
    "collision_data.drop(columns=['EXCEPTRSNCODE', 'EXCEPTRSNDESC'], inplace=True)"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 8,
   "metadata": {},
   "outputs": [
    {
     "output_type": "execute_result",
     "data": {
      "text/plain": [
       "                          SEVERITYDESC  SEVERITYCODE\n",
       "0                     Injury Collision             2\n",
       "1       Property Damage Only Collision             1\n",
       "2       Property Damage Only Collision             1\n",
       "3       Property Damage Only Collision             1\n",
       "4                     Injury Collision             2\n",
       "...                                ...           ...\n",
       "194668                Injury Collision             2\n",
       "194669  Property Damage Only Collision             1\n",
       "194670                Injury Collision             2\n",
       "194671                Injury Collision             2\n",
       "194672  Property Damage Only Collision             1\n",
       "\n",
       "[189035 rows x 2 columns]"
      ],
      "text/html": "<div>\n<style scoped>\n    .dataframe tbody tr th:only-of-type {\n        vertical-align: middle;\n    }\n\n    .dataframe tbody tr th {\n        vertical-align: top;\n    }\n\n    .dataframe thead th {\n        text-align: right;\n    }\n</style>\n<table border=\"1\" class=\"dataframe\">\n  <thead>\n    <tr style=\"text-align: right;\">\n      <th></th>\n      <th>SEVERITYDESC</th>\n      <th>SEVERITYCODE</th>\n    </tr>\n  </thead>\n  <tbody>\n    <tr>\n      <td>0</td>\n      <td>Injury Collision</td>\n      <td>2</td>\n    </tr>\n    <tr>\n      <td>1</td>\n      <td>Property Damage Only Collision</td>\n      <td>1</td>\n    </tr>\n    <tr>\n      <td>2</td>\n      <td>Property Damage Only Collision</td>\n      <td>1</td>\n    </tr>\n    <tr>\n      <td>3</td>\n      <td>Property Damage Only Collision</td>\n      <td>1</td>\n    </tr>\n    <tr>\n      <td>4</td>\n      <td>Injury Collision</td>\n      <td>2</td>\n    </tr>\n    <tr>\n      <td>...</td>\n      <td>...</td>\n      <td>...</td>\n    </tr>\n    <tr>\n      <td>194668</td>\n      <td>Injury Collision</td>\n      <td>2</td>\n    </tr>\n    <tr>\n      <td>194669</td>\n      <td>Property Damage Only Collision</td>\n      <td>1</td>\n    </tr>\n    <tr>\n      <td>194670</td>\n      <td>Injury Collision</td>\n      <td>2</td>\n    </tr>\n    <tr>\n      <td>194671</td>\n      <td>Injury Collision</td>\n      <td>2</td>\n    </tr>\n    <tr>\n      <td>194672</td>\n      <td>Property Damage Only Collision</td>\n      <td>1</td>\n    </tr>\n  </tbody>\n</table>\n<p>189035 rows × 2 columns</p>\n</div>"
     },
     "metadata": {},
     "execution_count": 8
    }
   ],
   "source": [
    "collision_data[['SEVERITYDESC','SEVERITYCODE']]"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 9,
   "metadata": {},
   "outputs": [],
   "source": [
    "# INATTENTIONIND SET Y = 1 BLANK = 0\n",
    "# UNDERINFL SET Y, = 1, N = 0, BLANK = 0\n",
    "# PEDROWNOTGRNT SET Y = 1, BLANK = 0\n",
    "# SPEEDING SET Y = 1, BLANK = 0\n",
    "# HITPARKEDCAR SET Y = 1, N = 1\n",
    "collision_data['INATTENTIONIND'] = np.where((collision_data.INATTENTIONIND == 'Y'), 1, 0)\n",
    "collision_data['PEDROWNOTGRNT'] = np.where((collision_data.PEDROWNOTGRNT == 'Y'), 1, 0)\n",
    "collision_data['SPEEDING'] = np.where((collision_data.SPEEDING == 'Y'), 1, 0)\n",
    "collision_data['HITPARKEDCAR'] = np.where((collision_data.HITPARKEDCAR == 'Y'), 1, 0)\n",
    "collision_data['UNDERINFL'] =   np.where(((collision_data.UNDERINFL == 'Y') | (collision_data.UNDERINFL == '1')), 1, 0)"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 10,
   "metadata": {},
   "outputs": [],
   "source": [
    "#Now to convert the datetime to just the time of the day, and place them into buckets. these buckets will occur by just returning the hour of the day, and using that hour as the bucket for our incident.\n",
    "# pd.to_datetime(collision_data['INCDTTM'])\n",
    "collision_data['HOUROFDAY'] = pd.to_datetime(collision_data['INCDTTM']).dt.hour"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 11,
   "metadata": {},
   "outputs": [
    {
     "output_type": "execute_result",
     "data": {
      "text/plain": [
       "   SEVERITYCODE      ADDRTYPE COLLISIONTYPE  PERSONCOUNT  PEDCOUNT  \\\n",
       "0             2  Intersection        Angles            2         0   \n",
       "1             1         Block     Sideswipe            2         0   \n",
       "2             1         Block    Parked Car            4         0   \n",
       "3             1         Block         Other            3         0   \n",
       "4             2  Intersection        Angles            2         0   \n",
       "5             1  Intersection        Angles            2         0   \n",
       "6             1  Intersection        Angles            2         0   \n",
       "7             2  Intersection        Cycles            3         0   \n",
       "8             1         Block    Parked Car            2         0   \n",
       "9             2  Intersection        Angles            2         0   \n",
       "\n",
       "   PEDCYLCOUNT  VEHCOUNT                             JUNCTIONTYPE  \\\n",
       "0            0         2   At Intersection (intersection related)   \n",
       "1            0         2  Mid-Block (not related to intersection)   \n",
       "2            0         3  Mid-Block (not related to intersection)   \n",
       "3            0         3  Mid-Block (not related to intersection)   \n",
       "4            0         2   At Intersection (intersection related)   \n",
       "5            0         2   At Intersection (intersection related)   \n",
       "6            0         2   At Intersection (intersection related)   \n",
       "7            1         1   At Intersection (intersection related)   \n",
       "8            0         2  Mid-Block (not related to intersection)   \n",
       "9            0         2   At Intersection (intersection related)   \n",
       "\n",
       "   INATTENTIONIND  UNDERINFL   WEATHER ROADCOND                LIGHTCOND  \\\n",
       "0               0          0  Overcast      Wet                 Daylight   \n",
       "1               0          0   Raining      Wet  Dark - Street Lights On   \n",
       "2               0          0  Overcast      Dry                 Daylight   \n",
       "3               0          0     Clear      Dry                 Daylight   \n",
       "4               0          0   Raining      Wet                 Daylight   \n",
       "5               0          0     Clear      Dry                 Daylight   \n",
       "6               0          0   Raining      Wet                 Daylight   \n",
       "7               0          0     Clear      Dry                 Daylight   \n",
       "8               0          0     Clear      Dry                 Daylight   \n",
       "9               0          0     Clear      Dry                 Daylight   \n",
       "\n",
       "   PEDROWNOTGRNT  SPEEDING                                         ST_COLDESC  \\\n",
       "0              0         0                                  Entering at angle   \n",
       "1              0         0  From same direction - both going straight - bo...   \n",
       "2              0         0                             One parked--one moving   \n",
       "3              0         0                   From same direction - all others   \n",
       "4              0         0                                  Entering at angle   \n",
       "5              0         0                                  Entering at angle   \n",
       "6              0         0                                  Entering at angle   \n",
       "7              0         0                       Vehicle Strikes Pedalcyclist   \n",
       "8              0         0                             One parked--one moving   \n",
       "9              0         0                                  Entering at angle   \n",
       "\n",
       "   CROSSWALKKEY  HITPARKEDCAR  HOUROFDAY  \n",
       "0             0             0         14  \n",
       "1             0             0         18  \n",
       "2             0             0         10  \n",
       "3             0             0          9  \n",
       "4             0             0          8  \n",
       "5             0             0         17  \n",
       "6             0             0          0  \n",
       "7             0             0         17  \n",
       "8             0             0         13  \n",
       "9             0             0         15  "
      ],
      "text/html": "<div>\n<style scoped>\n    .dataframe tbody tr th:only-of-type {\n        vertical-align: middle;\n    }\n\n    .dataframe tbody tr th {\n        vertical-align: top;\n    }\n\n    .dataframe thead th {\n        text-align: right;\n    }\n</style>\n<table border=\"1\" class=\"dataframe\">\n  <thead>\n    <tr style=\"text-align: right;\">\n      <th></th>\n      <th>SEVERITYCODE</th>\n      <th>ADDRTYPE</th>\n      <th>COLLISIONTYPE</th>\n      <th>PERSONCOUNT</th>\n      <th>PEDCOUNT</th>\n      <th>PEDCYLCOUNT</th>\n      <th>VEHCOUNT</th>\n      <th>JUNCTIONTYPE</th>\n      <th>INATTENTIONIND</th>\n      <th>UNDERINFL</th>\n      <th>WEATHER</th>\n      <th>ROADCOND</th>\n      <th>LIGHTCOND</th>\n      <th>PEDROWNOTGRNT</th>\n      <th>SPEEDING</th>\n      <th>ST_COLDESC</th>\n      <th>CROSSWALKKEY</th>\n      <th>HITPARKEDCAR</th>\n      <th>HOUROFDAY</th>\n    </tr>\n  </thead>\n  <tbody>\n    <tr>\n      <td>0</td>\n      <td>2</td>\n      <td>Intersection</td>\n      <td>Angles</td>\n      <td>2</td>\n      <td>0</td>\n      <td>0</td>\n      <td>2</td>\n      <td>At Intersection (intersection related)</td>\n      <td>0</td>\n      <td>0</td>\n      <td>Overcast</td>\n      <td>Wet</td>\n      <td>Daylight</td>\n      <td>0</td>\n      <td>0</td>\n      <td>Entering at angle</td>\n      <td>0</td>\n      <td>0</td>\n      <td>14</td>\n    </tr>\n    <tr>\n      <td>1</td>\n      <td>1</td>\n      <td>Block</td>\n      <td>Sideswipe</td>\n      <td>2</td>\n      <td>0</td>\n      <td>0</td>\n      <td>2</td>\n      <td>Mid-Block (not related to intersection)</td>\n      <td>0</td>\n      <td>0</td>\n      <td>Raining</td>\n      <td>Wet</td>\n      <td>Dark - Street Lights On</td>\n      <td>0</td>\n      <td>0</td>\n      <td>From same direction - both going straight - bo...</td>\n      <td>0</td>\n      <td>0</td>\n      <td>18</td>\n    </tr>\n    <tr>\n      <td>2</td>\n      <td>1</td>\n      <td>Block</td>\n      <td>Parked Car</td>\n      <td>4</td>\n      <td>0</td>\n      <td>0</td>\n      <td>3</td>\n      <td>Mid-Block (not related to intersection)</td>\n      <td>0</td>\n      <td>0</td>\n      <td>Overcast</td>\n      <td>Dry</td>\n      <td>Daylight</td>\n      <td>0</td>\n      <td>0</td>\n      <td>One parked--one moving</td>\n      <td>0</td>\n      <td>0</td>\n      <td>10</td>\n    </tr>\n    <tr>\n      <td>3</td>\n      <td>1</td>\n      <td>Block</td>\n      <td>Other</td>\n      <td>3</td>\n      <td>0</td>\n      <td>0</td>\n      <td>3</td>\n      <td>Mid-Block (not related to intersection)</td>\n      <td>0</td>\n      <td>0</td>\n      <td>Clear</td>\n      <td>Dry</td>\n      <td>Daylight</td>\n      <td>0</td>\n      <td>0</td>\n      <td>From same direction - all others</td>\n      <td>0</td>\n      <td>0</td>\n      <td>9</td>\n    </tr>\n    <tr>\n      <td>4</td>\n      <td>2</td>\n      <td>Intersection</td>\n      <td>Angles</td>\n      <td>2</td>\n      <td>0</td>\n      <td>0</td>\n      <td>2</td>\n      <td>At Intersection (intersection related)</td>\n      <td>0</td>\n      <td>0</td>\n      <td>Raining</td>\n      <td>Wet</td>\n      <td>Daylight</td>\n      <td>0</td>\n      <td>0</td>\n      <td>Entering at angle</td>\n      <td>0</td>\n      <td>0</td>\n      <td>8</td>\n    </tr>\n    <tr>\n      <td>5</td>\n      <td>1</td>\n      <td>Intersection</td>\n      <td>Angles</td>\n      <td>2</td>\n      <td>0</td>\n      <td>0</td>\n      <td>2</td>\n      <td>At Intersection (intersection related)</td>\n      <td>0</td>\n      <td>0</td>\n      <td>Clear</td>\n      <td>Dry</td>\n      <td>Daylight</td>\n      <td>0</td>\n      <td>0</td>\n      <td>Entering at angle</td>\n      <td>0</td>\n      <td>0</td>\n      <td>17</td>\n    </tr>\n    <tr>\n      <td>6</td>\n      <td>1</td>\n      <td>Intersection</td>\n      <td>Angles</td>\n      <td>2</td>\n      <td>0</td>\n      <td>0</td>\n      <td>2</td>\n      <td>At Intersection (intersection related)</td>\n      <td>0</td>\n      <td>0</td>\n      <td>Raining</td>\n      <td>Wet</td>\n      <td>Daylight</td>\n      <td>0</td>\n      <td>0</td>\n      <td>Entering at angle</td>\n      <td>0</td>\n      <td>0</td>\n      <td>0</td>\n    </tr>\n    <tr>\n      <td>7</td>\n      <td>2</td>\n      <td>Intersection</td>\n      <td>Cycles</td>\n      <td>3</td>\n      <td>0</td>\n      <td>1</td>\n      <td>1</td>\n      <td>At Intersection (intersection related)</td>\n      <td>0</td>\n      <td>0</td>\n      <td>Clear</td>\n      <td>Dry</td>\n      <td>Daylight</td>\n      <td>0</td>\n      <td>0</td>\n      <td>Vehicle Strikes Pedalcyclist</td>\n      <td>0</td>\n      <td>0</td>\n      <td>17</td>\n    </tr>\n    <tr>\n      <td>8</td>\n      <td>1</td>\n      <td>Block</td>\n      <td>Parked Car</td>\n      <td>2</td>\n      <td>0</td>\n      <td>0</td>\n      <td>2</td>\n      <td>Mid-Block (not related to intersection)</td>\n      <td>0</td>\n      <td>0</td>\n      <td>Clear</td>\n      <td>Dry</td>\n      <td>Daylight</td>\n      <td>0</td>\n      <td>0</td>\n      <td>One parked--one moving</td>\n      <td>0</td>\n      <td>0</td>\n      <td>13</td>\n    </tr>\n    <tr>\n      <td>9</td>\n      <td>2</td>\n      <td>Intersection</td>\n      <td>Angles</td>\n      <td>2</td>\n      <td>0</td>\n      <td>0</td>\n      <td>2</td>\n      <td>At Intersection (intersection related)</td>\n      <td>0</td>\n      <td>0</td>\n      <td>Clear</td>\n      <td>Dry</td>\n      <td>Daylight</td>\n      <td>0</td>\n      <td>0</td>\n      <td>Entering at angle</td>\n      <td>0</td>\n      <td>0</td>\n      <td>15</td>\n    </tr>\n  </tbody>\n</table>\n</div>"
     },
     "metadata": {},
     "execution_count": 11
    }
   ],
   "source": [
    "collision_data_relevant = collision_data.drop(columns=['X', 'Y', 'OBJECTID', 'INCKEY','INCDATE', 'COLDETKEY', 'INTKEY', 'STATUS', 'LOCATION', 'STATUS', 'REPORTNO', 'SEVERITYCODE.1', 'SDOT_COLDESC', 'SDOTCOLNUM', 'ST_COLCODE','SDOT_COLCODE','INCDTTM','SEVERITYDESC','SEGLANEKEY']).dropna()\n",
    "collision_data_relevant.head(10)"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 12,
   "metadata": {},
   "outputs": [],
   "source": [
    "collision_data_relevant.head(10).to_csv('String-Cleaned-Data-Collisions.csv')"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 13,
   "metadata": {},
   "outputs": [
    {
     "output_type": "stream",
     "name": "stdout",
     "text": [
      "{'ADDRTYPE': {'Alley': 1, 'Block': 2, 'Intersection': 3}}\n",
      "{'COLLISIONTYPE': {'Angles': 1, 'Cycles': 2, 'Head On': 3, 'Left Turn': 4, 'Other': 5, 'Parked Car': 6, 'Pedestrian': 7, 'Rear Ended': 8, 'Right Turn': 9, 'Sideswipe': 10}}\n",
      "{'JUNCTIONTYPE': {'At Intersection (but not related to intersection)': 1, 'At Intersection (intersection related)': 2, 'Driveway Junction': 3, 'Mid-Block (but intersection related)': 4, 'Mid-Block (not related to intersection)': 5, 'Ramp Junction': 6, 'Unknown': 7}}\n",
      "{'WEATHER': {'Blowing Sand/Dirt': 1, 'Clear': 2, 'Fog/Smog/Smoke': 3, 'Other': 4, 'Overcast': 5, 'Partly Cloudy': 6, 'Raining': 7, 'Severe Crosswind': 8, 'Sleet/Hail/Freezing Rain': 9, 'Snowing': 10, 'Unknown': 11}}\n",
      "{'ROADCOND': {'Dry': 1, 'Ice': 2, 'Oil': 3, 'Other': 4, 'Sand/Mud/Dirt': 5, 'Snow/Slush': 6, 'Standing Water': 7, 'Unknown': 8, 'Wet': 9}}\n",
      "{'LIGHTCOND': {'Dark - No Street Lights': 1, 'Dark - Street Lights Off': 2, 'Dark - Street Lights On': 3, 'Dark - Unknown Lighting': 4, 'Dawn': 5, 'Daylight': 6, 'Dusk': 7, 'Other': 8, 'Unknown': 9}}\n",
      "{'ST_COLDESC': {'All Other Multi Vehicle': 1, 'All other non-collision': 2, 'Breakage of any part of the vehicle resulting in injury or in further property damage': 3, 'Domestic animal other (cat, dog, etc)': 4, 'Entering at angle': 5, 'Fire started in vehicle': 6, 'Fixed object': 7, 'From opposite direction - all others': 8, 'From opposite direction - both going straight - one stopped - sideswipe': 9, 'From opposite direction - both going straight - sideswipe': 10, 'From opposite direction - both moving - head-on': 11, 'From opposite direction - one left turn - one right turn': 12, 'From opposite direction - one left turn - one straight': 13, 'From opposite direction - one stopped - head-on': 14, 'From same direction - all others': 15, 'From same direction - both going straight - both moving - rear-end': 16, 'From same direction - both going straight - both moving - sideswipe': 17, 'From same direction - both going straight - one stopped - rear-end': 18, 'From same direction - both going straight - one stopped - sideswipe': 19, 'From same direction - one left turn - one straight': 20, 'From same direction - one right turn - one straight': 21, 'Non-domestic animal (deer, bear, elk, etc)': 22, 'Not stated': 23, 'One car entering driveway access': 24, 'One car entering parked position': 25, 'One car leaving driveway access': 26, 'One car leaving parked position': 27, 'One parked--one moving': 28, 'Other object': 29, 'Pedalcyclist All Other Involvements ONE UNIT - PEDALCYCLIST ONLY or PEDALCYCLIST STR': 30, 'Pedalcyclist Strikes Moving Vehicle': 31, 'Pedalcyclist Strikes Pedalcyclist or Pedestrian': 32, 'Person fell, jumped or was pushed from vehicle': 33, 'Railway Vehicle Strikes Pedalcyclist': 34, 'Railway Vehicle Strikes Pedestrian': 35, 'Railway Vehicle Strikes Vehicle': 36, 'Same direction -- both turning left -- both moving -- rear end': 37, 'Same direction -- both turning left -- both moving -- sideswipe': 38, 'Same direction -- both turning left -- one stopped -- rear end': 39, 'Same direction -- both turning left -- one stopped -- sideswipe': 40, 'Same direction -- both turning right -- both moving -- rear end': 41, 'Same direction -- both turning right -- both moving -- sideswipe': 42, 'Same direction -- both turning right -- one stopped -- rear end': 43, 'Same direction -- both turning right -- one stopped -- sideswipe': 44, 'Strikes or Was Struck by Object from the Load of Another Vehicle': 45, 'Strikes or Was Struck by a Part of Another Vehicle (Not from Load)': 46, 'Vehicle - Pedalcyclist': 47, 'Vehicle Hits City Road or Construction Machinery': 48, 'Vehicle Hits Other Road or Construction Machinery': 49, 'Vehicle Hits State Road or Construction Machinery': 50, 'Vehicle Strikes All Other Non-Domestic Animal': 51, 'Vehicle Strikes Deer': 52, 'Vehicle Strikes Pedalcyclist': 53, 'Vehicle Strikes Railway Vehicle': 54, 'Vehicle Struck by City Road or Construction Machinery': 55, 'Vehicle Struck by Other Road or Construction Machinery': 56, 'Vehicle backing hits pedestrian': 57, 'Vehicle going straight hits pedestrian': 58, 'Vehicle hits Pedestrian - All Other Actions': 59, 'Vehicle overturned': 60, 'Vehicle turning left hits pedestrian': 61, 'Vehicle turning right hits pedestrian': 62}}\n"
     ]
    }
   ],
   "source": [
    "#Now to convert our categorical values into numeric values, so that our tree can accurately interpret them. We will utilize a for-loop in order to rapidly do this\n",
    "labels_list = []\n",
    "for i in ['ADDRTYPE','COLLISIONTYPE','JUNCTIONTYPE','WEATHER','ROADCOND','LIGHTCOND','ST_COLDESC']:\n",
    "    labels = collision_data_relevant[i].astype('category').cat.categories.tolist()\n",
    "    replace_map_comp = {i : {k: v for k,v in zip(labels,list(range(1,len(labels)+1)))}}\n",
    "    collision_data_relevant.replace(replace_map_comp, inplace=True)\n",
    "    labels_list.append(i)\n",
    "    # df = pd.DataFrame.from_dict(replace_map_comp)\n",
    "    # df.to_csv('{0}.csv'.format(i))\n",
    "    print(replace_map_comp)"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 14,
   "metadata": {},
   "outputs": [
    {
     "output_type": "execute_result",
     "data": {
      "text/plain": [
       "        SEVERITYCODE  ADDRTYPE  COLLISIONTYPE  PERSONCOUNT  PEDCOUNT  \\\n",
       "0                  2         3              1            2         0   \n",
       "1                  1         2             10            2         0   \n",
       "2                  1         2              6            4         0   \n",
       "3                  1         2              5            3         0   \n",
       "4                  2         3              1            2         0   \n",
       "...              ...       ...            ...          ...       ...   \n",
       "181061             2         2              3            3         0   \n",
       "181062             1         2              8            2         0   \n",
       "181063             2         3              4            3         0   \n",
       "181064             2         3              2            2         0   \n",
       "181065             1         2              8            2         0   \n",
       "\n",
       "        PEDCYLCOUNT  VEHCOUNT  JUNCTIONTYPE  INATTENTIONIND  UNDERINFL  \\\n",
       "0                 0         2             2               0          0   \n",
       "1                 0         2             5               0          0   \n",
       "2                 0         3             5               0          0   \n",
       "3                 0         3             5               0          0   \n",
       "4                 0         2             2               0          0   \n",
       "...             ...       ...           ...             ...        ...   \n",
       "181061            0         2             5               0          0   \n",
       "181062            0         2             5               1          0   \n",
       "181063            0         2             2               0          0   \n",
       "181064            1         1             2               0          0   \n",
       "181065            0         2             5               0          0   \n",
       "\n",
       "        WEATHER  ROADCOND  LIGHTCOND  PEDROWNOTGRNT  SPEEDING  ST_COLDESC  \\\n",
       "0             5         9          6              0         0           5   \n",
       "1             7         9          3              0         0          17   \n",
       "2             5         1          6              0         0          28   \n",
       "3             2         1          6              0         0          15   \n",
       "4             7         9          6              0         0           5   \n",
       "...         ...       ...        ...            ...       ...         ...   \n",
       "181061        2         1          6              0         0          11   \n",
       "181062        7         9          6              0         0          16   \n",
       "181063        2         1          6              0         0          13   \n",
       "181064        2         1          7              0         0          53   \n",
       "181065        2         9          6              0         0          18   \n",
       "\n",
       "        CROSSWALKKEY  HITPARKEDCAR  HOUROFDAY  \n",
       "0                  0             0         14  \n",
       "1                  0             0         18  \n",
       "2                  0             0         10  \n",
       "3                  0             0          9  \n",
       "4                  0             0          8  \n",
       "...              ...           ...        ...  \n",
       "181061             0             0          8  \n",
       "181062             0             0          9  \n",
       "181063             0             0          9  \n",
       "181064             0             0         16  \n",
       "181065             0             0         15  \n",
       "\n",
       "[181066 rows x 19 columns]"
      ],
      "text/html": "<div>\n<style scoped>\n    .dataframe tbody tr th:only-of-type {\n        vertical-align: middle;\n    }\n\n    .dataframe tbody tr th {\n        vertical-align: top;\n    }\n\n    .dataframe thead th {\n        text-align: right;\n    }\n</style>\n<table border=\"1\" class=\"dataframe\">\n  <thead>\n    <tr style=\"text-align: right;\">\n      <th></th>\n      <th>SEVERITYCODE</th>\n      <th>ADDRTYPE</th>\n      <th>COLLISIONTYPE</th>\n      <th>PERSONCOUNT</th>\n      <th>PEDCOUNT</th>\n      <th>PEDCYLCOUNT</th>\n      <th>VEHCOUNT</th>\n      <th>JUNCTIONTYPE</th>\n      <th>INATTENTIONIND</th>\n      <th>UNDERINFL</th>\n      <th>WEATHER</th>\n      <th>ROADCOND</th>\n      <th>LIGHTCOND</th>\n      <th>PEDROWNOTGRNT</th>\n      <th>SPEEDING</th>\n      <th>ST_COLDESC</th>\n      <th>CROSSWALKKEY</th>\n      <th>HITPARKEDCAR</th>\n      <th>HOUROFDAY</th>\n    </tr>\n  </thead>\n  <tbody>\n    <tr>\n      <td>0</td>\n      <td>2</td>\n      <td>3</td>\n      <td>1</td>\n      <td>2</td>\n      <td>0</td>\n      <td>0</td>\n      <td>2</td>\n      <td>2</td>\n      <td>0</td>\n      <td>0</td>\n      <td>5</td>\n      <td>9</td>\n      <td>6</td>\n      <td>0</td>\n      <td>0</td>\n      <td>5</td>\n      <td>0</td>\n      <td>0</td>\n      <td>14</td>\n    </tr>\n    <tr>\n      <td>1</td>\n      <td>1</td>\n      <td>2</td>\n      <td>10</td>\n      <td>2</td>\n      <td>0</td>\n      <td>0</td>\n      <td>2</td>\n      <td>5</td>\n      <td>0</td>\n      <td>0</td>\n      <td>7</td>\n      <td>9</td>\n      <td>3</td>\n      <td>0</td>\n      <td>0</td>\n      <td>17</td>\n      <td>0</td>\n      <td>0</td>\n      <td>18</td>\n    </tr>\n    <tr>\n      <td>2</td>\n      <td>1</td>\n      <td>2</td>\n      <td>6</td>\n      <td>4</td>\n      <td>0</td>\n      <td>0</td>\n      <td>3</td>\n      <td>5</td>\n      <td>0</td>\n      <td>0</td>\n      <td>5</td>\n      <td>1</td>\n      <td>6</td>\n      <td>0</td>\n      <td>0</td>\n      <td>28</td>\n      <td>0</td>\n      <td>0</td>\n      <td>10</td>\n    </tr>\n    <tr>\n      <td>3</td>\n      <td>1</td>\n      <td>2</td>\n      <td>5</td>\n      <td>3</td>\n      <td>0</td>\n      <td>0</td>\n      <td>3</td>\n      <td>5</td>\n      <td>0</td>\n      <td>0</td>\n      <td>2</td>\n      <td>1</td>\n      <td>6</td>\n      <td>0</td>\n      <td>0</td>\n      <td>15</td>\n      <td>0</td>\n      <td>0</td>\n      <td>9</td>\n    </tr>\n    <tr>\n      <td>4</td>\n      <td>2</td>\n      <td>3</td>\n      <td>1</td>\n      <td>2</td>\n      <td>0</td>\n      <td>0</td>\n      <td>2</td>\n      <td>2</td>\n      <td>0</td>\n      <td>0</td>\n      <td>7</td>\n      <td>9</td>\n      <td>6</td>\n      <td>0</td>\n      <td>0</td>\n      <td>5</td>\n      <td>0</td>\n      <td>0</td>\n      <td>8</td>\n    </tr>\n    <tr>\n      <td>...</td>\n      <td>...</td>\n      <td>...</td>\n      <td>...</td>\n      <td>...</td>\n      <td>...</td>\n      <td>...</td>\n      <td>...</td>\n      <td>...</td>\n      <td>...</td>\n      <td>...</td>\n      <td>...</td>\n      <td>...</td>\n      <td>...</td>\n      <td>...</td>\n      <td>...</td>\n      <td>...</td>\n      <td>...</td>\n      <td>...</td>\n      <td>...</td>\n    </tr>\n    <tr>\n      <td>181061</td>\n      <td>2</td>\n      <td>2</td>\n      <td>3</td>\n      <td>3</td>\n      <td>0</td>\n      <td>0</td>\n      <td>2</td>\n      <td>5</td>\n      <td>0</td>\n      <td>0</td>\n      <td>2</td>\n      <td>1</td>\n      <td>6</td>\n      <td>0</td>\n      <td>0</td>\n      <td>11</td>\n      <td>0</td>\n      <td>0</td>\n      <td>8</td>\n    </tr>\n    <tr>\n      <td>181062</td>\n      <td>1</td>\n      <td>2</td>\n      <td>8</td>\n      <td>2</td>\n      <td>0</td>\n      <td>0</td>\n      <td>2</td>\n      <td>5</td>\n      <td>1</td>\n      <td>0</td>\n      <td>7</td>\n      <td>9</td>\n      <td>6</td>\n      <td>0</td>\n      <td>0</td>\n      <td>16</td>\n      <td>0</td>\n      <td>0</td>\n      <td>9</td>\n    </tr>\n    <tr>\n      <td>181063</td>\n      <td>2</td>\n      <td>3</td>\n      <td>4</td>\n      <td>3</td>\n      <td>0</td>\n      <td>0</td>\n      <td>2</td>\n      <td>2</td>\n      <td>0</td>\n      <td>0</td>\n      <td>2</td>\n      <td>1</td>\n      <td>6</td>\n      <td>0</td>\n      <td>0</td>\n      <td>13</td>\n      <td>0</td>\n      <td>0</td>\n      <td>9</td>\n    </tr>\n    <tr>\n      <td>181064</td>\n      <td>2</td>\n      <td>3</td>\n      <td>2</td>\n      <td>2</td>\n      <td>0</td>\n      <td>1</td>\n      <td>1</td>\n      <td>2</td>\n      <td>0</td>\n      <td>0</td>\n      <td>2</td>\n      <td>1</td>\n      <td>7</td>\n      <td>0</td>\n      <td>0</td>\n      <td>53</td>\n      <td>0</td>\n      <td>0</td>\n      <td>16</td>\n    </tr>\n    <tr>\n      <td>181065</td>\n      <td>1</td>\n      <td>2</td>\n      <td>8</td>\n      <td>2</td>\n      <td>0</td>\n      <td>0</td>\n      <td>2</td>\n      <td>5</td>\n      <td>0</td>\n      <td>0</td>\n      <td>2</td>\n      <td>9</td>\n      <td>6</td>\n      <td>0</td>\n      <td>0</td>\n      <td>18</td>\n      <td>0</td>\n      <td>0</td>\n      <td>15</td>\n    </tr>\n  </tbody>\n</table>\n<p>181066 rows × 19 columns</p>\n</div>"
     },
     "metadata": {},
     "execution_count": 14
    }
   ],
   "source": [
    "collision_data_relevant.reset_index(inplace=True, drop=True)\n",
    "collision_data_relevant"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 15,
   "metadata": {},
   "outputs": [
    {
     "output_type": "execute_result",
     "data": {
      "text/plain": [
       "                SEVERITYCODE  ADDRTYPE  COLLISIONTYPE  PERSONCOUNT  PEDCOUNT  \\\n",
       "SEVERITYCODE        1.000000  0.191201      -0.126293     0.123792  0.244164   \n",
       "ADDRTYPE            0.191201  1.000000      -0.482232     0.059587  0.143217   \n",
       "COLLISIONTYPE      -0.126293 -0.482232       1.000000     0.015785  0.093463   \n",
       "PERSONCOUNT         0.123792  0.059587       0.015785     1.000000 -0.026629   \n",
       "PEDCOUNT            0.244164  0.143217       0.093463    -0.026629  1.000000   \n",
       "PEDCYLCOUNT         0.213477  0.082480      -0.211996    -0.042534 -0.018562   \n",
       "VEHCOUNT           -0.079848 -0.090043       0.104975     0.399715 -0.315981   \n",
       "JUNCTIONTYPE       -0.198740 -0.919140       0.482510    -0.069830 -0.130424   \n",
       "INATTENTIONIND      0.040400 -0.083471       0.122779     0.071111 -0.008240   \n",
       "UNDERINFL           0.039705 -0.047527       0.005498     0.018098  0.014795   \n",
       "WEATHER            -0.084248 -0.069945       0.018963    -0.050895 -0.004351   \n",
       "ROADCOND           -0.033417 -0.018598      -0.006616    -0.023667  0.009657   \n",
       "LIGHTCOND          -0.036926 -0.033325       0.025141    -0.027323 -0.035135   \n",
       "PEDROWNOTGRNT       0.206038  0.155258      -0.020564    -0.031731  0.496801   \n",
       "SPEEDING            0.033914 -0.065089      -0.002296    -0.007835 -0.035003   \n",
       "ST_COLDESC          0.099013 -0.168275       0.361238    -0.067916  0.564382   \n",
       "CROSSWALKKEY        0.172777  0.176120       0.033517    -0.034363  0.568736   \n",
       "HITPARKEDCAR       -0.087120 -0.114501       0.032658    -0.042441 -0.031187   \n",
       "HOUROFDAY           0.031489  0.041482      -0.005694     0.030907  0.025825   \n",
       "\n",
       "                PEDCYLCOUNT  VEHCOUNT  JUNCTIONTYPE  INATTENTIONIND  \\\n",
       "SEVERITYCODE       0.213477 -0.079848     -0.198740        0.040400   \n",
       "ADDRTYPE           0.082480 -0.090043     -0.919140       -0.083471   \n",
       "COLLISIONTYPE     -0.211996  0.104975      0.482510        0.122779   \n",
       "PERSONCOUNT       -0.042534  0.399715     -0.069830        0.071111   \n",
       "PEDCOUNT          -0.018562 -0.315981     -0.130424       -0.008240   \n",
       "PEDCYLCOUNT        1.000000 -0.306282     -0.087600        0.001044   \n",
       "VEHCOUNT          -0.306282  1.000000      0.088328        0.051240   \n",
       "JUNCTIONTYPE      -0.087600  0.088328      1.000000        0.072035   \n",
       "INATTENTIONIND     0.001044  0.051240      0.072035        1.000000   \n",
       "UNDERINFL         -0.018475 -0.011347      0.057061       -0.030593   \n",
       "WEATHER           -0.050059 -0.012246      0.081328       -0.074548   \n",
       "ROADCOND          -0.047357 -0.017825      0.025302       -0.050762   \n",
       "LIGHTCOND          0.019001  0.034697      0.026615        0.011343   \n",
       "PEDROWNOTGRNT      0.325585 -0.277556     -0.153624       -0.030380   \n",
       "SPEEDING          -0.022378 -0.048845      0.067151       -0.054071   \n",
       "ST_COLDESC         0.357401 -0.216368      0.172640        0.024330   \n",
       "CROSSWALKKEY       0.109444 -0.236850     -0.160084       -0.004677   \n",
       "HITPARKEDCAR      -0.027379  0.073987      0.137860        0.019401   \n",
       "HOUROFDAY          0.022931  0.010129     -0.033514        0.026332   \n",
       "\n",
       "                UNDERINFL   WEATHER  ROADCOND  LIGHTCOND  PEDROWNOTGRNT  \\\n",
       "SEVERITYCODE     0.039705 -0.084248 -0.033417  -0.036926       0.206038   \n",
       "ADDRTYPE        -0.047527 -0.069945 -0.018598  -0.033325       0.155258   \n",
       "COLLISIONTYPE    0.005498  0.018963 -0.006616   0.025141      -0.020564   \n",
       "PERSONCOUNT      0.018098 -0.050895 -0.023667  -0.027323      -0.031731   \n",
       "PEDCOUNT         0.014795 -0.004351  0.009657  -0.035135       0.496801   \n",
       "PEDCYLCOUNT     -0.018475 -0.050059 -0.047357   0.019001       0.325585   \n",
       "VEHCOUNT        -0.011347 -0.012246 -0.017825   0.034697      -0.277556   \n",
       "JUNCTIONTYPE     0.057061  0.081328  0.025302   0.026615      -0.153624   \n",
       "INATTENTIONIND  -0.030593 -0.074548 -0.050762   0.011343      -0.030380   \n",
       "UNDERINFL        1.000000 -0.033861 -0.007447  -0.218660      -0.019470   \n",
       "WEATHER         -0.033861  1.000000  0.749529   0.140448      -0.009420   \n",
       "ROADCOND        -0.007447  0.749529  1.000000  -0.017991       0.002180   \n",
       "LIGHTCOND       -0.218660  0.140448 -0.017991   1.000000      -0.009389   \n",
       "PEDROWNOTGRNT   -0.019470 -0.009420  0.002180  -0.009389       1.000000   \n",
       "SPEEDING         0.090495  0.051841  0.095767  -0.097009      -0.030462   \n",
       "ST_COLDESC      -0.006102  0.035161 -0.017557   0.044615       0.440815   \n",
       "CROSSWALKKEY    -0.010661 -0.000250  0.011714  -0.018754       0.453206   \n",
       "HITPARKEDCAR     0.022893  0.017034 -0.003130  -0.001216      -0.027785   \n",
       "HOUROFDAY       -0.030735 -0.027889 -0.023917  -0.042155       0.013348   \n",
       "\n",
       "                SPEEDING  ST_COLDESC  CROSSWALKKEY  HITPARKEDCAR  HOUROFDAY  \n",
       "SEVERITYCODE    0.033914    0.099013      0.172777     -0.087120   0.031489  \n",
       "ADDRTYPE       -0.065089   -0.168275      0.176120     -0.114501   0.041482  \n",
       "COLLISIONTYPE  -0.002296    0.361238      0.033517      0.032658  -0.005694  \n",
       "PERSONCOUNT    -0.007835   -0.067916     -0.034363     -0.042441   0.030907  \n",
       "PEDCOUNT       -0.035003    0.564382      0.568736     -0.031187   0.025825  \n",
       "PEDCYLCOUNT    -0.022378    0.357401      0.109444     -0.027379   0.022931  \n",
       "VEHCOUNT       -0.048845   -0.216368     -0.236850      0.073987   0.010129  \n",
       "JUNCTIONTYPE    0.067151    0.172640     -0.160084      0.137860  -0.033514  \n",
       "INATTENTIONIND -0.054071    0.024330     -0.004677      0.019401   0.026332  \n",
       "UNDERINFL       0.090495   -0.006102     -0.010661      0.022893  -0.030735  \n",
       "WEATHER         0.051841    0.035161     -0.000250      0.017034  -0.027889  \n",
       "ROADCOND        0.095767   -0.017557      0.011714     -0.003130  -0.023917  \n",
       "LIGHTCOND      -0.097009    0.044615     -0.018754     -0.001216  -0.042155  \n",
       "PEDROWNOTGRNT  -0.030462    0.440815      0.453206     -0.027785   0.013348  \n",
       "SPEEDING        1.000000   -0.083141     -0.026746     -0.022224  -0.033919  \n",
       "ST_COLDESC     -0.083141    1.000000      0.404324      0.105874   0.005503  \n",
       "CROSSWALKKEY   -0.026746    0.404324      1.000000     -0.023644   0.029860  \n",
       "HITPARKEDCAR   -0.022224    0.105874     -0.023644      1.000000   0.031115  \n",
       "HOUROFDAY      -0.033919    0.005503      0.029860      0.031115   1.000000  "
      ],
      "text/html": "<div>\n<style scoped>\n    .dataframe tbody tr th:only-of-type {\n        vertical-align: middle;\n    }\n\n    .dataframe tbody tr th {\n        vertical-align: top;\n    }\n\n    .dataframe thead th {\n        text-align: right;\n    }\n</style>\n<table border=\"1\" class=\"dataframe\">\n  <thead>\n    <tr style=\"text-align: right;\">\n      <th></th>\n      <th>SEVERITYCODE</th>\n      <th>ADDRTYPE</th>\n      <th>COLLISIONTYPE</th>\n      <th>PERSONCOUNT</th>\n      <th>PEDCOUNT</th>\n      <th>PEDCYLCOUNT</th>\n      <th>VEHCOUNT</th>\n      <th>JUNCTIONTYPE</th>\n      <th>INATTENTIONIND</th>\n      <th>UNDERINFL</th>\n      <th>WEATHER</th>\n      <th>ROADCOND</th>\n      <th>LIGHTCOND</th>\n      <th>PEDROWNOTGRNT</th>\n      <th>SPEEDING</th>\n      <th>ST_COLDESC</th>\n      <th>CROSSWALKKEY</th>\n      <th>HITPARKEDCAR</th>\n      <th>HOUROFDAY</th>\n    </tr>\n  </thead>\n  <tbody>\n    <tr>\n      <td>SEVERITYCODE</td>\n      <td>1.000000</td>\n      <td>0.191201</td>\n      <td>-0.126293</td>\n      <td>0.123792</td>\n      <td>0.244164</td>\n      <td>0.213477</td>\n      <td>-0.079848</td>\n      <td>-0.198740</td>\n      <td>0.040400</td>\n      <td>0.039705</td>\n      <td>-0.084248</td>\n      <td>-0.033417</td>\n      <td>-0.036926</td>\n      <td>0.206038</td>\n      <td>0.033914</td>\n      <td>0.099013</td>\n      <td>0.172777</td>\n      <td>-0.087120</td>\n      <td>0.031489</td>\n    </tr>\n    <tr>\n      <td>ADDRTYPE</td>\n      <td>0.191201</td>\n      <td>1.000000</td>\n      <td>-0.482232</td>\n      <td>0.059587</td>\n      <td>0.143217</td>\n      <td>0.082480</td>\n      <td>-0.090043</td>\n      <td>-0.919140</td>\n      <td>-0.083471</td>\n      <td>-0.047527</td>\n      <td>-0.069945</td>\n      <td>-0.018598</td>\n      <td>-0.033325</td>\n      <td>0.155258</td>\n      <td>-0.065089</td>\n      <td>-0.168275</td>\n      <td>0.176120</td>\n      <td>-0.114501</td>\n      <td>0.041482</td>\n    </tr>\n    <tr>\n      <td>COLLISIONTYPE</td>\n      <td>-0.126293</td>\n      <td>-0.482232</td>\n      <td>1.000000</td>\n      <td>0.015785</td>\n      <td>0.093463</td>\n      <td>-0.211996</td>\n      <td>0.104975</td>\n      <td>0.482510</td>\n      <td>0.122779</td>\n      <td>0.005498</td>\n      <td>0.018963</td>\n      <td>-0.006616</td>\n      <td>0.025141</td>\n      <td>-0.020564</td>\n      <td>-0.002296</td>\n      <td>0.361238</td>\n      <td>0.033517</td>\n      <td>0.032658</td>\n      <td>-0.005694</td>\n    </tr>\n    <tr>\n      <td>PERSONCOUNT</td>\n      <td>0.123792</td>\n      <td>0.059587</td>\n      <td>0.015785</td>\n      <td>1.000000</td>\n      <td>-0.026629</td>\n      <td>-0.042534</td>\n      <td>0.399715</td>\n      <td>-0.069830</td>\n      <td>0.071111</td>\n      <td>0.018098</td>\n      <td>-0.050895</td>\n      <td>-0.023667</td>\n      <td>-0.027323</td>\n      <td>-0.031731</td>\n      <td>-0.007835</td>\n      <td>-0.067916</td>\n      <td>-0.034363</td>\n      <td>-0.042441</td>\n      <td>0.030907</td>\n    </tr>\n    <tr>\n      <td>PEDCOUNT</td>\n      <td>0.244164</td>\n      <td>0.143217</td>\n      <td>0.093463</td>\n      <td>-0.026629</td>\n      <td>1.000000</td>\n      <td>-0.018562</td>\n      <td>-0.315981</td>\n      <td>-0.130424</td>\n      <td>-0.008240</td>\n      <td>0.014795</td>\n      <td>-0.004351</td>\n      <td>0.009657</td>\n      <td>-0.035135</td>\n      <td>0.496801</td>\n      <td>-0.035003</td>\n      <td>0.564382</td>\n      <td>0.568736</td>\n      <td>-0.031187</td>\n      <td>0.025825</td>\n    </tr>\n    <tr>\n      <td>PEDCYLCOUNT</td>\n      <td>0.213477</td>\n      <td>0.082480</td>\n      <td>-0.211996</td>\n      <td>-0.042534</td>\n      <td>-0.018562</td>\n      <td>1.000000</td>\n      <td>-0.306282</td>\n      <td>-0.087600</td>\n      <td>0.001044</td>\n      <td>-0.018475</td>\n      <td>-0.050059</td>\n      <td>-0.047357</td>\n      <td>0.019001</td>\n      <td>0.325585</td>\n      <td>-0.022378</td>\n      <td>0.357401</td>\n      <td>0.109444</td>\n      <td>-0.027379</td>\n      <td>0.022931</td>\n    </tr>\n    <tr>\n      <td>VEHCOUNT</td>\n      <td>-0.079848</td>\n      <td>-0.090043</td>\n      <td>0.104975</td>\n      <td>0.399715</td>\n      <td>-0.315981</td>\n      <td>-0.306282</td>\n      <td>1.000000</td>\n      <td>0.088328</td>\n      <td>0.051240</td>\n      <td>-0.011347</td>\n      <td>-0.012246</td>\n      <td>-0.017825</td>\n      <td>0.034697</td>\n      <td>-0.277556</td>\n      <td>-0.048845</td>\n      <td>-0.216368</td>\n      <td>-0.236850</td>\n      <td>0.073987</td>\n      <td>0.010129</td>\n    </tr>\n    <tr>\n      <td>JUNCTIONTYPE</td>\n      <td>-0.198740</td>\n      <td>-0.919140</td>\n      <td>0.482510</td>\n      <td>-0.069830</td>\n      <td>-0.130424</td>\n      <td>-0.087600</td>\n      <td>0.088328</td>\n      <td>1.000000</td>\n      <td>0.072035</td>\n      <td>0.057061</td>\n      <td>0.081328</td>\n      <td>0.025302</td>\n      <td>0.026615</td>\n      <td>-0.153624</td>\n      <td>0.067151</td>\n      <td>0.172640</td>\n      <td>-0.160084</td>\n      <td>0.137860</td>\n      <td>-0.033514</td>\n    </tr>\n    <tr>\n      <td>INATTENTIONIND</td>\n      <td>0.040400</td>\n      <td>-0.083471</td>\n      <td>0.122779</td>\n      <td>0.071111</td>\n      <td>-0.008240</td>\n      <td>0.001044</td>\n      <td>0.051240</td>\n      <td>0.072035</td>\n      <td>1.000000</td>\n      <td>-0.030593</td>\n      <td>-0.074548</td>\n      <td>-0.050762</td>\n      <td>0.011343</td>\n      <td>-0.030380</td>\n      <td>-0.054071</td>\n      <td>0.024330</td>\n      <td>-0.004677</td>\n      <td>0.019401</td>\n      <td>0.026332</td>\n    </tr>\n    <tr>\n      <td>UNDERINFL</td>\n      <td>0.039705</td>\n      <td>-0.047527</td>\n      <td>0.005498</td>\n      <td>0.018098</td>\n      <td>0.014795</td>\n      <td>-0.018475</td>\n      <td>-0.011347</td>\n      <td>0.057061</td>\n      <td>-0.030593</td>\n      <td>1.000000</td>\n      <td>-0.033861</td>\n      <td>-0.007447</td>\n      <td>-0.218660</td>\n      <td>-0.019470</td>\n      <td>0.090495</td>\n      <td>-0.006102</td>\n      <td>-0.010661</td>\n      <td>0.022893</td>\n      <td>-0.030735</td>\n    </tr>\n    <tr>\n      <td>WEATHER</td>\n      <td>-0.084248</td>\n      <td>-0.069945</td>\n      <td>0.018963</td>\n      <td>-0.050895</td>\n      <td>-0.004351</td>\n      <td>-0.050059</td>\n      <td>-0.012246</td>\n      <td>0.081328</td>\n      <td>-0.074548</td>\n      <td>-0.033861</td>\n      <td>1.000000</td>\n      <td>0.749529</td>\n      <td>0.140448</td>\n      <td>-0.009420</td>\n      <td>0.051841</td>\n      <td>0.035161</td>\n      <td>-0.000250</td>\n      <td>0.017034</td>\n      <td>-0.027889</td>\n    </tr>\n    <tr>\n      <td>ROADCOND</td>\n      <td>-0.033417</td>\n      <td>-0.018598</td>\n      <td>-0.006616</td>\n      <td>-0.023667</td>\n      <td>0.009657</td>\n      <td>-0.047357</td>\n      <td>-0.017825</td>\n      <td>0.025302</td>\n      <td>-0.050762</td>\n      <td>-0.007447</td>\n      <td>0.749529</td>\n      <td>1.000000</td>\n      <td>-0.017991</td>\n      <td>0.002180</td>\n      <td>0.095767</td>\n      <td>-0.017557</td>\n      <td>0.011714</td>\n      <td>-0.003130</td>\n      <td>-0.023917</td>\n    </tr>\n    <tr>\n      <td>LIGHTCOND</td>\n      <td>-0.036926</td>\n      <td>-0.033325</td>\n      <td>0.025141</td>\n      <td>-0.027323</td>\n      <td>-0.035135</td>\n      <td>0.019001</td>\n      <td>0.034697</td>\n      <td>0.026615</td>\n      <td>0.011343</td>\n      <td>-0.218660</td>\n      <td>0.140448</td>\n      <td>-0.017991</td>\n      <td>1.000000</td>\n      <td>-0.009389</td>\n      <td>-0.097009</td>\n      <td>0.044615</td>\n      <td>-0.018754</td>\n      <td>-0.001216</td>\n      <td>-0.042155</td>\n    </tr>\n    <tr>\n      <td>PEDROWNOTGRNT</td>\n      <td>0.206038</td>\n      <td>0.155258</td>\n      <td>-0.020564</td>\n      <td>-0.031731</td>\n      <td>0.496801</td>\n      <td>0.325585</td>\n      <td>-0.277556</td>\n      <td>-0.153624</td>\n      <td>-0.030380</td>\n      <td>-0.019470</td>\n      <td>-0.009420</td>\n      <td>0.002180</td>\n      <td>-0.009389</td>\n      <td>1.000000</td>\n      <td>-0.030462</td>\n      <td>0.440815</td>\n      <td>0.453206</td>\n      <td>-0.027785</td>\n      <td>0.013348</td>\n    </tr>\n    <tr>\n      <td>SPEEDING</td>\n      <td>0.033914</td>\n      <td>-0.065089</td>\n      <td>-0.002296</td>\n      <td>-0.007835</td>\n      <td>-0.035003</td>\n      <td>-0.022378</td>\n      <td>-0.048845</td>\n      <td>0.067151</td>\n      <td>-0.054071</td>\n      <td>0.090495</td>\n      <td>0.051841</td>\n      <td>0.095767</td>\n      <td>-0.097009</td>\n      <td>-0.030462</td>\n      <td>1.000000</td>\n      <td>-0.083141</td>\n      <td>-0.026746</td>\n      <td>-0.022224</td>\n      <td>-0.033919</td>\n    </tr>\n    <tr>\n      <td>ST_COLDESC</td>\n      <td>0.099013</td>\n      <td>-0.168275</td>\n      <td>0.361238</td>\n      <td>-0.067916</td>\n      <td>0.564382</td>\n      <td>0.357401</td>\n      <td>-0.216368</td>\n      <td>0.172640</td>\n      <td>0.024330</td>\n      <td>-0.006102</td>\n      <td>0.035161</td>\n      <td>-0.017557</td>\n      <td>0.044615</td>\n      <td>0.440815</td>\n      <td>-0.083141</td>\n      <td>1.000000</td>\n      <td>0.404324</td>\n      <td>0.105874</td>\n      <td>0.005503</td>\n    </tr>\n    <tr>\n      <td>CROSSWALKKEY</td>\n      <td>0.172777</td>\n      <td>0.176120</td>\n      <td>0.033517</td>\n      <td>-0.034363</td>\n      <td>0.568736</td>\n      <td>0.109444</td>\n      <td>-0.236850</td>\n      <td>-0.160084</td>\n      <td>-0.004677</td>\n      <td>-0.010661</td>\n      <td>-0.000250</td>\n      <td>0.011714</td>\n      <td>-0.018754</td>\n      <td>0.453206</td>\n      <td>-0.026746</td>\n      <td>0.404324</td>\n      <td>1.000000</td>\n      <td>-0.023644</td>\n      <td>0.029860</td>\n    </tr>\n    <tr>\n      <td>HITPARKEDCAR</td>\n      <td>-0.087120</td>\n      <td>-0.114501</td>\n      <td>0.032658</td>\n      <td>-0.042441</td>\n      <td>-0.031187</td>\n      <td>-0.027379</td>\n      <td>0.073987</td>\n      <td>0.137860</td>\n      <td>0.019401</td>\n      <td>0.022893</td>\n      <td>0.017034</td>\n      <td>-0.003130</td>\n      <td>-0.001216</td>\n      <td>-0.027785</td>\n      <td>-0.022224</td>\n      <td>0.105874</td>\n      <td>-0.023644</td>\n      <td>1.000000</td>\n      <td>0.031115</td>\n    </tr>\n    <tr>\n      <td>HOUROFDAY</td>\n      <td>0.031489</td>\n      <td>0.041482</td>\n      <td>-0.005694</td>\n      <td>0.030907</td>\n      <td>0.025825</td>\n      <td>0.022931</td>\n      <td>0.010129</td>\n      <td>-0.033514</td>\n      <td>0.026332</td>\n      <td>-0.030735</td>\n      <td>-0.027889</td>\n      <td>-0.023917</td>\n      <td>-0.042155</td>\n      <td>0.013348</td>\n      <td>-0.033919</td>\n      <td>0.005503</td>\n      <td>0.029860</td>\n      <td>0.031115</td>\n      <td>1.000000</td>\n    </tr>\n  </tbody>\n</table>\n</div>"
     },
     "metadata": {},
     "execution_count": 15
    }
   ],
   "source": [
    "collision_data_relevant.corr(method='pearson', min_periods=1)"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 16,
   "metadata": {},
   "outputs": [],
   "source": [
    "collision_data_relevant.to_csv('Cleaned-Data-Collisions.csv')\n",
    "collision_data_relevant.head(10).to_csv('Numeric-Cleaned-Data-Collisions.csv')\n",
    "collision_data_relevant.corr(method='pearson', min_periods=1).to_csv('Collision-Data-Correlation.csv')"
   ]
  },
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": [
    "### Data Cleaning Analysis\n",
    "#### Looking closer at the remaining variables that we will use for our model.\n",
    "We have accomiplished our stated goals for cleaning the data. As we build and test our model, we will return to this file to adjust what data we want to utilize, in order to maximize the performance of the model.  \n",
    "We eliminated columns that did not seem to have any bearing on the outcome; latitude/longitude coordinates were irrelevant, as well as the primary/secondary keys that each accident was uniquely assigned. Any component of the analysis that was unique to the incident and was not repeated with any level of meaning was dropped from the dataset. A good example of this is the date, since the date of the incident will bear very little meaning on the severity of the incident itself.  \n",
    "Next, we identified categorical variables that used strings as their values. We chose to include the string version instead of the numeric version in order to create the appropriate list of references for our dataset, thereby making the analysis component much smoother. With the string versions included, and the numeric versions dropped, we then ran a quick for loop to apply integer values to the categorical variables, and replaced the strings with the new numbers. Finally, there were some columns in the dataset that has many \"blank\" values. We assumed that any blank value was a \"null\" value, and that the officer/data entrist simply neglected to fill in the information. The assumption, while potentially slightly flawed, is that the \"importance\" of a variable would have incentivized a data entrist to record in the affirmative, such as in the case of a driver under the influence. If the driver was indeed under the influence, then we can assume that the entrist would have included it in the data. If the driver was not, however, then the entrist may have simply neglected to record the information. Finally, we converted the timestamp provided into buckets by hour, since the approximate time of day might have an impact. While \"LIGHTCONDITIONS\" exists as an independent variable, we also account for driver/pedestrian tiredness by incorporating the hour in the dataset. \n",
    "Now, with our data in numerical integer form, we created a correlation matrix. While some correlation values seem small and otherwise insignificant, we will retain them, as they still might add to our accuracy, and not detract.\n"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 17,
   "metadata": {},
   "outputs": [],
   "source": [
    "import pandas as pd\n",
    "import numpy as np\n",
    "from sklearn.model_selection import train_test_split\n",
    "from sklearn.tree import DecisionTreeClassifier\n",
    "from sklearn import metrics\n",
    "import matplotlib.pyplot as plt\n",
    "from sklearn.metrics import jaccard_similarity_score\n",
    "from sklearn.metrics import f1_score\n",
    "from sklearn import linear_model\n",
    "import plotly.express as px"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 18,
   "metadata": {},
   "outputs": [],
   "source": [
    "#Import csv with cleaned data\n",
    "raw_collision_data = pd.read_csv('Cleaned-Data-Collisions.csv').drop(columns=['Unnamed: 0'])"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 19,
   "metadata": {},
   "outputs": [],
   "source": [
    "#Create the tree\n",
    "y = raw_collision_data['SEVERITYCODE']\n",
    "x = raw_collision_data.drop(columns=['SEVERITYCODE']).values\n",
    "x_trainset, x_testset, y_trainset, y_testset = train_test_split(x, y, test_size=0.25, random_state=3)"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 20,
   "metadata": {},
   "outputs": [
    {
     "output_type": "stream",
     "name": "stdout",
     "text": [
      "DecisionTrees's Accuracy:  0.7403848277995008\n",
      "DecisionTrees's Accuracy:  0.7403848277995008\n",
      "DecisionTrees's Accuracy:  0.7403848277995008\n",
      "DecisionTrees's Accuracy:  0.7420416639052732\n",
      "DecisionTrees's Accuracy:  0.7487131906245168\n",
      "DecisionTrees's Accuracy:  0.7497072922879802\n",
      "DecisionTrees's Accuracy:  0.7504583913225971\n",
      "DecisionTrees's Accuracy:  0.7507234850995206\n",
      "DecisionTrees's Accuracy:  0.7514745841341375\n",
      "DecisionTrees's Accuracy:  0.7515629487264454\n",
      "DecisionTrees's Accuracy:  0.7516954956149071\n",
      "DecisionTrees's Accuracy:  0.7518059513552919\n",
      "DecisionTrees's Accuracy:  0.750480482470674\n",
      "DecisionTrees's Accuracy:  0.74919919588221\n",
      "DecisionTrees's Accuracy:  0.7471226279629752\n",
      "DecisionTrees's Accuracy:  0.7465703492610511\n",
      "DecisionTrees's Accuracy:  0.7457971590783573\n",
      "DecisionTrees's Accuracy:  0.7435438619745068\n",
      "DecisionTrees's Accuracy:  0.7401860074668081\n",
      "DecisionTrees's Accuracy:  0.7359886893321846\n",
      "The best depth was: 12 and the best accuracy was: 0.7518059513552919\n"
     ]
    }
   ],
   "source": [
    "# Creating the decision tree\n",
    "best_depth = 0\n",
    "best_accuracy = 0\n",
    "for depth in range(1, 21):\n",
    "    collisionTree = DecisionTreeClassifier(criterion=\"entropy\", max_depth = depth)\n",
    "    collisionTree.fit(x_trainset,y_trainset)\n",
    "\n",
    "    # Predicting the output using the decision tree\n",
    "    prediction = collisionTree.predict(x_testset)\n",
    "\n",
    "    # Testing the accuracy of the model\n",
    "    print(\"DecisionTrees's Accuracy: \", metrics.accuracy_score(y_testset, prediction))\n",
    "\n",
    "    if (metrics.accuracy_score(y_testset, prediction) > best_accuracy):\n",
    "        best_depth = depth\n",
    "        best_accuracy = metrics.accuracy_score(y_testset, prediction)\n",
    "print(\"The best depth was: {0} and the best accuracy was: {1}\".format(best_depth, best_accuracy))"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 21,
   "metadata": {},
   "outputs": [
    {
     "output_type": "stream",
     "name": "stderr",
     "text": [
      "C:\\Users\\eisen\\Anaconda3\\lib\\site-packages\\sklearn\\metrics\\classification.py:635: DeprecationWarning: jaccard_similarity_score has been deprecated and replaced with jaccard_score. It will be removed in version 0.23. This implementation has surprising behavior for binary and multiclass classification tasks.\n  'and multiclass classification tasks.', DeprecationWarning)\n"
     ]
    }
   ],
   "source": [
    "jaccard = jaccard_similarity_score(y_testset, prediction)\n",
    "f1_score = f1_score(y_testset, prediction, average='weighted')\n",
    "accuracies = ['Score:' ,best_accuracy, jaccard, f1_score]"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 26,
   "metadata": {},
   "outputs": [
    {
     "output_type": "execute_result",
     "data": {
      "text/plain": [
       "        R_Squared  Jaccard_Score  F1_Score\n",
       "                                          \n",
       "Score:   0.751806       0.735989  0.715054"
      ],
      "text/html": "<div>\n<style scoped>\n    .dataframe tbody tr th:only-of-type {\n        vertical-align: middle;\n    }\n\n    .dataframe tbody tr th {\n        vertical-align: top;\n    }\n\n    .dataframe thead th {\n        text-align: right;\n    }\n</style>\n<table border=\"1\" class=\"dataframe\">\n  <thead>\n    <tr style=\"text-align: right;\">\n      <th></th>\n      <th>R_Squared</th>\n      <th>Jaccard_Score</th>\n      <th>F1_Score</th>\n    </tr>\n    <tr>\n      <th></th>\n      <th></th>\n      <th></th>\n      <th></th>\n    </tr>\n  </thead>\n  <tbody>\n    <tr>\n      <td>Score:</td>\n      <td>0.751806</td>\n      <td>0.735989</td>\n      <td>0.715054</td>\n    </tr>\n  </tbody>\n</table>\n</div>"
     },
     "metadata": {},
     "execution_count": 26
    }
   ],
   "source": [
    "scores_df = pd.DataFrame(columns=['','R_Squared','Jaccard_Score','F1_Score'])\n",
    "acc_series = pd.Series(accuracies, index = scores_df.columns)\n",
    "scores_df = scores_df.append(acc_series, ignore_index=True).set_index('')\n",
    "scores_df.to_csv('Scores.csv')\n",
    "scores_df"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 23,
   "metadata": {},
   "outputs": [
    {
     "output_type": "execute_result",
     "data": {
      "text/plain": [
       "        SEVERITYCODE       ADDRTYPE  COLLISIONTYPE    PERSONCOUNT  \\\n",
       "count  181066.000000  181066.000000  181066.000000  181066.000000   \n",
       "mean        1.311665       2.345681       5.478174       2.480913   \n",
       "std         0.463175       0.478301       2.827011       1.375298   \n",
       "min         1.000000       1.000000       1.000000       0.000000   \n",
       "25%         1.000000       2.000000       4.000000       2.000000   \n",
       "50%         1.000000       2.000000       6.000000       2.000000   \n",
       "75%         2.000000       3.000000       8.000000       3.000000   \n",
       "max         2.000000       3.000000      10.000000      81.000000   \n",
       "\n",
       "            PEDCOUNT    PEDCYLCOUNT       VEHCOUNT   JUNCTIONTYPE  \\\n",
       "count  181066.000000  181066.000000  181066.000000  181066.000000   \n",
       "mean        0.038886       0.029785       1.972590       3.710084   \n",
       "std         0.202696       0.171320       0.564807       1.375412   \n",
       "min         0.000000       0.000000       0.000000       1.000000   \n",
       "25%         0.000000       0.000000       2.000000       2.000000   \n",
       "50%         0.000000       0.000000       2.000000       4.000000   \n",
       "75%         0.000000       0.000000       2.000000       5.000000   \n",
       "max         6.000000       2.000000      12.000000       7.000000   \n",
       "\n",
       "       INATTENTIONIND      UNDERINFL        WEATHER       ROADCOND  \\\n",
       "count   181066.000000  181066.000000  181066.000000  181066.000000   \n",
       "mean         0.160047       0.049584       3.927711       3.500149   \n",
       "std          0.366650       0.217085       2.686812       3.632597   \n",
       "min          0.000000       0.000000       1.000000       1.000000   \n",
       "25%          0.000000       0.000000       2.000000       1.000000   \n",
       "50%          0.000000       0.000000       2.000000       1.000000   \n",
       "75%          0.000000       0.000000       5.000000       9.000000   \n",
       "max          1.000000       1.000000      11.000000       9.000000   \n",
       "\n",
       "           LIGHTCOND  PEDROWNOTGRNT       SPEEDING     ST_COLDESC  \\\n",
       "count  181066.000000  181066.000000  181066.000000  181066.000000   \n",
       "mean        5.329885       0.025455       0.050667      19.509411   \n",
       "std         1.652370       0.157502       0.219317      13.014233   \n",
       "min         1.000000       0.000000       0.000000       1.000000   \n",
       "25%         3.000000       0.000000       0.000000       7.000000   \n",
       "50%         6.000000       0.000000       0.000000      18.000000   \n",
       "75%         6.000000       0.000000       0.000000      28.000000   \n",
       "max         9.000000       1.000000       1.000000      62.000000   \n",
       "\n",
       "       CROSSWALKKEY   HITPARKEDCAR      HOUROFDAY  \n",
       "count  1.810660e+05  181066.000000  181066.000000  \n",
       "mean   1.009966e+04       0.028708      11.403781  \n",
       "std    7.343535e+04       0.166984       6.950869  \n",
       "min    0.000000e+00       0.000000       0.000000  \n",
       "25%    0.000000e+00       0.000000       7.000000  \n",
       "50%    0.000000e+00       0.000000      13.000000  \n",
       "75%    0.000000e+00       0.000000      17.000000  \n",
       "max    5.239700e+06       1.000000      23.000000  "
      ],
      "text/html": "<div>\n<style scoped>\n    .dataframe tbody tr th:only-of-type {\n        vertical-align: middle;\n    }\n\n    .dataframe tbody tr th {\n        vertical-align: top;\n    }\n\n    .dataframe thead th {\n        text-align: right;\n    }\n</style>\n<table border=\"1\" class=\"dataframe\">\n  <thead>\n    <tr style=\"text-align: right;\">\n      <th></th>\n      <th>SEVERITYCODE</th>\n      <th>ADDRTYPE</th>\n      <th>COLLISIONTYPE</th>\n      <th>PERSONCOUNT</th>\n      <th>PEDCOUNT</th>\n      <th>PEDCYLCOUNT</th>\n      <th>VEHCOUNT</th>\n      <th>JUNCTIONTYPE</th>\n      <th>INATTENTIONIND</th>\n      <th>UNDERINFL</th>\n      <th>WEATHER</th>\n      <th>ROADCOND</th>\n      <th>LIGHTCOND</th>\n      <th>PEDROWNOTGRNT</th>\n      <th>SPEEDING</th>\n      <th>ST_COLDESC</th>\n      <th>CROSSWALKKEY</th>\n      <th>HITPARKEDCAR</th>\n      <th>HOUROFDAY</th>\n    </tr>\n  </thead>\n  <tbody>\n    <tr>\n      <td>count</td>\n      <td>181066.000000</td>\n      <td>181066.000000</td>\n      <td>181066.000000</td>\n      <td>181066.000000</td>\n      <td>181066.000000</td>\n      <td>181066.000000</td>\n      <td>181066.000000</td>\n      <td>181066.000000</td>\n      <td>181066.000000</td>\n      <td>181066.000000</td>\n      <td>181066.000000</td>\n      <td>181066.000000</td>\n      <td>181066.000000</td>\n      <td>181066.000000</td>\n      <td>181066.000000</td>\n      <td>181066.000000</td>\n      <td>1.810660e+05</td>\n      <td>181066.000000</td>\n      <td>181066.000000</td>\n    </tr>\n    <tr>\n      <td>mean</td>\n      <td>1.311665</td>\n      <td>2.345681</td>\n      <td>5.478174</td>\n      <td>2.480913</td>\n      <td>0.038886</td>\n      <td>0.029785</td>\n      <td>1.972590</td>\n      <td>3.710084</td>\n      <td>0.160047</td>\n      <td>0.049584</td>\n      <td>3.927711</td>\n      <td>3.500149</td>\n      <td>5.329885</td>\n      <td>0.025455</td>\n      <td>0.050667</td>\n      <td>19.509411</td>\n      <td>1.009966e+04</td>\n      <td>0.028708</td>\n      <td>11.403781</td>\n    </tr>\n    <tr>\n      <td>std</td>\n      <td>0.463175</td>\n      <td>0.478301</td>\n      <td>2.827011</td>\n      <td>1.375298</td>\n      <td>0.202696</td>\n      <td>0.171320</td>\n      <td>0.564807</td>\n      <td>1.375412</td>\n      <td>0.366650</td>\n      <td>0.217085</td>\n      <td>2.686812</td>\n      <td>3.632597</td>\n      <td>1.652370</td>\n      <td>0.157502</td>\n      <td>0.219317</td>\n      <td>13.014233</td>\n      <td>7.343535e+04</td>\n      <td>0.166984</td>\n      <td>6.950869</td>\n    </tr>\n    <tr>\n      <td>min</td>\n      <td>1.000000</td>\n      <td>1.000000</td>\n      <td>1.000000</td>\n      <td>0.000000</td>\n      <td>0.000000</td>\n      <td>0.000000</td>\n      <td>0.000000</td>\n      <td>1.000000</td>\n      <td>0.000000</td>\n      <td>0.000000</td>\n      <td>1.000000</td>\n      <td>1.000000</td>\n      <td>1.000000</td>\n      <td>0.000000</td>\n      <td>0.000000</td>\n      <td>1.000000</td>\n      <td>0.000000e+00</td>\n      <td>0.000000</td>\n      <td>0.000000</td>\n    </tr>\n    <tr>\n      <td>25%</td>\n      <td>1.000000</td>\n      <td>2.000000</td>\n      <td>4.000000</td>\n      <td>2.000000</td>\n      <td>0.000000</td>\n      <td>0.000000</td>\n      <td>2.000000</td>\n      <td>2.000000</td>\n      <td>0.000000</td>\n      <td>0.000000</td>\n      <td>2.000000</td>\n      <td>1.000000</td>\n      <td>3.000000</td>\n      <td>0.000000</td>\n      <td>0.000000</td>\n      <td>7.000000</td>\n      <td>0.000000e+00</td>\n      <td>0.000000</td>\n      <td>7.000000</td>\n    </tr>\n    <tr>\n      <td>50%</td>\n      <td>1.000000</td>\n      <td>2.000000</td>\n      <td>6.000000</td>\n      <td>2.000000</td>\n      <td>0.000000</td>\n      <td>0.000000</td>\n      <td>2.000000</td>\n      <td>4.000000</td>\n      <td>0.000000</td>\n      <td>0.000000</td>\n      <td>2.000000</td>\n      <td>1.000000</td>\n      <td>6.000000</td>\n      <td>0.000000</td>\n      <td>0.000000</td>\n      <td>18.000000</td>\n      <td>0.000000e+00</td>\n      <td>0.000000</td>\n      <td>13.000000</td>\n    </tr>\n    <tr>\n      <td>75%</td>\n      <td>2.000000</td>\n      <td>3.000000</td>\n      <td>8.000000</td>\n      <td>3.000000</td>\n      <td>0.000000</td>\n      <td>0.000000</td>\n      <td>2.000000</td>\n      <td>5.000000</td>\n      <td>0.000000</td>\n      <td>0.000000</td>\n      <td>5.000000</td>\n      <td>9.000000</td>\n      <td>6.000000</td>\n      <td>0.000000</td>\n      <td>0.000000</td>\n      <td>28.000000</td>\n      <td>0.000000e+00</td>\n      <td>0.000000</td>\n      <td>17.000000</td>\n    </tr>\n    <tr>\n      <td>max</td>\n      <td>2.000000</td>\n      <td>3.000000</td>\n      <td>10.000000</td>\n      <td>81.000000</td>\n      <td>6.000000</td>\n      <td>2.000000</td>\n      <td>12.000000</td>\n      <td>7.000000</td>\n      <td>1.000000</td>\n      <td>1.000000</td>\n      <td>11.000000</td>\n      <td>9.000000</td>\n      <td>9.000000</td>\n      <td>1.000000</td>\n      <td>1.000000</td>\n      <td>62.000000</td>\n      <td>5.239700e+06</td>\n      <td>1.000000</td>\n      <td>23.000000</td>\n    </tr>\n  </tbody>\n</table>\n</div>"
     },
     "metadata": {},
     "execution_count": 23
    }
   ],
   "source": [
    "raw_collision_data.describe()"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 24,
   "metadata": {},
   "outputs": [
    {
     "output_type": "display_data",
     "data": {
      "text/plain": "<Figure size 720x720 with 1 Axes>",
      "image/svg+xml": "<?xml version=\"1.0\" encoding=\"utf-8\" standalone=\"no\"?>\r\n<!DOCTYPE svg PUBLIC \"-//W3C//DTD SVG 1.1//EN\"\r\n  \"http://www.w3.org/Graphics/SVG/1.1/DTD/svg11.dtd\">\r\n<!-- Created with matplotlib (https://matplotlib.org/) -->\r\n<svg height=\"607.233625pt\" version=\"1.1\" viewBox=\"0 0 633.18875 607.233625\" width=\"633.18875pt\" xmlns=\"http://www.w3.org/2000/svg\" xmlns:xlink=\"http://www.w3.org/1999/xlink\">\r\n <defs>\r\n  <style type=\"text/css\">\r\n*{stroke-linecap:butt;stroke-linejoin:round;}\r\n  </style>\r\n </defs>\r\n <g id=\"figure_1\">\r\n  <g id=\"patch_1\">\r\n   <path d=\"M 0 607.233625 \r\nL 633.18875 607.233625 \r\nL 633.18875 0 \r\nL 0 0 \r\nz\r\n\" style=\"fill:#ffffff;\"/>\r\n  </g>\r\n  <g id=\"axes_1\">\r\n   <g id=\"patch_2\">\r\n    <path d=\"M 67.98875 567.74175 \r\nL 625.98875 567.74175 \r\nL 625.98875 24.14175 \r\nL 67.98875 24.14175 \r\nz\r\n\" style=\"fill:#e5e5e5;\"/>\r\n   </g>\r\n   <g id=\"matplotlib.axis_1\">\r\n    <g id=\"xtick_1\">\r\n     <g id=\"line2d_1\">\r\n      <path clip-path=\"url(#p4bc770188d)\" d=\"M 177.897841 567.74175 \r\nL 177.897841 24.14175 \r\n\" style=\"fill:none;stroke:#ffffff;stroke-linecap:square;stroke-width:0.8;\"/>\r\n     </g>\r\n     <g id=\"line2d_2\">\r\n      <defs>\r\n       <path d=\"M 0 0 \r\nL 0 3.5 \r\n\" id=\"mbb81738b00\" style=\"stroke:#555555;stroke-width:0.8;\"/>\r\n      </defs>\r\n      <g>\r\n       <use style=\"fill:#555555;stroke:#555555;stroke-width:0.8;\" x=\"177.897841\" xlink:href=\"#mbb81738b00\" y=\"567.74175\"/>\r\n      </g>\r\n     </g>\r\n     <g id=\"text_1\">\r\n      <!-- Property Damage Only Collision -->\r\n      <defs>\r\n       <path d=\"M 19.671875 64.796875 \r\nL 19.671875 37.40625 \r\nL 32.078125 37.40625 \r\nQ 38.96875 37.40625 42.71875 40.96875 \r\nQ 46.484375 44.53125 46.484375 51.125 \r\nQ 46.484375 57.671875 42.71875 61.234375 \r\nQ 38.96875 64.796875 32.078125 64.796875 \r\nz\r\nM 9.8125 72.90625 \r\nL 32.078125 72.90625 \r\nQ 44.34375 72.90625 50.609375 67.359375 \r\nQ 56.890625 61.8125 56.890625 51.125 \r\nQ 56.890625 40.328125 50.609375 34.8125 \r\nQ 44.34375 29.296875 32.078125 29.296875 \r\nL 19.671875 29.296875 \r\nL 19.671875 0 \r\nL 9.8125 0 \r\nz\r\n\" id=\"DejaVuSans-80\"/>\r\n       <path d=\"M 41.109375 46.296875 \r\nQ 39.59375 47.171875 37.8125 47.578125 \r\nQ 36.03125 48 33.890625 48 \r\nQ 26.265625 48 22.1875 43.046875 \r\nQ 18.109375 38.09375 18.109375 28.8125 \r\nL 18.109375 0 \r\nL 9.078125 0 \r\nL 9.078125 54.6875 \r\nL 18.109375 54.6875 \r\nL 18.109375 46.1875 \r\nQ 20.953125 51.171875 25.484375 53.578125 \r\nQ 30.03125 56 36.53125 56 \r\nQ 37.453125 56 38.578125 55.875 \r\nQ 39.703125 55.765625 41.0625 55.515625 \r\nz\r\n\" id=\"DejaVuSans-114\"/>\r\n       <path d=\"M 30.609375 48.390625 \r\nQ 23.390625 48.390625 19.1875 42.75 \r\nQ 14.984375 37.109375 14.984375 27.296875 \r\nQ 14.984375 17.484375 19.15625 11.84375 \r\nQ 23.34375 6.203125 30.609375 6.203125 \r\nQ 37.796875 6.203125 41.984375 11.859375 \r\nQ 46.1875 17.53125 46.1875 27.296875 \r\nQ 46.1875 37.015625 41.984375 42.703125 \r\nQ 37.796875 48.390625 30.609375 48.390625 \r\nz\r\nM 30.609375 56 \r\nQ 42.328125 56 49.015625 48.375 \r\nQ 55.71875 40.765625 55.71875 27.296875 \r\nQ 55.71875 13.875 49.015625 6.21875 \r\nQ 42.328125 -1.421875 30.609375 -1.421875 \r\nQ 18.84375 -1.421875 12.171875 6.21875 \r\nQ 5.515625 13.875 5.515625 27.296875 \r\nQ 5.515625 40.765625 12.171875 48.375 \r\nQ 18.84375 56 30.609375 56 \r\nz\r\n\" id=\"DejaVuSans-111\"/>\r\n       <path d=\"M 18.109375 8.203125 \r\nL 18.109375 -20.796875 \r\nL 9.078125 -20.796875 \r\nL 9.078125 54.6875 \r\nL 18.109375 54.6875 \r\nL 18.109375 46.390625 \r\nQ 20.953125 51.265625 25.265625 53.625 \r\nQ 29.59375 56 35.59375 56 \r\nQ 45.5625 56 51.78125 48.09375 \r\nQ 58.015625 40.1875 58.015625 27.296875 \r\nQ 58.015625 14.40625 51.78125 6.484375 \r\nQ 45.5625 -1.421875 35.59375 -1.421875 \r\nQ 29.59375 -1.421875 25.265625 0.953125 \r\nQ 20.953125 3.328125 18.109375 8.203125 \r\nz\r\nM 48.6875 27.296875 \r\nQ 48.6875 37.203125 44.609375 42.84375 \r\nQ 40.53125 48.484375 33.40625 48.484375 \r\nQ 26.265625 48.484375 22.1875 42.84375 \r\nQ 18.109375 37.203125 18.109375 27.296875 \r\nQ 18.109375 17.390625 22.1875 11.75 \r\nQ 26.265625 6.109375 33.40625 6.109375 \r\nQ 40.53125 6.109375 44.609375 11.75 \r\nQ 48.6875 17.390625 48.6875 27.296875 \r\nz\r\n\" id=\"DejaVuSans-112\"/>\r\n       <path d=\"M 56.203125 29.59375 \r\nL 56.203125 25.203125 \r\nL 14.890625 25.203125 \r\nQ 15.484375 15.921875 20.484375 11.0625 \r\nQ 25.484375 6.203125 34.421875 6.203125 \r\nQ 39.59375 6.203125 44.453125 7.46875 \r\nQ 49.3125 8.734375 54.109375 11.28125 \r\nL 54.109375 2.78125 \r\nQ 49.265625 0.734375 44.1875 -0.34375 \r\nQ 39.109375 -1.421875 33.890625 -1.421875 \r\nQ 20.796875 -1.421875 13.15625 6.1875 \r\nQ 5.515625 13.8125 5.515625 26.8125 \r\nQ 5.515625 40.234375 12.765625 48.109375 \r\nQ 20.015625 56 32.328125 56 \r\nQ 43.359375 56 49.78125 48.890625 \r\nQ 56.203125 41.796875 56.203125 29.59375 \r\nz\r\nM 47.21875 32.234375 \r\nQ 47.125 39.59375 43.09375 43.984375 \r\nQ 39.0625 48.390625 32.421875 48.390625 \r\nQ 24.90625 48.390625 20.390625 44.140625 \r\nQ 15.875 39.890625 15.1875 32.171875 \r\nz\r\n\" id=\"DejaVuSans-101\"/>\r\n       <path d=\"M 18.3125 70.21875 \r\nL 18.3125 54.6875 \r\nL 36.8125 54.6875 \r\nL 36.8125 47.703125 \r\nL 18.3125 47.703125 \r\nL 18.3125 18.015625 \r\nQ 18.3125 11.328125 20.140625 9.421875 \r\nQ 21.96875 7.515625 27.59375 7.515625 \r\nL 36.8125 7.515625 \r\nL 36.8125 0 \r\nL 27.59375 0 \r\nQ 17.1875 0 13.234375 3.875 \r\nQ 9.28125 7.765625 9.28125 18.015625 \r\nL 9.28125 47.703125 \r\nL 2.6875 47.703125 \r\nL 2.6875 54.6875 \r\nL 9.28125 54.6875 \r\nL 9.28125 70.21875 \r\nz\r\n\" id=\"DejaVuSans-116\"/>\r\n       <path d=\"M 32.171875 -5.078125 \r\nQ 28.375 -14.84375 24.75 -17.8125 \r\nQ 21.140625 -20.796875 15.09375 -20.796875 \r\nL 7.90625 -20.796875 \r\nL 7.90625 -13.28125 \r\nL 13.1875 -13.28125 \r\nQ 16.890625 -13.28125 18.9375 -11.515625 \r\nQ 21 -9.765625 23.484375 -3.21875 \r\nL 25.09375 0.875 \r\nL 2.984375 54.6875 \r\nL 12.5 54.6875 \r\nL 29.59375 11.921875 \r\nL 46.6875 54.6875 \r\nL 56.203125 54.6875 \r\nz\r\n\" id=\"DejaVuSans-121\"/>\r\n       <path id=\"DejaVuSans-32\"/>\r\n       <path d=\"M 19.671875 64.796875 \r\nL 19.671875 8.109375 \r\nL 31.59375 8.109375 \r\nQ 46.6875 8.109375 53.6875 14.9375 \r\nQ 60.6875 21.78125 60.6875 36.53125 \r\nQ 60.6875 51.171875 53.6875 57.984375 \r\nQ 46.6875 64.796875 31.59375 64.796875 \r\nz\r\nM 9.8125 72.90625 \r\nL 30.078125 72.90625 \r\nQ 51.265625 72.90625 61.171875 64.09375 \r\nQ 71.09375 55.28125 71.09375 36.53125 \r\nQ 71.09375 17.671875 61.125 8.828125 \r\nQ 51.171875 0 30.078125 0 \r\nL 9.8125 0 \r\nz\r\n\" id=\"DejaVuSans-68\"/>\r\n       <path d=\"M 34.28125 27.484375 \r\nQ 23.390625 27.484375 19.1875 25 \r\nQ 14.984375 22.515625 14.984375 16.5 \r\nQ 14.984375 11.71875 18.140625 8.90625 \r\nQ 21.296875 6.109375 26.703125 6.109375 \r\nQ 34.1875 6.109375 38.703125 11.40625 \r\nQ 43.21875 16.703125 43.21875 25.484375 \r\nL 43.21875 27.484375 \r\nz\r\nM 52.203125 31.203125 \r\nL 52.203125 0 \r\nL 43.21875 0 \r\nL 43.21875 8.296875 \r\nQ 40.140625 3.328125 35.546875 0.953125 \r\nQ 30.953125 -1.421875 24.3125 -1.421875 \r\nQ 15.921875 -1.421875 10.953125 3.296875 \r\nQ 6 8.015625 6 15.921875 \r\nQ 6 25.140625 12.171875 29.828125 \r\nQ 18.359375 34.515625 30.609375 34.515625 \r\nL 43.21875 34.515625 \r\nL 43.21875 35.40625 \r\nQ 43.21875 41.609375 39.140625 45 \r\nQ 35.0625 48.390625 27.6875 48.390625 \r\nQ 23 48.390625 18.546875 47.265625 \r\nQ 14.109375 46.140625 10.015625 43.890625 \r\nL 10.015625 52.203125 \r\nQ 14.9375 54.109375 19.578125 55.046875 \r\nQ 24.21875 56 28.609375 56 \r\nQ 40.484375 56 46.34375 49.84375 \r\nQ 52.203125 43.703125 52.203125 31.203125 \r\nz\r\n\" id=\"DejaVuSans-97\"/>\r\n       <path d=\"M 52 44.1875 \r\nQ 55.375 50.25 60.0625 53.125 \r\nQ 64.75 56 71.09375 56 \r\nQ 79.640625 56 84.28125 50.015625 \r\nQ 88.921875 44.046875 88.921875 33.015625 \r\nL 88.921875 0 \r\nL 79.890625 0 \r\nL 79.890625 32.71875 \r\nQ 79.890625 40.578125 77.09375 44.375 \r\nQ 74.3125 48.1875 68.609375 48.1875 \r\nQ 61.625 48.1875 57.5625 43.546875 \r\nQ 53.515625 38.921875 53.515625 30.90625 \r\nL 53.515625 0 \r\nL 44.484375 0 \r\nL 44.484375 32.71875 \r\nQ 44.484375 40.625 41.703125 44.40625 \r\nQ 38.921875 48.1875 33.109375 48.1875 \r\nQ 26.21875 48.1875 22.15625 43.53125 \r\nQ 18.109375 38.875 18.109375 30.90625 \r\nL 18.109375 0 \r\nL 9.078125 0 \r\nL 9.078125 54.6875 \r\nL 18.109375 54.6875 \r\nL 18.109375 46.1875 \r\nQ 21.1875 51.21875 25.484375 53.609375 \r\nQ 29.78125 56 35.6875 56 \r\nQ 41.65625 56 45.828125 52.96875 \r\nQ 50 49.953125 52 44.1875 \r\nz\r\n\" id=\"DejaVuSans-109\"/>\r\n       <path d=\"M 45.40625 27.984375 \r\nQ 45.40625 37.75 41.375 43.109375 \r\nQ 37.359375 48.484375 30.078125 48.484375 \r\nQ 22.859375 48.484375 18.828125 43.109375 \r\nQ 14.796875 37.75 14.796875 27.984375 \r\nQ 14.796875 18.265625 18.828125 12.890625 \r\nQ 22.859375 7.515625 30.078125 7.515625 \r\nQ 37.359375 7.515625 41.375 12.890625 \r\nQ 45.40625 18.265625 45.40625 27.984375 \r\nz\r\nM 54.390625 6.78125 \r\nQ 54.390625 -7.171875 48.1875 -13.984375 \r\nQ 42 -20.796875 29.203125 -20.796875 \r\nQ 24.46875 -20.796875 20.265625 -20.09375 \r\nQ 16.0625 -19.390625 12.109375 -17.921875 \r\nL 12.109375 -9.1875 \r\nQ 16.0625 -11.328125 19.921875 -12.34375 \r\nQ 23.78125 -13.375 27.78125 -13.375 \r\nQ 36.625 -13.375 41.015625 -8.765625 \r\nQ 45.40625 -4.15625 45.40625 5.171875 \r\nL 45.40625 9.625 \r\nQ 42.625 4.78125 38.28125 2.390625 \r\nQ 33.9375 0 27.875 0 \r\nQ 17.828125 0 11.671875 7.65625 \r\nQ 5.515625 15.328125 5.515625 27.984375 \r\nQ 5.515625 40.671875 11.671875 48.328125 \r\nQ 17.828125 56 27.875 56 \r\nQ 33.9375 56 38.28125 53.609375 \r\nQ 42.625 51.21875 45.40625 46.390625 \r\nL 45.40625 54.6875 \r\nL 54.390625 54.6875 \r\nz\r\n\" id=\"DejaVuSans-103\"/>\r\n       <path d=\"M 39.40625 66.21875 \r\nQ 28.65625 66.21875 22.328125 58.203125 \r\nQ 16.015625 50.203125 16.015625 36.375 \r\nQ 16.015625 22.609375 22.328125 14.59375 \r\nQ 28.65625 6.59375 39.40625 6.59375 \r\nQ 50.140625 6.59375 56.421875 14.59375 \r\nQ 62.703125 22.609375 62.703125 36.375 \r\nQ 62.703125 50.203125 56.421875 58.203125 \r\nQ 50.140625 66.21875 39.40625 66.21875 \r\nz\r\nM 39.40625 74.21875 \r\nQ 54.734375 74.21875 63.90625 63.9375 \r\nQ 73.09375 53.65625 73.09375 36.375 \r\nQ 73.09375 19.140625 63.90625 8.859375 \r\nQ 54.734375 -1.421875 39.40625 -1.421875 \r\nQ 24.03125 -1.421875 14.8125 8.828125 \r\nQ 5.609375 19.09375 5.609375 36.375 \r\nQ 5.609375 53.65625 14.8125 63.9375 \r\nQ 24.03125 74.21875 39.40625 74.21875 \r\nz\r\n\" id=\"DejaVuSans-79\"/>\r\n       <path d=\"M 54.890625 33.015625 \r\nL 54.890625 0 \r\nL 45.90625 0 \r\nL 45.90625 32.71875 \r\nQ 45.90625 40.484375 42.875 44.328125 \r\nQ 39.84375 48.1875 33.796875 48.1875 \r\nQ 26.515625 48.1875 22.3125 43.546875 \r\nQ 18.109375 38.921875 18.109375 30.90625 \r\nL 18.109375 0 \r\nL 9.078125 0 \r\nL 9.078125 54.6875 \r\nL 18.109375 54.6875 \r\nL 18.109375 46.1875 \r\nQ 21.34375 51.125 25.703125 53.5625 \r\nQ 30.078125 56 35.796875 56 \r\nQ 45.21875 56 50.046875 50.171875 \r\nQ 54.890625 44.34375 54.890625 33.015625 \r\nz\r\n\" id=\"DejaVuSans-110\"/>\r\n       <path d=\"M 9.421875 75.984375 \r\nL 18.40625 75.984375 \r\nL 18.40625 0 \r\nL 9.421875 0 \r\nz\r\n\" id=\"DejaVuSans-108\"/>\r\n       <path d=\"M 64.40625 67.28125 \r\nL 64.40625 56.890625 \r\nQ 59.421875 61.53125 53.78125 63.8125 \r\nQ 48.140625 66.109375 41.796875 66.109375 \r\nQ 29.296875 66.109375 22.65625 58.46875 \r\nQ 16.015625 50.828125 16.015625 36.375 \r\nQ 16.015625 21.96875 22.65625 14.328125 \r\nQ 29.296875 6.6875 41.796875 6.6875 \r\nQ 48.140625 6.6875 53.78125 8.984375 \r\nQ 59.421875 11.28125 64.40625 15.921875 \r\nL 64.40625 5.609375 \r\nQ 59.234375 2.09375 53.4375 0.328125 \r\nQ 47.65625 -1.421875 41.21875 -1.421875 \r\nQ 24.65625 -1.421875 15.125 8.703125 \r\nQ 5.609375 18.84375 5.609375 36.375 \r\nQ 5.609375 53.953125 15.125 64.078125 \r\nQ 24.65625 74.21875 41.21875 74.21875 \r\nQ 47.75 74.21875 53.53125 72.484375 \r\nQ 59.328125 70.75 64.40625 67.28125 \r\nz\r\n\" id=\"DejaVuSans-67\"/>\r\n       <path d=\"M 9.421875 54.6875 \r\nL 18.40625 54.6875 \r\nL 18.40625 0 \r\nL 9.421875 0 \r\nz\r\nM 9.421875 75.984375 \r\nL 18.40625 75.984375 \r\nL 18.40625 64.59375 \r\nL 9.421875 64.59375 \r\nz\r\n\" id=\"DejaVuSans-105\"/>\r\n       <path d=\"M 44.28125 53.078125 \r\nL 44.28125 44.578125 \r\nQ 40.484375 46.53125 36.375 47.5 \r\nQ 32.28125 48.484375 27.875 48.484375 \r\nQ 21.1875 48.484375 17.84375 46.4375 \r\nQ 14.5 44.390625 14.5 40.28125 \r\nQ 14.5 37.15625 16.890625 35.375 \r\nQ 19.28125 33.59375 26.515625 31.984375 \r\nL 29.59375 31.296875 \r\nQ 39.15625 29.25 43.1875 25.515625 \r\nQ 47.21875 21.78125 47.21875 15.09375 \r\nQ 47.21875 7.46875 41.1875 3.015625 \r\nQ 35.15625 -1.421875 24.609375 -1.421875 \r\nQ 20.21875 -1.421875 15.453125 -0.5625 \r\nQ 10.6875 0.296875 5.421875 2 \r\nL 5.421875 11.28125 \r\nQ 10.40625 8.6875 15.234375 7.390625 \r\nQ 20.0625 6.109375 24.8125 6.109375 \r\nQ 31.15625 6.109375 34.5625 8.28125 \r\nQ 37.984375 10.453125 37.984375 14.40625 \r\nQ 37.984375 18.0625 35.515625 20.015625 \r\nQ 33.0625 21.96875 24.703125 23.78125 \r\nL 21.578125 24.515625 \r\nQ 13.234375 26.265625 9.515625 29.90625 \r\nQ 5.8125 33.546875 5.8125 39.890625 \r\nQ 5.8125 47.609375 11.28125 51.796875 \r\nQ 16.75 56 26.8125 56 \r\nQ 31.78125 56 36.171875 55.265625 \r\nQ 40.578125 54.546875 44.28125 53.078125 \r\nz\r\n\" id=\"DejaVuSans-115\"/>\r\n      </defs>\r\n      <g style=\"fill:#555555;\" transform=\"translate(98.285341 582.340187)scale(0.1 -0.1)\">\r\n       <use xlink:href=\"#DejaVuSans-80\"/>\r\n       <use x=\"60.287109\" xlink:href=\"#DejaVuSans-114\"/>\r\n       <use x=\"101.369141\" xlink:href=\"#DejaVuSans-111\"/>\r\n       <use x=\"162.550781\" xlink:href=\"#DejaVuSans-112\"/>\r\n       <use x=\"226.027344\" xlink:href=\"#DejaVuSans-101\"/>\r\n       <use x=\"287.550781\" xlink:href=\"#DejaVuSans-114\"/>\r\n       <use x=\"328.664062\" xlink:href=\"#DejaVuSans-116\"/>\r\n       <use x=\"367.873047\" xlink:href=\"#DejaVuSans-121\"/>\r\n       <use x=\"427.052734\" xlink:href=\"#DejaVuSans-32\"/>\r\n       <use x=\"458.839844\" xlink:href=\"#DejaVuSans-68\"/>\r\n       <use x=\"535.841797\" xlink:href=\"#DejaVuSans-97\"/>\r\n       <use x=\"597.121094\" xlink:href=\"#DejaVuSans-109\"/>\r\n       <use x=\"694.533203\" xlink:href=\"#DejaVuSans-97\"/>\r\n       <use x=\"755.8125\" xlink:href=\"#DejaVuSans-103\"/>\r\n       <use x=\"819.289062\" xlink:href=\"#DejaVuSans-101\"/>\r\n       <use x=\"880.8125\" xlink:href=\"#DejaVuSans-32\"/>\r\n       <use x=\"912.599609\" xlink:href=\"#DejaVuSans-79\"/>\r\n       <use x=\"991.310547\" xlink:href=\"#DejaVuSans-110\"/>\r\n       <use x=\"1054.689453\" xlink:href=\"#DejaVuSans-108\"/>\r\n       <use x=\"1082.472656\" xlink:href=\"#DejaVuSans-121\"/>\r\n       <use x=\"1141.652344\" xlink:href=\"#DejaVuSans-32\"/>\r\n       <use x=\"1173.439453\" xlink:href=\"#DejaVuSans-67\"/>\r\n       <use x=\"1243.263672\" xlink:href=\"#DejaVuSans-111\"/>\r\n       <use x=\"1304.445312\" xlink:href=\"#DejaVuSans-108\"/>\r\n       <use x=\"1332.228516\" xlink:href=\"#DejaVuSans-108\"/>\r\n       <use x=\"1360.011719\" xlink:href=\"#DejaVuSans-105\"/>\r\n       <use x=\"1387.794922\" xlink:href=\"#DejaVuSans-115\"/>\r\n       <use x=\"1439.894531\" xlink:href=\"#DejaVuSans-105\"/>\r\n       <use x=\"1467.677734\" xlink:href=\"#DejaVuSans-111\"/>\r\n       <use x=\"1528.859375\" xlink:href=\"#DejaVuSans-110\"/>\r\n      </g>\r\n     </g>\r\n    </g>\r\n    <g id=\"xtick_2\">\r\n     <g id=\"line2d_3\">\r\n      <path clip-path=\"url(#p4bc770188d)\" d=\"M 516.079659 567.74175 \r\nL 516.079659 24.14175 \r\n\" style=\"fill:none;stroke:#ffffff;stroke-linecap:square;stroke-width:0.8;\"/>\r\n     </g>\r\n     <g id=\"line2d_4\">\r\n      <g>\r\n       <use style=\"fill:#555555;stroke:#555555;stroke-width:0.8;\" x=\"516.079659\" xlink:href=\"#mbb81738b00\" y=\"567.74175\"/>\r\n      </g>\r\n     </g>\r\n     <g id=\"text_2\">\r\n      <!-- Injury Collision -->\r\n      <defs>\r\n       <path d=\"M 9.8125 72.90625 \r\nL 19.671875 72.90625 \r\nL 19.671875 0 \r\nL 9.8125 0 \r\nz\r\n\" id=\"DejaVuSans-73\"/>\r\n       <path d=\"M 9.421875 54.6875 \r\nL 18.40625 54.6875 \r\nL 18.40625 -0.984375 \r\nQ 18.40625 -11.421875 14.421875 -16.109375 \r\nQ 10.453125 -20.796875 1.609375 -20.796875 \r\nL -1.8125 -20.796875 \r\nL -1.8125 -13.1875 \r\nL 0.59375 -13.1875 \r\nQ 5.71875 -13.1875 7.5625 -10.8125 \r\nQ 9.421875 -8.453125 9.421875 -0.984375 \r\nz\r\nM 9.421875 75.984375 \r\nL 18.40625 75.984375 \r\nL 18.40625 64.59375 \r\nL 9.421875 64.59375 \r\nz\r\n\" id=\"DejaVuSans-106\"/>\r\n       <path d=\"M 8.5 21.578125 \r\nL 8.5 54.6875 \r\nL 17.484375 54.6875 \r\nL 17.484375 21.921875 \r\nQ 17.484375 14.15625 20.5 10.265625 \r\nQ 23.53125 6.390625 29.59375 6.390625 \r\nQ 36.859375 6.390625 41.078125 11.03125 \r\nQ 45.3125 15.671875 45.3125 23.6875 \r\nL 45.3125 54.6875 \r\nL 54.296875 54.6875 \r\nL 54.296875 0 \r\nL 45.3125 0 \r\nL 45.3125 8.40625 \r\nQ 42.046875 3.421875 37.71875 1 \r\nQ 33.40625 -1.421875 27.6875 -1.421875 \r\nQ 18.265625 -1.421875 13.375 4.4375 \r\nQ 8.5 10.296875 8.5 21.578125 \r\nz\r\nM 31.109375 56 \r\nz\r\n\" id=\"DejaVuSans-117\"/>\r\n      </defs>\r\n      <g style=\"fill:#555555;\" transform=\"translate(479.334347 582.340187)scale(0.1 -0.1)\">\r\n       <use xlink:href=\"#DejaVuSans-73\"/>\r\n       <use x=\"29.492188\" xlink:href=\"#DejaVuSans-110\"/>\r\n       <use x=\"92.871094\" xlink:href=\"#DejaVuSans-106\"/>\r\n       <use x=\"120.654297\" xlink:href=\"#DejaVuSans-117\"/>\r\n       <use x=\"184.033203\" xlink:href=\"#DejaVuSans-114\"/>\r\n       <use x=\"225.146484\" xlink:href=\"#DejaVuSans-121\"/>\r\n       <use x=\"284.326172\" xlink:href=\"#DejaVuSans-32\"/>\r\n       <use x=\"316.113281\" xlink:href=\"#DejaVuSans-67\"/>\r\n       <use x=\"385.9375\" xlink:href=\"#DejaVuSans-111\"/>\r\n       <use x=\"447.119141\" xlink:href=\"#DejaVuSans-108\"/>\r\n       <use x=\"474.902344\" xlink:href=\"#DejaVuSans-108\"/>\r\n       <use x=\"502.685547\" xlink:href=\"#DejaVuSans-105\"/>\r\n       <use x=\"530.46875\" xlink:href=\"#DejaVuSans-115\"/>\r\n       <use x=\"582.568359\" xlink:href=\"#DejaVuSans-105\"/>\r\n       <use x=\"610.351562\" xlink:href=\"#DejaVuSans-111\"/>\r\n       <use x=\"671.533203\" xlink:href=\"#DejaVuSans-110\"/>\r\n      </g>\r\n     </g>\r\n    </g>\r\n    <g id=\"text_3\">\r\n     <!-- Type of Incident -->\r\n     <defs>\r\n      <path d=\"M -0.296875 72.90625 \r\nL 61.375 72.90625 \r\nL 61.375 64.59375 \r\nL 35.5 64.59375 \r\nL 35.5 0 \r\nL 25.59375 0 \r\nL 25.59375 64.59375 \r\nL -0.296875 64.59375 \r\nz\r\n\" id=\"DejaVuSans-84\"/>\r\n      <path d=\"M 37.109375 75.984375 \r\nL 37.109375 68.5 \r\nL 28.515625 68.5 \r\nQ 23.6875 68.5 21.796875 66.546875 \r\nQ 19.921875 64.59375 19.921875 59.515625 \r\nL 19.921875 54.6875 \r\nL 34.71875 54.6875 \r\nL 34.71875 47.703125 \r\nL 19.921875 47.703125 \r\nL 19.921875 0 \r\nL 10.890625 0 \r\nL 10.890625 47.703125 \r\nL 2.296875 47.703125 \r\nL 2.296875 54.6875 \r\nL 10.890625 54.6875 \r\nL 10.890625 58.5 \r\nQ 10.890625 67.625 15.140625 71.796875 \r\nQ 19.390625 75.984375 28.609375 75.984375 \r\nz\r\n\" id=\"DejaVuSans-102\"/>\r\n      <path d=\"M 48.78125 52.59375 \r\nL 48.78125 44.1875 \r\nQ 44.96875 46.296875 41.140625 47.34375 \r\nQ 37.3125 48.390625 33.40625 48.390625 \r\nQ 24.65625 48.390625 19.8125 42.84375 \r\nQ 14.984375 37.3125 14.984375 27.296875 \r\nQ 14.984375 17.28125 19.8125 11.734375 \r\nQ 24.65625 6.203125 33.40625 6.203125 \r\nQ 37.3125 6.203125 41.140625 7.25 \r\nQ 44.96875 8.296875 48.78125 10.40625 \r\nL 48.78125 2.09375 \r\nQ 45.015625 0.34375 40.984375 -0.53125 \r\nQ 36.96875 -1.421875 32.421875 -1.421875 \r\nQ 20.0625 -1.421875 12.78125 6.34375 \r\nQ 5.515625 14.109375 5.515625 27.296875 \r\nQ 5.515625 40.671875 12.859375 48.328125 \r\nQ 20.21875 56 33.015625 56 \r\nQ 37.15625 56 41.109375 55.140625 \r\nQ 45.0625 54.296875 48.78125 52.59375 \r\nz\r\n\" id=\"DejaVuSans-99\"/>\r\n      <path d=\"M 45.40625 46.390625 \r\nL 45.40625 75.984375 \r\nL 54.390625 75.984375 \r\nL 54.390625 0 \r\nL 45.40625 0 \r\nL 45.40625 8.203125 \r\nQ 42.578125 3.328125 38.25 0.953125 \r\nQ 33.9375 -1.421875 27.875 -1.421875 \r\nQ 17.96875 -1.421875 11.734375 6.484375 \r\nQ 5.515625 14.40625 5.515625 27.296875 \r\nQ 5.515625 40.1875 11.734375 48.09375 \r\nQ 17.96875 56 27.875 56 \r\nQ 33.9375 56 38.25 53.625 \r\nQ 42.578125 51.265625 45.40625 46.390625 \r\nz\r\nM 14.796875 27.296875 \r\nQ 14.796875 17.390625 18.875 11.75 \r\nQ 22.953125 6.109375 30.078125 6.109375 \r\nQ 37.203125 6.109375 41.296875 11.75 \r\nQ 45.40625 17.390625 45.40625 27.296875 \r\nQ 45.40625 37.203125 41.296875 42.84375 \r\nQ 37.203125 48.484375 30.078125 48.484375 \r\nQ 22.953125 48.484375 18.875 42.84375 \r\nQ 14.796875 37.203125 14.796875 27.296875 \r\nz\r\n\" id=\"DejaVuSans-100\"/>\r\n     </defs>\r\n     <g style=\"fill:#555555;\" transform=\"translate(298.494687 597.538)scale(0.12 -0.12)\">\r\n      <use xlink:href=\"#DejaVuSans-84\"/>\r\n      <use x=\"60.849609\" xlink:href=\"#DejaVuSans-121\"/>\r\n      <use x=\"120.029297\" xlink:href=\"#DejaVuSans-112\"/>\r\n      <use x=\"183.505859\" xlink:href=\"#DejaVuSans-101\"/>\r\n      <use x=\"245.029297\" xlink:href=\"#DejaVuSans-32\"/>\r\n      <use x=\"276.816406\" xlink:href=\"#DejaVuSans-111\"/>\r\n      <use x=\"337.998047\" xlink:href=\"#DejaVuSans-102\"/>\r\n      <use x=\"373.203125\" xlink:href=\"#DejaVuSans-32\"/>\r\n      <use x=\"404.990234\" xlink:href=\"#DejaVuSans-73\"/>\r\n      <use x=\"434.482422\" xlink:href=\"#DejaVuSans-110\"/>\r\n      <use x=\"497.861328\" xlink:href=\"#DejaVuSans-99\"/>\r\n      <use x=\"552.841797\" xlink:href=\"#DejaVuSans-105\"/>\r\n      <use x=\"580.625\" xlink:href=\"#DejaVuSans-100\"/>\r\n      <use x=\"644.101562\" xlink:href=\"#DejaVuSans-101\"/>\r\n      <use x=\"705.625\" xlink:href=\"#DejaVuSans-110\"/>\r\n      <use x=\"769.003906\" xlink:href=\"#DejaVuSans-116\"/>\r\n     </g>\r\n    </g>\r\n   </g>\r\n   <g id=\"matplotlib.axis_2\">\r\n    <g id=\"ytick_1\">\r\n     <g id=\"line2d_5\">\r\n      <path clip-path=\"url(#p4bc770188d)\" d=\"M 67.98875 567.74175 \r\nL 625.98875 567.74175 \r\n\" style=\"fill:none;stroke:#ffffff;stroke-linecap:square;stroke-width:0.8;\"/>\r\n     </g>\r\n     <g id=\"line2d_6\">\r\n      <defs>\r\n       <path d=\"M 0 0 \r\nL -3.5 0 \r\n\" id=\"m570fe79ed4\" style=\"stroke:#555555;stroke-width:0.8;\"/>\r\n      </defs>\r\n      <g>\r\n       <use style=\"fill:#555555;stroke:#555555;stroke-width:0.8;\" x=\"67.98875\" xlink:href=\"#m570fe79ed4\" y=\"567.74175\"/>\r\n      </g>\r\n     </g>\r\n     <g id=\"text_4\">\r\n      <!-- 0 -->\r\n      <defs>\r\n       <path d=\"M 31.78125 66.40625 \r\nQ 24.171875 66.40625 20.328125 58.90625 \r\nQ 16.5 51.421875 16.5 36.375 \r\nQ 16.5 21.390625 20.328125 13.890625 \r\nQ 24.171875 6.390625 31.78125 6.390625 \r\nQ 39.453125 6.390625 43.28125 13.890625 \r\nQ 47.125 21.390625 47.125 36.375 \r\nQ 47.125 51.421875 43.28125 58.90625 \r\nQ 39.453125 66.40625 31.78125 66.40625 \r\nz\r\nM 31.78125 74.21875 \r\nQ 44.046875 74.21875 50.515625 64.515625 \r\nQ 56.984375 54.828125 56.984375 36.375 \r\nQ 56.984375 17.96875 50.515625 8.265625 \r\nQ 44.046875 -1.421875 31.78125 -1.421875 \r\nQ 19.53125 -1.421875 13.0625 8.265625 \r\nQ 6.59375 17.96875 6.59375 36.375 \r\nQ 6.59375 54.828125 13.0625 64.515625 \r\nQ 19.53125 74.21875 31.78125 74.21875 \r\nz\r\n\" id=\"DejaVuSans-48\"/>\r\n      </defs>\r\n      <g style=\"fill:#555555;\" transform=\"translate(54.62625 571.540969)scale(0.1 -0.1)\">\r\n       <use xlink:href=\"#DejaVuSans-48\"/>\r\n      </g>\r\n     </g>\r\n    </g>\r\n    <g id=\"ytick_2\">\r\n     <g id=\"line2d_7\">\r\n      <path clip-path=\"url(#p4bc770188d)\" d=\"M 67.98875 484.664213 \r\nL 625.98875 484.664213 \r\n\" style=\"fill:none;stroke:#ffffff;stroke-linecap:square;stroke-width:0.8;\"/>\r\n     </g>\r\n     <g id=\"line2d_8\">\r\n      <g>\r\n       <use style=\"fill:#555555;stroke:#555555;stroke-width:0.8;\" x=\"67.98875\" xlink:href=\"#m570fe79ed4\" y=\"484.664213\"/>\r\n      </g>\r\n     </g>\r\n     <g id=\"text_5\">\r\n      <!-- 20000 -->\r\n      <defs>\r\n       <path d=\"M 19.1875 8.296875 \r\nL 53.609375 8.296875 \r\nL 53.609375 0 \r\nL 7.328125 0 \r\nL 7.328125 8.296875 \r\nQ 12.9375 14.109375 22.625 23.890625 \r\nQ 32.328125 33.6875 34.8125 36.53125 \r\nQ 39.546875 41.84375 41.421875 45.53125 \r\nQ 43.3125 49.21875 43.3125 52.78125 \r\nQ 43.3125 58.59375 39.234375 62.25 \r\nQ 35.15625 65.921875 28.609375 65.921875 \r\nQ 23.96875 65.921875 18.8125 64.3125 \r\nQ 13.671875 62.703125 7.8125 59.421875 \r\nL 7.8125 69.390625 \r\nQ 13.765625 71.78125 18.9375 73 \r\nQ 24.125 74.21875 28.421875 74.21875 \r\nQ 39.75 74.21875 46.484375 68.546875 \r\nQ 53.21875 62.890625 53.21875 53.421875 \r\nQ 53.21875 48.921875 51.53125 44.890625 \r\nQ 49.859375 40.875 45.40625 35.40625 \r\nQ 44.1875 33.984375 37.640625 27.21875 \r\nQ 31.109375 20.453125 19.1875 8.296875 \r\nz\r\n\" id=\"DejaVuSans-50\"/>\r\n      </defs>\r\n      <g style=\"fill:#555555;\" transform=\"translate(29.17625 488.463432)scale(0.1 -0.1)\">\r\n       <use xlink:href=\"#DejaVuSans-50\"/>\r\n       <use x=\"63.623047\" xlink:href=\"#DejaVuSans-48\"/>\r\n       <use x=\"127.246094\" xlink:href=\"#DejaVuSans-48\"/>\r\n       <use x=\"190.869141\" xlink:href=\"#DejaVuSans-48\"/>\r\n       <use x=\"254.492188\" xlink:href=\"#DejaVuSans-48\"/>\r\n      </g>\r\n     </g>\r\n    </g>\r\n    <g id=\"ytick_3\">\r\n     <g id=\"line2d_9\">\r\n      <path clip-path=\"url(#p4bc770188d)\" d=\"M 67.98875 401.586677 \r\nL 625.98875 401.586677 \r\n\" style=\"fill:none;stroke:#ffffff;stroke-linecap:square;stroke-width:0.8;\"/>\r\n     </g>\r\n     <g id=\"line2d_10\">\r\n      <g>\r\n       <use style=\"fill:#555555;stroke:#555555;stroke-width:0.8;\" x=\"67.98875\" xlink:href=\"#m570fe79ed4\" y=\"401.586677\"/>\r\n      </g>\r\n     </g>\r\n     <g id=\"text_6\">\r\n      <!-- 40000 -->\r\n      <defs>\r\n       <path d=\"M 37.796875 64.3125 \r\nL 12.890625 25.390625 \r\nL 37.796875 25.390625 \r\nz\r\nM 35.203125 72.90625 \r\nL 47.609375 72.90625 \r\nL 47.609375 25.390625 \r\nL 58.015625 25.390625 \r\nL 58.015625 17.1875 \r\nL 47.609375 17.1875 \r\nL 47.609375 0 \r\nL 37.796875 0 \r\nL 37.796875 17.1875 \r\nL 4.890625 17.1875 \r\nL 4.890625 26.703125 \r\nz\r\n\" id=\"DejaVuSans-52\"/>\r\n      </defs>\r\n      <g style=\"fill:#555555;\" transform=\"translate(29.17625 405.385895)scale(0.1 -0.1)\">\r\n       <use xlink:href=\"#DejaVuSans-52\"/>\r\n       <use x=\"63.623047\" xlink:href=\"#DejaVuSans-48\"/>\r\n       <use x=\"127.246094\" xlink:href=\"#DejaVuSans-48\"/>\r\n       <use x=\"190.869141\" xlink:href=\"#DejaVuSans-48\"/>\r\n       <use x=\"254.492188\" xlink:href=\"#DejaVuSans-48\"/>\r\n      </g>\r\n     </g>\r\n    </g>\r\n    <g id=\"ytick_4\">\r\n     <g id=\"line2d_11\">\r\n      <path clip-path=\"url(#p4bc770188d)\" d=\"M 67.98875 318.50914 \r\nL 625.98875 318.50914 \r\n\" style=\"fill:none;stroke:#ffffff;stroke-linecap:square;stroke-width:0.8;\"/>\r\n     </g>\r\n     <g id=\"line2d_12\">\r\n      <g>\r\n       <use style=\"fill:#555555;stroke:#555555;stroke-width:0.8;\" x=\"67.98875\" xlink:href=\"#m570fe79ed4\" y=\"318.50914\"/>\r\n      </g>\r\n     </g>\r\n     <g id=\"text_7\">\r\n      <!-- 60000 -->\r\n      <defs>\r\n       <path d=\"M 33.015625 40.375 \r\nQ 26.375 40.375 22.484375 35.828125 \r\nQ 18.609375 31.296875 18.609375 23.390625 \r\nQ 18.609375 15.53125 22.484375 10.953125 \r\nQ 26.375 6.390625 33.015625 6.390625 \r\nQ 39.65625 6.390625 43.53125 10.953125 \r\nQ 47.40625 15.53125 47.40625 23.390625 \r\nQ 47.40625 31.296875 43.53125 35.828125 \r\nQ 39.65625 40.375 33.015625 40.375 \r\nz\r\nM 52.59375 71.296875 \r\nL 52.59375 62.3125 \r\nQ 48.875 64.0625 45.09375 64.984375 \r\nQ 41.3125 65.921875 37.59375 65.921875 \r\nQ 27.828125 65.921875 22.671875 59.328125 \r\nQ 17.53125 52.734375 16.796875 39.40625 \r\nQ 19.671875 43.65625 24.015625 45.921875 \r\nQ 28.375 48.1875 33.59375 48.1875 \r\nQ 44.578125 48.1875 50.953125 41.515625 \r\nQ 57.328125 34.859375 57.328125 23.390625 \r\nQ 57.328125 12.15625 50.6875 5.359375 \r\nQ 44.046875 -1.421875 33.015625 -1.421875 \r\nQ 20.359375 -1.421875 13.671875 8.265625 \r\nQ 6.984375 17.96875 6.984375 36.375 \r\nQ 6.984375 53.65625 15.1875 63.9375 \r\nQ 23.390625 74.21875 37.203125 74.21875 \r\nQ 40.921875 74.21875 44.703125 73.484375 \r\nQ 48.484375 72.75 52.59375 71.296875 \r\nz\r\n\" id=\"DejaVuSans-54\"/>\r\n      </defs>\r\n      <g style=\"fill:#555555;\" transform=\"translate(29.17625 322.308359)scale(0.1 -0.1)\">\r\n       <use xlink:href=\"#DejaVuSans-54\"/>\r\n       <use x=\"63.623047\" xlink:href=\"#DejaVuSans-48\"/>\r\n       <use x=\"127.246094\" xlink:href=\"#DejaVuSans-48\"/>\r\n       <use x=\"190.869141\" xlink:href=\"#DejaVuSans-48\"/>\r\n       <use x=\"254.492188\" xlink:href=\"#DejaVuSans-48\"/>\r\n      </g>\r\n     </g>\r\n    </g>\r\n    <g id=\"ytick_5\">\r\n     <g id=\"line2d_13\">\r\n      <path clip-path=\"url(#p4bc770188d)\" d=\"M 67.98875 235.431603 \r\nL 625.98875 235.431603 \r\n\" style=\"fill:none;stroke:#ffffff;stroke-linecap:square;stroke-width:0.8;\"/>\r\n     </g>\r\n     <g id=\"line2d_14\">\r\n      <g>\r\n       <use style=\"fill:#555555;stroke:#555555;stroke-width:0.8;\" x=\"67.98875\" xlink:href=\"#m570fe79ed4\" y=\"235.431603\"/>\r\n      </g>\r\n     </g>\r\n     <g id=\"text_8\">\r\n      <!-- 80000 -->\r\n      <defs>\r\n       <path d=\"M 31.78125 34.625 \r\nQ 24.75 34.625 20.71875 30.859375 \r\nQ 16.703125 27.09375 16.703125 20.515625 \r\nQ 16.703125 13.921875 20.71875 10.15625 \r\nQ 24.75 6.390625 31.78125 6.390625 \r\nQ 38.8125 6.390625 42.859375 10.171875 \r\nQ 46.921875 13.96875 46.921875 20.515625 \r\nQ 46.921875 27.09375 42.890625 30.859375 \r\nQ 38.875 34.625 31.78125 34.625 \r\nz\r\nM 21.921875 38.8125 \r\nQ 15.578125 40.375 12.03125 44.71875 \r\nQ 8.5 49.078125 8.5 55.328125 \r\nQ 8.5 64.0625 14.71875 69.140625 \r\nQ 20.953125 74.21875 31.78125 74.21875 \r\nQ 42.671875 74.21875 48.875 69.140625 \r\nQ 55.078125 64.0625 55.078125 55.328125 \r\nQ 55.078125 49.078125 51.53125 44.71875 \r\nQ 48 40.375 41.703125 38.8125 \r\nQ 48.828125 37.15625 52.796875 32.3125 \r\nQ 56.78125 27.484375 56.78125 20.515625 \r\nQ 56.78125 9.90625 50.3125 4.234375 \r\nQ 43.84375 -1.421875 31.78125 -1.421875 \r\nQ 19.734375 -1.421875 13.25 4.234375 \r\nQ 6.78125 9.90625 6.78125 20.515625 \r\nQ 6.78125 27.484375 10.78125 32.3125 \r\nQ 14.796875 37.15625 21.921875 38.8125 \r\nz\r\nM 18.3125 54.390625 \r\nQ 18.3125 48.734375 21.84375 45.5625 \r\nQ 25.390625 42.390625 31.78125 42.390625 \r\nQ 38.140625 42.390625 41.71875 45.5625 \r\nQ 45.3125 48.734375 45.3125 54.390625 \r\nQ 45.3125 60.0625 41.71875 63.234375 \r\nQ 38.140625 66.40625 31.78125 66.40625 \r\nQ 25.390625 66.40625 21.84375 63.234375 \r\nQ 18.3125 60.0625 18.3125 54.390625 \r\nz\r\n\" id=\"DejaVuSans-56\"/>\r\n      </defs>\r\n      <g style=\"fill:#555555;\" transform=\"translate(29.17625 239.230822)scale(0.1 -0.1)\">\r\n       <use xlink:href=\"#DejaVuSans-56\"/>\r\n       <use x=\"63.623047\" xlink:href=\"#DejaVuSans-48\"/>\r\n       <use x=\"127.246094\" xlink:href=\"#DejaVuSans-48\"/>\r\n       <use x=\"190.869141\" xlink:href=\"#DejaVuSans-48\"/>\r\n       <use x=\"254.492188\" xlink:href=\"#DejaVuSans-48\"/>\r\n      </g>\r\n     </g>\r\n    </g>\r\n    <g id=\"ytick_6\">\r\n     <g id=\"line2d_15\">\r\n      <path clip-path=\"url(#p4bc770188d)\" d=\"M 67.98875 152.354066 \r\nL 625.98875 152.354066 \r\n\" style=\"fill:none;stroke:#ffffff;stroke-linecap:square;stroke-width:0.8;\"/>\r\n     </g>\r\n     <g id=\"line2d_16\">\r\n      <g>\r\n       <use style=\"fill:#555555;stroke:#555555;stroke-width:0.8;\" x=\"67.98875\" xlink:href=\"#m570fe79ed4\" y=\"152.354066\"/>\r\n      </g>\r\n     </g>\r\n     <g id=\"text_9\">\r\n      <!-- 100000 -->\r\n      <defs>\r\n       <path d=\"M 12.40625 8.296875 \r\nL 28.515625 8.296875 \r\nL 28.515625 63.921875 \r\nL 10.984375 60.40625 \r\nL 10.984375 69.390625 \r\nL 28.421875 72.90625 \r\nL 38.28125 72.90625 \r\nL 38.28125 8.296875 \r\nL 54.390625 8.296875 \r\nL 54.390625 0 \r\nL 12.40625 0 \r\nz\r\n\" id=\"DejaVuSans-49\"/>\r\n      </defs>\r\n      <g style=\"fill:#555555;\" transform=\"translate(22.81375 156.153285)scale(0.1 -0.1)\">\r\n       <use xlink:href=\"#DejaVuSans-49\"/>\r\n       <use x=\"63.623047\" xlink:href=\"#DejaVuSans-48\"/>\r\n       <use x=\"127.246094\" xlink:href=\"#DejaVuSans-48\"/>\r\n       <use x=\"190.869141\" xlink:href=\"#DejaVuSans-48\"/>\r\n       <use x=\"254.492188\" xlink:href=\"#DejaVuSans-48\"/>\r\n       <use x=\"318.115234\" xlink:href=\"#DejaVuSans-48\"/>\r\n      </g>\r\n     </g>\r\n    </g>\r\n    <g id=\"ytick_7\">\r\n     <g id=\"line2d_17\">\r\n      <path clip-path=\"url(#p4bc770188d)\" d=\"M 67.98875 69.27653 \r\nL 625.98875 69.27653 \r\n\" style=\"fill:none;stroke:#ffffff;stroke-linecap:square;stroke-width:0.8;\"/>\r\n     </g>\r\n     <g id=\"line2d_18\">\r\n      <g>\r\n       <use style=\"fill:#555555;stroke:#555555;stroke-width:0.8;\" x=\"67.98875\" xlink:href=\"#m570fe79ed4\" y=\"69.27653\"/>\r\n      </g>\r\n     </g>\r\n     <g id=\"text_10\">\r\n      <!-- 120000 -->\r\n      <g style=\"fill:#555555;\" transform=\"translate(22.81375 73.075748)scale(0.1 -0.1)\">\r\n       <use xlink:href=\"#DejaVuSans-49\"/>\r\n       <use x=\"63.623047\" xlink:href=\"#DejaVuSans-50\"/>\r\n       <use x=\"127.246094\" xlink:href=\"#DejaVuSans-48\"/>\r\n       <use x=\"190.869141\" xlink:href=\"#DejaVuSans-48\"/>\r\n       <use x=\"254.492188\" xlink:href=\"#DejaVuSans-48\"/>\r\n       <use x=\"318.115234\" xlink:href=\"#DejaVuSans-48\"/>\r\n      </g>\r\n     </g>\r\n    </g>\r\n    <g id=\"text_11\">\r\n     <!-- Count of Occurrence -->\r\n     <g style=\"fill:#555555;\" transform=\"translate(16.318125 357.896437)rotate(-90)scale(0.12 -0.12)\">\r\n      <use xlink:href=\"#DejaVuSans-67\"/>\r\n      <use x=\"69.824219\" xlink:href=\"#DejaVuSans-111\"/>\r\n      <use x=\"131.005859\" xlink:href=\"#DejaVuSans-117\"/>\r\n      <use x=\"194.384766\" xlink:href=\"#DejaVuSans-110\"/>\r\n      <use x=\"257.763672\" xlink:href=\"#DejaVuSans-116\"/>\r\n      <use x=\"296.972656\" xlink:href=\"#DejaVuSans-32\"/>\r\n      <use x=\"328.759766\" xlink:href=\"#DejaVuSans-111\"/>\r\n      <use x=\"389.941406\" xlink:href=\"#DejaVuSans-102\"/>\r\n      <use x=\"425.146484\" xlink:href=\"#DejaVuSans-32\"/>\r\n      <use x=\"456.933594\" xlink:href=\"#DejaVuSans-79\"/>\r\n      <use x=\"535.644531\" xlink:href=\"#DejaVuSans-99\"/>\r\n      <use x=\"590.625\" xlink:href=\"#DejaVuSans-99\"/>\r\n      <use x=\"645.605469\" xlink:href=\"#DejaVuSans-117\"/>\r\n      <use x=\"708.984375\" xlink:href=\"#DejaVuSans-114\"/>\r\n      <use x=\"750.082031\" xlink:href=\"#DejaVuSans-114\"/>\r\n      <use x=\"791.164062\" xlink:href=\"#DejaVuSans-101\"/>\r\n      <use x=\"852.6875\" xlink:href=\"#DejaVuSans-110\"/>\r\n      <use x=\"916.066406\" xlink:href=\"#DejaVuSans-99\"/>\r\n      <use x=\"971.046875\" xlink:href=\"#DejaVuSans-101\"/>\r\n     </g>\r\n    </g>\r\n   </g>\r\n   <g id=\"patch_3\">\r\n    <path clip-path=\"url(#p4bc770188d)\" d=\"M 93.352386 567.74175 \r\nL 262.443295 567.74175 \r\nL 262.443295 50.027464 \r\nL 93.352386 50.027464 \r\nz\r\n\" style=\"fill:#0000ff;\"/>\r\n   </g>\r\n   <g id=\"patch_4\">\r\n    <path clip-path=\"url(#p4bc770188d)\" d=\"M 431.534205 567.74175 \r\nL 600.625114 567.74175 \r\nL 600.625114 333.330172 \r\nL 431.534205 333.330172 \r\nz\r\n\" style=\"fill:#0000ff;\"/>\r\n   </g>\r\n   <g id=\"patch_5\">\r\n    <path d=\"M 67.98875 567.74175 \r\nL 67.98875 24.14175 \r\n\" style=\"fill:none;stroke:#ffffff;stroke-linecap:square;stroke-linejoin:miter;\"/>\r\n   </g>\r\n   <g id=\"patch_6\">\r\n    <path d=\"M 625.98875 567.74175 \r\nL 625.98875 24.14175 \r\n\" style=\"fill:none;stroke:#ffffff;stroke-linecap:square;stroke-linejoin:miter;\"/>\r\n   </g>\r\n   <g id=\"patch_7\">\r\n    <path d=\"M 67.98875 567.74175 \r\nL 625.98875 567.74175 \r\n\" style=\"fill:none;stroke:#ffffff;stroke-linecap:square;stroke-linejoin:miter;\"/>\r\n   </g>\r\n   <g id=\"patch_8\">\r\n    <path d=\"M 67.98875 24.14175 \r\nL 625.98875 24.14175 \r\n\" style=\"fill:none;stroke:#ffffff;stroke-linecap:square;stroke-linejoin:miter;\"/>\r\n   </g>\r\n   <g id=\"text_12\">\r\n    <!-- Total Count of Each Collision Type -->\r\n    <defs>\r\n     <path d=\"M 9.8125 72.90625 \r\nL 55.90625 72.90625 \r\nL 55.90625 64.59375 \r\nL 19.671875 64.59375 \r\nL 19.671875 43.015625 \r\nL 54.390625 43.015625 \r\nL 54.390625 34.71875 \r\nL 19.671875 34.71875 \r\nL 19.671875 8.296875 \r\nL 56.78125 8.296875 \r\nL 56.78125 0 \r\nL 9.8125 0 \r\nz\r\n\" id=\"DejaVuSans-69\"/>\r\n     <path d=\"M 54.890625 33.015625 \r\nL 54.890625 0 \r\nL 45.90625 0 \r\nL 45.90625 32.71875 \r\nQ 45.90625 40.484375 42.875 44.328125 \r\nQ 39.84375 48.1875 33.796875 48.1875 \r\nQ 26.515625 48.1875 22.3125 43.546875 \r\nQ 18.109375 38.921875 18.109375 30.90625 \r\nL 18.109375 0 \r\nL 9.078125 0 \r\nL 9.078125 75.984375 \r\nL 18.109375 75.984375 \r\nL 18.109375 46.1875 \r\nQ 21.34375 51.125 25.703125 53.5625 \r\nQ 30.078125 56 35.796875 56 \r\nQ 45.21875 56 50.046875 50.171875 \r\nQ 54.890625 44.34375 54.890625 33.015625 \r\nz\r\n\" id=\"DejaVuSans-104\"/>\r\n    </defs>\r\n    <g transform=\"translate(223.926125 18.14175)scale(0.144 -0.144)\">\r\n     <use xlink:href=\"#DejaVuSans-84\"/>\r\n     <use x=\"60.818359\" xlink:href=\"#DejaVuSans-111\"/>\r\n     <use x=\"122\" xlink:href=\"#DejaVuSans-116\"/>\r\n     <use x=\"161.208984\" xlink:href=\"#DejaVuSans-97\"/>\r\n     <use x=\"222.488281\" xlink:href=\"#DejaVuSans-108\"/>\r\n     <use x=\"250.271484\" xlink:href=\"#DejaVuSans-32\"/>\r\n     <use x=\"282.058594\" xlink:href=\"#DejaVuSans-67\"/>\r\n     <use x=\"351.882812\" xlink:href=\"#DejaVuSans-111\"/>\r\n     <use x=\"413.064453\" xlink:href=\"#DejaVuSans-117\"/>\r\n     <use x=\"476.443359\" xlink:href=\"#DejaVuSans-110\"/>\r\n     <use x=\"539.822266\" xlink:href=\"#DejaVuSans-116\"/>\r\n     <use x=\"579.03125\" xlink:href=\"#DejaVuSans-32\"/>\r\n     <use x=\"610.818359\" xlink:href=\"#DejaVuSans-111\"/>\r\n     <use x=\"672\" xlink:href=\"#DejaVuSans-102\"/>\r\n     <use x=\"707.205078\" xlink:href=\"#DejaVuSans-32\"/>\r\n     <use x=\"738.992188\" xlink:href=\"#DejaVuSans-69\"/>\r\n     <use x=\"802.175781\" xlink:href=\"#DejaVuSans-97\"/>\r\n     <use x=\"863.455078\" xlink:href=\"#DejaVuSans-99\"/>\r\n     <use x=\"918.435547\" xlink:href=\"#DejaVuSans-104\"/>\r\n     <use x=\"981.814453\" xlink:href=\"#DejaVuSans-32\"/>\r\n     <use x=\"1013.601562\" xlink:href=\"#DejaVuSans-67\"/>\r\n     <use x=\"1083.425781\" xlink:href=\"#DejaVuSans-111\"/>\r\n     <use x=\"1144.607422\" xlink:href=\"#DejaVuSans-108\"/>\r\n     <use x=\"1172.390625\" xlink:href=\"#DejaVuSans-108\"/>\r\n     <use x=\"1200.173828\" xlink:href=\"#DejaVuSans-105\"/>\r\n     <use x=\"1227.957031\" xlink:href=\"#DejaVuSans-115\"/>\r\n     <use x=\"1280.056641\" xlink:href=\"#DejaVuSans-105\"/>\r\n     <use x=\"1307.839844\" xlink:href=\"#DejaVuSans-111\"/>\r\n     <use x=\"1369.021484\" xlink:href=\"#DejaVuSans-110\"/>\r\n     <use x=\"1432.400391\" xlink:href=\"#DejaVuSans-32\"/>\r\n     <use x=\"1464.1875\" xlink:href=\"#DejaVuSans-84\"/>\r\n     <use x=\"1525.037109\" xlink:href=\"#DejaVuSans-121\"/>\r\n     <use x=\"1584.216797\" xlink:href=\"#DejaVuSans-112\"/>\r\n     <use x=\"1647.693359\" xlink:href=\"#DejaVuSans-101\"/>\r\n    </g>\r\n   </g>\r\n  </g>\r\n </g>\r\n <defs>\r\n  <clipPath id=\"p4bc770188d\">\r\n   <rect height=\"543.6\" width=\"558\" x=\"67.98875\" y=\"24.14175\"/>\r\n  </clipPath>\r\n </defs>\r\n</svg>\r\n",
      "image/png": "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fS95vD8WFRUlPz8/bdy4scryTZs2eXSG7ZXatGmTbr31Vj311FMaMGCAevTooYMHD7pvt9ls6tevn9avX1+v93vLLbcoKipKL7/8crU/k5MnT8rlcnn0XLpa0dHR+s1vfqP169fr/vvv15IlS6pdz5Pnibc98cQTWrFihf74xz/K399fd9999yXrXHypIsuylJGR4d5bFxsbq71796pdu3aXRH9DnGEMeIrQA5qB3r17a9SoUZo0aZJSU1P1zTffKCkpSbm5uXrmmWcknb98RWBgoNavX6/vv//efVB7z549tXr1an355ZfatWuXJk6cqMLCwiu6/9atW2vp0qVat26d7rjjDq1fv14HDhzQV199pVdeeUW33367JGn48OGKjo7Wz3/+c23ZskU7d+7UAw88IEnujypvvPFGRUREaPr06dq7d682btyo//zP/7zin4nNZtMNN9ygtLQ05efnq6ioqNr12rZtqyeffFLPP/+81qxZo5ycHM2YMUPr16+v9eSG2hQVFenYsWNV/pw6dUrS+Z/39u3b9dFHHyk3N1evvfbaJdewmz59ulavXq1nn31WO3fu1J49e5SSkqL9+/df1TzS+T2l77zzjvbt26f4+Hj9/e9/1759+/TNN99o0aJF6tu3r8rKyjx6Ll2p3bt3a9q0adq8ebO+/fZbbd68WVu2bFGvXr2qXd+T54m33XnnnQoLC9O0adP08MMPV3soQ3JyslavXq29e/fqmWee0Z49ezR58mRJ0n/8x3+oTZs2GjVqlP71r3/p0KFD2rJli2bMmKF//vOfDfIYAI80xoGBAKrn6eVV/P39L7kkhmVZ1pIlS6wbbrjB8vX1dV9e5cCBA9bQoUOtoKAg67rrrrP+8Ic/WA888ECVS4h4ciKCZVnW9u3brfHjx1sdOnSwWrRoYV1//fXWuHHjrM2bN7vX+e6776y7777bfdmMIUOGWFlZWZc8zptuuskKDAy0YmJi3I/7xydj/PgyJpGRkdbLL7/s/vrvf/+7FRUVZbVo0cKjy6tcmPvHl1fx9GdwYa7q/jzzzDPu+5owYYLVtm1bKyQkxHrooYesOXPmXDLfP/7xD+vmm2+2AgICrDZt2lhDhw695PIqF1uyZEmtj/GC3Nxc67HHHrM6depk+fv7WxEREdbw4cOrnNRwuefSlZ6McfjwYWv06NFWRESE+z5/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uvEo9F5//XWFh4fr4YcfVkBAgLdnAgAAQD3wKPSOHDmiP/zhD/LxadRfpAEAAIAr4FG53XjjjTp06JCXRwEAAEB98miPXrt27TRz5kzdcsstatu2bZXbxo8f75XBAACoDb9hyFv4udanxv4tQx6FXmlpqQYMGKDKykoVFRV5eyYAAADUA49CLykpydtzAAAAoJ55FHoXfhVadcLDw+ttGAAAANQfj0Lv4l+F9mMXfnsGAAAAmhaPQu/HMXf8+HH99a9/1Y033uiVoQAAAFB3V3VhvLZt2+rRRx/VX/7yl/qeBwAAAPXkqq+AnJeXp9LS0vqcBQAAAPXIo49up0+fLpvN5v66tLRU3333ncaNG+e1wQAAAFA3HoXe0KFDq3wdGBioG264Qdddd51XhgIAAEDdeRR6CQkJXh4DAAAA9c2j0KuoqNDq1au1adMmFRcXy263a9CgQRo7dqz8/DzaBAAAABqYR5W2fPly7d+/X48//rjatWunH374QR988IHOnDmjRx991MsjAgAA4Gp4FHoZGRl69dVX1bp1a0lSRESEunTpomeffZbQAwAAaKI8uryKZVnengMAAAD1zKM9egMHDtQrr7yicePGKSwsTIWFhfrggw80cOBAb88HAACAq+RR6D344IP64IMPlJKSouLiYoWGhio+Pl533323t+cDAADAVbJZfC5brby8PK9uPzIywqvbB+rq6FHvvgaAuuJ9FM1BQ7yXRkTU/Fqo9Ri9PXv2aPny5dXe9u677yonJ6dukwEAAMBrag29NWvWqFevXtXe1qtXL61evdorQwEAAKDuag29Q4cOKSYmptrboqOjdfDgQa8MBQAAgLqrNfTOnj2rioqKam+rrKzU2bNnvTIUAAAA6q7W0IuMjNSOHTuqvW3Hjh2KjIz0ylAAAACou1pDb8SIEfqf//kfffHFF3K5XJIkl8ulL774QkuWLNGIESMaZEgAAABcuVqvo3fbbbfp+PHjWrhwocrLyxUSEqKTJ0/K399f99xzj2677baGmhMAAABX6LIXTB45cqSGDh2qnJwclZSUKDg4WFFRUQoKCmqI+QAAAHCVPPrNGEFBQTWefQsAAICmqdZj9AAAANB8EXoAAACGIvQAAAAMRegBAAAYitADAAAwFKEHAABgKEIPAADAUIQeAACAoQg9AAAAQxF6AAAAhiL0AAAADEXo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\n"
     },
     "metadata": {}
    }
   ],
   "source": [
    "filename = 'SeverityCounts.png'\n",
    "plt.style.use('ggplot')\n",
    "plt.figure(figsize=(10,10))\n",
    "sev = ['Property Damage Only Collision', 'Injury Collision']\n",
    "sev_counts = [raw_collision_data['SEVERITYCODE'].value_counts()[i] for i in range(1,len(raw_collision_data['SEVERITYCODE'].value_counts().to_list())+1)]\n",
    "\n",
    "\n",
    "plt.bar(sev, sev_counts, color='blue', width=.5)\n",
    "plt.xlabel(\"Type of Incident\")\n",
    "plt.ylabel(\"Count of Occurrence\")\n",
    "plt.title(\"Total Count of Each Collision Type\")\n",
    "\n",
    "plt.xticks(sev)\n",
    "plt.savefig(filename)\n",
    "plt.show()"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 25,
   "metadata": {},
   "outputs": [
    {
     "output_type": "display_data",
     "data": {
      "application/vnd.plotly.v1+json": {
       "config": {
        "plotlyServerURL": "https://plot.ly"
       },
       "data": [
        {
         "alignmentgroup": "True",
         "hovertemplate": "Classification of Incident=%{x}<br># of Occurrences=%{y}<extra></extra>",
         "legendgroup": "",
         "marker": {
          "color": "#636efa"
         },
         "name": "",
         "offsetgroup": "",
         "orientation": "v",
         "showlegend": false,
         "textposition": "auto",
         "type": "bar",
         "x": [
          "Property Damage Only Collision",
          "Injury Collision"
         ],
         "xaxis": "x",
         "y": [
          124634,
          56432
         ],
         "yaxis": "y"
        }
       ],
       "layout": {
        "barmode": "relative",
        "legend": {
         "tracegroupgap": 0
        },
        "template": {
         "data": {
          "bar": [
           {
            "error_x": {
             "color": "#2a3f5f"
            },
            "error_y": {
             "color": "#2a3f5f"
            },
            "marker": {
             "line": {
              "color": "#E5ECF6",
              "width": 0.5
             }
            },
            "type": "bar"
           }
          ],
          "barpolar": [
           {
            "marker": {
             "line": {
              "color": "#E5ECF6",
              "width": 0.5
             }
            },
            "type": "barpolar"
           }
          ],
          "carpet": [
           {
            "aaxis": {
             "endlinecolor": "#2a3f5f",
             "gridcolor": "white",
             "linecolor": "white",
             "minorgridcolor": "white",
             "startlinecolor": "#2a3f5f"
            },
            "baxis": {
             "endlinecolor": "#2a3f5f",
             "gridcolor": "white",
             "linecolor": "white",
             "minorgridcolor": "white",
             "startlinecolor": "#2a3f5f"
            },
            "type": "carpet"
           }
          ],
          "choropleth": [
           {
            "colorbar": {
             "outlinewidth": 0,
             "ticks": ""
            },
            "type": "choropleth"
           }
          ],
          "contour": [
           {
            "colorbar": {
             "outlinewidth": 0,
             "ticks": ""
            },
            "colorscale": [
             [
              0,
              "#0d0887"
             ],
             [
              0.1111111111111111,
              "#46039f"
             ],
             [
              0.2222222222222222,
              "#7201a8"
             ],
             [
              0.3333333333333333,
              "#9c179e"
             ],
             [
              0.4444444444444444,
              "#bd3786"
             ],
             [
              0.5555555555555556,
              "#d8576b"
             ],
             [
              0.6666666666666666,
              "#ed7953"
             ],
             [
              0.7777777777777778,
              "#fb9f3a"
             ],
             [
              0.8888888888888888,
              "#fdca26"
             ],
             [
              1,
              "#f0f921"
             ]
            ],
            "type": "contour"
           }
          ],
          "contourcarpet": [
           {
            "colorbar": {
             "outlinewidth": 0,
             "ticks": ""
            },
            "type": "contourcarpet"
           }
          ],
          "heatmap": [
           {
            "colorbar": {
             "outlinewidth": 0,
             "ticks": ""
            },
            "colorscale": [
             [
              0,
              "#0d0887"
             ],
             [
              0.1111111111111111,
              "#46039f"
             ],
             [
              0.2222222222222222,
              "#7201a8"
             ],
             [
              0.3333333333333333,
              "#9c179e"
             ],
             [
              0.4444444444444444,
              "#bd3786"
             ],
             [
              0.5555555555555556,
              "#d8576b"
             ],
             [
              0.6666666666666666,
              "#ed7953"
             ],
             [
              0.7777777777777778,
              "#fb9f3a"
             ],
             [
              0.8888888888888888,
              "#fdca26"
             ],
             [
              1,
              "#f0f921"
             ]
            ],
            "type": "heatmap"
           }
          ],
          "heatmapgl": [
           {
            "colorbar": {
             "outlinewidth": 0,
             "ticks": ""
            },
            "colorscale": [
             [
              0,
              "#0d0887"
             ],
             [
              0.1111111111111111,
              "#46039f"
             ],
             [
              0.2222222222222222,
              "#7201a8"
             ],
             [
              0.3333333333333333,
              "#9c179e"
             ],
             [
              0.4444444444444444,
              "#bd3786"
             ],
             [
              0.5555555555555556,
              "#d8576b"
             ],
             [
              0.6666666666666666,
              "#ed7953"
             ],
             [
              0.7777777777777778,
              "#fb9f3a"
             ],
             [
              0.8888888888888888,
              "#fdca26"
             ],
             [
              1,
              "#f0f921"
             ]
            ],
            "type": "heatmapgl"
           }
          ],
          "histogram": [
           {
            "marker": {
             "colorbar": {
              "outlinewidth": 0,
              "ticks": ""
             }
            },
            "type": "histogram"
           }
          ],
          "histogram2d": [
           {
            "colorbar": {
             "outlinewidth": 0,
             "ticks": ""
            },
            "colorscale": [
             [
              0,
              "#0d0887"
             ],
             [
              0.1111111111111111,
              "#46039f"
             ],
             [
              0.2222222222222222,
              "#7201a8"
             ],
             [
              0.3333333333333333,
              "#9c179e"
             ],
             [
              0.4444444444444444,
              "#bd3786"
             ],
             [
              0.5555555555555556,
              "#d8576b"
             ],
             [
              0.6666666666666666,
              "#ed7953"
             ],
             [
              0.7777777777777778,
              "#fb9f3a"
             ],
             [
              0.8888888888888888,
              "#fdca26"
             ],
             [
              1,
              "#f0f921"
             ]
            ],
            "type": "histogram2d"
           }
          ],
          "histogram2dcontour": [
           {
            "colorbar": {
             "outlinewidth": 0,
             "ticks": ""
            },
            "colorscale": [
             [
              0,
              "#0d0887"
             ],
             [
              0.1111111111111111,
              "#46039f"
             ],
             [
              0.2222222222222222,
              "#7201a8"
             ],
             [
              0.3333333333333333,
              "#9c179e"
             ],
             [
              0.4444444444444444,
              "#bd3786"
             ],
             [
              0.5555555555555556,
              "#d8576b"
             ],
             [
              0.6666666666666666,
              "#ed7953"
             ],
             [
              0.7777777777777778,
              "#fb9f3a"
             ],
             [
              0.8888888888888888,
              "#fdca26"
             ],
             [
              1,
              "#f0f921"
             ]
            ],
            "type": "histogram2dcontour"
           }
          ],
          "mesh3d": [
           {
            "colorbar": {
             "outlinewidth": 0,
             "ticks": ""
            },
            "type": "mesh3d"
           }
          ],
          "parcoords": [
           {
            "line": {
             "colorbar": {
              "outlinewidth": 0,
              "ticks": ""
             }
            },
            "type": "parcoords"
           }
          ],
          "pie": [
           {
            "automargin": true,
            "type": "pie"
           }
          ],
          "scatter": [
           {
            "marker": {
             "colorbar": {
              "outlinewidth": 0,
              "ticks": ""
             }
            },
            "type": "scatter"
           }
          ],
          "scatter3d": [
           {
            "line": {
             "colorbar": {
              "outlinewidth": 0,
              "ticks": ""
             }
            },
            "marker": {
             "colorbar": {
              "outlinewidth": 0,
              "ticks": ""
             }
            },
            "type": "scatter3d"
           }
          ],
          "scattercarpet": [
           {
            "marker": {
             "colorbar": {
              "outlinewidth": 0,
              "ticks": ""
             }
            },
            "type": "scattercarpet"
           }
          ],
          "scattergeo": [
           {
            "marker": {
             "colorbar": {
              "outlinewidth": 0,
              "ticks": ""
             }
            },
            "type": "scattergeo"
           }
          ],
          "scattergl": [
           {
            "marker": {
             "colorbar": {
              "outlinewidth": 0,
              "ticks": ""
             }
            },
            "type": "scattergl"
           }
          ],
          "scattermapbox": [
           {
            "marker": {
             "colorbar": {
              "outlinewidth": 0,
              "ticks": ""
             }
            },
            "type": "scattermapbox"
           }
          ],
          "scatterpolar": [
           {
            "marker": {
             "colorbar": {
              "outlinewidth": 0,
              "ticks": ""
             }
            },
            "type": "scatterpolar"
           }
          ],
          "scatterpolargl": [
           {
            "marker": {
             "colorbar": {
              "outlinewidth": 0,
              "ticks": ""
             }
            },
            "type": "scatterpolargl"
           }
          ],
          "scatterternary": [
           {
            "marker": {
             "colorbar": {
              "outlinewidth": 0,
              "ticks": ""
             }
            },
            "type": "scatterternary"
           }
          ],
          "surface": [
           {
            "colorbar": {
             "outlinewidth": 0,
             "ticks": ""
            },
            "colorscale": [
             [
              0,
              "#0d0887"
             ],
             [
              0.1111111111111111,
              "#46039f"
             ],
             [
              0.2222222222222222,
              "#7201a8"
             ],
             [
              0.3333333333333333,
              "#9c179e"
             ],
             [
              0.4444444444444444,
              "#bd3786"
             ],
             [
              0.5555555555555556,
              "#d8576b"
             ],
             [
              0.6666666666666666,
              "#ed7953"
             ],
             [
              0.7777777777777778,
              "#fb9f3a"
             ],
             [
              0.8888888888888888,
              "#fdca26"
             ],
             [
              1,
              "#f0f921"
             ]
            ],
            "type": "surface"
           }
          ],
          "table": [
           {
            "cells": {
             "fill": {
              "color": "#EBF0F8"
             },
             "line": {
              "color": "white"
             }
            },
            "header": {
             "fill": {
              "color": "#C8D4E3"
             },
             "line": {
              "color": "white"
             }
            },
            "type": "table"
           }
          ]
         },
         "layout": {
          "annotationdefaults": {
           "arrowcolor": "#2a3f5f",
           "arrowhead": 0,
           "arrowwidth": 1
          },
          "coloraxis": {
           "colorbar": {
            "outlinewidth": 0,
            "ticks": ""
           }
          },
          "colorscale": {
           "diverging": [
            [
             0,
             "#8e0152"
            ],
            [
             0.1,
             "#c51b7d"
            ],
            [
             0.2,
             "#de77ae"
            ],
            [
             0.3,
             "#f1b6da"
            ],
            [
             0.4,
             "#fde0ef"
            ],
            [
             0.5,
             "#f7f7f7"
            ],
            [
             0.6,
             "#e6f5d0"
            ],
            [
             0.7,
             "#b8e186"
            ],
            [
             0.8,
             "#7fbc41"
            ],
            [
             0.9,
             "#4d9221"
            ],
            [
             1,
             "#276419"
            ]
           ],
           "sequential": [
            [
             0,
             "#0d0887"
            ],
            [
             0.1111111111111111,
             "#46039f"
            ],
            [
             0.2222222222222222,
             "#7201a8"
            ],
            [
             0.3333333333333333,
             "#9c179e"
            ],
            [
             0.4444444444444444,
             "#bd3786"
            ],
            [
             0.5555555555555556,
             "#d8576b"
            ],
            [
             0.6666666666666666,
             "#ed7953"
            ],
            [
             0.7777777777777778,
             "#fb9f3a"
            ],
            [
             0.8888888888888888,
             "#fdca26"
            ],
            [
             1,
             "#f0f921"
            ]
           ],
           "sequentialminus": [
            [
             0,
             "#0d0887"
            ],
            [
             0.1111111111111111,
             "#46039f"
            ],
            [
             0.2222222222222222,
             "#7201a8"
            ],
            [
             0.3333333333333333,
             "#9c179e"
            ],
            [
             0.4444444444444444,
             "#bd3786"
            ],
            [
             0.5555555555555556,
             "#d8576b"
            ],
            [
             0.6666666666666666,
             "#ed7953"
            ],
            [
             0.7777777777777778,
             "#fb9f3a"
            ],
            [
             0.8888888888888888,
             "#fdca26"
            ],
            [
             1,
             "#f0f921"
            ]
           ]
          },
          "colorway": [
           "#636efa",
           "#EF553B",
           "#00cc96",
           "#ab63fa",
           "#FFA15A",
           "#19d3f3",
           "#FF6692",
           "#B6E880",
           "#FF97FF",
           "#FECB52"
          ],
          "font": {
           "color": "#2a3f5f"
          },
          "geo": {
           "bgcolor": "white",
           "lakecolor": "white",
           "landcolor": "#E5ECF6",
           "showlakes": true,
           "showland": true,
           "subunitcolor": "white"
          },
          "hoverlabel": {
           "align": "left"
          },
          "hovermode": "closest",
          "mapbox": {
           "style": "light"
          },
          "paper_bgcolor": "white",
          "plot_bgcolor": "#E5ECF6",
          "polar": {
           "angularaxis": {
            "gridcolor": "white",
            "linecolor": "white",
            "ticks": ""
           },
           "bgcolor": "#E5ECF6",
           "radialaxis": {
            "gridcolor": "white",
            "linecolor": "white",
            "ticks": ""
           }
          },
          "scene": {
           "xaxis": {
            "backgroundcolor": "#E5ECF6",
            "gridcolor": "white",
            "gridwidth": 2,
            "linecolor": "white",
            "showbackground": true,
            "ticks": "",
            "zerolinecolor": "white"
           },
           "yaxis": {
            "backgroundcolor": "#E5ECF6",
            "gridcolor": "white",
            "gridwidth": 2,
            "linecolor": "white",
            "showbackground": true,
            "ticks": "",
            "zerolinecolor": "white"
           },
           "zaxis": {
            "backgroundcolor": "#E5ECF6",
            "gridcolor": "white",
            "gridwidth": 2,
            "linecolor": "white",
            "showbackground": true,
            "ticks": "",
            "zerolinecolor": "white"
           }
          },
          "shapedefaults": {
           "line": {
            "color": "#2a3f5f"
           }
          },
          "ternary": {
           "aaxis": {
            "gridcolor": "white",
            "linecolor": "white",
            "ticks": ""
           },
           "baxis": {
            "gridcolor": "white",
            "linecolor": "white",
            "ticks": ""
           },
           "bgcolor": "#E5ECF6",
           "caxis": {
            "gridcolor": "white",
            "linecolor": "white",
            "ticks": ""
           }
          },
          "title": {
           "x": 0.05
          },
          "xaxis": {
           "automargin": true,
           "gridcolor": "white",
           "linecolor": "white",
           "ticks": "",
           "title": {
            "standoff": 15
           },
           "zerolinecolor": "white",
           "zerolinewidth": 2
          },
          "yaxis": {
           "automargin": true,
           "gridcolor": "white",
           "linecolor": "white",
           "ticks": "",
           "title": {
            "standoff": 15
           },
           "zerolinecolor": "white",
           "zerolinewidth": 2
          }
         }
        },
        "title": {
         "text": "Total Count of Each Collision Type"
        },
        "xaxis": {
         "anchor": "y",
         "domain": [
          0,
          1
         ],
         "title": {
          "text": "Classification of Incident"
         }
        },
        "yaxis": {
         "anchor": "x",
         "domain": [
          0,
          1
         ],
         "title": {
          "text": "# of Occurrences"
         }
        }
       }
      }
     },
     "metadata": {}
    }
   ],
   "source": [
    "filename = 'SeverityCounts-px.html'\n",
    "\n",
    "\n",
    "sev = ['Property Damage Only Collision', 'Injury Collision']\n",
    "sev_counts = [raw_collision_data['SEVERITYCODE'].value_counts()[i] for i in range(1,len(raw_collision_data['SEVERITYCODE'].value_counts().to_list())+1)]\n",
    "\n",
    "fig = px.bar(x=sev, y=sev_counts, title='Total Count of Each Collision Type', labels={'y':'# of Occurrences', 'x':'Classification of Incident'})\n",
    "fig.show()\n"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": null,
   "metadata": {},
   "outputs": [],
   "source": []
  },
  {
   "cell_type": "code",
   "execution_count": null,
   "metadata": {},
   "outputs": [],
   "source": []
  }
 ]
}