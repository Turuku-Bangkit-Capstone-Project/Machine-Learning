# Sleep Analysis Machine Learning Project 💤💤

## Overview
This project implements machine learning models to analyze sleep patterns and predict sleep duration based on personal characteristics. It also includes a chronotype classification system to determine an individual's sleep-wake preference pattern.

## Models

### 1. Sleep Duration Prediction Model
**Features:**
- Chronotype (Bear,Lion,Dolphin,Wolf)
- Age
- Gender
- Daily Steps
- Pyhsical Activity Level

**Target:**
- Sleep Duration (hours)

### 2. Chronotype Classification Model
**Features:**
- Wake-up Time
- Bedtime

**Target:**
- Chronotype Categories (Bear,Lion,Dolphin,Wolf)
1. Lion 🦁   : Lions are early risers, highly productive in the morning, and tend to sleep early. They are often described as disciplined, organized, and natural leaders.
3. Bear 🐻   : Bears follow the sun's cycle, waking up and sleeping at regular hours, with peak productivity during midday. They are relaxed, social, and thrive on routine.
4. Dolphin 🐬: Dolphins have irregular sleep patterns, often struggle with insomnia, and experience unpredictable energy bursts. They are typically perfectionists, intelligent, and prone to anxiety.
5. Wolf 🐺   : Wolves are night owls, with peak productivity in the evening and late at night. They are creative, innovative, and often introverted.

## Dependencies
- Python 3.8+
- scikit-learn
- Tensorflow
- Tfjs
- pandas
- numpy

## Install Required Packages
Create a `requirements.txt` file with the following content:
Install the requirements:
```bash
pip install -r requirements.txt
```

## Data Format
Ensure your input data follows this format:

**Sleep Duration Model:**
```
chronotype | age | gender | sleep_duration | daily_steps | physical_activity_level
----------------------------------------------------------------------------------
lion       | 25  | M      | 7.5            | 4000        | 70
bear       | 30  | F      | 6.8            | 7500        | 85
```

**Chronotype Model:**
```
wakeup_time | bedtime | chronotype
---------------------------------
06:00       | 22:00   | lion
08:00       | 00:00   | bear
```

## Contributing
Feel free to submit issues and enhancement requests.
