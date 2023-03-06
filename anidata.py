import json
import requests

import config
import db

class AniData:

    def __init__(self):
        self._cache = db.redis.get_connection()

    def query(self, query, variables=None):
        response = requests.post(
            config.anidata['api']['url'],
            json={
                'query': query,
                'variables': variables
            }
        )

        results = json.loads(response.text)

        return results['data']

    def get_user_anime_list(self, options={}):
        cache_key = f"anime_list:{options['user_name']}"

        if not options.get('no_cache'):
            cached_results = self._cache.get(cache_key)
            if cached_results:
                return json.loads(cached_results)

        query = """
            query UserAnimeList ($userName:String) {
                User(name: $userName) {
                    id
                    name
                }
                MediaListCollection(userName:$userName, type:ANIME) {
                    lists {
                        name
                        status
                        entries {
                            score
                            media {
                                id
                                title {
                                    romaji
                                }
                                genres
                                tags {
                                    name
                                }
                                nextAiringEpisode {
                                    airingAt
                                }
                                season
                                seasonYear
                            }
                        }
                    }
                }
            }
        """

        variables = {
            'userName': options['user_name']
        }

        results = self.query(query, variables=variables)

        if not options.get('no_cache'):
            self._cache.set(
                cache_key,
                json.dumps(results),
                ex=config.anidata['cache']['ttl']
            )

        return results

if __name__ == "__main__":
    import sys
    import pprint
    anime_list = AniData().get_user_anime_list(options={ 'user_name': sys.argv[1] })
    pprint.pprint(anime_list)
