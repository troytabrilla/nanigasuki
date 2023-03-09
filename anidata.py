import json
import typing
import requests

import config
import db

Dict = typing.Dict[str, typing.Any]
OptionalDict = typing.Optional[Dict]

class AniData:

    def __init__(self):
        # @todo Move cache into its own module, fallback to file
        self._cache = db.redis.get_connection()

    def query(self, query:str, variables:OptionalDict=None) -> Dict:
        response = requests.post(
            config.anidata['api']['url'],
            json={'query': query, 'variables': variables},
            timeout=60
        )

        results = json.loads(response.text)

        return results['data']

    def get_user_anime_list(self, user_name:str, options:OptionalDict=None) -> Dict:
        should_cache = isinstance(options, dict) and not options.get('no_cache')
        cache_key = f"anime_list:{user_name}"

        if should_cache:
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
        variables = {'userName':user_name}

        results = self.query(query, variables=variables)

        if should_cache:
            self._cache.set(
                cache_key,
                json.dumps(results),
                ex=config.anidata['cache']['ttl']
            )

        return results

if __name__ == "__main__":
    import sys
    import pprint
    anime_list = AniData().get_user_anime_list(sys.argv[1])
    pprint.pprint(anime_list)
