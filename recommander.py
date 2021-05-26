import pandas as pd
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity


def get_title_from_index(index):
    return df[df.index == index]["title"].values[0]


def get_index_from_title(title):
    return df[df.title.apply(str.lower) == title.lower()]["index"].values[0]


# --------------------------Content-Based Filtering--------------------------

## 1. csv 읽어오기
df = pd.read_csv("movie_dataset.csv")

# print(df.head)
# print(df.columns)

## 2. Feature 선택

features = ['keywords', 'cast', 'genres', 'director']

## 3. 모든 feature를 포함하는 새로운 열 생성

for feature in features:
    df[feature] = df[feature].fillna('')


def combine_features(row):
    return row['keywords'] + " " + row['cast'] + " " + row["genres"] + " " + row["director"]


df['combined_features'] = df.apply(combine_features, axis=1)

# print(df['combined_features'].head())

## 4. 새로운 열로부터 count matrix 생성

cv = CountVectorizer()

count_matrix = cv.fit_transform(df["combined_features"])

## 5. Cosine Similarity 계산
cosine_sim = cosine_similarity(count_matrix)


## 6. 입력한 영화로 모든 영화들과 cosine similarity 계산하고, 리스트 생성
def get_similar_movies(title):
    movie_index = get_index_from_title(title)
    similar_movie_tuples = list(enumerate(cosine_sim[movie_index]))

    ## 7. cosine similarity가 높은 순으로 영화리스트 정렬
    sorted_similar_movies = sorted(similar_movie_tuples, key=lambda x: x[1], reverse=True)
    similar_movie_titles = []
    for i in range(1, 51):
        similar_movie_titles.append(get_title_from_index(sorted_similar_movies[i][0]))
    similar_movie_titles.reverse()
    return similar_movie_titles

#--------------------------Collaborative Filtering--------------------------

# ## 1. 평점 데이터 불러오기
# ratings = pd.read_csv('dataset/ratings.csv')
# movies = pd.read_csv('dataset/movies.csv')
# ratings = pd.merge(movies,ratings).drop(['genres','timestamp'], axis=1)
# print(ratings.head())
#
# ## 2. 용도에 맞게 피봇하기
# user_ratings = ratings.pivot_table(index = ['userId'], columns=['title'],values='rating')
# print(user_ratings.head())
#
# ## 3. 결측치 처리(평점이 10명 미만인 영화 삭제, 나머지 0으로 교체)
# user_ratings = user_ratings.dropna(thresh=10, axis=1).fillna(0)
# print(user_ratings.head())
#
# ## 4. Pearson Corelation 계산
# item_similarity_df = user_ratings.corr(method = 'pearson')
# print(item_similarity_df.head(50))
#
# ## 5. 비슷한 영화 불러오기
#
# def get_similar_movies(movie_name, user_rating):
#     similar_score = item_similarity_df[movie_name]*(user_rating-2.5)
#     similar_score = similar_score.sort_values(ascending=False)
#
#     return similar_score
#
# my_favorite_movies = [("50/50 (2011)", 0), ("A.I. Artificial Intelligence (2001)", 0)]
#
# similar_movies = pd.DataFrame()
#
# for movie, rating in my_favorite_movies:
#     similar_movies = similar_movies.append(get_similar_movies(movie,rating), ignore_index=True)
#
# print(similar_movies.head())
#
# similar_movies = similar_movies.sum().sort_values(ascending=False)
# print(similar_movies.index)
