#pylint: disable=import-error
import anidata

name = 'test'

def test_query():
    query = """
        query UserTest($userName:String) {
            User(name:$userName) {
                id
                name
            }
        }
    """
    data = anidata.AniData().query(query, variables={'userName':name})
    test_data = {
        'User': {
            'id': 14719,
            'name': 'test'
        }
    }
    assert data == test_data

def test_get_user_anime_list():
    data = anidata.AniData().get_user_anime_list(name)
    test_data = {
        'User': {
            'id': 14719,
            'name': 'test'
        },
        'MediaListCollection': {
            'lists': []
        }
    }
    assert data == test_data
