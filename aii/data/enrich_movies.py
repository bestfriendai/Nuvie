import pandas as pd

from sqlalchemy import create_engine, text

from tmdbv3api import TMDb, Movie, Search

import sys



# --- CONFIGURATION ---

# Replace with your actual database URL and API key

DATABASE_URL = "postgresql://neondb_owner:npg_ANY0Q7uFlZSi@ep-restless-art-ah6dr023-pooler.c-3.us-east-1.aws.neon.tech/neondb?sslmode=require&channel_binding=require"

TMDB_API_KEY = os.environ.get('TMDB_API_KEY')


# Initialize database engine

try:

    engine = create_engine(DATABASE_URL)

except Exception as e:

    print(f"FATAL: Could not establish DB connection. Error: {e}")

    sys.exit(1)



# Initialize TMDb API

tmdb = TMDb()

tmdb.api_key = TMDB_API_KEY

tmdb.language = 'en'

search = Search()



# Posterlerin temel URL'si (TMDb kuralı)

POSTER_BASE_URL = "https://image.tmdb.org/t/p/w500" 



print("Configuration loaded. Starting enrichment process.")



# ----------------------------------------------------------------------



def enrich_movies_data():

    """

    Fetches movie titles from DB, searches TMDb for metadata (posters, overview),

    and updates the 'movies' table with the new data.

    """

    

    # 1. EXTRACT: Get existing MovieLens movies from the database

    print("\n[STEP 1/4] Extracting movies from PostgreSQL...")

    query = "SELECT movie_id, title FROM movies"

    movies_df = pd.read_sql(query, con=engine)

    

    print(f"Found {len(movies_df)} movies to enrich.")

    

    enriched_data = []

    

    # 2. TRANSFORM & SEARCH: Iterate through movies and search TMDb

    print("[STEP 2/4] Searching TMDb for metadata (This may take a few minutes)...")

    

    # Yeni eklenecek sütunların SQL yapısı (veri tipi olarak 'text' en güvenlisidir)

    with engine.begin() as connection:

        # DB şemasını güncelleme (yeni sütunlar ekleme)

        try:

            connection.execute(text("ALTER TABLE movies ADD COLUMN tmdb_id INTEGER;"))

            connection.execute(text("ALTER TABLE movies ADD COLUMN poster_url TEXT;"))

            connection.execute(text("ALTER TABLE movies ADD COLUMN overview TEXT;"))

            connection.execute(text("ALTER TABLE movies ADD COLUMN release_date TEXT;"))

            print("Database schema successfully updated (New columns added).")

        except Exception as e:

            # Sütun zaten varsa bu hatayı yakalarız.

            print(f"Schema update skipped (Columns already exist).")





    for index, row in movies_df.iterrows():

        movie_title = row['title']

        movie_id = row['movie_id']

        

        # Basit bir ilerleme göstergesi

        if index % 100 == 0:

            print(f"   Processing: {index}/{len(movies_df)} - {movie_title}")

        

        try:

            # TMDb'de filmi arama

            # MovieLens'deki filmlerin yanında yayın yılı da yazar (Örn: Toy Story (1995))

            # Sadece filmin adını almalıyız.

            clean_title = movie_title[:-6].strip() 

            

            # API arama

            results = search.movies(clean_title)

            

            if results and results[0].id:

                # İlk ve en iyi sonucu al

                result = results[0]

                

                # Güncelleme için SQL komutunu hazırlama

                poster_path = result.poster_path

                full_poster_url = f"{POSTER_BASE_URL}{poster_path}" if poster_path else None

                

                # 3. LOAD: Veritabanını Güncelleme

                update_query = text(

                    """

                    UPDATE movies 

                    SET tmdb_id = :tmdb_id, 

                        poster_url = :poster_url, 

                        overview = :overview,

                        release_date = :release_date

                    WHERE movie_id = :movie_id

                    """

                )

                

                with engine.begin() as connection:

                    connection.execute(update_query, {

                        'tmdb_id': result.id,

                        'poster_url': full_poster_url,

                        'overview': result.overview,

                        'release_date': result.release_date,

                        'movie_id': movie_id

                    })

            

        except Exception as e:

            # API limit hatası veya bağlantı sorunu olursa

            # print(f"Warning: Could not enrich movie {movie_title}. Error: {e}")

            pass # Hata durumunda döngüyü kesme

    

    print("\n[STEP 3/4] TMDb enrichment complete.")

    

    # 4. VERIFICATION: Kontrol amaçlı örnek bir filmi okuma

    print("[STEP 4/4] Verifying updated data...")

    check_query = "SELECT movie_id, title, tmdb_id, poster_url, overview FROM movies WHERE poster_url IS NOT NULL LIMIT 5"

    verified_movies = pd.read_sql(check_query, con=engine)

    

    print("\nSuccessfully enriched sample movies:")

    print(verified_movies[['title', 'tmdb_id', 'poster_url']])



# ----------------------------------------------------------------------



if __name__ == '__main__':

    try:

        enrich_movies_data()

        print("\nSUCCESS: All movies have been searched and database updated!")

    except Exception as e:

        print(f"\nFATAL ERROR: Enrichment process failed. Error: {e}")