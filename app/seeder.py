import datetime
import logging
from sqlalchemy.orm import Session
from app.models.category import Category
from app.models.featured import FeaturedPost
from app.models.post import Post

logger = logging.getLogger("seeder")

def seed_db(db: Session):
    # 1. Seed Categories
    if db.query(Category).count() == 0:
        logger.info("Seeding categories...")
        categories = [
            Category(id=1, name="Hiphop"),
            Category(id=2, name="Rap"),
            Category(id=3, name="RnB"),
            Category(id=4, name="News"),
            Category(id=5, name="Underground"),
            Category(id=6, name="Trap")
        ]
        db.add_all(categories)
        db.commit()
        logger.info("Successfully seeded categories!")

    # 2. Seed Featured Posts
    if db.query(FeaturedPost).count() == 0:
        logger.info("Seeding featured posts...")
        featured_posts = [
            FeaturedPost(
                id=1,
                title="Drake vs Kendrick: The Ultimate Feud Timeline",
                portrait_image="https://images.unsplash.com/photo-1511671782779-c97d3d27a1d4?w=500&q=80",
                image="https://images.unsplash.com/photo-1514525253161-7a46d19cd819?w=1200&q=80"
            ),
            FeaturedPost(
                id=2,
                title="Travis Scott Announces 'Utopia Tour' Extension",
                portrait_image="https://images.unsplash.com/photo-1470225620780-dba8ba36b745?w=500&q=80",
                image="https://images.unsplash.com/photo-1498038432885-c6f3f1b912ee?w=1200&q=80"
            ),
            FeaturedPost(
                id=3,
                title="SZA Rules the R&B Charts with New Single",
                portrait_image="https://images.unsplash.com/photo-1516450360452-9312f5e86fc7?w=500&q=80",
                image="https://images.unsplash.com/photo-1459749411175-04bf5292ceea?w=1200&q=80"
            )
        ]
        db.add_all(featured_posts)
        db.commit()
        logger.info("Successfully seeded featured posts!")

    # 3. Seed Posts
    if db.query(Post).count() == 0:
        logger.info("Seeding posts...")
        
        # Calculate dynamic dates
        today_dt = datetime.date.today()
        today = today_dt.strftime("%Y-%m-%d")
        yesterday = (today_dt - datetime.timedelta(days=1)).strftime("%Y-%m-%d")
        day_before_yesterday = (today_dt - datetime.timedelta(days=2)).strftime("%Y-%m-%d")
        older_date = (today_dt - datetime.timedelta(days=5)).strftime("%Y-%m-%d")

        posts = [
            # TODAY'S POSTS
            Post(
                id=1,
                title="Lil Baby drops fire new freestyle in Paris",
                title_translate="Lil Baby lanza un freestyle ardiente en París",
                description="The Atlanta star surprised fans at a local street cipher in Paris.",
                des="Lil Baby surprised fans in Paris by joining a street cipher and dropping a completely unreleased freestyle that went viral instantly on TikTok.",
                des_translate="Lil Baby sorprendió a los fanáticos en París al unirse a un cifrado callejero y lanzar un estilo libre completamente inédito que se volvió viral al instante en TikTok.",
                portrait_image="https://images.unsplash.com/photo-1524368535928-5b5e00ddc76b?w=500&q=80",
                image="https://images.unsplash.com/photo-1501386761578-eac5c94b800a?w=1200&q=80",
                video=None,
                link="https://www.youtube.com/watch?v=dQw4w9WgXcQ",
                categories="Rap, News",
                categories_id=2,  # Rap
                social_media="@lilbaby, @hiphopboombox",
                views=1500,
                date=today,
                comment_count=45
            ),
            Post(
                id=2,
                title="Tyler, The Creator Teases New Album Aesthetics",
                title_translate="Tyler, The Creator anticipa la estética de su nuevo álbum",
                description="Tyler posts mysterious audio clips and pastel-colored moodboards.",
                des="Grammy-winning artist Tyler, The Creator has sparked new album rumors after wiping his Instagram feed and posting a series of vintage pastel moodboards.",
                des_translate="El artista ganador del Grammy Tyler, The Creator ha desatado rumores sobre un nuevo álbum tras borrar su feed de Instagram y publicar una serie de paneles de inspiración de colores pastel vintage.",
                portrait_image="https://images.unsplash.com/photo-1508700115892-45ecd05ae2ad?w=500&q=80",
                image="https://images.unsplash.com/photo-1511671782779-c97d3d27a1d4?w=1200&q=80",
                video="videos/tyler_teaser.mp4",
                link=None,
                categories="Hiphop",
                categories_id=1,  # Hiphop
                social_media="@feliciathegoat",
                views=3200,  # High views to show in trending
                date=today,
                comment_count=122
            ),
            
            # YESTERDAY'S POSTS
            Post(
                id=3,
                title="The Evolution of Trap Drum Patterns",
                title_translate="La evolución de los patrones de batería del Trap",
                description="A deep dive into how the 808 and hi-hats changed modern music.",
                des="From early Atlanta pioneers to the global pop chart dominance, we trace the history of trap music and the signature drum patterns that define the genre.",
                des_translate="Desde los primeros pioneros de Atlanta hasta el dominio global en las listas de éxitos, rastreamos la historia de la música trap y los patrones de batería característicos que definen el género.",
                portrait_image="https://images.unsplash.com/photo-1470225620780-dba8ba36b745?w=500&q=80",
                image="https://images.unsplash.com/photo-1514525253161-7a46d19cd819?w=1200&q=80",
                video=None,
                link="https://www.youtube.com/watch?v=dQw4w9WgXcQ",
                categories="Trap, Underground",
                categories_id=6,  # Trap
                social_media="@metroboomin",
                views=850,
                date=yesterday,
                comment_count=12
            ),
            Post(
                id=4,
                title="Frank Ocean Spotted in Tokyo Music Studio",
                title_translate="Frank Ocean visto en un estudio de música de Tokio",
                description="Fans are speculating that new music is finally on the way.",
                des="Mysterious R&B genius Frank Ocean was photographed by fans walking out of a legendary analog recording studio in Tokyo's Shibuya district, raising anticipation.",
                des_translate="El misterioso genio del R&B Frank Ocean fue fotografiado por fanáticos al salir de un legendario estudio de grabación analógico en el distrito Shibuya de Tokio, aumentando la expectativa.",
                portrait_image="https://images.unsplash.com/photo-1516450360452-9312f5e86fc7?w=500&q=80",
                image="https://images.unsplash.com/photo-1459749411175-04bf5292ceea?w=1200&q=80",
                video=None,
                link=None,
                categories="RnB",
                categories_id=3,  # RnB
                social_media="@frankocean",
                views=5400,  # Very high views to top the trending list!
                date=yesterday,
                comment_count=230
            ),

            # DAY BEFORE YESTERDAY'S POSTS
            Post(
                id=5,
                title="Underground Hiphop Scene Explodes in London",
                title_translate="La escena del Hiphop Underground explota en Londres",
                description="Grime meets boom-bap in a new wave of street artists.",
                des="A brand new wave of independent London artists are blending traditional UK drill and grime beats with classic 90s boom-bap production to create a unique local sound.",
                des_translate="Una nueva ola de artistas independientes de Londres está mezclando ritmos tradicionales de drill y grime del Reino Unido con la producción clásica de boom-bap de los 90 para crear un sonido local único.",
                portrait_image="https://images.unsplash.com/photo-1508700115892-45ecd05ae2ad?w=500&q=80",
                image="https://images.unsplash.com/photo-1498038432885-c6f3f1b912ee?w=1200&q=80",
                video=None,
                link="https://www.youtube.com/watch?v=dQw4w9WgXcQ",
                categories="Underground, Hiphop",
                categories_id=5,  # Underground
                social_media="@london_underground_rap",
                views=600,
                date=day_before_yesterday,
                comment_count=8
            ),

            # AN OLDER POST FOR DATE FILTER TESTING
            Post(
                id=6,
                title="Kendrick Lamar's 'DAMN.' Wins Pulitzer Prize",
                title_translate="'DAMN.' de Kendrick Lamar gana el premio Pulitzer",
                description="Looking back at this historic moment in hip-hop history.",
                des="We look back at the historic achievement of Kendrick Lamar's album DAMN., which became the first non-classical, non-jazz work to win the prestigious Pulitzer Prize for Music.",
                des_translate="Recordamos el logro histórico del álbum DAMN. de Kendrick Lamar, que se convirtió en la primera obra que no es clásica ni de jazz en ganar el prestigioso Premio Pulitzer de Música.",
                portrait_image="https://images.unsplash.com/photo-1524368535928-5b5e00ddc76b?w=500&q=80",
                image="https://images.unsplash.com/photo-1501386761578-eac5c94b800a?w=1200&q=80",
                video=None,
                link=None,
                categories="Rap, News",
                categories_id=2,
                social_media="@kendricklamar",
                views=12000,
                date=older_date,
                comment_count=980
            )
        ]
        db.add_all(posts)
        db.commit()
        logger.info("Successfully seeded posts!")
