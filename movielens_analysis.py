# -*- coding: utf-8 -*-
"""movielens-analysis.ipynb

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/1TH7hYB_0GBOTjckwz4by_7EGqn_CFegK
"""

from google.colab import drive
drive.mount('/content/drive')

import pandas as pd

data_path = '/content/drive/My Drive/movielens/ml-100k/'

ratings_columns = ['user_id', 'movie_id', 'rating', 'timestamp']
ratings = pd.read_csv(data_path + 'u.data', sep='\t', names=ratings_columns)

user_columns = ['user_id', 'age', 'gender', 'occupation', 'zip_code']
users = pd.read_csv(data_path + 'u.user', sep='|', names=user_columns)

movie_columns = ['movie_id', 'movie_title', 'release_date', 'video_release_date', 'IMDb_URL',
                 'unknown', 'Action', 'Adventure', 'Animation', "Children's", 'Comedy',
                 'Crime', 'Documentary', 'Drama', 'Fantasy', 'Film-Noir', 'Horror',
                 'Musical', 'Mystery', 'Romance', 'Sci-Fi', 'Thriller', 'War', 'Western']
movies = pd.read_csv(data_path + 'u.item', sep='|', names=movie_columns, encoding='latin-1')

ratings['timestamp'] = pd.to_datetime(ratings['timestamp'], unit='s')
ratings['year'] = ratings['timestamp'].dt.year
ratings['month'] = ratings['timestamp'].dt.month
ratings['day'] = ratings['timestamp'].dt.day

genre_counts = movies.iloc[:, 5:].sum().sort_values(ascending=False)
print(genre_counts)

movie_ratings = ratings.groupby('movie_id')['rating'].agg(['mean', 'count']).reset_index()
movie_ratings.rename(columns={'mean': 'average_rating', 'count': 'num_ratings'}, inplace=True)

user_ratings = ratings.groupby('user_id')['rating'].agg(['mean', 'count']).reset_index()
user_ratings.rename(columns={'mean': 'user_avg_rating', 'count': 'user_num_ratings'}, inplace=True)

"""**Explaratory Data Analsis**"""

print(ratings.describe())
print(users.describe())
print(movies.describe())

import matplotlib.pyplot as plt
import seaborn as sns

sns.histplot(ratings['rating'], bins=5, kde=False)
plt.title('Distribution of Ratings')
plt.xlabel('Rating')
plt.ylabel('Frequency')
plt.show()

import matplotlib.pyplot as plt
import seaborn as sns

sns.histplot(ratings['rating'], bins=5, kde=False)
plt.title('Distribution of Ratings')
plt.xlabel('Rating')
plt.ylabel('Frequency')
plt.show()

sns.histplot(users['age'], bins=20, kde=True)
plt.title('Age Distribution of Users')
plt.xlabel('Age')
plt.ylabel('Frequency')
plt.show()

gender_counts = users['gender'].value_counts()
gender_counts.plot(kind='bar')
plt.title('Gender Distribution')
plt.xlabel('Gender')
plt.ylabel('Frequency')
plt.show()

most_rated = ratings['movie_id'].value_counts().head(10)
most_rated_movies = movies[movies['movie_id'].isin(most_rated.index)][['movie_id', 'movie_title']]
print(most_rated_movies)

movies.rename(columns={movies.columns[0]: 'movie_id'}, inplace=True)

movie_ratings_genres = pd.merge(movie_ratings, movies, on='movie_id', how='inner')

genre_columns = ['unknown', 'Action', 'Adventure', 'Animation', "Children's",
                 'Comedy', 'Crime', 'Documentary', 'Drama', 'Fantasy',
                 'Film-Noir', 'Horror', 'Musical', 'Mystery', 'Romance',
                 'Sci-Fi', 'Thriller', 'War', 'Western']

genre_avg_ratings = {}
for genre in genre_columns:
    genre_avg_ratings[genre] = movie_ratings_genres[movie_ratings_genres[genre] == 1]['average_rating'].mean()

genre_avg_ratings = pd.Series(genre_avg_ratings).sort_values(ascending=False)
print(genre_avg_ratings)

genre_avg_ratings.plot(kind='bar', title='Average Rating by Genre', xlabel='Genre', ylabel='Average Rating')
plt.show()

correlation = movie_ratings['num_ratings'].corr(movie_ratings['average_rating'])
print(f"Correlation between number of ratings and average rating: {correlation}")

sns.scatterplot(data=movie_ratings, x='num_ratings', y='average_rating')
plt.title('Number of Ratings vs. Average Rating')
plt.show()

movie_ratings = movie_ratings.sort_values('num_ratings', ascending=False)
movie_ratings['cumulative_percentage'] = movie_ratings['num_ratings'].cumsum() / movie_ratings['num_ratings'].sum()

movie_ratings['cumulative_percentage'].plot(kind='line', title='Long-Tail Analysis', xlabel='Movies (sorted by popularity)', ylabel='Cumulative % of Ratings')
plt.show()

full_data = pd.merge(ratings, users, on='user_id')
full_data = pd.merge(full_data, movies, on='movie_id')
full_data.to_csv('/content/drive/My Drive/movielens/ml-100k/processed_data.csv', index=False)